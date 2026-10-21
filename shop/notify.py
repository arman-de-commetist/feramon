import json
import logging
import urllib.request

from django.conf import settings

logger = logging.getLogger(__name__)


def _money(n):
    return f'{n:,}'.replace(',', ' ') + ' ₸'


def notify_new_order(order):
    """Send a Telegram message about a new order if a bot is configured."""
    token, chat_id = settings.TELEGRAM_BOT_TOKEN, settings.TELEGRAM_CHAT_ID
    if not (token and chat_id):
        return
    lines = [f'🛍 Новый заказ №{order.pk} — {_money(order.total)}']
    for item in order.items.all():
        lines.append(f'• {item.variant} — {_money(item.price)}')
        if item.gift:
            lines.append(f'   🎁 {item.gift_summary()}')
    lines += [
        f'👤 {order.name}', f'📞 {order.phone}', f'📍 {order.city}',
        f'🚚 {order.get_delivery_display()}', f'💳 {order.get_payment_display()}',
        f'💬 {order.comment or "—"}',
        f'👩‍💼 Менеджер: {order.manager or "—"}',
    ]
    req = urllib.request.Request(
        f'https://api.telegram.org/bot{token}/sendMessage',
        data=json.dumps({'chat_id': chat_id, 'text': '\n'.join(lines)}).encode(),
        headers={'Content-Type': 'application/json'},
    )
    try:
        urllib.request.urlopen(req, timeout=5)
    except Exception:
        logger.exception('Не удалось отправить уведомление в Telegram')


def notify_new_review(review):
    """Reviews and answers appear on the site at once — tell the owner so a bad one can be hidden quickly."""
    token, chat_id = settings.TELEGRAM_BOT_TOKEN, settings.TELEGRAM_CHAT_ID
    if not (token and chat_id):
        return
    head = f'💬 Ответ на отзыв {review.parent.name}' if review.parent_id else f'⭐ Новый отзыв {"★" * (review.rating or 0)}'
    text = f'{head}\n👤 {review.name}\n{review.text}\n\nСкрыть можно в админке: Отзывы → снять «Опубликован».'
    req = urllib.request.Request(
        f'https://api.telegram.org/bot{token}/sendMessage',
        data=json.dumps({'chat_id': chat_id, 'text': text}).encode(),
        headers={'Content-Type': 'application/json'},
    )
    try:
        urllib.request.urlopen(req, timeout=5)
    except Exception:
        logger.exception('Не удалось отправить уведомление в Telegram')
