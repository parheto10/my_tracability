# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import time
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe

from chocolotiers.models import Client
# from cooperatives.models import Cooperative, Section, ACQUISITION, CERTIFICATION
from parametres.models import Projet, Espece, Region, Campagne


def upload_logo_site(self, filename):
    # verification de l'extension
    real_name, extension = os.path.splitext(filename)
    name = str(int(time.time())) + extension
    return "logos/" + self.code + ".jpeg"

CULTURE = (
    ('anacarde', 'ANACARDE'),
    ('cacao', 'CACAO'),
    ('cafe', 'CAFE'),
    ('coton', 'COTON'),
    ('hevea', 'HEVEA'),
    ('palmier', 'PALMIER A HUILE'),
    ('SOJA', 'SOJA'),
    ('autre', 'AUTRES'),
)

CULTURE_ASSOCIEE = (
    ("banane", "BANANE"),
    ("mais", "MAIS"),
    # ("coton", "COTON"),
    # ("coton", "COTON"),
)

class Organisation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    siege = models.CharField(max_length=255, verbose_name="SIEGE/LOCALITE", blank=True, null=True)
    sigle = models.CharField(max_length=500, verbose_name="SIGLE COMMUNAUTE")
    libelle = models.CharField(max_length=255, verbose_name="NOM COMMUNAUTE")
    # localisation = models.CharField(max_length=255, verbose_name="LOCALISATION")
    responsable = models.CharField(max_length=255, verbose_name="NOM ET PRENOMS RESPONSABLE")
    contacts = models.CharField(max_length=50, blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    projet_com = models.ManyToManyField(Projet, related_name="projet_commaunautaire")
    # culture_associee = models.CharField(max_length=50, verbose_name="CULTURE ASSOCIEE", choices=CULTURE_ASSOCIEE)
    logo = models.ImageField(verbose_name="Logo", upload_to=upload_logo_site, blank=True)
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('communaute:dashboard', kwargs={"id": self.id})

    def get_projet_values(self):
        ret = ''
        # print(self.projet.all())
        for proj in self.projet_com.all():
            ret = ret + proj.accronyme + ','
        return ret[:-1]

    def __str__(self):
        return '%s %s' %(self.libelle, self.get_projet_values())
        # return '%s - %s (%s)' %(self.sigle, self.activite, self.get_projet_values())

    def save(self, force_insert=False, force_update=False):
        self.libelle = self.libelle.upper()
        self.responsable = self.responsable.upper()
        # self.user.last_name = self.user.last_name.upper()
        # self.user.first_name = self.user.first_name.upper()
        super(Organisation, self).save(force_insert, force_update)

    class Meta:
        verbose_name_plural = "COMMUNAUTES"
        verbose_name = "Communaute"
        ordering = ["libelle"]

    def Logo(self):
        if self.logo:
            return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.logo.url)
        else:
            return "Aucun Logo"

    Logo.short_description = 'Logo'

class Parcelle(models.Model):
    code = models.CharField(max_length=150, blank=True, null=True, verbose_name='CODE PARCELLE')
    communaute = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    # projet = models.ForeignKey(Projet, on_delete=models.CASCADE)
    latitude = models.CharField(max_length=10)
    longitude = models.CharField(max_length=10)
    superficie = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True)
    culture = models.CharField(max_length=50, verbose_name="CULTURE", choices=CULTURE)
    associee = models.CharField(max_length=50, verbose_name="CULTURE ASSOCIEE", choices=CULTURE_ASSOCIEE)
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    # def get_projet_values(self):
    #     ret = ''
    #     # print(self.projet.all())
    #     for proj in self.projet.all():
    #         ret = ret + proj.accronyme + ','
    #     return ret[:-1]

    def __str__(self):
        return '%s - (%s)' % (self.communaute, self.culture)

    def coordonnees(self):
        return str(self.longitude) + ', ' + str(self.latitude)

    class Meta:
        verbose_name_plural = "PARCELLES COMMUNAUTAIRES"
        verbose_name = "parcelle communautaire"
        # ordering = ["code"]

