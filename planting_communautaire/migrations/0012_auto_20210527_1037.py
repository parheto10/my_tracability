# Generated by Django 3.1.7 on 2021-05-27 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planting_communautaire', '0011_auto_20210527_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parcelle',
            name='associee',
            field=models.CharField(choices=[('banane', 'BANANE'), ('mais', 'MAIS')], max_length=50, verbose_name='CULTURE ASSOCIEE'),
        ),
    ]
