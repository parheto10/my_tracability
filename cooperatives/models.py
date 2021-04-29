# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import time
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
import datetime

from django.db.models import Sum, Count
from django.http import request
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.safestring import mark_safe
from sorl.thumbnail import get_thumbnail

from chocolotiers.models import Client


def producteurs_images(self, filename):
    # verification de l'extension
    real_name, extension = os.path.splitext(filename)
    name = str(int(time.time())) + extension
    return "Producteurs/Images/" + self.code + ".jpeg"

def producteurs_documents(self, filename):
    # verification de l'extension
    real_name, extension = os.path.splitext(filename)
    name = str(int(time.time())) + extension
    return "Producteurs/Documents/" + self.code


def upload_logo_site(self, filename):
    # verification de l'extension
    real_name, extension = os.path.splitext(filename)
    name = str(int(time.time())) + extension
    return "logos/" + self.code + ".jpeg"

from parametres.models import Region, Activite, Origine, Sous_Prefecture, Projet, Espece, Campagne

TYPE_PRODUCTEUR = (
    ('membre', "MEMBRE"),
    ('usager', "USAGER"),
    # ('caummunautaire', "COMMUNAUTAIRE"),
)

NATURE_DOC = (
    ('AUCUN', 'AUCUN'),
    ('ATTESTATION', 'ATTESTATION'),
    ('CNI', 'CNI'),
    ('PASSEPORT', 'PASSEPORT'),
    ('SEJOUR', 'CARTE DE SEJOUR'),
    ('CONSULAIRE', 'CARTE CONSULAIRE'),
)

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

CERTIFICATION = (
    ('utz', 'UTZ'),
    ('ra', 'RA'),
    ('bio', 'BIO'),
    ('projet', 'PROJET'),
    ('autre', 'PROJET'),
)

GENRE = (
    ('H', "HOMME"),
    ('F', "FEMME"),
)

ACQUISITION = (
    ('heritage', 'HERITAGE'),
    ('achat', 'ACHAT'),
    ('autres', 'AUTRES'),
)

MODEL_AGRO = (
    ("autour", "AUTOUR"),
    ("autour_centre", "AUTOUR & CENTRE"),
)

class Cooperative(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    siege = models.CharField(max_length=255, verbose_name="SIEGE/LOCALITE", blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    projet = models.ManyToManyField(Projet)
    sigle = models.CharField(max_length=500)
    activite = models.ForeignKey(Activite, on_delete=models.CASCADE)
    contacts = models.CharField(max_length=50)
    logo = models.ImageField(verbose_name="Logo", upload_to=upload_logo_site, blank=True)
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('cooperatives:dashboard', kwargs={"id": self.id})



    def get_projet_values(self):
        ret = ''
        # print(self.projet.all())
        for proj in self.projet.all():
            ret = ret + proj.accronyme + ','
        return ret[:-1]

    def __str__(self):
        return '%s' %(self.sigle)
        # return '%s - %s (%s)' %(self.sigle, self.activite, self.get_projet_values())

    def save(self, force_insert=False, force_update=False):
        self.sigle = self.sigle.upper()
        self.siege = self.siege.upper()
        self.user.last_name = self.user.last_name.upper()
        self.user.first_name = self.user.first_name.upper()
        super(Cooperative, self).save(force_insert, force_update)

    class Meta:
        verbose_name_plural = "COOPERATIVES"
        verbose_name = "cooperative"
        ordering = ["sigle"]

    def Logo(self):
        if self.logo:
            return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.logo.url)
        else:
            return "Aucun Logo"

    Logo.short_description = 'Logo'
    # Create your models here.

class Section(models.Model):
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE)
    libelle = models.CharField(max_length=250)
    responsable = models.CharField(max_length=250)
    contacts = models.CharField(max_length=50)
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return '%s' %(self.libelle)

    def save(self, force_insert=False, force_update=False):
        self.libelle = self.libelle.upper()
        self.responsable = self.responsable.upper()
        super(Section, self).save(force_insert, force_update)

    class Meta:
        verbose_name_plural = "SECTIONS"
        verbose_name = "section"
        ordering = ["libelle"]

