# Generated by Django 3.1.1 on 2021-03-10 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mylife', '0007_profile_foto_portada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, default='', max_length=255, null=True),
        ),
    ]
