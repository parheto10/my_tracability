from django.contrib import admin

from .models import (
    Communaute,
    # Sous_Section,
    Parcelle,
    Planting,
    Details_planting
)

admin.site.register(Communaute)
# admin.site.register(Sous_Section)
admin.site.register(Parcelle)
admin.site.register(Planting)
admin.site.register(Details_planting)

# Register your models here.
