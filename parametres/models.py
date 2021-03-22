# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import time
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
import datetime

from django.utils.safestring import mark_safe
from django_countries.fields import CountryField

# from cooperatives.models import Cooperative
from chocolotiers.models import Client

ANNEES = []
for r in range(2019, (datetime.datetime.now().year+1)):
    ANNEES.append((r,r))

def upload_logo_site(self, filename):
    # verification de l'extension
    real_name, extension = os.path.splitext(filename)
    name = str(int(time.time())) + extension
    return "logos/" + self.code + ".jpeg"

ETAT = (
    ('en_cours', 'EN COURS'),
    ('suspendu', 'SUSPENDU'),
    ('traite', 'TRAITE'),
)

CULTURE = (
    ('ANACARDE', 'ANACARDE'),
    ('CACAO', 'CACAO'),
    ('CAFE', 'CAFE'),
    ('COTON', 'COTON'),
    ('HEVEA', 'HEVEA'),
    ('PALMIER', 'PALMIER A HUILE'),
)

CERTIFICATION = (
    ('UTZ', 'UTZ'),
    ('RA', 'RA'),
    ('BIO', 'BIO'),
    ('PROJET', 'PROJET'),
)

# class Client(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     sigle = models.CharField(max_length=500, verbose_name="NOM / SIGLE")
#     contacts = models.CharField(max_length=50, verbose_name="CONTACTS")
#     code = models.CharField(max_length=5, verbose_name="CODE", unique=True)
#     libelle = models.CharField(max_length=250, verbose_name="NOM")
#     pays = CountryField(blank_label='(Préciser Le Pays)')
#     adresse = models.CharField(max_length=250, verbose_name="ADRESSE", blank=True)
#     telephone1 = models.CharField(max_length=50)  # CharField(max_length=50, verbose_name="TELEPHONE 1")
#     telephone2 = models.CharField(max_length=50, blank=True, null=True)  # CharField(max_length=50, verbose_name="TELEPHONE 1")
#     # telephone2 = PhoneNumberField(help_text="+22545485648", blank=True)
#     email = models.EmailField(max_length=120, blank=True, verbose_name="ADRESSE EMAIL")
#     siteweb = models.CharField(max_length=120, blank=True, verbose_name="SITE WEB")
#     logo = models.ImageField(verbose_name="Logo", upload_to=upload_logo_site, blank=True)
#     add_le = models.DateTimeField(auto_now_add=True)
#     update_le = models.DateTimeField(auto_now=True)
#     objects = models.Manager()
#
#     def __str__(self):
#         return '%s' % (self.libelle)
#
#     def save(self, force_insert=False, force_update=False):
#         self.code = self.code.upper()
#         self.libelle = self.libelle.upper()
#         # self.pays = self.pays.upper()
#         super(Client, self).save(force_insert, force_update)
#
#     class Meta:
#         verbose_name_plural = "CLIENTS"
#         verbose_name = "client"
#
#     def Logo(self):
#         if self.logo:
#             return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.logo.url)
#         else:
#             return "Aucun Logo"
#
#     Logo.short_description = 'Logo'

class Origine(models.Model):
    code = models.CharField(max_length=2, verbose_name="CODE PAYS")
    pays = models.CharField(max_length=255, verbose_name="PAYS")
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return "%s" %(self.pays)

    class Meta:
        verbose_name_plural = "ORIGINES"
        verbose_name = "origine"
        ordering = ["pays"]

    def save(self, force_insert=False, force_update=False):
        self.code = self.code.upper()
        self.pays = self.pays.upper()
        super(Origine, self).save(force_insert, force_update)

class Region(models.Model):
    libelle = models.CharField(max_length=250)
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return "%s" %(self.libelle)

    class Meta:
        verbose_name_plural = "REGIONS"
        verbose_name = "region"
        ordering = ["libelle"]

    def save(self, force_insert=False, force_update=False):
        self.libelle = self.libelle.upper()
        super(Region, self).save(force_insert, force_update)

class Sous_Prefecture(models.Model):
    libelle = models.CharField(max_length=250)
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return "%s" %(self.libelle)

    class Meta:
        verbose_name_plural = "SOUS PREFECTURES"
        verbose_name = "sous prefecture"
        ordering = ["libelle"]

    def save(self, force_insert=False, force_update=False):
        self.libelle = self.libelle.upper()
        super(Sous_Prefecture, self).save(force_insert, force_update)

