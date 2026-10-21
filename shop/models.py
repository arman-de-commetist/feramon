import uuid
from datetime import date

from django.db import models
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _


class Translatable:
    """Fields with `<field>_en` / `<field>_kk` twins: obj.tr('name') returns the current language."""

    def tr(self, field):
        lang = (get_language() or 'ru')[:2]
        if lang != 'ru':
            value = getattr(self, f'{field}_{lang}', '')
            if value:
                return value
        return getattr(self, field)


class Product(Translatable, models.Model):
    ROSE, ICE, CARAMEL = 'rose', 'ice', 'caramel'
    THEMES = [(ROSE, 'Розовый'), (ICE, 'Холодный голубой'), (CARAMEL, 'Карамельный')]

    name = models.CharField('Название', max_length=100)
    slug = models.SlugField('Адрес (латиницей)', unique=True)
    subtitle = models.CharField('Подзаголовок', max_length=100, default='PHEROMONE')
    tagline = models.CharField('Слоган', max_length=150, blank=True)
    traits = models.CharField('Характеристики (через запятую)', max_length=200, blank=True)
    lead = models.TextField('Короткое описание', blank=True)
    description = models.TextField('Описание «О парфюме»', blank=True)

    name_en = models.CharField('Название (EN)', max_length=100, blank=True)
    tagline_en = models.CharField('Слоган (EN)', max_length=150, blank=True)
    traits_en = models.CharField('Характеристики (EN)', max_length=200, blank=True)
    lead_en = models.TextField('Короткое описание (EN)', blank=True)
    description_en = models.TextField('Описание (EN)', blank=True)
    name_kk = models.CharField('Название (KZ)', max_length=100, blank=True)
    tagline_kk = models.CharField('Слоган (KZ)', max_length=150, blank=True)
    traits_kk = models.CharField('Характеристики (KZ)', max_length=200, blank=True)
    lead_kk = models.TextField('Короткое описание (KZ)', blank=True)
    description_kk = models.TextField('Описание (KZ)', blank=True)
    image = models.FileField('Фото / постер', upload_to='products/', blank=True)
    theme = models.CharField('Цветовая тема', max_length=10, choices=THEMES, default=ROSE)
    old_price = models.PositiveIntegerField('Старая цена, ₸', null=True, blank=True)
    rating = models.DecimalField('Рейтинг', max_digits=2, decimal_places=1, default=5)
    position = models.PositiveSmallIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Показывать на сайте', default=True)

    class Meta:
        ordering = ['position', 'id']
        verbose_name = 'Парфюм'
        verbose_name_plural = 'Парфюмы'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('product', args=[self.slug])

    def trait_list(self):
        return [t.strip() for t in self.tr('traits').split(',') if t.strip()]

    def main_variant(self):
        return self.variants.first()

    def gift_variant(self):
        return next((v for v in self.variants.all() if v.gift_type == Variant.DYSON), None)

    def discount(self):
        main = self.main_variant()
        if not (main and self.old_price and self.old_price > main.price):
            return None
        return round((1 - main.price / self.old_price) * 100)


class Variant(Translatable, models.Model):
    PERFUME, DYSON = 'perfume', 'dyson'
    GIFT_TYPES = [('', 'Без подарка'), (PERFUME, 'Французский парфюм'), (DYSON, 'Dyson Airwrap')]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    label = models.CharField('Объём', max_length=50)
    sublabel = models.CharField('Подпись', max_length=50, blank=True)
    price = models.PositiveIntegerField('Цена, ₸')
    old_price = models.PositiveIntegerField('Старая цена, ₸', null=True, blank=True)
    gift_type = models.CharField('Тип подарка', max_length=10, choices=GIFT_TYPES, blank=True)
    gift_count = models.PositiveSmallIntegerField('Сколько подарков', default=0,
                                                  help_text='Для французских парфюмов: 1 или 2')
    gift = models.CharField('Подарок к покупке', max_length=100, blank=True,
                            help_text='Например: Стайлер Dyson в подарок. Пусто — без подарка.')
    gift_en = models.CharField('Подарок (EN)', max_length=100, blank=True)
    gift_kk = models.CharField('Подарок (KZ)', max_length=100, blank=True)
    position = models.PositiveSmallIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['position', 'id']
        verbose_name = 'Вариант (объём и цена)'
        verbose_name_plural = 'Варианты (объём и цена)'

    def __str__(self):
        return f'{self.product} — {self.label}'

    def discount(self):
        if self.old_price and self.old_price > self.price:
            return int((1 - self.price / self.old_price) * 100)  # 39 500 of 80 000 -> 50%, not 51%
        return None

    def saving(self):
        return (self.old_price - self.price) if self.discount() else 0


