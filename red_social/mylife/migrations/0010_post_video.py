# Generated by Django 3.1.1 on 2021-03-14 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mylife', '0009_auto_20210310_0021'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='videos'),
        ),
    ]