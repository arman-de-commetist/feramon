from django.conf import settings
from django.db.models import Count, F, Prefetch
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy
from django.views.decorators.http import require_POST

from .cart import Cart
from .dyson import ATTACHMENTS, CHOICES as DYSON_COLORS
from .forms import AddToCartForm, CheckoutForm, ReplyForm, ReviewForm
from .models import (Article, GalleryPhoto, GiftPerfume, Manager, Note, Order, OrderItem, Product, Review,
                     SiteSettings, Variant)
from .notify import notify_new_order, notify_new_review
from .whatsapp import order_message, topic_message, wa_link, wa_number_link

TIER_TIMES = [gettext_lazy('Первые 15 минут'), gettext_lazy('От 30 минут до 4 часов'), gettext_lazy('Шлейф до 12 часов')]


def _attach_tiers(product):
    notes = list(product.notes.all())
    product.tiers = [
        {'title': title, 'notes': [n for n in notes if n.tier == key], 'time': time}
        for (key, title), time in zip(Note.TIERS, TIER_TIMES)
    ]
    return product


def _active_products():
    return Product.objects.filter(is_active=True).prefetch_related('variants', 'notes')


def _all_variants():
    return list(Variant.objects.filter(product__is_active=True).select_related('product')
                .prefetch_related('product__notes')
                .order_by('product__position', 'product_id', 'position', 'id'))


def _configurator(request, variants, form=None):
    """Context for the perfume + volume + gift picker (shop/_buy.html)."""
    wanted = str(request.GET.get('v', ''))
    if form is not None and form.data.get('variant'):
        wanted = str(form.data.get('variant'))
    selected = next((v for v in variants if str(v.pk) == wanted), variants[0] if variants else None)
    return {
        'variants': variants,
        'selected': selected,
        'cart_form': form or AddToCartForm(initial={
            'variant': selected,
            'gift_color': request.GET.get('color') if request.GET.get('color') in dict(DYSON_COLORS) else None,
        }),
        'gift_perfumes': GiftPerfume.objects.filter(is_active=True),
        'chosen_perfumes': form.data.getlist('gift_perfumes') if form is not None else [],
    }


def _reviews(product=None):
    reviews = Review.objects.filter(is_published=True, parent__isnull=True, rating__isnull=False)
    return {'reviews': reviews.order_by('-rating', '-created')[:6], 'review_count': reviews.count()}


# ---------- shop ----------

def index(request):
    products = [_attach_tiers(p) for p in _active_products()]
    variants = [v for p in products for v in p.variants.all()]
    return render(request, 'shop/index.html', {'products': products, **_configurator(request, variants), **_reviews()})


def product_detail(request, slug):
    product = _attach_tiers(get_object_or_404(_active_products(), slug=slug))
    others = Product.objects.filter(is_active=True).exclude(pk=product.pk).prefetch_related('variants')
    return render(request, 'shop/product.html', {
        'product': product, 'others': others,
        **_configurator(request, list(product.variants.all())), **_reviews(),
    })


def catalog(request):
    return render(request, 'shop/catalog.html', {'products': _active_products()})


def order(request):
    """Standalone picker: choose perfume, volume and gift, then add to the cart."""
    return render(request, 'shop/order.html', {**_configurator(request, _all_variants()), **_reviews()})


@require_POST
def cart_add(request):
    form = AddToCartForm(request.POST)
    if not form.is_valid():
        return render(request, 'shop/order.html', {**_configurator(request, _all_variants(), form), **_reviews()},
                      status=400)
    Cart(request).add(form.cleaned_data)
    if request.POST.get('buy_now'):
        return redirect('checkout')
    messages.success(request, _('Добавлено в корзину: %(item)s') % {
        'item': f"{form.cleaned_data['variant'].product.tr('name')} "
                f"{form.cleaned_data['variant'].label.replace('мл', _('мл'))}"})
    return redirect('cart')


def cart(request):
    c = Cart(request)
    if request.method == 'POST':
        c.remove(request.POST.get('remove', ''))
        return redirect('cart')
    items = c.items()
    return render(request, 'shop/cart.html', {'items': items, **Cart.totals(items)})