class Sous_Section(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    libelle = models.CharField(max_length=250)
    responsable = models.CharField(max_length=250)
    contacts = models.CharField(max_length=50)
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return '%s' %(self.libelle)

    def save(self, force_insert=False, force_update=False):
        self.libelle = self.libelle.upper()
        self.responsable = self.responsable.upper()
        super(Sous_Section, self).save(force_insert, force_update)

    class Meta:
        verbose_name_plural = "SOUS SECTIONS"
        verbose_name = "sous section"
        ordering = ["libelle"]

class Producteur(models.Model):
    code = models.CharField(max_length=150, blank=True, null=True, verbose_name='CODE PRODUCTEUR')
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE)
    origine = models.ForeignKey(Origine, on_delete=models.CASCADE)
    sous_prefecture = models.ForeignKey(Sous_Prefecture, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    sous_section = models.ForeignKey(Sous_Section, related_name="sous_section", on_delete=models.SET_NULL, null=True)
    type_producteur = models.CharField(max_length=50, verbose_name="TYPE PRODUCTEUR", choices=TYPE_PRODUCTEUR, default="membre")
    genre = models.CharField(max_length=2, choices=GENRE, default="H")
    nom = models.CharField(max_length=250, blank=True, null=True)
    prenoms = models.CharField(max_length=500,  blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    contacts = models.CharField(max_length=50, blank=True, null=True)
    localite = models.CharField(max_length=100, blank=True, null=True, verbose_name="LOCALITE")
    nb_enfant = models.PositiveIntegerField(default=0, null=True, blank=True)
    nb_parcelle = models.PositiveIntegerField(default=0)
    image = models.ImageField(verbose_name="Logo", upload_to=producteurs_images, blank=True)
    type_document = models.CharField(max_length=50, verbose_name="TYPE DOCUMENT", choices=NATURE_DOC, default="AUCUN")
    num_document = models.CharField(max_length=150, verbose_name="N° PIECE", null=True, blank=True)
    document = models.FileField(verbose_name="Documents", upload_to=producteurs_documents, blank=True, null=True)
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return '%s %s' %(self.nom, self.prenoms)

    def Producteur(self):
        return '%s %s' % (self.nom, self.prenoms)

    def save(self, force_insert=False, force_update=False):
        self.nom = self.nom.upper()
        self.prenoms = self.prenoms.upper()
        # self.responsable = self.responsable.upper()
        if self.localite:
            self.localite = self.localite.upper()

        # if self.prod_coop==0 and self.prod_section==0:
        #     cooperative = get_object_or_404(Cooperative, id=id)
        #     self.prod_coop = Producteur.objects.all().filter(cooperative_id=cooperative).count()
        #     self.prod_section = Producteur.objects.all().filter(section__cooperative_id=cooperative).count()
            # return prod_coop
        super(Producteur, self).save(force_insert, force_update)

    # def tot_prod_coop(self):
    #     cooperative = get_object_or_404(Cooperative, id=id)
    #     prod_coop = Producteur.objects.all().filter(cooperative_id=cooperative).count()
    #     return prod_coop

    def clean(self):
        if self.type_document != "AUCUN" and self.document == "":
            raise ValidationError('Veuillez Charger le Document Approprié SVP')


        # numerotation automatique
        # if not self.id:
        #     tot = Producteur.objects.count()
        #     num = tot + 1
        #     #zcode = num.zfill(3)
        #     if not self.code:
        #         self.code = "00%s" % (num)
        #     else:
        #         pass
            # self.code = "%s-%s" % (numero, datetime.date.strftime(madate, '%d/%m/%Y'))

    # def save(self, force_insert=False, force_update=False):
    #     self.code = self.code.upper()
    #     self.nom = self.nom.upper()
    #     self.prenoms = self.prenoms.upper()
    #     if self.localite:
    #         self.localite = self.localite.upper()
    #    super(Producteur, self).save(force_insert, force_update)

    def Photo(self):
        if self.image:
            photoLink = "/media/%s" % self.image
            thumb = mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.image.url)
            return "<img src='%s' />" % thumb.url
        elif self.genre == "H":
            thumb = mark_safe('<img src="127.0.0.1:8000/static/img/logo_homme.jpeg" style="width: 45px; height:45px;" />')
            # thumb = get_thumbnail('127.0.0.1:8000/static/img/logo_home.jpeg', "60x60", crop='center', quality=99)
            return "<img src='%s' />" % thumb
            # return ""
        else:
            thumb = mark_safe('<img src="127.0.0.1:8000/static/img/logo_femme.jpeg" style="width: 45px; height:45px;" />')
            return "<img src='%s' />" % thumb
            # return "127.0.0.1:8000/img/avatar3.png"
            # return "Aucun logo"

    Photo.short_description = "Logo"
    Photo.allow_tags = True

    class Meta:
        verbose_name_plural = "PRODUCTEURS"
        verbose_name = "producteur"
        ordering = ["id"]

class Parcelle(models.Model):
    code = models.CharField(max_length=150, blank=True, null=True, verbose_name='CODE PARCELLE', help_text="LE CODE PARCELLE EST GENERE AUTOMATIQUEMENT")
    producteur = models.ForeignKey(Producteur, related_name='parcelles', on_delete=models.CASCADE)
    # section = models.ForeignKey(Section, on_delete=models.CASCADE)
    # projet = models.ForeignKey(Projet, on_delete=models.CASCADE)
    sous_section = models.ForeignKey(Sous_Section, related_name="sous_section_parcelle", on_delete=models.SET_NULL, null=True)
    acquisition = models.CharField(max_length=50, verbose_name="MODE ACQUISITION", choices=ACQUISITION, default="heritage")
    # model_agro = models.CharField(max_length=50, verbose_name="MODEL AGROFORESTIER", choices=MODEL_AGRO)
    latitude = models.CharField(max_length=10, null=True, blank=True)
    longitude = models.CharField(max_length=10, null=True, blank=True)
    superficie = models.DecimalField(max_digits=5, decimal_places=3, null=True, blank=True)
    culture = models.CharField(max_length=50, verbose_name="CULTURE", choices=CULTURE, default="cacao")
    certification = models.CharField(max_length=50, verbose_name="CERTIFICATION", choices=CERTIFICATION, default="utz")
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        if self.code:
            return "%s - %s" % (self.code, self.producteur)
        else:
            return "%s - %s" % (self.producteur.code, self.producteur)

    def clean(self):
       # numerotation automatique
       if not self.id and self.code == "":
           # tot = Parcelle.objects.count(campagne = models.ForeignKey(Campagne, on_delete=models.CASCADE, default=3))
           # tot =  Producteur.objects.annotate(num_parcelle=Count('parcelles'))
           for prod in Producteur.objects.all():
               tot = Parcelle.objects.all().filter(producteur=prod).count()
               self.code = "%s-%s"%(self.producteur.code, tot)

    # def clean(self):
    #    # numerotation automatique
    #    if not self.id and self.code == "":
    #        tot = Parcelle.objects.count()
    #        # tot = Producteur.objects.annotate(Count('parcelle'))
    #        # tot = Producteur.objects.annotate(nombre_parcelle=Count('parcelle'))
    #        num = tot
    #        self.code = "%s"%(num)

    # if self.sous_section == "":
    #     self.sous_section = self.producteur.section

    def coordonnees(self):
        return str(self.longitude) + ', ' + str(self.latitude)

    # def coordonnees(self):
    #     return str(self.latitude) + ', ' + str(self.longitude)

    class Meta:
        verbose_name_plural = "PARCELLES"
        verbose_name = "parcelle"
        # ordering = ["code"]

class Reception(models.Model):
    parcelle = models.ForeignKey(Parcelle, on_delete=models.CASCADE)
    total_plant_recus = models.PositiveIntegerField(default=0, verbose_name="NOMBRE TOTAL DE PLANTS RECUS")
    date = models.DateField(verbose_name="Date Reception")
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return '%s (%s)' %(self.parcelle, self.total_plant_recus)

    class Meta:
        verbose_name_plural = "RECEPTIONS"
        verbose_name = "reception"
        # ordering = ["code"]

class DetailsReception(models.Model):
    reception = models.ForeignKey(Reception, on_delete=models.CASCADE)
    espece = models.ForeignKey(Espece, on_delete=models.CASCADE, default=1)
    nb_plant_recu = models.PositiveIntegerField(default=0, verbose_name="NOMBRE PLANT RECUS")
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        verbose_name_plural = "DETAILS RECEPTIONS"
        verbose_name = "detail reception"

class Planting(models.Model):
    parcelle = models.ForeignKey(Parcelle, on_delete=models.CASCADE)
    nb_plant_exitant = models.PositiveIntegerField(default=0, verbose_name="NBRE PLANTS EXISTANTS")
    plant_recus = models.PositiveIntegerField(default=0, verbose_name="NOMBRE DE PLANTS RECUS")
    plant_total = models.PositiveIntegerField(default=0, verbose_name="NOMBRE TOTAL DE PLANTS")
    plant_recu = models.CharField(max_length=4, blank=True, null=True)
    campagne = models.ForeignKey(Campagne, on_delete=models.CASCADE, default=1)
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, default=1)
    date = models.DateField()
    details = models.TextField(blank=True, null=True)
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return '%s - (%s) plants reçus' % (self.parcelle.producteur, self.parcelle)

    def save(self, force_insert=False, force_update=False):
        self.plant_total = (self.nb_plant_exitant) + (self.plant_recus)
        super(Planting, self).save(force_insert, force_update)

    class Meta:
        verbose_name_plural = "PLANTINGS"
        verbose_name = "planting"
        #ordering = ["code"]

