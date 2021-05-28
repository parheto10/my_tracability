from django.contrib import admin
from .models import Planting_Com, DetailPlanting, Monitoring, Organisation, Parcelle, Formation, Detail_Formation

class OrganisationAdmin(admin.ModelAdmin):
    list_display = ["region", "siege", "responsable", "contacts", "user",  "sigle", "libelle", "client"]

class DetailPlantingAdmin(admin.TabularInline):
   model = DetailPlanting
   extra = 0

class MinitoringAdmin(admin.TabularInline):
   model = Monitoring
   fields = ['espece', 'mort', 'remplace', 'date', 'mature', 'observation']
   list_display = ['espece', 'mort', 'remplace', 'date', 'mature', 'observation']
   extra = 0

class PLantingAdmin(admin.ModelAdmin):
   fields = ('parcelle','projet', "campagne", "nb_plant_exitant", "nb_plant", "plant_total", "date")
   list_display = ('parcelle','projet', "campagne", "nb_plant_exitant", "nb_plant", "plant_total", "date")
   list_display_links = ('parcelle',)
   readonly_fields = ["plant_total"]
   inlines = [DetailPlantingAdmin, MinitoringAdmin]


class ParcelleAdmin(admin.ModelAdmin):
   list_display = ('communaute', 'code', "culture", "associee", "superficie", "coordonnees")
   list_display_links = ('code',)
   list_filter = ['communaute__sigle', 'culture', 'associee', ]
   search_fields = ['code', 'culture', 'communaute', ]

admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Planting_Com, PLantingAdmin)
# admin.site.register(DetailPlanting)
admin.site.register(Parcelle, ParcelleAdmin)
# admin.site.register(Monitoring)
admin.site.register(Formation)
admin.site.register(Detail_Formation)

# Register your models here.
