from django.db import migrations

VOLUMES = {
    # label: (price, old price, gift type, count, gift ru, gift en, gift kk)
    '30 мл': (39500, 80000, 'perfume', 1, 'Французский парфюм 100 мл в подарок',
              'French perfume 100 ml as a gift', 'Сыйлыққа 100 мл француз парфюмі'),
    '50 мл': (55000, 110000, 'perfume', 2, '2 французских парфюма по 100 мл в подарок',
              'Two 100 ml French perfumes as a gift', 'Сыйлыққа 100 мл-ден 2 француз парфюмі'),
    '100 мл': (120000, 240000, 'dyson', 1, 'Dyson Airwrap в подарок',
               'Dyson Airwrap as a gift', 'Сыйлыққа Dyson Airwrap'),
}

GIFTS = [
    ('Chanel', 'Bleu de Chanel', 'bleu-de-chanel', 'gifts/bleu-de-chanel.webp', 'm',
     ('Грейпфрут, мята, имбирь, ладан, кедр', 'Grapefruit, mint, ginger, incense, cedar', 'Грейпфрут, жалбыз, імбір, ладан, балқарағай'),
     ('Свободный и решительный мужской аромат: цитрусовая свежесть, пряный имбирь и глубокий древесный шлейф ладана и кедра.',
      'A free-spirited, determined men\'s fragrance: citrus freshness, spicy ginger and a deep woody trail of incense and cedar.',
      'Еркін әрі батыл ерлер хош иісі: цитрус балғындығы, ащы імбір және ладан мен балқарағайдың терең ағаш ізі.')),
    ('Dior', 'Sauvage', 'dior-sauvage', 'gifts/dior-sauvage.webp', 'm',
     ('Бергамот, перец, лаванда, амброксан', 'Bergamot, pepper, lavender, ambroxan', 'Бергамот, бұрыш, лаванда, амброксан'),
     ('Дикий и благородный: сочный калабрийский бергамот, пряный перец и тёплый, магнетический амброксан.',
      'Wild and noble: juicy Calabrian bergamot, spicy pepper and warm, magnetic ambroxan.',
      'Жабайы әрі асыл: шырынды калабрия бергамоты, ащы бұрыш және жылы, магниттей тартатын амброксан.')),
    ('Emporio Armani', 'Stronger With You Absolutely', 'armani-stronger-with-you-absolutely',
     'gifts/armani-stronger-with-you-absolutely.webp', 'm',
     ('Ром, каштан, ваниль, лаванда', 'Rum, chestnut, vanilla, lavender', 'Ром, талшын, ваниль, лаванда'),
     ('Тёплый и чувственный: ноты рома, жареного каштана и мягкой ванили создают уютный, притягательный шлейф.',
      'Warm and sensual: notes of rum, roasted chestnut and soft vanilla create a cosy, alluring trail.',
      'Жылы әрі сезімтал: ром, қуырылған талшын және жұмсақ ваниль ноталары жайлы, тартымды із қалдырады.')),
    ('Tom Ford', 'Lost Cherry', 'tom-ford-lost-cherry', 'gifts/tom-ford-lost-cherry.webp', 'u',
     ('Вишня, вишнёвый ликёр, горький миндаль, тонка', 'Cherry, cherry liqueur, bitter almond, tonka', 'Шие, шие ликері, ащы бадам, тонка'),
     ('Дерзкий и соблазнительный: сочная тёмная вишня, вишнёвый ликёр и горький миндаль на тёплой базе.',
      'Bold and seductive: juicy dark cherry, cherry liqueur and bitter almond on a warm base.',
      'Батыл әрі азғырушы: шырынды қою шие, шие ликері және жылы базадағы ащы бадам.')),
    ('Yves Saint Laurent', 'Libre', 'ysl-libre', 'gifts/ysl-libre.webp', 'w',
     ('Лаванда, цветок апельсина, ваниль, мускус', 'Lavender, orange blossom, vanilla, musk', 'Лаванда, апельсин гүлі, ваниль, мускус'),
     ('Аромат свободы: французская лаванда и марокканский цветок апельсина на тёплой ванили и мускусе.',
      'The scent of freedom: French lavender and Moroccan orange blossom on warm vanilla and musk.',
      'Еркіндік хош иісі: француз лавандасы мен марокко апельсин гүлі жылы ваниль мен мускуста.')),
    ('Dior', 'Miss Dior', 'miss-dior', 'gifts/miss-dior.webp', 'w',
     ('Роза, пион, ландыш, мускус', 'Rose, peony, lily of the valley, musk', 'Раушан, пион, інжугүл, мускус'),
     ('Нежный цветочный букет из розы, пиона и ландыша — классика романтичной женственности.',
      'A tender floral bouquet of rose, peony and lily of the valley — the classic of romantic femininity.',
      'Раушан, пион және інжугүлден тұратын нәзік гүл шоғы — романтикалық әйелдіктің классикасы.')),
]