def checkout(request):
    c = Cart(request)
    items = c.items()
    if not items:
        return redirect('cart')
    form = CheckoutForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        with transaction.atomic():
            order_obj = form.save(commit=False)
            manager = None if SiteSettings.load().order_phone else Manager.next_in_line('last_order')
            if manager:
                order_obj.manager = manager
                Manager.objects.filter(pk=manager.pk).update(last_order=timezone.now())
            order_obj.save()
            for i in items:
                v = i['variant']
                item = OrderItem.objects.create(
                    order=order_obj, variant=v, price=v.price, old_price=v.old_price, gift=v.gift,
                    gift_color=i['gift_color'], engraving=i['engraving'])
                item.gift_perfumes.set(i['perfumes'])
        c.clear()
        notify_new_order(order_obj)
        return redirect('thanks', token=order_obj.token)
    return render(request, 'shop/checkout.html', {'form': form, 'items': items, **Cart.totals(items)})


def thanks(request, token):
    order_obj = get_object_or_404(Order.objects.prefetch_related('items__variant__product', 'items__gift_perfumes'),
                                  token=token)
    site = SiteSettings.load()
    if site.order_phone:  # every order goes to the single order number
        return render(request, 'shop/thanks.html', {
            'order': order_obj, 'order_desk': site,
            'order_wa': wa_number_link(site.order_digits(), order_message(order_obj)),
        })
    manager = order_obj.manager or Manager.next_in_line('last_order')
    return render(request, 'shop/thanks.html', {
        'order': order_obj, 'manager': manager,
        'order_wa': wa_link(manager, order_message(order_obj)) if manager else '',
    })


# ---------- gifts & offers ----------

def promotions(request):
    return render(request, 'shop/promotions.html', {
        'volumes': _volume_table(), 'gift_perfumes': GiftPerfume.objects.filter(is_active=True)})


def dyson(request):
    return render(request, 'shop/dyson.html', {'attachments': ATTACHMENTS})


def gifts(request):
    return render(request, 'shop/gifts.html', {'gift_perfumes': GiftPerfume.objects.filter(is_active=True),
                                               'volumes': _volume_table()})


def gift_perfume(request, slug):
    perfume = get_object_or_404(GiftPerfume, slug=slug, is_active=True)
    others = GiftPerfume.objects.filter(is_active=True).exclude(pk=perfume.pk)
    return render(request, 'shop/gift_perfume.html', {'perfume': perfume, 'others': others,
                                                      'volumes': _volume_table()})


def _volume_table():
    """One row per volume label (30/50/100 ml) with price, old price and gift — taken from the first perfume."""
    rows = {}
    for v in Variant.objects.filter(product__is_active=True).order_by('position', 'product__position'):
        rows.setdefault(v.label, v)
    return list(rows.values())


def compare(request):
    return render(request, 'shop/compare.html', {'volumes': _volume_table(), 'products': _active_products()})


def quiz(request):
    return render(request, 'shop/quiz.html', {'products': _active_products()})


# ---------- community ----------

# quick picks for the review form; any emoji from the phone keyboard works too
REVIEW_EMOJIS = ('😍 🥰 😊 😘 🤩 😁 😂 🙂 😌 😇 🥹 😢 😮 🤔 😎 🙏 👍 👏 💪 🔥 ✨ 💯 ❤️ 🩷 💖 💕 💝 '
                 '💐 🌸 🌹 🌷 🍒 🍓 🎁 🛍️ 💋 👑 💎 ⭐ 🌟 💫 🧴').split()


def _too_many_posts(request, limit=6, minutes=10):
    """A visitor may post a few reviews/answers per 10 minutes — enough to talk, too few to spam."""
    now = timezone.now().timestamp()
    recent = [t for t in request.session.get('review_posts', []) if now - t < minutes * 60]
    if len(recent) >= limit:
        return True
    request.session['review_posts'] = recent + [now]
    return False


