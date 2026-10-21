"""Send a test message to the Telegram chat configured for order notifications.

Usage:
    set TELEGRAM_BOT_TOKEN=123456:ABC...
    set TELEGRAM_CHAT_ID=123456789
    python manage.py testtelegram
"""
import json
import urllib.error
import urllib.request

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Send a test order notification to Telegram.'

    def handle(self, *args, **options):
        token, chat_id = settings.TELEGRAM_BOT_TOKEN, settings.TELEGRAM_CHAT_ID
        if not token or not chat_id:
            raise CommandError('Задайте TELEGRAM_BOT_TOKEN и TELEGRAM_CHAT_ID (см. README).')
        text = '✅ MONA: уведомления о заказах подключены. Сюда будут приходить новые заказы с сайта.'
        req = urllib.request.Request(
            f'https://api.telegram.org/bot{token}/sendMessage',
            data=json.dumps({'chat_id': chat_id, 'text': text}).encode(),
            headers={'Content-Type': 'application/json'},
        )
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                answer = json.loads(r.read())
        except urllib.error.HTTPError as e:
            raise CommandError(f'Telegram ответил ошибкой {e.code}: {e.read().decode(errors="ignore")}')
        except urllib.error.URLError as e:
            raise CommandError(f'Нет связи с Telegram: {e.reason}')
        if not answer.get('ok'):
            raise CommandError(f'Telegram не принял сообщение: {answer}')
        self.stdout.write(self.style.SUCCESS('Сообщение отправлено — проверьте Telegram.'))
