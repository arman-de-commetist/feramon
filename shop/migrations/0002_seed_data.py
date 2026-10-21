from django.db import migrations

NOTES = [
    ('top', 'Цитрусовый', 'Свежий · бодрящий', '🍊', '#ffd8b8'),
    ('top', 'Белые цветы', 'Чистый · нежный', '🌼', '#eef5e4'),
    ('top', 'Фруктовый', 'Сочный · игривый', '🍑', '#ffd2c4'),
    ('middle', 'Цветочный', 'Романтичный · женственный', '🌹', '#ffc9d6'),
    ('middle', 'Жасмин', 'Нежный · элегантный', '💮', '#f1f4e6'),
    ('middle', 'Сладкий', 'Мягкий · обволакивающий', '🌸', '#ffd5e4'),
    ('base', 'Ваниль', 'Тёплый · уютный', '🍦', '#f5e6c8'),
    ('base', 'Лимон', 'Свежий · освежающий', '🍋', '#fff1b0'),
    ('base', 'Юзу', 'Сочный · цитрусовый', '🟡', '#ffe58a'),
    ('base', 'Жасмин', 'Нежный · стойкий', '🤍', '#eef3e6'),
]

VARIANTS = [
    ('30 мл', 'флакон', 29990),
    ('2 × 30 мл', 'набор', 52990),
    ('10 мл', 'travel', 9990),
]

REVIEWS = [
    ('Диана', 'Свежий цитрус утром и уютная сладость к вечеру. Очень женственно.'),
    ('Мария', 'Держится до вечера, а шлейф ванили просто волшебный. Уже второй флакон.'),
    ('Алина', 'Нежный, но заметный. Коллеги весь день спрашивали, что за духи!'),
]


def seed(apps, schema_editor):
    Product = apps.get_model('shop', 'Product')
    Variant = apps.get_model('shop', 'Variant')
    Note = apps.get_model('shop', 'Note')
    Review = apps.get_model('shop', 'Review')

    product = Product.objects.create(
        name='Mona',
        subtitle='PHEROMONE',
        tagline='Средний нежный запах',
        traits='Женственный, Притягательный, Стойкий',
        lead='Сочный грейпфрут, белые цветы и тёплая ваниль. Аромат, который оставляет шлейф '
             'нежности и притягивает взгляды весь день.',
        description='MONA Pheromone создан для женщины, которая притягивает без слов. Солнечные цитрусы '
                    'будят чувства, жасмин и роза раскрывают романтичное сердце, а ваниль оставляет '
                    'тёплый, уютный след, который хочется запомнить.',
        old_price=39000,
        rating=4.9,
    )
    for i, (label, sub, price) in enumerate(VARIANTS):
        Variant.objects.create(product=product, label=label, sublabel=sub, price=price, position=i)
    for i, (tier, name, desc, emoji, color) in enumerate(NOTES):
        Note.objects.create(product=product, tier=tier, name=name, description=desc,
                            emoji=emoji, color=color, position=i)
    for name, text in REVIEWS:
        Review.objects.create(name=name, text=text, rating=5)


def unseed(apps, schema_editor):
    apps.get_model('shop', 'Product').objects.all().delete()
    apps.get_model('shop', 'Review').objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