ARTICLES = [
    {
        'slug': 'kak-vybrat-aromat', 'emoji': '🌸',
        'title': 'Как выбрать свой аромат MONA',
        'excerpt': 'Нежный, Холодный или Сладкий? Рассказываем, какой аромат подойдёт под ваш характер и случай.',
        'body': 'Аромат — это продолжение вашего настроения. Поэтому в коллекции MONA три характера, и каждый звучит по-своему.\n\n'
                'Нежный — для тех, кто любит мягкость и романтику. Цитрусы, белые цветы и тёплая ваниль делают его идеальным на каждый день: в офис, на встречу с подругами или прогулку.\n\n'
                'Холодный — выбор для любительниц чистоты и свежести. Альдегиды, белый мускус и фиалка звучат как прохлада после дождя. Особенно хорош в жару и для активного дня.\n\n'
                'Сладкий — десертный и шлейфовый. Сливки, ваниль, белый шоколад и амбра создают аромат для вечера, свиданий и особых моментов.\n\n'
                'Не можете выбрать? Пройдите наш короткий тест на сайте — он подскажет аромат за минуту.',
        'title_en': 'How to choose your MONA scent',
        'excerpt_en': 'Tender, Cool or Sweet? Here is which scent suits your character and occasion.',
        'body_en': 'A scent is an extension of your mood. That is why the MONA collection has three characters, each with its own voice.\n\n'
                   'Tender is for those who love softness and romance. Citrus, white flowers and warm vanilla make it perfect for every day: the office, meeting friends or a walk.\n\n'
                   'Cool is the choice for lovers of purity and freshness. Aldehydes, white musk and violet feel like coolness after rain. Especially good in hot weather and on active days.\n\n'
                   'Sweet is dessert-like with a rich trail. Cream, vanilla, white chocolate and amber create a scent for evenings, dates and special moments.\n\n'
                   'Can\'t decide? Take our short quiz on the website — it will suggest a scent in a minute.',
        'title_kk': 'Өзіңізге MONA хош иісін қалай таңдауға болады',
        'excerpt_kk': 'Нәзік, Салқын әлде Тәтті ме? Қай хош иіс мінезіңіз бен жағдайға сай келетінін айтамыз.',
        'body_kk': 'Хош иіс — көңіл-күйіңіздің жалғасы. Сондықтан MONA коллекциясында үш мінез бар, әрқайсысы өзінше естіледі.\n\n'
                   'Нәзік — жұмсақтық пен романтиканы сүйетіндерге. Цитрустар, ақ гүлдер және жылы ваниль оны күнделікті қолдануға тамаша етеді: кеңсеге, достармен кездесуге немесе серуенге.\n\n'
                   'Салқын — тазалық пен балғындықты ұнататындардың таңдауы. Альдегидтер, ақ мускус және шегіргүл жаңбырдан кейінгі салқындықтай естіледі. Әсіресе ыстық күндері жақсы.\n\n'
                   'Тәтті — десерттік, ізі қалатын хош иіс. Кілегей, ваниль, ақ шоколад және амбра кешке, кездесулерге және ерекше сәттерге арналған.\n\n'
                   'Таңдай алмай жүрсіз бе? Сайттағы қысқа тестті өтіңіз — ол бір минутта хош иіс ұсынады.',
    },
    {
        'slug': 'kak-prodlit-stoykost', 'emoji': '⏳',
        'title': '7 секретов, чтобы аромат держался весь день',
        'excerpt': 'Простые привычки, которые продлят стойкость парфюма в два раза.',
        'body': 'Даже самый стойкий extrait de parfum можно сделать ещё долговечнее, если знать несколько простых правил.\n\n'
                '1. Наносите на увлажнённую кожу. Сухая кожа «впитывает» аромат быстрее, а крем без запаха помогает ему держаться дольше.\n\n'
                '2. Выбирайте точки пульса: запястья, шея, за ушами, сгибы локтей. Там кожа теплее, и аромат раскрывается ярче.\n\n'
                '3. Не растирайте запястья — трение разрушает верхние ноты.\n\n'
                '4. Немного на волосы или расчёску: волосы держат аромат часами и мягко отдают его при движении.\n\n'
                '5. Одежда тоже помогает — шарф или воротник сохранят шлейф до вечера.\n\n'
                '6. Храните флакон в тёмном прохладном месте, а не в ванной.\n\n'
                '7. Берите аромат с собой: флакон 30 мл удобно положить в сумочку.',
        'title_en': '7 secrets to make your scent last all day',
        'excerpt_en': 'Simple habits that can double the longevity of your perfume.',
        'body_en': 'Even the most long-lasting extrait de parfum can last longer if you know a few simple rules.\n\n'
                   '1. Apply to moisturised skin. Dry skin absorbs fragrance faster, and an unscented cream helps it stay longer.\n\n'
                   '2. Choose pulse points: wrists, neck, behind the ears, inner elbows. The skin is warmer there and the scent opens up brighter.\n\n'
                   '3. Do not rub your wrists — friction destroys the top notes.\n\n'
                   '4. A little on your hair or hairbrush: hair holds a scent for hours and releases it softly as you move.\n\n'
                   '5. Clothes help too — a scarf or collar will keep the trail until evening.\n\n'
                   '6. Store the bottle in a dark, cool place, not in the bathroom.\n\n'
                   '7. Take your scent with you: a 30 ml bottle fits easily in your handbag.',
        'title_kk': 'Хош иіс күні бойы сақталуы үшін 7 құпия',
        'excerpt_kk': 'Парфюмның тұрақтылығын екі есе ұзартатын қарапайым әдеттер.',
        'body_kk': 'Ең тұрақты extrait de parfum-ды да бірнеше қарапайым ережені білсеңіз, одан да ұзақ сақтауға болады.\n\n'
                   '1. Ылғалданған теріге себіңіз. Құрғақ тері хош иісті тез сіңіреді, ал иіссіз крем оның ұзақ сақталуына көмектеседі.\n\n'
                   '2. Пульс нүктелерін таңдаңыз: білек, мойын, құлақ арты, шынтақ бүгілісі. Онда тері жылырақ, хош иіс жарқынырақ ашылады.\n\n'
                   '3. Білекті ыспаламаңыз — ысу жоғарғы ноталарды бұзады.\n\n'
                   '4. Шашқа немесе тарақа аздап: шаш хош иісті сағаттар бойы сақтап, қимылдағанда жұмсақ таратады.\n\n'
                   '5. Киім де көмектеседі — орамал немесе жаға ізді кешке дейін сақтайды.\n\n'
                   '6. Флаконды жуынатын бөлмеде емес, қараңғы салқын жерде сақтаңыз.\n\n'
                   '7. Хош иісті өзіңізбен алып жүріңіз: 30 мл флакон сөмкеге оңай сыяды.',
    },
    {
        'slug': 'dyson-airwrap-v-podarok', 'emoji': '💇‍♀️',
        'title': 'Dyson Airwrap в подарок: как работает акция',
        'excerpt': 'Покупаете MONA 100 мл — получаете Dyson Airwrap с вашим именем на корпусе.',
        'body': 'До конца акции при покупке любого аромата MONA в объёме 100 мл вы получаете в подарок стайлер Dyson Airwrap.\n\n'
                'В комплекте 6 насадок — для объёма, красивых локонов и идеально гладких волос. Вы сами выбираете цвет: розовый, синий, карамельный или бордовый.\n\n'
                'Персонализация бесплатно: мы нанесём ваше имя на корпус Dyson, чтобы он стал по-настоящему вашим. Стайлер приходит в фирменной брендированной упаковке, с официальным чеком и гарантией 1 год.\n\n'
                'А если вы выбираете 30 или 50 мл — в подарок идут французские парфюмы 100 мл: один к 30 мл и два к 50 мл.',
        'title_en': 'Dyson Airwrap as a gift: how the offer works',
        'excerpt_en': 'Buy MONA 100 ml and get a Dyson Airwrap with your name on it.',
        'body_en': 'Until the end of the offer, when you buy any MONA scent in 100 ml you get a Dyson Airwrap styler as a gift.\n\n'
                   'It comes with 6 attachments — for volume, beautiful curls and perfectly smooth hair. You choose the colour: pink, blue, caramel or burgundy.\n\n'
                   'Personalisation is free: we put your name on the Dyson so it is truly yours. The styler comes in signature branded packaging, with an official receipt and a 1-year warranty.\n\n'
                   'And if you choose 30 or 50 ml, you get 100 ml French perfumes as a gift: one with 30 ml and two with 50 ml.',
        'title_kk': 'Сыйлыққа Dyson Airwrap: акция қалай жұмыс істейді',
        'excerpt_kk': 'MONA 100 мл сатып алыңыз — корпусында атыңыз жазылған Dyson Airwrap алыңыз.',
        'body_kk': 'Акция аяқталғанға дейін кез келген MONA хош иісін 100 мл көлемінде сатып алсаңыз, сыйлыққа Dyson Airwrap стайлерін аласыз.\n\n'
                   'Жинақта 6 саптама бар — көлем, әдемі бұйра және мінсіз тегіс шаш үшін. Түсін өзіңіз таңдайсыз: қызғылт, көк, карамель немесе шие қызыл.\n\n'
                   'Жекелендіру тегін: Dyson корпусына атыңызды жазамыз. Стайлер фирмалық қаптамада, ресми чекпен және 1 жылдық кепілдікпен келеді.\n\n'
                   'Ал 30 немесе 50 мл таңдасаңыз — сыйлыққа 100 мл француз парфюмдері беріледі: 30 мл-ге біреу, 50 мл-ге екеу.',
    },
]

