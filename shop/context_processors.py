from pathlib import Path

from . import dyson
from .cart import Cart
from .models import GiftPerfume, Manager, Product, SiteSettings, Variant

STATIC_DIR = Path(__file__).resolve().parent / 'static' / 'shop'


def _asset_version():
    # changes whenever a css/js file changes, so phones don't keep an old cached copy
    return int(max(f.stat().st_mtime for f in STATIC_DIR.glob('*.*')))



def _offer_volumes():
    """One variant per volume (30/50/100 ml) — prices and gifts are the same for every perfume."""
    rows = {}
    for v in Variant.objects.filter(product__is_active=True).select_related('product').order_by('position', 'product__position'):
        rows.setdefault(v.label, v)
    return list(rows.values())



def _wa_query(request):
    """What the «write to a manager» buttons should talk about on the current page."""
    match = getattr(request, 'resolver_match', None)
    name = match.url_name if match else ''
    if name == 'product':
        return f"p={match.kwargs.get('slug', '')}"
    if request.GET.get('v', '').isdigit():
        return f"v={request.GET['v']}"
    return {'dyson': 'topic=dyson', 'gifts': 'topic=gifts', 'gift_perfume': 'topic=gifts', 'cart': 'topic=cart',
            'checkout': 'topic=cart', 'thanks': 'topic=cart'}.get(name, 'topic=general')


def site(request):
    return {
        'site': SiteSettings.load(),
        'asset_v': _asset_version(),
        'nav_products': Product.objects.filter(is_active=True),
        'dyson_variants': list(Variant.objects.filter(product__is_active=True, gift_type=Variant.DYSON)
                               .select_related('product').order_by('product__position', 'product_id')),
        'offer_volumes': _offer_volumes(),
        'offer_gifts': list(GiftPerfume.objects.filter(is_active=True)),
        'dyson_colors': dyson.colors(),
        'managers': list(Manager.objects.filter(is_active=True)),
        'wa_query': _wa_query(request),
        'cart_count': len(Cart(request)) if hasattr(request, 'session') else 0,
    }
