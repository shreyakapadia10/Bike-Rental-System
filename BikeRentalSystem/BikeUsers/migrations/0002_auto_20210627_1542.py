# Generated by Django 3.1.7 on 2021-06-27 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BikeUsers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='first_name',
            field=models.CharField(help_text='Enter your first name', max_length=50),
        ),
        migrations.AlterField(
            model_name='customer',
            name='last_name',
            field=models.CharField(help_text='Enter your last name', max_length=50),
        ),
    ]
