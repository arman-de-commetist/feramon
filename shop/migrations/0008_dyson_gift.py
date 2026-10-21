from django.db import migrations


def set_gift(apps, schema_editor):
    Variant = apps.get_model('shop', 'Variant')
    Variant.objects.filter(label__startswith='100').update(gift='Стайлер Dyson в подарок')


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_gift'),
    ]

    operations = [
        migrations.RunPython(set_gift, migrations.RunPython.noop),
    ]
