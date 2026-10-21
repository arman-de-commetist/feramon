#!/usr/bin/env bash
# MONA Perfume — connect a domain and a free HTTPS certificate (Let's Encrypt).
# Before running: in the domain's DNS add an A record  @ -> server IP  (and  www -> server IP), wait ~30 min.
# Run as root:   bash /srv/mona/deploy/add_domain.sh mona.kz
set -euo pipefail
DOMAIN=${1:?Укажите домен, например: bash add_domain.sh mona.kz}
APP=/srv/mona
IP=$(hostname -I | awk '{print $1}')

apt-get install -y certbot python3-certbot-nginx
sed -i "s/server_name _;/server_name $DOMAIN www.$DOMAIN $IP;/" /etc/nginx/sites-available/mona
nginx -t && systemctl reload nginx
certbot --nginx -d "$DOMAIN" -d "www.$DOMAIN" --redirect --agree-tos --register-unsafely-without-email -n

sed -i "s|^DJANGO_ALLOWED_HOSTS=.*|DJANGO_ALLOWED_HOSTS=$DOMAIN,www.$DOMAIN,$IP|" "$APP/.env"
sed -i "s|^DJANGO_CSRF_ORIGINS=.*|DJANGO_CSRF_ORIGINS=https://$DOMAIN,https://www.$DOMAIN|" "$APP/.env"
sed -i "s|^DJANGO_HTTPS=.*|DJANGO_HTTPS=1|" "$APP/.env"
systemctl restart mona
echo "Готово: https://$DOMAIN/"
