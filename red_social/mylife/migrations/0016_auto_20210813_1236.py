# Generated by Django 3.1.1 on 2021-08-13 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mylife', '0015_auto_20210320_1802'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='link_facebook',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='link_instagram',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='link_linkedin',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='link_twitter',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='tipo_permiso',
            field=models.CharField(choices=[('Administrador', 'Administrador'), ('Usuario', 'Usuario')], default='Usuario', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='tipo_verificacion',
            field=models.CharField(choices=[('Verificado', 'Verificado'), ('No Verificado', 'No Verificado')], default='No Verificado', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='imagen',
            field=models.ImageField(null=True, upload_to='imagenes'),
        ),
        migrations.AlterField(
            model_name='post',
            name='texto',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='video',
            field=models.FileField(upload_to='videos'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, max_length=255),
        ),
    ]
