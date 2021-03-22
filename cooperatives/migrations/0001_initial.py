# Generated by Django 3.1.2 on 2021-01-08 11:23

import cooperatives.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chocolotiers', '0001_initial'),
        ('parametres', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cooperative',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sigle', models.CharField(max_length=500)),
                ('contacts', models.CharField(max_length=50)),
                ('logo', models.ImageField(blank=True, upload_to=cooperatives.models.upload_logo_site, verbose_name='Logo')),
                ('add_le', models.DateTimeField(auto_now_add=True)),
                ('update_le', models.DateTimeField(auto_now=True)),
                ('activite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parametres.activite')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chocolotiers.client')),
                ('projet', models.ManyToManyField(to='parametres.Projet')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parametres.region')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'cooperative',
                'verbose_name_plural': 'COOPERATIVES',
                'ordering': ['sigle'],
            },
        ),
        migrations.CreateModel(
            name='Parcelle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, help_text='LE CODE PARCELLE EST GENERE AUTOMATIQUEMENT', max_length=150, null=True, verbose_name='CODE PARCELLE')),
                ('acquisition', models.CharField(choices=[('heritage', 'HERITAGE'), ('achat', 'ACHAT'), ('autres', 'AUTRES')], max_length=50, verbose_name='MODE ACQUISITION')),
                ('latitude', models.CharField(max_length=10)),
                ('longitude', models.CharField(max_length=10)),
                ('superficie', models.DecimalField(blank=True, decimal_places=12, max_digits=15, null=True)),
                ('culture', models.CharField(choices=[('anacarde', 'ANACARDE'), ('cacao', 'CACAO'), ('cafe', 'CAFE'), ('coton', 'COTON'), ('hevea', 'HEVEA'), ('palmier', 'PALMIER A HUILE'), ('SOJA', 'SOJA'), ('autre', 'AUTRES')], max_length=50, verbose_name='CULTURE')),
                ('certification', models.CharField(choices=[('utz', 'UTZ'), ('ra', 'RA'), ('bio', 'BIO'), ('projet', 'PROJET'), ('autre', 'PROJET')], max_length=50, verbose_name='CERTIFICATION')),
                ('add_le', models.DateTimeField(auto_now_add=True)),
                ('update_le', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'parcelle',
                'verbose_name_plural': 'PARCELLE',
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=250)),
                ('responsable', models.CharField(max_length=250)),
                ('contacts', models.CharField(max_length=50)),
                ('add_le', models.DateTimeField(auto_now_add=True)),
                ('update_le', models.DateTimeField(auto_now=True)),
                ('cooperative', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooperatives.cooperative')),
            ],
            options={
                'verbose_name': 'section',
                'verbose_name_plural': 'SECTIONS',
                'ordering': ['libelle'],
            },
        ),
        migrations.CreateModel(
            name='Sous_Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=250)),
                ('responsable', models.CharField(max_length=250)),
                ('contacts', models.CharField(max_length=50)),
                ('add_le', models.DateTimeField(auto_now_add=True)),
                ('update_le', models.DateTimeField(auto_now=True)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooperatives.section')),
            ],
            options={
                'verbose_name': 'sous section',
                'verbose_name_plural': 'SOUS SECTIONS',
                'ordering': ['libelle'],
            },
        ),
        migrations.CreateModel(
            name='Producteur',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(blank=True, max_length=150, verbose_name='CODE PRODUCTEUR')),
                ('type_producteur', models.CharField(choices=[('membre', 'MEMBRE'), ('usager', 'USAGER')], max_length=50, verbose_name='TYPE PRODUCTEUR')),
                ('genre', models.CharField(choices=[('H', 'HOMME'), ('F', 'FEMME')], max_length=2)),
                ('nom', models.CharField(max_length=250)),
                ('prenoms', models.CharField(max_length=500)),
                ('dob', models.DateField(blank=True, null=True)),
                ('contacts', models.CharField(blank=True, max_length=50, null=True)),
                ('localite', models.CharField(blank=True, max_length=100, null=True, verbose_name='LOCALITE')),
                ('nb_enfant', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('nb_parcelle', models.PositiveIntegerField(default=0)),
                ('image', models.ImageField(blank=True, upload_to=cooperatives.models.producteurs_images, verbose_name='Logo')),
                ('type_document', models.CharField(choices=[('AUCUN', 'AUCUN'), ('ATTESTATION', 'ATTESTATION'), ('CNI', 'CNI'), ('PASSEPORT', 'PASSEPORT'), ('SEJOUR', 'CARTE DE SEJOUR'), ('CONSULAIRE', 'CARTE CONSULAIRE')], default='AUCUN', max_length=50, verbose_name='TYPE DOCUMENT')),
                ('num_document', models.CharField(blank=True, max_length=150, null=True, verbose_name='N° PIECE')),
                ('document', models.FileField(blank=True, null=True, upload_to=cooperatives.models.producteurs_documents, verbose_name='Documents')),
                ('add_le', models.DateTimeField(auto_now_add=True)),
                ('update_le', models.DateTimeField(auto_now=True)),
                ('cooperative', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooperatives.cooperative')),
                ('origine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parametres.origine')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooperatives.section')),
                ('sous_prefecture', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parametres.sous_prefecture')),
                ('sous_section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sous_section', to='cooperatives.sous_section')),
            ],
            options={
                'verbose_name': 'producteur',
                'verbose_name_plural': 'PRODUCTEURS',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Planting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nb_plant', models.PositiveIntegerField(default=0)),
                ('date', models.DateField()),
                ('details', models.TextField(blank=True, null=True)),
                ('parcelle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooperatives.parcelle')),
                ('projet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parametres.projet')),
            ],
            options={
                'verbose_name': 'planting',
                'verbose_name_plural': 'PLANTINGS',
            },
        ),
        migrations.AddField(
            model_name='parcelle',
            name='producteur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooperatives.producteur'),
        ),
        migrations.AddField(
            model_name='parcelle',
            name='sous_section',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sous_section_parcelle', to='cooperatives.sous_section'),
        ),
        migrations.CreateModel(
            name='Formation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('formateur', models.CharField(max_length=255, verbose_name='FORMATEUR')),
                ('libelle', models.CharField(max_length=500, verbose_name='INTITULE DE LA FORMATION')),
                ('debut', models.DateField(verbose_name='DATE DEBUT')),
                ('fin', models.DateField(verbose_name='DATE FIN')),
                ('details', models.TextField(blank=True, null=True)),
                ('observation', models.TextField(blank=True, null=True)),
                ('add_le', models.DateTimeField(auto_now_add=True)),
                ('update_le', models.DateTimeField(auto_now=True)),
                ('copperative', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooperatives.cooperative')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooperatives.producteur')),
            ],
            options={
                'verbose_name': 'formation',
                'verbose_name_plural': 'FORMATIONS',
                'ordering': ['libelle'],
            },
        ),
        migrations.CreateModel(
            name='Details_planting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plante', models.PositiveIntegerField(default=0, verbose_name='NBRE PLANTS PLANTE')),
                ('remplace', models.PositiveIntegerField(default=0, verbose_name='NBRE PLANTS REMPLACES')),
                ('mort', models.PositiveIntegerField(default=0, verbose_name='NBRE PLANTS MORTS')),
                ('mature', models.PositiveIntegerField(default=0, verbose_name='NBRE PLANTS MATURE')),
                ('observation', models.TextField(blank=True, null=True)),
                ('espece', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parametres.espece')),
                ('planting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooperatives.planting')),
            ],
        ),
    ]
