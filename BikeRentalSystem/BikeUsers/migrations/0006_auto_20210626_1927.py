# Generated by Django 3.1.7 on 2021-06-26 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BikeUsers', '0005_auto_20210622_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='station',
            name='address',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Address'),
        ),
    ]