class Projet_Cat(models.Model):
    libelle = models.CharField(max_length=500, verbose_name="CATEGORIE PROJET")
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return "%s" % (self.libelle)

    def save(self, force_insert=False, force_update=False):
        self.libelle = self.libelle.upper()
        super(Projet_Cat, self).save(force_insert, force_update)

    class Meta:
        verbose_name_plural = "CATEGORIES PROJETS"
        verbose_name = "catégorie projet"
        ordering = ["libelle"]

class Projet(models.Model):
    client = models.ForeignKey(Client, verbose_name="CLIENT", on_delete=models.CASCADE, default=1)
    categorie = models.ForeignKey(Projet_Cat, on_delete=models.CASCADE, verbose_name="CATEGORIE PROJET", default=1)
    accronyme = models.CharField(max_length=255)
    titre = models.CharField(max_length=500)
    chef = models.CharField(max_length=255)
    debut = models.DateField()
    fin = models.DateField()
    etat = models.CharField(max_length=50, choices=ETAT)
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return "%s - (%s) de %s" %(self.titre, self.categorie.libelle, self.client)

    class Meta:
        verbose_name_plural = "PROJETS"
        verbose_name = "projet"
        ordering = ["accronyme"]

    def save(self, force_insert=False, force_update=False):
        self.accronyme = self.accronyme.upper()
        self.titre = self.titre.upper()
        self.chef = self.chef.upper()
        super(Projet, self).save(force_insert, force_update)

class Campagne(models.Model):
    accronyme = models.CharField(max_length=255)
    titre = models.CharField(max_length=500)
    annee = models.IntegerField(verbose_name='Année', choices=ANNEES, default=datetime.datetime.now().year)
    debut = models.DateField()
    fin = models.DateField()
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return "%s %s" %(self.titre, self.annee)

    class Meta:
        verbose_name_plural = "CAMPAGNES"
        verbose_name = "campagne"
        ordering = ["accronyme"]

    def save(self, force_insert=False, force_update=False):
        self.accronyme = self.accronyme.upper()
        self.titre = self.titre.upper()
        self.chef = self.chef.upper()
        super(Campagne, self).save(force_insert, force_update)

class Prime(models.Model):
    campagne = models.ForeignKey(Campagne, on_delete=models.CASCADE)
    culture = models.CharField(max_length=150, choices=CULTURE)
    certification = models.CharField(max_length=150, choices=CERTIFICATION)
    prix = models.PositiveIntegerField(default=100, verbose_name="Prix/Kg")
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return "%s-%s %s" %(self.culture, self.certification, self.prix)

    class Meta:
        verbose_name_plural = "PRIMES"
        verbose_name = "prime"
        # ordering = ["accronyme"]

class Activite(models.Model):
    libelle = models.CharField(max_length=500, verbose_name="NATURE ACTIVITE")
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return '%s' %(self.libelle)

    def save(self, force_insert=False, force_update=False):
        self.libelle = self.libelle.upper()
        super(Activite, self).save(force_insert, force_update)

    class Meta:
        verbose_name_plural = "ACTIVITES"
        verbose_name = "activite"
        ordering = ["libelle"]

class Cat_Plant(models.Model):
    libelle = models.CharField(max_length=50, verbose_name="Categorie")

    def __str__(self):
        return '%s' %(self.libelle)

    def save(self, force_insert=False, force_update=False):
        self.libelle = self.libelle.upper()
        super(Cat_Plant, self).save(force_insert, force_update)

    class Meta:
        verbose_name_plural = "CATEGORIES PLANTS"
        verbose_name = "categorie plant"
        ordering = ["libelle"]

class Espece(models.Model):
    categorie = models.ForeignKey(Cat_Plant, on_delete=models.CASCADE)
    accronyme = models.CharField(max_length=250, verbose_name="NOM SCIENTIFIQUE")
    libelle = models.CharField(max_length=250, verbose_name="NOM USUEL")

    def __str__(self):
        return '%s (%s)' %(self.libelle, self.accronyme)

    def save(self, force_insert=False, force_update=False):
        self.accronyme = self.accronyme.upper()
        self.libelle = self.libelle.upper()
        super(Espece, self).save(force_insert, force_update)

    class Meta:
        verbose_name_plural = "ESPECES"
        verbose_name = "espece"
        ordering = ["libelle"]




