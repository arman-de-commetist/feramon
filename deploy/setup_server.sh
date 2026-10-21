#!/usr/bin/env bash
# MONA Perfume — first install on a fresh Ubuntu 22.04/24.04 VPS (hoster.kz).
# Run as root:   bash setup_server.sh
# Expects /root/mona-site.zip (uploaded from the computer with scp).
set -euo pipefail

APP=/srv/mona
ZIP=/root/mona-site.zip
IP=$(hostname -I | awk '{print $1}')

[ -f "$ZIP" ] || { echo "Нет файла $ZIP — сначала загрузите архив сайта (см. deploy/КАК_ЗАКИНУТЬ_НА_ХОСТИНГ.md)"; exit 1; }

# small servers (1 GB RAM): add 1 GB swap so installs never run out of memory, and use 2 workers
MEM_MB=$(awk '/MemTotal/ {print int($2/1024)}' /proc/meminfo)
WORKERS=3
if [ "$MEM_MB" -lt 1500 ]; then
  WORKERS=2
  if ! swapon --show | grep -q .; then
    echo "==> Мало памяти ($MEM_MB МБ) — добавляю swap 1 ГБ"
    { fallocate -l 1G /swapfile 2>/dev/null || dd if=/dev/zero of=/swapfile bs=1M count=1024 status=none; } && chmod 600 /swapfile && mkswap /swapfile >/dev/null && swapon /swapfile
    grep -q '/swapfile' /etc/fstab || echo '/swapfile none swap sw 0 0' >> /etc/fstab
  fi
fi

echo "==> Устанавливаю Python, nginx"
apt-get update -y
DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-venv python3-pip nginx unzip

echo "==> Распаковываю сайт в $APP"
mkdir -p "$APP"
unzip -oq "$ZIP" -d "$APP"
id -u mona >/dev/null 2>&1 || useradd --system --home "$APP" --shell /usr/sbin/nologin mona

echo "==> Виртуальное окружение и библиотеки"
python3 -m venv "$APP/.venv"
"$APP/.venv/bin/pip" install --upgrade pip -q
"$APP/.venv/bin/pip" install -r "$APP/requirements.txt" -q

if [ ! -f "$APP/.env" ]; then
  echo "==> Создаю $APP/.env (секретный ключ генерируется здесь, на сервере)"
  SECRET=$("$APP/.venv/bin/python" -c 'import secrets; print(secrets.token_urlsafe(50))')
  cat > "$APP/.env" <<EOF
DJANGO_DEBUG=0
DJANGO_SECRET_KEY=$SECRET
DJANGO_ALLOWED_HOSTS=$IP
DJANGO_CSRF_ORIGINS=http://$IP
DJANGO_HTTPS=0
DJANGO_SERVE_MEDIA=0
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
EOF
  chmod 600 "$APP/.env"
fi

echo "==> База, переводы, статика"
cd "$APP"
set -a; . "$APP/.env"; set +a
"$APP/.venv/bin/python" manage.py migrate --noinput
"$APP/.venv/bin/python" manage.py compiletranslations
"$APP/.venv/bin/python" manage.py collectstatic --noinput -v 0
chown -R mona:mona "$APP"

echo "==> Служба gunicorn"
cat > /etc/systemd/system/mona.service <<EOF
[Unit]
Description=MONA Perfume (gunicorn)
After=network.target

[Service]
User=mona
Group=mona
WorkingDirectory=$APP
EnvironmentFile=$APP/.env
ExecStart=$APP/.venv/bin/gunicorn mona.wsgi --bind 127.0.0.1:8000 --workers $WORKERS --timeout 60
Restart=always

[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable --now mona
systemctl restart mona

echo "==> nginx"
cat > /etc/nginx/sites-available/mona <<EOF
server {
    listen 80 default_server;
    server_name _;
    client_max_body_size 20m;

    location /static/ { alias $APP/staticfiles/; expires 30d; access_log off; }
    location /media/  { alias $APP/media/;       expires 7d;  access_log off; }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF
ln -sf /etc/nginx/sites-available/mona /etc/nginx/sites-enabled/mona
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx

sleep 2
if curl -fsS -o /dev/null -H "Host: $IP" "http://127.0.0.1/"; then
  echo
  echo "ГОТОВО! Сайт работает: http://$IP/"
  echo "Админка: http://$IP/admin/  (логин и пароль те же, что на компьютере)"
else
  echo "Что-то пошло не так. Покажите этот вывод:"; systemctl status mona --no-pager | tail -20
fi
