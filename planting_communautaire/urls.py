from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static

from .views import com_dashboard, parcelles, parcelle_update, parcelle_delete

app_name='communautes'

urlpatterns = [
    path('dashboard/', com_dashboard, name='dashboard'),
    path('parcelles/', parcelles, name='parcelles'),
    path('parcelle/<int:id>/modifier', parcelle_update, name='edit_parcelle'),
    path('parcelle/<int:id>/supprimer', parcelle_delete, name='parcelle_delete'),
]