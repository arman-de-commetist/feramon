from django.db import migrations


def to_women(apps, schema_editor):
    GiftPerfume = apps.get_model('shop', 'GiftPerfume')
    GiftPerfume.objects.filter(gender='u').update(gender='w')


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0024_tiktok'),
    ]

    operations = [
        migrations.RunPython(to_women, migrations.RunPython.noop),
    ]