class Planting_Com(models.Model):
    campagne = models.ForeignKey(Campagne, on_delete=models.CASCADE)
    parcelle = models.ForeignKey(Parcelle, on_delete=models.CASCADE)
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE)
    nb_plant_exitant = models.PositiveIntegerField(default=0, verbose_name="NBRE PLANTS EXISTANTS")
    nb_plant = models.PositiveIntegerField(default=0)
    plant_total = models.PositiveIntegerField(default=0, verbose_name="NOMBRE TOTAL DE PLANTS")
    date = models.DateField()
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()
    # details = models.TextField(blank=True, null=True)

    def __str__(self):
        return '%s - (%s) plants reçus' % (self.parcelle.communaute, self.nb_plant)

    def save(self, force_insert=False, force_update=False):
        self.plant_total = (self.nb_plant_exitant) + (self.nb_plant)
        super(Planting_Com, self).save(force_insert, force_update)

    class Meta:
        verbose_name_plural = "PLANTINGS COMMUNAUTAIRES"
        verbose_name = "planting communautaire"
        # ordering = ["code"]

class DetailPlanting(models.Model):
    planting = models.ForeignKey(Planting_Com, on_delete=models.CASCADE)
    espece = models.ForeignKey(Espece, on_delete=models.CASCADE, related_name="espece_planting")
    nb_plante = models.PositiveIntegerField(default=0, verbose_name="NBRE PLANTS PLANTE/ESPECE")
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    # def save(self, force_insert=False, force_update=False):
    #     # cooperative = Cooperative.objects.get(user_id=request.user.id)
    #     # planting = Planting.objects.filter(parcelle__producteur__cooperative_id=cooperative)
    #     total_espece = DetailPlanting.objects.filter(planting_id=planting).aggregate(total=Sum('nb_plante'))['total']
    #     if self.planting.plant_total != total_espece:
    #         raise ValidationError('Erreur sur le Total de Plants Récus, Vérifié SVP...')
    #     super(DetailPlanting, self).save(force_insert, force_update)

    class Meta:
        verbose_name_plural = "DETAILS PLANTINGS"
        verbose_name = "detail planting"

class Monitoring(models.Model):
    planting = models.ForeignKey(Planting_Com, on_delete=models.CASCADE)
    espece = models.ForeignKey(Espece, on_delete=models.CASCADE, related_name="espece_monitoring")
    mort = models.PositiveIntegerField(default=0, verbose_name="NBRE PLANTS MORTS")
    remplace = models.PositiveIntegerField(default=0, verbose_name="NBRE PLANTS REMPLACES")
    mature = models.PositiveIntegerField(default=0, verbose_name="NBRE PLANTS VIVANTS")
    observation = models.TextField(blank=True, null=True)
    date = models.DateField()
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    # def save(self, force_insert=False, force_update=False):
    #     # cooperative = Cooperative.objects.get(user_id=request.user.id)
    #     # planting = Planting.objects.filter(parcelle__producteur__cooperative_id=cooperative)
    #     total_espece = DetailPlanting.objects.filter(planting_id=planting).aggregate(total=Sum('nb_plante'))['total']
    #     if self.planting.plant_total != total_espece:
    #         raise ValidationError('Erreur sur le Total de Plants Récus, Vérifié SVP...')
    #     super(DetailPlanting, self).save(force_insert, force_update)

    class Meta:
        verbose_name_plural = "MONITORINGS PLANTINGS"
        verbose_name = "details planting"

class Formation(models.Model):
    communaute = models.ForeignKey(Organisation, on_delete=models.CASCADE)
    projet_formation = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name="projet_formation")
    campagne_formation = models.ForeignKey(Campagne, on_delete=models.CASCADE, related_name="campagne_formation")
    formateur = models.CharField(max_length=255, verbose_name="FORMATEUR")
    libelle = models.CharField(max_length=500, verbose_name='INTITULE DE LA FORMATION')
    debut = models.DateField(verbose_name="DATE DEBUT")
    fin = models.DateField(verbose_name="DATE FIN")
    observation = models.TextField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return "%s" %(self.libelle)

    def Duree(self):
        delta = (self.fin - self.debut).days
        return delta - (delta // 7) * 2 #calcul nombrede jours travailler(sans week-end)
        # return (self.fin - self.debut).days
        # return delta

    class Meta:
        verbose_name_plural = "FORMATIONS & SENSIBILISATIONS"
        verbose_name = "formation & sensibilisation"
        ordering = ["libelle"]

class Detail_Formation(models.Model):
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE)
    nom_prenoms = models.CharField(max_length=500)
    contacts = models.CharField(max_length=50, blank=True, null=True)
    localite = models.CharField(max_length=50, blank=True, null=True)
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    # def Participants(self):
    #     nb_participants = self.participant.all().count()
    #     return nb_participants

    def __str__(self):
        return "%s" % (self.formation.libelle)

    class Meta:
        verbose_name_plural = "DETAILS FORMATIONS"
        verbose_name = "details formation"