# Generated by Django 3.1.7 on 2021-05-25 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('planting_communautaire', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organisation',
            name='localisation',
        ),
    ]
