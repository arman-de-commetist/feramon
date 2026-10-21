from django.db import migrations

PERFUMES = [
    {
        'slug': 'nezhnyi',
        'name': 'Нежный',
        'tagline': 'Средний нежный запах',
        'traits': 'Женственный, Притягательный, Стойкий',
        'theme': 'rose',
        'image': 'products/nezhnyi.webp',
        'lead': 'Сочный грейпфрут, белые цветы и тёплая ваниль — аромат, который обнимает.',
        'description': 'Как утро в цветущем саду: сочные цитрусы и спелый персик, белые цветы в каплях '
                       'росы и романтичный жасмин. А следом — тёплая ваниль и искрящийся юзу, которые '
                       'остаются на коже до самого вечера мягким, притягательным шлейфом.',
        'variant': ('30 мл', 'extrait de parfum', 29990),
        'notes': [
            ('top', 'Цитрусовый', 'Свежий · бодрящий', '🍊', '#ffd8b8'),
            ('top', 'Белые цветы', 'Чистый · нежный', '🌼', '#eef5e4'),
            ('top', 'Фруктовый', 'Сочный · игривый', '🍑', '#ffd2c4'),
            ('middle', 'Цветочный', 'Романтичный · женственный', '🌹', '#ffc9d6'),
            ('middle', 'Жасмин', 'Нежный · элегантный', '💮', '#f1f4e6'),
            ('middle', 'Сладкий', 'Мягкий · обволакивающий', '🌸', '#ffd5e4'),
            ('base', 'Ваниль', 'Тёплый · уютный', '🍮', '#f5e6c8'),
            ('base', 'Лимон', 'Свежий · освежающий', '🍋', '#fff1b0'),
            ('base', 'Юзу', 'Сочный · цитрусовый', '🟡', '#ffe58a'),
            ('base', 'Жасмин', 'Нежный · стойкий', '🤍', '#eef3e6'),
        ],
    },
    {
        'slug': 'holodnyi',
        'name': 'Холодный',
        'tagline': 'Холодный запах',
        'traits': 'Запах чистоты, Запах свежести, Освежающий',
        'theme': 'ice',
        'image': 'products/holodnyi.webp',
        'lead': 'Прохлада горного воздуха, белый мускус и фиалка — аромат кристальной чистоты.',
        'description': 'Свежесть, которую хочется вдыхать снова и снова. Воздушные альдегиды и белый мускус '
                       'звучат как прохлада после дождя и чистое бельё на ветру. Фиалка, цветок апельсина '
                       'и роза добавляют утончённой нежности, а лимон и юзу — искрящейся энергии.',
        'variant': ('50 мл', 'extrait de parfum', 39990),
        'notes': [
            ('top', 'Альдегидный', 'Свежий · воздушный', '🫧', '#dde9ff'),
            ('top', 'Мускусный', 'Нежный · чистый', '☁️', '#f1f3fa'),
            ('top', 'Цветочный', 'Лёгкий · женственный', '🌸', '#ffdbe6'),
            ('middle', 'Фиалка', 'Нежная · элегантная', '🪻', '#e6defc'),
            ('middle', 'Цветок апельсина', 'Свежий · романтичный', '🌼', '#f2f6e8'),
            ('middle', 'Роза', 'Женственная · утончённая', '🌹', '#ffd3df'),
            ('base', 'Лимон', 'Освежающий · цитрусовый', '🍋', '#fff3b8'),
            ('base', 'Юзу', 'Свежий · бодрящий', '🟡', '#ffeaa0'),
            ('base', 'Жасмин', 'Нежный · стойкий', '🤍', '#eef2f8'),
        ],
    },
    {
        'slug': 'sladkii',
        'name': 'Сладкий',
        'tagline': 'Сладкий женственный запах',
        'traits': 'Притягательный, Стойкий, Шлейфовый, Обвораживающий',
        'theme': 'caramel',
        'image': 'products/sladkii.webp',
        'lead': 'Взбитые сливки, ваниль и белый шоколад — десерт, от которого невозможно оторваться.',
        'description': 'Утро в парижской кондитерской: воздушные сливки, тёплое молоко и тончайшие сахарные '
                       'нити. В сердце — обволакивающая ваниль, нежный пион и цветок апельсина. А шлейф '
                       'из белого шоколада, амбры и мягкого мускуса держится часами и сводит с ума.',
        'variant': ('100 мл', 'extrait de parfum', 54990),
        'notes': [
            ('top', 'Сливки', 'Нежный · воздушный · аппетитный', '🍦', '#fff4e6'),
            ('top', 'Молоко', 'Мягкий · кремовый · бархатный', '🥛', '#f6f1ea'),
            ('top', 'Сахарные нити', 'Деликатная сладость', '🍬', '#ffe3c4'),
            ('middle', 'Ваниль', 'Тёплая · женственная · обволакивающая', '🍮', '#f5e3c3'),
            ('middle', 'Пион', 'Нежный · элегантный · цветочный', '🌺', '#ffd0dc'),
            ('middle', 'Цветок апельсина', 'Романтичный · свежий · утончённый', '🌼', '#f5f2e4'),
            ('base', 'Сахар', 'Сладкий · уютный · стойкий', '🧁', '#fbefe6'),
            ('base', 'Белый шоколад', 'Нежный · обволакивающий · кремовый', '🍫', '#f3e4cf'),
            ('base', 'Амбра', 'Тёплая · глубокая · сенсуальная', '🔶', '#ffd9a8'),
            ('base', 'Мускус', 'Мягкий · притягательный · шлейфовый', '☁️', '#f4efeb'),
        ],
    },
]


def seed(apps, schema_editor):
    Product = apps.get_model('shop', 'Product')
    Variant = apps.get_model('shop', 'Variant')
    Note = apps.get_model('shop', 'Note')
    Order = apps.get_model('shop', 'Order')

    for position, data in enumerate(PERFUMES):
        data = dict(data)
        notes = data.pop('notes')
        label, sublabel, price = data.pop('variant')
        slug = data.pop('slug')
        product, _ = Product.objects.update_or_create(
            slug=slug, defaults={**data, 'position': position, 'old_price': None, 'is_active': True},
        )
        # keep variants that already have orders, replace the rest
        product.variants.exclude(pk__in=Order.objects.values('variant')).delete()
        Variant.objects.create(product=product, label=label, sublabel=sublabel, price=price)
        product.notes.all().delete()
        for i, (tier, name, desc, emoji, color) in enumerate(notes):
            Note.objects.create(product=product, tier=tier, name=name, description=desc,
                                emoji=emoji, color=color, position=i)


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_product_collection'),
    ]

    operations = [
        migrations.RunPython(seed, migrations.RunPython.noop),
    ]
