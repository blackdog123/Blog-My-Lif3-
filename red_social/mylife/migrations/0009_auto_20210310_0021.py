# Generated by Django 3.1.1 on 2021-03-10 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mylife', '0008_auto_20210310_0017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
    ]
