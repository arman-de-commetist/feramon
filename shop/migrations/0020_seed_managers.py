from django.db import migrations

MANAGERS = [
    ('Аяжан', '8 707 711 3214', 'rose'),
    ('Ұлдана', '8 706 620 0594', 'wine'),
    ('Мейірбек', '8 771 494 6108', 'caramel'),
    ('Ұлжан', '8 708 930 4029', 'gold'),
]


def seed(apps, schema_editor):
    Manager = apps.get_model('shop', 'Manager')
    if Manager.objects.exists():
        return
    for pos, (name, phone, tone) in enumerate(MANAGERS):
        Manager.objects.create(name=name, phone=phone, tone=tone, position=pos)


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0019_managers'),
    ]

    operations = [
        migrations.RunPython(seed, migrations.RunPython.noop),
    ]
