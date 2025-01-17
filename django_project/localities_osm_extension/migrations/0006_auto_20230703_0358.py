# Generated by Django 3.2.18 on 2023-07-03 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('localities_osm_extension', '0005_auto_20190712_0831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='localityosmextension',
            name='osm_type',
            field=models.CharField(blank=True, choices=[('node', 'node'), ('way', 'way'), ('relation', 'relation')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='pendingreview',
            name='payload',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='pendingreview',
            name='reason',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
