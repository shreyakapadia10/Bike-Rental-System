# Generated by Django 3.2.3 on 2021-06-10 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BikeUsers', '0010_auto_20210610_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='star',
            field=models.IntegerField(help_text='Add ratings'),
        ),
    ]
