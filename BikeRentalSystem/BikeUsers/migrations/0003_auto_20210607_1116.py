# Generated by Django 3.1.7 on 2021-06-07 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BikeUsers', '0002_auto_20210607_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='status',
            field=models.CharField(choices=[('P', 'Pending'), ('V', 'Verified')], default='P', max_length=1),
        ),
    ]
