from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_seed_data'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['position', 'id'], 'verbose_name': 'Парфюм', 'verbose_name_plural': 'Парфюмы'},
        ),
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='nezhnyi', unique=True, verbose_name='Адрес (латиницей)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.FileField(blank=True, upload_to='products/', verbose_name='Фото / постер'),
        ),
        migrations.AddField(
            model_name='product',
            name='theme',
            field=models.CharField(choices=[('rose', 'Розовый'), ('ice', 'Холодный голубой'), ('caramel', 'Карамельный')], default='rose', max_length=10, verbose_name='Цветовая тема'),
        ),
        migrations.AddField(
            model_name='product',
            name='position',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Порядок'),
        ),
    ]
