# Generated by Django 3.1.2 on 2021-01-13 10:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cooperatives', '0005_auto_20210113_0958'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='producteur',
            options={'ordering': ['id'], 'verbose_name': 'producteur', 'verbose_name_plural': 'PRODUCTEURS'},
        ),
    ]
