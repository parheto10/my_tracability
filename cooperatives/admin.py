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
    Details_planting,
    Formation,
    Detail_Formation,
    Pepiniere,
    Semence_Pepiniere,
    Retrait_plant,
    Detail_Retrait_plant,
    Stat
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
    list_filter = ["sous_section__libelle", "producteur__cooperative", ]
    search_fields = ["code", "sction__libelle", "sous_sction__libelle", "producteur__nom", "producteur__prenoms", ]

class DetailsPlantingAdmin(admin.TabularInline):
   model = Details_planting
   extra = 0
   # fields = ('employe',)
   # formset = EquipeEmployeInlineFormset

   # def formfield_for_foreignkey(self,db_field,request,**kwargs):
   #    #parent_obj_id = request.META['PATH_INFO'].rstrip('/').split('/')[-1]
   #    #equipe = Equipe.objects.filter(pk=parent_obj_id)[0]
   #    if db_field.name == "employe":
   #       kwargs["queryset"] = Employe.objects.order_by('nom','prenoms')
   #    return super(EquipeEmployeInlineAdmin,self).formfield_for_foreignkey(db_field,request,**kwargs)

class PLantingAdmin(admin.ModelAdmin):
   # fields = ('libequipe','service')
   # list_display = ('libequipe','service')
   # list_display_links = ('libequipe',)
   inlines = [DetailsPlantingAdmin]

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
# Register your models here.
