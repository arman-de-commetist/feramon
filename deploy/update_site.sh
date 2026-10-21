#!/usr/bin/env bash
# MONA Perfume — update the code on the server, KEEPING the server's orders, reviews and photos.
# 1) on the computer: python deploy/make_archive.py --code-only   2) scp mona-site.zip root@IP:/root/
# 3) on the server:   bash /srv/mona/deploy/update_site.sh
set -euo pipefail
APP=/srv/mona
ZIP=/root/mona-site.zip
[ -f "$ZIP" ] || { echo "Нет файла $ZIP"; exit 1; }

cp "$APP/db.sqlite3" "/root/db-backup-$(date +%Y%m%d-%H%M).sqlite3"
# the archive made with --code-only has no db.sqlite3 and no media/, so they stay untouched
unzip -oq "$ZIP" -x 'db.sqlite3' 'media/*' -d "$APP"
cd "$APP"
"$APP/.venv/bin/pip" install -r requirements.txt -q
set -a; . "$APP/.env"; set +a
"$APP/.venv/bin/python" manage.py migrate --noinput
"$APP/.venv/bin/python" manage.py compiletranslations
"$APP/.venv/bin/python" manage.py collectstatic --noinput -v 0
chown -R mona:mona "$APP"
systemctl restart mona
echo "Обновлено. Копия базы до обновления лежит в /root/db-backup-*.sqlite3"
