release: python manage.py migrate --noinput && python manage.py compiletranslations && python manage.py collectstatic --noinput
web: gunicorn mona.wsgi --bind 0.0.0.0:$PORT --workers 3 --timeout 60