class Note(Translatable, models.Model):
    TOP, MIDDLE, BASE = 'top', 'middle', 'base'
    TIERS = [(TOP, _('Верхние ноты')), (MIDDLE, _('Средние ноты')), (BASE, _('Базовые ноты'))]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='notes')
    tier = models.CharField('Уровень', max_length=10, choices=TIERS)
    name = models.CharField('Нота', max_length=50)
    description = models.CharField('Описание', max_length=100, blank=True)
    name_en = models.CharField('Нота (EN)', max_length=50, blank=True)
    description_en = models.CharField('Описание (EN)', max_length=100, blank=True)
    name_kk = models.CharField('Нота (KZ)', max_length=50, blank=True)
    description_kk = models.CharField('Описание (KZ)', max_length=100, blank=True)
    emoji = models.CharField('Иконка (эмодзи)', max_length=8, default='🌸')
    color = models.CharField('Цвет фона иконки', max_length=7, default='#ffe1e7')
    position = models.PositiveSmallIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['position', 'id']
        verbose_name = 'Нота аромата'
        verbose_name_plural = 'Ноты аромата'

    def __str__(self):
        return f'{self.get_tier_display()}: {self.name}'


class Review(models.Model):
    name = models.CharField('Имя', max_length=60)
    text = models.TextField('Отзыв')
    rating = models.PositiveSmallIntegerField('Оценка', null=True, blank=True, help_text='У ответов оценки нет.')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies',
                               verbose_name='Ответ на отзыв')
    is_staff_reply = models.BooleanField('Ответ магазина', default=False)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Аромат',
                                related_name='reviews')
    is_published = models.BooleanField('Опубликован', default=True,
                                       help_text='Снимите галочку, чтобы скрыть отзыв или ответ с сайта.')
    created = models.DateTimeField('Дата', auto_now_add=True)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.name}: {self.text[:40]}'


class GiftPerfume(Translatable, models.Model):
    WOMEN, MEN, UNISEX = 'w', 'm', 'u'
    GENDERS = [(WOMEN, _('Женский')), (MEN, _('Мужской')), (UNISEX, _('Унисекс'))]

    brand = models.CharField('Бренд', max_length=60)
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField('Адрес (латиницей)', unique=True)
    image = models.FileField('Фото', upload_to='gifts/', blank=True)
    gender = models.CharField('Для кого', max_length=1, choices=GENDERS, default=WOMEN)
    notes = models.CharField('Ноты', max_length=200, blank=True)
    description = models.TextField('Описание', blank=True)
    notes_en = models.CharField('Ноты (EN)', max_length=200, blank=True)
    description_en = models.TextField('Описание (EN)', blank=True)
    notes_kk = models.CharField('Ноты (KZ)', max_length=200, blank=True)
    description_kk = models.TextField('Описание (KZ)', blank=True)
    position = models.PositiveSmallIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Доступен в подарок', default=True)

    class Meta:
        ordering = ['position', 'id']
        verbose_name = 'Парфюм в подарок'
        verbose_name_plural = 'Парфюмы в подарок'

    def __str__(self):
        return f'{self.brand} {self.name}'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('gift_perfume', args=[self.slug])


from .dyson import CHOICES as GIFT_COLORS  # noqa: E402  (4 Dyson Airwrap colours)