class DetailPlanting(models.Model):
    planting = models.ForeignKey(Planting, on_delete=models.CASCADE)
    espece = models.ForeignKey(Espece, on_delete=models.CASCADE, default=1)
    nb_plante = models.PositiveIntegerField(default=0, verbose_name="NBRE PLANTS PLANTE/ESPECE")
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        verbose_name_plural = "DETAILS PLANTINGS"
        verbose_name = "details planting"


class Monitoring(models.Model):
    planting = models.ForeignKey(Planting, on_delete=models.CASCADE)
    mort = models.PositiveIntegerField(default=0, verbose_name="NBRE PLANTS MORTS")
    remplace = models.PositiveIntegerField(default=0, verbose_name="NBRE PLANTS REMPLACES")
    mature = models.PositiveIntegerField(default=0, verbose_name="NBRE PLANTS VIVANTS")
    observation = models.TextField(blank=True, null=True)
    date = models.DateField()
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        verbose_name_plural = "MONITORINGS"
        verbose_name = "monitoring"
    # Create your models here.

class Formation(models.Model):
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE)
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, default=1)
    campagne = models.ForeignKey(Campagne, on_delete=models.CASCADE, default=1)
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
        verbose_name_plural = "FORMATIONS"
        verbose_name = "formation"
        ordering = ["libelle"]

