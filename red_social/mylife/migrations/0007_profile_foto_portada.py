# Generated by Django 3.1.1 on 2021-03-09 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mylife', '0006_auto_20210308_1228'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='foto_portada',
            field=models.ImageField(default='banner_default.jpg', upload_to='fotos_portada'),
        ),
    ]