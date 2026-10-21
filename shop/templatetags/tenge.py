from django import template

register = template.Library()


@register.filter
def tenge(value):
    """29990 -> '29 990 ₸'"""
    if value in (None, ''):
        return ''
    return f'{int(value):,}'.replace(',', ' ') + ' ₸'


@register.filter
def tr(obj, field):
    """{{ product|tr:"name" }} — the field in the current language (falls back to Russian)."""
    return obj.tr(field) if obj else ''


@register.filter
def vol(label):
    """'100 мл' -> '100 ml' in English."""
    from django.utils.translation import gettext
    return str(label).replace('мл', gettext('мл'))


@register.simple_tag(takes_context=True)
def absolute(context, path=''):
    """Full https://… address for link previews, canonical links and structured data."""
    request = context.get('request')
    if not request:
        return path
    return request.build_absolute_uri(path or request.path)



@register.simple_tag
def qr_svg(data, dark='#111111'):
    """Inline SVG QR code for a link (Kaspi payment)."""
    import io

    import segno
    from django.utils.safestring import mark_safe
    if not data:
        return ''
    buf = io.BytesIO()
    # high error correction: the «kaspi.kz» badge covers the middle of the code
    qr = segno.make(data, error='h')
    qr.save(buf, kind='svg', scale=10, border=2, dark=dark, light='#ffffff',
            xmldecl=False, svgns=True, svgclass='qr-svg', lineclass=None)
    svg = buf.getvalue().decode()
    # segno writes only width/height; without a viewBox CSS resizing crops the code instead of scaling it
    size = qr.symbol_size(scale=10, border=2)
    svg = svg.replace('<svg ', f'<svg viewBox="0 0 {size[0]} {size[1]}" ', 1)
    return mark_safe(svg)
