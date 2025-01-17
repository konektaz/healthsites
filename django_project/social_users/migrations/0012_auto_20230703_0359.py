# Generated by Django 3.2.18 on 2023-07-03 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_users', '0011_profile_osm_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='contact',
            field=models.CharField(blank=True, default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='organisationsupported',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='Is Staff'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='osm_name',
            field=models.CharField(blank=True, default='', max_length=512),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.CharField(blank=True, default='', max_length=512),
        ),
    ]