class Detail_Formation(models.Model):
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE)
    participant = models.ManyToManyField(Producteur)
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def Participants(self):
        nb_participants = self.participant.all().count()
        return nb_participants

    def __str__(self):
        return "%s" % (self.formation.libelle)

    class Meta:
        verbose_name_plural = "DETAILS FORMATIONS"
        verbose_name = "details formation"
        # ordering = ["libelle"]

class Pepiniere(models.Model):
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE)
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, default=1)
    campagne = models.ForeignKey(Campagne, on_delete=models.CASCADE, default=1)
    region = models.CharField(max_length=250, verbose_name="DELEGATION REGIONALE")
    ville = models.CharField(max_length=250, verbose_name="VILLE")
    site = models.CharField(max_length=250, verbose_name="SITE")
    latitude = models.CharField(max_length=10, null=True, blank=True)
    longitude = models.CharField(max_length=10, null=True, blank=True)
    technicien = models.CharField(max_length=255, verbose_name="NOM ET PRENOMS TECHNICIEN")
    contacts_technicien = models.CharField(max_length=50, blank=True, null=True, verbose_name="CONTACTS TECHNICIEN")
    superviseur = models.CharField(max_length=255, verbose_name="NOM ET PRENOMS TECHNICIEN")
    contacts_superviseur = models.CharField(max_length=50, blank=True, null=True, verbose_name="CONTACTS SUPERVISUER")
    # localisation = models.CharField(max_length=255, verbose_name="LOCALITE (S/P - VILLAGE)")
    # total_semence = models.PositiveIntegerField(default=0, verbose_name="QTE TOTAL SEMENCE RECU")
    sachet_recus = models.PositiveIntegerField(default=0, verbose_name="QTE TOTAL SACHET RECU")
    production_plant = models.PositiveIntegerField(default=0, verbose_name="PLANTS A PRODUIRE")
    production_realise = models.PositiveIntegerField(default=0, verbose_name="REALISATION")
    pourcentage_prod = models.PositiveIntegerField(default=0, verbose_name="POURCENTAGE DE PRODUCTION")
    plant_mature = models.PositiveIntegerField(default=0, verbose_name="NBRE PLANT MATURE")
    plant_retire = models.PositiveIntegerField(default=0, verbose_name="NBRE TOTAL PLANT RETIRE")
    # sachet_rempli = models.PositiveIntegerField(default=0, verbose_name="QTE TOTAL SACHET REMPLI")
    # sachet_perdu = models.PositiveIntegerField(default=0, verbose_name="QTE TOTAL SACHET PERDU")
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return '%s(%s - %s)' %(self.cooperative.sigle, self.region, self.site)

    def taux(self):
        if self.production_plant != 0 and self.production_realise != 0:
            Taux = float("{:.2f}".format((self.production_realise / self.production_plant) * 100))
            self.pourcentage_prod = Taux
            return Taux

    def save(self, force_insert=False, force_update=False):
        self.region = self.region.upper()
        self.ville = self.ville.upper()
        self.site = self.site.upper()
        self.technicien = self.technicien.upper()
        self.superviseur = self.superviseur.upper()
        if self.production_plant !=0 and self.production_realise !=0:
            self.pourcentage_prod = float("{:.2f}".format((self.production_realise / self.production_plant) * 100))
        super(Pepiniere, self).save(force_insert, force_update)

    def coordonnees(self):
        return str(self.longitude) + ', ' + str(self.latitude)

    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    class Meta:
        verbose_name_plural = "PEPINIERES"
        verbose_name = "pépinière"
        # ordering = ["libelle"]

