from django.db import migrations

GIFT = 'Стайлер Dyson в подарок'


def add_100ml(apps, schema_editor):
    Product = apps.get_model('shop', 'Product')
    Variant = apps.get_model('shop', 'Variant')
    for product in Product.objects.all():
        if product.variants.filter(label__startswith='100').exists():
            continue
        # placeholder price — same as the existing 100 ml, change it in the admin
        Variant.objects.create(product=product, label='100 мл', sublabel='extrait de parfum',
                               price=54990, gift=GIFT, position=10)
    Variant.objects.filter(label__startswith='100').update(gift=GIFT)


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_gift_color'),
    ]

    operations = [
        migrations.RunPython(add_100ml, migrations.RunPython.noop),
    ]
