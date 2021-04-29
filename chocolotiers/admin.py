from django.contrib import admin
from .models import Client

class ChocolatierAdmin(admin.ModelAdmin):
    list_display = ["Logo", "libelle", "telephone1", "telephone2", "email", "siteweb"]
    list_filter = ["libelle", ]
    search_fields = ["libelle", "telephone1", "email", ]

admin.site.register(Client, ChocolatierAdmin)
# Register your models here.
