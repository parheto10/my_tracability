from django import forms
from django.contrib import admin
from django.http import request
from import_export import resources
from import_export.admin import ImportExportModelAdmin
import django_select2

from .models import (
    Cooperative,
    Section,
    Sous_Section,
    Producteur,
    Parcelle,
    Planting,
    # Reception,
    DetailsReception,
    Monitoring,
    Formation,
    Detail_Formation,
    Pepiniere,
    Semence_Pepiniere,
    Retrait_plant,
    Detail_Retrait_plant,
    Stat, DetailsReception, DetailPlanting
)

class DetailsSemencePepiniereAdmin(admin.TabularInline):
   model = Semence_Pepiniere
   extra = 0

class DetailRetraitPlantAdmin(admin.TabularInline):
   model = Detail_Retrait_plant
   extra = 0

class RetraitPlantAdmin(admin.ModelAdmin):
    # model = Retrait_plant
    # extra = 0
    inlines = [DetailRetraitPlantAdmin]

class PepiniereAdmin(admin.ModelAdmin):
   inlines = [DetailsSemencePepiniereAdmin]
   # inlines = [Details_RetraitAdmin]

class CooperativeAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "sigle", "contacts"]

class SectionAdmin(admin.ModelAdmin):
    list_display = ["id", "libelle", "responsable"]

# class ProdAdminForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(ProdAdminForm, self).__init__(*args, **kwargs)
#         # access object through self.instance...
#         self.fields['section'].queryset = Section.objects.filter(cooperative=self.instance.cooperative)

class ProdResource(resources.ModelResource):
    class Meta:
        model = Producteur

class ProducteurAdmin(ImportExportModelAdmin):
    # fields = []
    list_display = ["id", "code", "nom", "prenoms", "origine", "contacts", "localite", "section"]
    list_filter = ["cooperative__sigle", "section__libelle", ]
    search_fields = ["code", "nom", "prenoms", "contacts", "section__libelle", ]
    # form = ProdAdminForm
    resource_class = ProdResource

class ParcelleResource(resources.ModelResource):
    class Meta:
        model = Parcelle

class ParcelleAdmin(ImportExportModelAdmin):
    list_display = ["id", "code", "producteur", "acquisition", "culture", "certification", "coordonnees"]
    list_filter = ["sous_section__section__libelle", "producteur__cooperative",]
    search_fields = ["code", "sction__libelle", "sous_sction__libelle", "producteur__nom", "producteur__prenoms", "latitude", "longitude", "superficie"]

# class DetailsReceptionAdmin(admin.TabularInline):
#    model = DetailsReception
#    extra = 0

class DetailPlantingAdmin(admin.TabularInline):
   model = DetailPlanting
   extra = 0

class MinitoringAdmin(admin.TabularInline):
   model = Monitoring
   fields = ['espece', 'mort', 'remplace', 'date', 'mature', 'observation']
   list_display = ['espece', 'mort', 'remplace', 'date', 'mature', 'observation']
   extra = 0

class PLantingAdmin(admin.ModelAdmin):
   fields = ('parcelle','projet', "campagne", "nb_plant_exitant", "plant_recus", "plant_total", "date")
   list_display = ('parcelle','projet', "campagne", "nb_plant_exitant", "plant_recus", "plant_total", "date")
   list_display_links = ('parcelle',)
   readonly_fields = ["plant_total"]
   inlines = [DetailPlantingAdmin, MinitoringAdmin]

# class ReceptionAdmin(admin.ModelAdmin):
#    fields = ("parcelle", "total_plant_recus", "date")
#    list_display = ("parcelle", "total_plant_recus", "date")
#    list_display_links = ('parcelle',)
#    inlines = [DetailsReceptionAdmin]

# class StatAdmin(admin.ModelAdmin):
#     cooperative = Cooperative.objects.get(user_id=request.user.id)
#     # cooperative = get_object_or_404(Cooperative, id=id)
#     cooperative = cooperative
#     if prod_section == 0 and self.prod_coop == 0:
#         self.prod_coop = Producteur.objects.all().filter(cooperative_id=cooperative).count()
#         self.prod_section = Producteur.objects.all().filter(section__cooperative_id=cooperative).count()

admin.site.register(Cooperative, CooperativeAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Sous_Section)
admin.site.register(Formation)
admin.site.register(Stat)
admin.site.register(Detail_Formation)
admin.site.register(Producteur, ProducteurAdmin)
admin.site.register(Parcelle, ParcelleAdmin)
admin.site.register(Planting, PLantingAdmin)
admin.site.register(Pepiniere, PepiniereAdmin)
admin.site.register(Retrait_plant, RetraitPlantAdmin)
# admin.site.register(Monitoring)
# admin.site.register(Reception, ReceptionAdmin)
# admin.site.register(DetailsReception)
# Register your models here.