GALLERY = [
    ('gallery/dyson-gift.webp', 'MONA и Dyson Airwrap в подарок', 'MONA and a Dyson Airwrap gift', 'MONA және сыйлыққа Dyson Airwrap'),
    ('gallery/gift-box.webp', 'Именная подарочная коробка', 'Personalised gift box', 'Атаулы сыйлық қорабы'),
    ('products/nezhnyi.webp', 'MONA Нежный', 'MONA Tender', 'MONA Нәзік'),
    ('products/holodnyi.webp', 'MONA Холодный', 'MONA Cool', 'MONA Салқын'),
    ('products/sladkii.webp', 'MONA Сладкий', 'MONA Sweet', 'MONA Тәтті'),
]


def seed(apps, schema_editor):
    Variant = apps.get_model('shop', 'Variant')
    GiftPerfume = apps.get_model('shop', 'GiftPerfume')
    Article = apps.get_model('shop', 'Article')
    GalleryPhoto = apps.get_model('shop', 'GalleryPhoto')

    for label, (price, old, gtype, count, g_ru, g_en, g_kk) in VOLUMES.items():
        Variant.objects.filter(label=label).update(price=price, old_price=old, gift_type=gtype, gift_count=count,
                                                   gift=g_ru, gift_en=g_en, gift_kk=g_kk)

    for pos, (brand, name, slug, image, gender, notes, desc) in enumerate(GIFTS):
        GiftPerfume.objects.update_or_create(slug=slug, defaults=dict(
            brand=brand, name=name, image=image, gender=gender, position=pos,
            notes=notes[0], notes_en=notes[1], notes_kk=notes[2],
            description=desc[0], description_en=desc[1], description_kk=desc[2]))

    for data in ARTICLES:
        data = dict(data)
        Article.objects.update_or_create(slug=data.pop('slug'), defaults=data)

    if not GalleryPhoto.objects.exists():
        for pos, (image, ru, en, kk) in enumerate(GALLERY):
            GalleryPhoto.objects.create(image=image, caption=ru, caption_en=en, caption_kk=kk, position=pos)


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0015_cart_gifts_blog'),
    ]

    operations = [
        migrations.RunPython(seed, migrations.RunPython.noop),
    ]
