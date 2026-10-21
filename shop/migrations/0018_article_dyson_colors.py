from django.db import migrations

REPLACE = [
    ('body', 'розовый, синий, карамельный или бордовый',
     'светлый бежево-розовый с медным, тёмно-синий с медным, бархатно-красный с золотом или розовый с розовым золотом'),
    ('body_en', 'pink, blue, caramel or burgundy',
     'light blush pink with copper, Prussian blue with copper, red velvet with gold or ceramic pink with rose gold'),
    ('body_kk', 'қызғылт, көк, карамель немесе шие қызыл',
     'мыс түсті ашық бежевый-қызғылт, мыс түсті қою көк, алтын түсті барқыт қызыл немесе раушан алтынды қызғылт'),
]


def update(apps, schema_editor):
    Article = apps.get_model('shop', 'Article')
    for a in Article.objects.filter(slug='dyson-airwrap-v-podarok'):
        for field, old, new in REPLACE:
            setattr(a, field, getattr(a, field).replace(old, new))
        a.save()


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0017_dyson_colors'),
    ]

    operations = [
        migrations.RunPython(update, migrations.RunPython.noop),
    ]
