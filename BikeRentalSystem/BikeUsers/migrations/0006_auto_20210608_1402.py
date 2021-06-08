# Generated by Django 3.1.7 on 2021-06-08 08:32

from django.db import migrations
import django_google_maps.fields


class Migration(migrations.Migration):

    dependencies = [
        ('BikeUsers', '0005_station'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='station',
            name='location',
        ),
        migrations.RemoveField(
            model_name='station',
            name='name',
        ),
        migrations.AddField(
            model_name='station',
            name='address',
            field=django_google_maps.fields.AddressField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='station',
            name='geolocation',
            field=django_google_maps.fields.GeoLocationField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
