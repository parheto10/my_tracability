# Generated by Django 3.1.2 on 2021-01-22 11:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cooperatives', '0010_auto_20210122_1050'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formation',
            name='observation',
        ),
        migrations.RemoveField(
            model_name='formation',
            name='participant',
        ),
        migrations.CreateModel(
            name='Detail_Formation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observation', models.TextField(blank=True, null=True)),
                ('add_le', models.DateTimeField(auto_now_add=True)),
                ('update_le', models.DateTimeField(auto_now=True)),
                ('formation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooperatives.formation')),
                ('participant', models.ManyToManyField(to='cooperatives.Producteur')),
            ],
            options={
                'verbose_name': 'details formation',
                'verbose_name_plural': 'DETAILS FORMATIONS',
            },
        ),
    ]