def reviews(request):
    """Reviews with 1–5 stars; anyone can answer a review. Everything is published at once, the owner can hide it."""
    is_reply = request.method == 'POST' and 'parent' in request.POST
    form = ReviewForm(request.POST if request.method == 'POST' and not is_reply else None)
    reply_form = ReplyForm(request.POST if is_reply else None)
    posted = reply_form if is_reply else form
    if request.method == 'POST' and posted.is_valid():
        if posted.cleaned_data.get('website'):  # hidden field only bots fill in
            return redirect('reviews')
        if _too_many_posts(request):
            messages.error(request, _('Слишком много сообщений подряд — попробуйте через несколько минут.'))
            return redirect('reviews')
        item = posted.save(commit=False)
        if is_reply:
            parent = posted.cleaned_data['parent']
            if parent.parent_id:  # answers stay one level deep; mention whom we answer
                item.text = f'@{parent.name}, {item.text}'
                parent = parent.parent
            item.parent = parent
            item.product = parent.product
            item.is_staff_reply = request.user.is_staff
        item.save()
        notify_new_review(item)
        messages.success(request, _('Спасибо! Ответ опубликован.') if is_reply else _('Спасибо за отзыв! Он уже на сайте.'))
        return redirect(f"{reverse('reviews')}#rev-{item.parent_id or item.pk}")

    published = Review.objects.filter(is_published=True)
    roots = published.filter(parent__isnull=True, rating__isnull=False)
    counts = dict(roots.values_list('rating').annotate(n=Count('id')))
    total = sum(counts.values())
    stats = {
        'total': total,
        'avg': round(sum(k * v for k, v in counts.items()) / total, 1) if total else 0,
        'full': int(sum(k * v for k, v in counts.items()) / total + 0.5) if total else 0,
        'rows': [{'stars': s, 'n': counts.get(s, 0), 'pct': round(counts.get(s, 0) * 100 / total) if total else 0}
                 for s in range(5, 0, -1)],
    }
    stars = request.GET.get('stars', '')
    items = roots.select_related('product').prefetch_related(
        Prefetch('replies', queryset=published.order_by('created'), to_attr='shown_replies'))
    if stars.isdigit() and 1 <= int(stars) <= 5:
        items = items.filter(rating=int(stars))
    return render(request, 'shop/reviews.html', {
        'form': form, 'reply_form': reply_form, 'items': items, 'stats': stats, 'stars': stars,
        'open_reply': reply_form['parent'].value() if is_reply else '',
        'emojis': REVIEW_EMOJIS})


def gallery(request):
    return render(request, 'shop/gallery.html', {
        'photos': GalleryPhoto.objects.all(), 'products': Product.objects.filter(is_active=True),
        'gift_perfumes': GiftPerfume.objects.filter(is_active=True)})


def blog(request):
    return render(request, 'shop/blog.html', {'articles': Article.objects.filter(is_published=True)})


def article(request, slug):
    a = get_object_or_404(Article, slug=slug, is_published=True)
    more = Article.objects.filter(is_published=True).exclude(pk=a.pk)[:3]
    return render(request, 'shop/article.html', {'article': a, 'more': more})


# ---------- info ----------

def about(request):
    return render(request, 'shop/about.html', {'products': Product.objects.filter(is_active=True)})


def page(template):
    def view(request):
        return render(request, template)
    return view


def set_language(request, code):
    nxt = request.GET.get('next') or '/'
    if not url_has_allowed_host_and_scheme(nxt, allowed_hosts={request.get_host()}):
        nxt = '/'
    response = redirect(nxt)
    if code in dict(settings.LANGUAGES):
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, code, max_age=365 * 24 * 3600, samesite='Lax')
    return response


def write_to_manager(request):
    """«Написать менеджеру»: open WhatsApp with a ready text; managers take turns unless one is chosen (?m=)."""
    manager = None
    if str(request.GET.get('m', '')).isdigit():
        manager = Manager.objects.filter(pk=request.GET['m'], is_active=True).first()
    # buying (a chosen volume or the cart) always goes to the order desk number
    order_digits = SiteSettings.load().order_digits()
    # buying, or the floating WhatsApp button (?desk=1) — straight to the main number
    buying = (str(request.GET.get('v', '')).isdigit() or request.GET.get('topic') == 'cart'
              or request.GET.get('desk') == '1')
    if not manager and buying and order_digits:
        return redirect(wa_number_link(order_digits, topic_message(request.GET)))
    manager = manager or Manager.next_in_line('last_chat') or Manager.objects.filter(is_active=True).first()
    if not manager:
        return redirect('contacts')
    Manager.objects.filter(pk=manager.pk).update(last_chat=timezone.now(), chats=F('chats') + 1)
    return redirect(wa_link(manager, topic_message(request.GET)))


def robots_txt(request):
    from django.http import HttpResponse
    from django.urls import reverse
    lines = ['User-agent: *', 'Allow: /']
    for path in ['/admin/', '/korzina/', '/oformlenie/', '/spasibo/', '/napisat/', '/lang/']:
        lines.append(f'Disallow: {path}')
    lines.append(f"Sitemap: {request.build_absolute_uri(reverse('sitemap'))}")
    lines.append('')
    return HttpResponse(chr(10).join(lines), content_type='text/plain')
