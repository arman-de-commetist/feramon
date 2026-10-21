from django.db import migrations

PRODUCTS = {
    'nezhnyi': {
        'name_en': 'Tender', 'name_kk': 'Нәзік',
        'tagline_en': 'Soft, tender scent', 'tagline_kk': 'Жұмсақ нәзік иіс',
        'traits_en': 'Feminine, Alluring, Long-lasting', 'traits_kk': 'Әйелдік, Тартымды, Тұрақты',
        'lead_en': 'Juicy grapefruit, white flowers and warm vanilla — a scent that embraces you.',
        'lead_kk': 'Шырынды грейпфрут, ақ гүлдер және жылы ваниль — сізді құшақтайтын хош иіс.',
        'description_en': 'Like a morning in a blooming garden: juicy citrus and ripe peach, white flowers in '
                          'dewdrops and romantic jasmine. Then warm vanilla and sparkling yuzu stay on your skin '
                          'until evening as a soft, alluring trail.',
        'description_kk': 'Гүлдеген бақтағы таң сияқты: шырынды цитрустар мен піскен шабдалы, шық тамған ақ гүлдер '
                          'және романтикалық жасмин. Одан кейін жылы ваниль мен жарқын юдзу теріде кешке дейін '
                          'жұмсақ, тартымды із қалдырады.',
    },
    'holodnyi': {
        'name_en': 'Cool', 'name_kk': 'Салқын',
        'tagline_en': 'Cool, fresh scent', 'tagline_kk': 'Салқын иіс',
        'traits_en': 'Scent of purity, Scent of freshness, Refreshing',
        'traits_kk': 'Тазалық иісі, Балғындық иісі, Сергітетін',
        'lead_en': 'Cool mountain air, white musk and violet — a scent of crystal purity.',
        'lead_kk': 'Таудың салқын ауасы, ақ мускус және шегіргүл — мөлдір тазалықтың хош иісі.',
        'description_en': 'A freshness you want to breathe in again and again. Airy aldehydes and white musk sound '
                          'like coolness after rain and clean linen in the wind. Violet, orange blossom and rose '
                          'add refined tenderness, while lemon and yuzu bring sparkling energy.',
        'description_kk': 'Қайта-қайта тыныстағыңыз келетін балғындық. Жеңіл альдегидтер мен ақ мускус жаңбырдан '
                          'кейінгі салқындық пен желде кепкен таза мата сияқты естіледі. Шегіргүл, апельсин гүлі '
                          'мен раушан нәзіктік қосады, ал лимон мен юдзу жарқын энергия береді.',
    },
    'sladkii': {
        'name_en': 'Sweet', 'name_kk': 'Тәтті',
        'tagline_en': 'Sweet feminine scent', 'tagline_kk': 'Тәтті әйелдік иіс',
        'traits_en': 'Alluring, Long-lasting, Trailing, Enchanting',
        'traits_kk': 'Тартымды, Тұрақты, Ізі қалатын, Баурайтын',
        'lead_en': 'Whipped cream, vanilla and white chocolate — a dessert you cannot resist.',
        'lead_kk': 'Көпіртілген кілегей, ваниль және ақ шоколад — қарсы тұру мүмкін емес десерт.',
        'description_en': 'A morning in a Parisian patisserie: airy cream, warm milk and delicate sugar threads. '
                          'At the heart — enveloping vanilla, tender peony and orange blossom. And a trail of white '
                          'chocolate, amber and soft musk lasts for hours and drives everyone crazy.',
        'description_kk': 'Париждік кондитерлік дүкендегі таң: жеңіл кілегей, жылы сүт және нәзік қант жіптері. '
                          'Жүрегінде — орап алатын ваниль, нәзік пион және апельсин гүлі. Ал ақ шоколад, амбра '
                          'және жұмсақ мускустан тұратын із сағаттар бойы сақталып, бас айналдырады.',
    },
}

