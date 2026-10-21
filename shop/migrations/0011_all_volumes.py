from django.db import migrations

GIFT = 'Стайлер Dyson в подарок'
# placeholder prices — change them in the admin
VOLUMES = [('30 мл', 29990, ''), ('50 мл', 39990, ''), ('100 мл', 54990, GIFT)]


def all_volumes(apps, schema_editor):
    Product = apps.get_model('shop', 'Product')
    Variant = apps.get_model('shop', 'Variant')
    for product in Product.objects.all():
        for position, (label, price, gift) in enumerate(VOLUMES):
            existing = product.variants.filter(label=label).first()
            if existing:
                existing.position = position
                existing.gift = gift
                existing.save()
            else:
                Variant.objects.create(product=product, label=label, sublabel='extrait de parfum',
                                       price=price, gift=gift, position=position)


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_100ml_for_all'),
    ]

    operations = [
        migrations.RunPython(all_volumes, migrations.RunPython.noop),
    ]
