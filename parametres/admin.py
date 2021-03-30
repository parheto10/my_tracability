from django.contrib import admin

from .models import (
    Sous_Prefecture,
    Origine,
    Prime,
    Projet,
    Activite,
    Region,
    Campagne,
    Espece,
    Cat_Plant,
    Projet_Cat,
    # Formation,
    # Pepiniere,
    # Detail_Pepiniere,
    # Detail_Retrait
)

admin.site.register(Activite)
admin.site.register(Campagne)
# admin.site.register(Client)
admin.site.register(Espece)
# admin.site.register(Formation)
admin.site.register(Prime)
admin.site.register(Origine)
admin.site.register(Projet)
admin.site.register(Region)
admin.site.register(Sous_Prefecture)
admin.site.register(Cat_Plant)
admin.site.register(Projet_Cat)
# admin.site.register(Pepiniere, PepiniereAdmin)
# admin.site.register(Detail_pepiniere)
# admin.site.register(Retrait_Plant)

# Register your models here.