class Semence_Pepiniere(models.Model):
    pepiniere = models.ForeignKey(Pepiniere, on_delete=models.CASCADE)
    espece_recu = models.ForeignKey(Espece, on_delete=models.CASCADE)
    production = models.PositiveIntegerField(default=0, verbose_name="NB PLANTS A PRODUIRE")
    qte_recu = models.PositiveIntegerField(default=0, verbose_name="QTE RECU")
    date = models.DateField(verbose_name="DATE RECEPTION")
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def total_semence(self):
        pepiniere = get_object_or_404(Pepiniere, id=id)
        t_semence = Semence_Pepiniere.objects.filter(pepiniere_id=pepiniere).aggregate(total=Sum('qte_recu'))
        return t_semence

    class Meta:
        verbose_name_plural = "DETAILS SEMENCES RECUS"
        verbose_name = "détail semence reçu"
        # ordering = ["libelle"]

class Retrait_plant(models.Model):
    pepiniere = models.ForeignKey(Pepiniere, on_delete=models.CASCADE)
    client = models.CharField(max_length=255, verbose_name="CLIENT", blank=True)
    destination = models.CharField(max_length=255, verbose_name="LOCALITE (S/P - Ville - VILLAGE)")
    plant_retire = models.PositiveIntegerField(default=0, verbose_name="NBRE TOTAL DE PLANTS RETIRES")
    date = models.DateField(verbose_name="DATE RETRAIT")
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return '%s - %s' %(self.destination, self.date)

    def save(self, force_insert=False, force_update=False):
        self.pepiniere.site = self.pepiniere.site.upper()
        self.client = self.client.upper()
        self.destination = self.destination.upper()
        super(Retrait_plant, self).save(force_insert, force_update)

    class Meta:
        verbose_name_plural = "RETRAITS PLANTS"
        verbose_name = "retrait plant"
        # ordering = ["espece"]

class Detail_Retrait_plant(models.Model):
    retait = models.ForeignKey(Retrait_plant, on_delete=models.CASCADE)
    espece = models.ForeignKey(Espece, on_delete=models.CASCADE)
    plant_retire = models.PositiveIntegerField(default=0, verbose_name="NBRE PLANT RETIRE")
    date = models.DateField(verbose_name="DATE RETRAIT")
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def total_plant_retire(self):
        if self.plant_retire != 0:
            pepiniere = get_object_or_404(Pepiniere, id=id)
            t_retrait = Detail_Retrait_plant.objects.filter(retait__pepiniere_id=pepiniere).aggregate(total=Sum('production'))
            return t_retrait

    class Meta:
        verbose_name_plural = "DETAILS RETRAITS PLANTS"
        verbose_name = "detail retrait plant"
        ordering = ["espece"]


class Stat(models.Model):
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE)
    campagne = models.ForeignKey(Campagne, on_delete=models.CASCADE, default=1)
    # section = models.ForeignKey(Section, on_delete=models.CASCADE)
    prod_section = models.PositiveIntegerField(default=0, null=True, blank=True)
    prod_coop = models.PositiveIntegerField(default=0, null=True, blank=True)

    def save(self, force_insert=False, force_update=False):
        cooperative = Cooperative.objects.get(user_id=request.user.id)
        # cooperative = get_object_or_404(Cooperative, id=id)
        self.cooperative = cooperative
        if self.prod_section ==0 and self.prod_coop ==0:
            self.prod_coop = Producteur.objects.all().filter(cooperative_id=cooperative).count()
            self.prod_section = Producteur.objects.all().filter(section__cooperative_id=cooperative).count()
        super(Stat, self).save(force_insert, force_update)


# Create your models here.