# (ru name, ru description) -> (en name, en description, kk name, kk description)
NOTES = {
    ('Цитрусовый', 'Свежий · бодрящий'): ('Citrus', 'Fresh · invigorating', 'Цитрусты', 'Балғын · сергітетін'),
    ('Белые цветы', 'Чистый · нежный'): ('White flowers', 'Clean · tender', 'Ақ гүлдер', 'Таза · нәзік'),
    ('Фруктовый', 'Сочный · игривый'): ('Fruity', 'Juicy · playful', 'Жемісті', 'Шырынды · ойнақы'),
    ('Цветочный', 'Романтичный · женственный'): ('Floral', 'Romantic · feminine', 'Гүлді', 'Романтикалық · әйелдік'),
    ('Жасмин', 'Нежный · элегантный'): ('Jasmine', 'Tender · elegant', 'Жасмин', 'Нәзік · талғампаз'),
    ('Сладкий', 'Мягкий · обволакивающий'): ('Sweet', 'Soft · enveloping', 'Тәтті', 'Жұмсақ · орап алатын'),
    ('Ваниль', 'Тёплый · уютный'): ('Vanilla', 'Warm · cozy', 'Ваниль', 'Жылы · жайлы'),
    ('Лимон', 'Свежий · освежающий'): ('Lemon', 'Fresh · refreshing', 'Лимон', 'Балғын · сергітетін'),
    ('Юзу', 'Сочный · цитрусовый'): ('Yuzu', 'Juicy · citrusy', 'Юдзу', 'Шырынды · цитрусты'),
    ('Жасмин', 'Нежный · стойкий'): ('Jasmine', 'Tender · long-lasting', 'Жасмин', 'Нәзік · тұрақты'),
    ('Альдегидный', 'Свежий · воздушный'): ('Aldehydic', 'Fresh · airy', 'Альдегидті', 'Балғын · жеңіл'),
    ('Мускусный', 'Нежный · чистый'): ('Musky', 'Tender · clean', 'Мускусты', 'Нәзік · таза'),
    ('Цветочный', 'Лёгкий · женственный'): ('Floral', 'Light · feminine', 'Гүлді', 'Жеңіл · әйелдік'),
    ('Фиалка', 'Нежная · элегантная'): ('Violet', 'Tender · elegant', 'Шегіргүл', 'Нәзік · талғампаз'),
    ('Цветок апельсина', 'Свежий · романтичный'): ('Orange blossom', 'Fresh · romantic', 'Апельсин гүлі', 'Балғын · романтикалық'),
    ('Роза', 'Женственная · утончённая'): ('Rose', 'Feminine · refined', 'Раушан', 'Әйелдік · сыпайы'),
    ('Лимон', 'Освежающий · цитрусовый'): ('Lemon', 'Refreshing · citrusy', 'Лимон', 'Сергітетін · цитрусты'),
    ('Юзу', 'Свежий · бодрящий'): ('Yuzu', 'Fresh · invigorating', 'Юдзу', 'Балғын · сергітетін'),
    ('Сливки', 'Нежный · воздушный · аппетитный'): ('Cream', 'Tender · airy · appetizing', 'Кілегей', 'Нәзік · жеңіл · тәбет ашатын'),
    ('Молоко', 'Мягкий · кремовый · бархатный'): ('Milk', 'Soft · creamy · velvety', 'Сүт', 'Жұмсақ · кремді · барқыттай'),
    ('Сахарные нити', 'Деликатная сладость'): ('Sugar threads', 'Delicate sweetness', 'Қант жіптері', 'Нәзік тәттілік'),
    ('Ваниль', 'Тёплая · женственная · обволакивающая'): ('Vanilla', 'Warm · feminine · enveloping', 'Ваниль', 'Жылы · әйелдік · орап алатын'),
    ('Пион', 'Нежный · элегантный · цветочный'): ('Peony', 'Tender · elegant · floral', 'Пион', 'Нәзік · талғампаз · гүлді'),
    ('Цветок апельсина', 'Романтичный · свежий · утончённый'): ('Orange blossom', 'Romantic · fresh · refined', 'Апельсин гүлі', 'Романтикалық · балғын · сыпайы'),
    ('Сахар', 'Сладкий · уютный · стойкий'): ('Sugar', 'Sweet · cozy · long-lasting', 'Қант', 'Тәтті · жайлы · тұрақты'),
    ('Белый шоколад', 'Нежный · обволакивающий · кремовый'): ('White chocolate', 'Tender · enveloping · creamy', 'Ақ шоколад', 'Нәзік · орап алатын · кремді'),
    ('Амбра', 'Тёплая · глубокая · сенсуальная'): ('Amber', 'Warm · deep · sensual', 'Амбра', 'Жылы · терең · сезімтал'),
    ('Мускус', 'Мягкий · притягательный · шлейфовый'): ('Musk', 'Soft · alluring · trailing', 'Мускус', 'Жұмсақ · тартымды · ізі қалатын'),
}


def fill(apps, schema_editor):
    Product = apps.get_model('shop', 'Product')
    Note = apps.get_model('shop', 'Note')
    Variant = apps.get_model('shop', 'Variant')
    for slug, fields in PRODUCTS.items():
        Product.objects.filter(slug=slug).update(**fields)
    for note in Note.objects.all():
        t = NOTES.get((note.name, note.description))
        if t:
            note.name_en, note.description_en, note.name_kk, note.description_kk = t
            note.save()
    Variant.objects.exclude(gift='').update(gift_en='Dyson styler as a gift', gift_kk='Dyson стайлері сыйлыққа')


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_translations'),
    ]

    operations = [
        migrations.RunPython(fill, migrations.RunPython.noop),
    ]