class Manager(models.Model):
    ROSE, WINE, CARAMEL, GOLD = 'rose', 'wine', 'caramel', 'gold'
    TONES = [(ROSE, 'Розовый'), (WINE, 'Бордовый'), (CARAMEL, 'Карамельный'), (GOLD, 'Золотой')]

    name = models.CharField('Имя', max_length=60)
    phone = models.CharField('Телефон', max_length=20, help_text='Например: 8 707 711 3214')
    whatsapp = models.CharField('WhatsApp', max_length=20, blank=True,
                                help_text='Если пусто — используется телефон')
    title = models.CharField('Должность', max_length=60, blank=True, help_text='Пусто — «Консультант MONA»')
    languages = models.CharField('Языки', max_length=40, blank=True, help_text='Например: RU, ҚАЗ')
    hours = models.CharField('Часы работы', max_length=60, blank=True)
    photo = models.FileField('Фото', upload_to='managers/', blank=True)
    tone = models.CharField('Цвет аватара', max_length=10, choices=TONES, default=ROSE)
    position = models.PositiveSmallIntegerField('Порядок', default=0)
    is_active = models.BooleanField('Показывать на сайте', default=True)
    in_rotation = models.BooleanField('Получает новых клиентов', default=True,
                                      help_text='Снимите галочку, если менеджер в отпуске')
    last_order = models.DateTimeField('Последний заказ', null=True, blank=True, editable=False)
    last_chat = models.DateTimeField('Последний чат с сайта', null=True, blank=True, editable=False)
    chats = models.PositiveIntegerField('Переходов в WhatsApp', default=0, editable=False)

    class Meta:
        ordering = ['position', 'id']
        verbose_name = 'Менеджер'
        verbose_name_plural = 'Менеджеры'

    def __str__(self):
        return self.name

    @staticmethod
    def _digits(value):
        d = ''.join(c for c in value if c.isdigit())
        if len(d) == 11 and d[0] == '8':
            d = '7' + d[1:]
        if len(d) == 10:
            d = '7' + d
        return d

    def wa_digits(self):
        return self._digits(self.whatsapp or self.phone)

    def tel(self):
        return '+' + self._digits(self.phone)

    def phone_display(self):
        d = self._digits(self.phone)
        if len(d) == 11:
            return f'+{d[0]} {d[1:4]} {d[4:7]} {d[7:9]} {d[9:]}'
        return self.phone

    def initial(self):
        return self.name[:1].upper()

    @classmethod
    def next_in_line(cls, field):
        """Round robin: the active manager who got a client longest ago (never = first)."""
        return (cls.objects.filter(is_active=True, in_rotation=True)
                .order_by(models.F(field).asc(nulls_first=True), 'position', 'id').first())


