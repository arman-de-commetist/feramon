"""Ready-made WhatsApp messages: every «write to a manager» button opens a chat with text that matches the page."""
from urllib.parse import quote

from django.utils.translation import gettext as _

from .dyson import CHOICES as DYSON_COLORS
from .models import GiftPerfume, Product, Variant


def _money(n):
    return f'{n:,}'.replace(',', ' ') + ' ₸'


def _vol(label):
    return label.replace('мл', _('мл'))


def topic_message(params):
    """Text for a chat started from a page. params: topic, v (variant id), p (product slug)."""
    variant = None
    if str(params.get('v', '')).isdigit():
        variant = Variant.objects.select_related('product').filter(pk=params['v'], product__is_active=True).first()
    product = variant.product if variant else Product.objects.filter(slug=params.get('p', ''), is_active=True).first()
    topic = params.get('topic', '')

    if variant and variant.gift_type == Variant.DYSON:
        color = dict(DYSON_COLORS).get(params.get('color', ''))
        if color:
            msg = _('Здравствуйте! Меня интересует феромон MONA «%(name)s» %(vol)s с подарком Dyson Airwrap, цвет: %(color)s. Подскажите, пожалуйста, подробнее 🌸')
            msg = msg % {'name': product.tr('name'), 'vol': _vol(variant.label), 'color': color}
        else:
            msg = _('Здравствуйте! Меня интересует феромон MONA «%(name)s» %(vol)s с подарком Dyson Airwrap. Подскажите, пожалуйста, подробнее 🌸')
            msg = msg % {'name': product.tr('name'), 'vol': _vol(variant.label)}
        engraving = (params.get('e') or '').strip()[:20]
        if engraving:
            msg += ' ' + _('Имя на корпусе: %(name)s.') % {'name': engraving}
        return msg
    if variant and variant.gift_type == Variant.PERFUME:
        ids = [i for i in (params.getlist('g') if hasattr(params, 'getlist') else []) if str(i).isdigit()][:variant.gift_count]
        chosen = ', '.join(str(g) for g in GiftPerfume.objects.filter(pk__in=ids, is_active=True))
        if chosen:
            msg = _('Здравствуйте! Хочу заказать MONA «%(name)s» %(vol)s. В подарок выбираю: %(gifts)s 🌸')
            return msg % {'name': product.tr('name'), 'vol': _vol(variant.label), 'gifts': chosen}
        if variant.gift_count == 1:
            return _('Здравствуйте! Хочу заказать MONA «%(name)s» %(vol)s и выбрать французский парфюм в подарок 🌸') % {
                'name': product.tr('name'), 'vol': _vol(variant.label)}
        return _('Здравствуйте! Хочу заказать MONA «%(name)s» %(vol)s и выбрать %(n)s французских парфюма в подарок 🌸') % {
            'name': product.tr('name'), 'vol': _vol(variant.label), 'n': variant.gift_count}
    if product:
        msg = _('Здравствуйте! Меня интересует феромон MONA «%(name)s». Какой объём посоветуете и какой подарок к нему идёт?')
        return msg % {'name': product.tr('name')}
    if topic == 'dyson':
        return _('Здравствуйте! Меня интересует феромон MONA 100 мл с подарком Dyson Airwrap. Подскажите, пожалуйста, подробнее 🌸')
    if topic == 'gifts':
        return _('Здравствуйте! Хочу заказать MONA и выбрать французский парфюм в подарок. Расскажите подробнее 🌸')
    if topic == 'cart':
        return _('Здравствуйте! У меня вопрос по заказу MONA на сайте.')
    return _('Здравствуйте! Меня интересуют феромоны MONA и акция −50% с подарком.')


def order_message(order):
    """Full order text that the customer sends to their manager after checkout."""
    lines = [_('Здравствуйте! Я оформил(а) заказ №%(n)s на сайте MONA.') % {'n': order.pk}, '']
    for item in order.items.all():
        v = item.variant
        lines.append(f'• MONA «{v.product.tr("name")}» {_vol(v.label)} — {_money(item.price)}')
        if item.gift_color:
            gift = f'Dyson Airwrap, {item.get_gift_color_display()}'
            if item.engraving:
                gift += ', ' + _('имя: %(name)s') % {'name': item.engraving}
            lines.append('   ' + _('Подарок') + ': ' + gift)
        else:
            perfumes = ', '.join(str(g) for g in item.gift_perfumes.all())
            if perfumes:
                lines.append('   ' + _('Подарок') + ': ' + perfumes)
    lines += [
        '',
        _('Итого: %(sum)s') % {'sum': _money(order.total)},
        _('Имя: %(v)s') % {'v': order.name},
        _('Телефон: %(v)s') % {'v': order.phone},
        _('Город: %(v)s') % {'v': order.city},
        _('Доставка: %(v)s') % {'v': order.get_delivery_display()},
        _('Оплата: %(v)s') % {'v': order.get_payment_display()},
    ]
    if order.comment:
        lines.append(_('Комментарий: %(v)s') % {'v': order.comment})
    return '\n'.join(lines)


def wa_number_link(digits, text):
    text = ''.join(ch for ch in text if ord(ch) <= 0xFFFF)
    text = chr(10).join(line.rstrip() for line in text.splitlines())
    return f'https://wa.me/{digits}?text={quote(text)}'


def wa_link(manager, text):
    # WhatsApp (desktop / web) shows emoji that arrive through a link as «�», so keep the text emoji-free
    text = ''.join(ch for ch in text if ord(ch) <= 0xFFFF)
    text = '\n'.join(line.rstrip() for line in text.splitlines())
    return f'https://wa.me/{manager.wa_digits()}?text={quote(text)}'
