import os
import time
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe

from chocolotiers.models import Client
from cooperatives.models import Cooperative, Section, ACQUISITION, CERTIFICATION
from parametres.models import Projet, Espece


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
    ("coton", "COTON"),
    ("coton", "COTON"),
)

class Communaute(models.Model):
    cooperative = models.ForeignKey(Cooperative, on_delete=models.CASCADE)
    libelle = models.CharField(max_length=255, verbose_name="NOM COMMUNAUTE")
    responsable = models.CharField(max_length=255, verbose_name="NOM ET PRENOMS RESPONSABLE")
    contacts = models.CharField(max_length=50, blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    projet = models.ManyToManyField(Projet)
    culture_associee = models.CharField(max_length=50, verbose_name="CULTURE ASSOCIEE", choices=CULTURE_ASSOCIEE)
    logo = models.ImageField(verbose_name="Logo", upload_to=upload_logo_site, blank=True)
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('communaute:dashboard', kwargs={"id": self.id})

    def get_projet_values(self):
        ret = ''
        # print(self.projet.all())
        for proj in self.projet.all():
            ret = ret + proj.accronyme + ','
        return ret[:-1]

    def __str__(self):
        return '%s' %(self.libelle)
        # return '%s - %s (%s)' %(self.sigle, self.activite, self.get_projet_values())

    def save(self, force_insert=False, force_update=False):
        self.libelle = self.libelle.upper()
        self.responsable = self.responsable.upper()
        # self.user.last_name = self.user.last_name.upper()
        # self.user.first_name = self.user.first_name.upper()
        super(Communaute, self).save(force_insert, force_update)

    class Meta:
        verbose_name_plural = "COMMUNAUTE"
        verbose_name = "Communaute"
        ordering = ["libelle"]

    def Logo(self):
        if self.logo:
            return mark_safe('<img src="%s" style="width: 45px; height:45px;" />' % self.logo.url)
        else:
            return "Aucun Logo"

    Logo.short_description = 'Logo'

# class Sous_Section(models.Model):
#     section = models.ForeignKey(Section, on_delete=models.CASCADE)
#     libelle = models.CharField(max_length=250)
#     responsable = models.CharField(max_length=250)
#     contacts = models.CharField(max_length=50)
#     add_le = models.DateTimeField(auto_now_add=True)
#     update_le = models.DateTimeField(auto_now=True)
#     objects = models.Manager()
#
#     def __str__(self):
#         return '%s - (%s)' %(self.libelle, self.section.libelle)
#
#     def save(self, force_insert=False, force_update=False):
#         self.libelle = self.libelle.upper()
#         self.responsable = self.responsable.upper()
#         super(Sous_Section, self).save(force_insert, force_update)
#
#     class Meta:
#         verbose_name_plural = "SOUS SECTIONS"
#         verbose_name = "sous section"
#         ordering = ["libelle"]

class Parcelle(models.Model):
    code = models.CharField(max_length=150, blank=True, null=True, verbose_name='CODE PARCELLE', help_text="LE CODE PARCELLE EST GENERE AUTOMATIQUEMENT")
    # producteur = models.ForeignKey(Communaute, on_delete=models.CASCADE)
    # section = models.ForeignKey(Section, on_delete=models.CASCADE)
    # projet = models.ForeignKey(Projet, on_delete=models.CASCADE)
    communaute = models.ForeignKey(Communaute, on_delete=models.CASCADE, related_name="parcelle_communautaire")
    acquisition = models.CharField(max_length=50, verbose_name="MODE ACQUISITION", choices=ACQUISITION)
    # model_agro = models.CharField(max_length=50, verbose_name="MODEL AGROFORESTIER", choices=MODEL_AGRO)
    latitude = models.CharField(max_length=10)
    longitude = models.CharField(max_length=10)
    superficie = models.DecimalField(max_digits=15, decimal_places=12, null=True, blank=True)
    culture = models.CharField(max_length=50, verbose_name="CULTURE", choices=CULTURE)
    certification = models.CharField(max_length=50, verbose_name="CERTIFICATION", choices=CERTIFICATION)
    add_le = models.DateTimeField(auto_now_add=True)
    update_le = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return '%s - (%s)' % (self.producteur, self.culture)

    # def clean(self):
    #     # numerotation automatique
    #     if not self.id:
    #         tot = Parcelle.objects.count()
    #         num = tot + 1
    #         self.code = "%s_%s"%(self.producteur.code, num)
    #
    #     if self.sous_section == "":
    #         self.sous_section = self.producteur.section

    def coordonnees(self):
        return str(self.longitude) + ', ' + str(self.latitude)

    class Meta:
        verbose_name_plural = "PARCELLE"
        verbose_name = "parcelle"
        # ordering = ["code"]

class Planting(models.Model):
    parcelle = models.ForeignKey(Parcelle, on_delete=models.CASCADE)
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE, related_name="projet_communautaire")
    nb_plant = models.PositiveIntegerField(default=0)
    date = models.DateField()
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return '%s - (%s) plants reçus' % (self.parcelle.communaute, self.nb_plant)

    class Meta:
        verbose_name_plural = "PLANTINGS"
        verbose_name = "planting"
        # ordering = ["code"]

class Details_planting(models.Model):
    planting = models.ForeignKey(Planting, on_delete=models.CASCADE)
    espece = models.ForeignKey(Espece, on_delete=models.CASCADE, related_name="details_planting_communautaire")
    plante = models.PositiveIntegerField(default=0, verbose_name="NBRE PLANTS PLANTE")
    remplace = models.PositiveIntegerField(default=0, verbose_name="NBRE PLANTS REMPLACES")
    mort = models.PositiveIntegerField(default=0, verbose_name="NBRE PLANTS MORTS")
    mature = models.PositiveIntegerField(default=0, verbose_name="NBRE PLANTS MATURE")
    observation = models.TextField(blank=True, null=True)
    # Create your models here.
# Create your models here.
