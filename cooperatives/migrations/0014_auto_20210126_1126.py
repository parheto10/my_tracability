# Generated by Django 3.1.2 on 2021-01-26 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cooperatives', '0013_remove_retrait_plant_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='retrait_plant',
            name='cooperative',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='cooperatives.cooperative', verbose_name='COOPERATIVE'),
        ),
        migrations.AlterField(
            model_name='retrait_plant',
            name='destination',
            field=models.CharField(max_length=255, verbose_name='LOCALITE (S/P - Ville - VILLAGE)'),
        ),
    ]