class Order(models.Model):
    NEW, CONFIRMED, SENT, DONE, CANCELLED = 'new', 'confirmed', 'sent', 'done', 'cancelled'
    STATUSES = [
        (NEW, 'Новый'),
        (CONFIRMED, 'Подтверждён'),
        (SENT, 'Отправлен'),
        (DONE, 'Выполнен'),
        (CANCELLED, 'Отменён'),
    ]

    DELIVERY = [
        ('courier', _('Курьер по городу')),
        ('post', _('Казпочта по Казахстану')),
        ('cdek', _('СДЭК')),
        ('pickup', _('Самовывоз')),
    ]
    PAYMENT = [
        ('kaspi_transfer', _('Kaspi перевод')),
        ('kaspi_qr', _('Kaspi QR')),
        ('cash', _('Наличными при получении')),
    ]

    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField('Имя', max_length=80)
    phone = models.CharField('Телефон', max_length=20)
    city = models.CharField('Город', max_length=60)
    delivery = models.CharField('Доставка', max_length=10, choices=DELIVERY, default='courier')
    payment = models.CharField('Оплата', max_length=15, choices=PAYMENT, default='kaspi_transfer')
    comment = models.TextField('Комментарий', blank=True)
    status = models.CharField('Статус', max_length=10, choices=STATUSES, default=NEW)
    manager = models.ForeignKey('Manager', on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name='Менеджер', related_name='orders')
    created = models.DateTimeField('Создан', auto_now_add=True)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ №{self.pk} — {self.name}'

    @property
    def total(self):
        return sum(i.price for i in self.items.all())

    @property
    def old_total(self):
        return sum(i.old_price or i.price for i in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    variant = models.ForeignKey(Variant, on_delete=models.PROTECT, verbose_name='Аромат')
    price = models.PositiveIntegerField('Цена, ₸')
    old_price = models.PositiveIntegerField('Старая цена, ₸', null=True, blank=True)
    gift = models.CharField('Подарок', max_length=100, blank=True)
    gift_color = models.CharField('Цвет Dyson', max_length=10, blank=True, choices=GIFT_COLORS)
    engraving = models.CharField('Имя на Dyson', max_length=20, blank=True)
    gift_perfumes = models.ManyToManyField(GiftPerfume, blank=True, verbose_name='Парфюмы в подарок')

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    def __str__(self):
        return str(self.variant)

    def gift_summary(self):
        if self.gift_color or self.engraving:
            parts = [self.gift or 'Dyson', str(self.get_gift_color_display())]
            if self.engraving:
                parts.append(f'имя: {self.engraving}')
            return ' · '.join(p for p in parts if p)
        perfumes = ', '.join(str(g) for g in self.gift_perfumes.all())
        return f'{self.gift}: {perfumes}' if perfumes else self.gift


class Article(Translatable, models.Model):
    title = models.CharField('Заголовок', max_length=150)
    slug = models.SlugField('Адрес (латиницей)', unique=True)
    excerpt = models.CharField('Коротко', max_length=250, blank=True)
    body = models.TextField('Текст', help_text='Абзацы разделяйте пустой строкой.')
    title_en = models.CharField('Заголовок (EN)', max_length=150, blank=True)
    excerpt_en = models.CharField('Коротко (EN)', max_length=250, blank=True)
    body_en = models.TextField('Текст (EN)', blank=True)
    title_kk = models.CharField('Заголовок (KZ)', max_length=150, blank=True)
    excerpt_kk = models.CharField('Коротко (KZ)', max_length=250, blank=True)
    body_kk = models.TextField('Текст (KZ)', blank=True)
    emoji = models.CharField('Иконка', max_length=8, default='🌸')
    image = models.FileField('Картинка', upload_to='blog/', blank=True)
    published = models.DateField('Дата публикации', default=date.today)
    is_published = models.BooleanField('Опубликована', default=True)

    class Meta:
        ordering = ['-published', '-id']
        verbose_name = 'Статья'
        verbose_name_plural = 'Блог'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('article', args=[self.slug])

    def paragraphs(self):
        return [p.strip() for p in self.tr('body').split('\n\n') if p.strip()]


class GalleryPhoto(Translatable, models.Model):
    image = models.FileField('Фото', upload_to='gallery/')
    caption = models.CharField('Подпись', max_length=120, blank=True)
    caption_en = models.CharField('Подпись (EN)', max_length=120, blank=True)
    caption_kk = models.CharField('Подпись (KZ)', max_length=120, blank=True)
    position = models.PositiveSmallIntegerField('Порядок', default=0)

    class Meta:
        ordering = ['position', 'id']
        verbose_name = 'Фото галереи'
        verbose_name_plural = 'Галерея'

    def __str__(self):
        return self.caption or self.image.name


class SiteSettings(Translatable, models.Model):
    phone = models.CharField('Телефон', max_length=30, blank=True)
    whatsapp = models.CharField('WhatsApp (номер, только цифры, напр. 77011234567)', max_length=20, blank=True)
    telegram = models.CharField('Telegram (ник без @)', max_length=60, blank=True)
    instagram = models.CharField('Instagram (ник без @)', max_length=60, blank=True)
    tiktok = models.CharField('TikTok (ник без @)', max_length=60, blank=True)
    email = models.EmailField('Email', blank=True)
    city = models.CharField('Город', max_length=100, blank=True)
    hours = models.CharField('Часы работы', max_length=100, blank=True)
    address = models.CharField('Адрес (самовывоз / шоурум)', max_length=200, blank=True)
    address_en = models.CharField('Адрес (EN)', max_length=200, blank=True)
    address_kk = models.CharField('Адрес (KZ)', max_length=200, blank=True)
    map_url = models.URLField('Ссылка на 2GIS', blank=True)
    kaspi_url = models.URLField('Ссылка Kaspi QR / Kaspi Pay', blank=True,
                                help_text='Например: https://pay.kaspi.kz/pay/… — по ней сайт рисует QR-код для оплаты')
    order_phone = models.CharField('Номер для заказов (WhatsApp)', max_length=20, blank=True,
                                   help_text='Все оформленные заказы уходят на этот номер. Пусто — по очереди менеджерам.')

    class Meta:
        verbose_name = 'Контакты сайта'
        verbose_name_plural = 'Контакты сайта'

    def __str__(self):
        return 'Контакты сайта'

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def instagram_url(self):
        nick = self.instagram.strip().lstrip('@').split('?')[0].rstrip('/').split('/')[-1]
        return f'https://www.instagram.com/{nick}/' if nick else ''

    def tiktok_url(self):
        nick = self.tiktok.strip().lstrip('@').split('?')[0].rstrip('/').split('/')[-1].lstrip('@')
        return f'https://www.tiktok.com/@{nick}' if nick else ''

    def order_digits(self):
        d = ''.join(c for c in self.order_phone if c.isdigit())
        if len(d) == 11 and d[0] == '8':
            d = '7' + d[1:]
        return d

    def order_phone_display(self):
        d = self.order_digits()
        return f'+{d[0]} {d[1:4]} {d[4:7]} {d[7:9]} {d[9:]}' if len(d) == 11 else self.order_phone

    def whatsapp_url(self):
        digits = ''.join(c for c in self.whatsapp if c.isdigit())
        return f'https://wa.me/{digits}' if digits else ''
