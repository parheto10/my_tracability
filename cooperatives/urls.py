from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static

from .views import (
    coop_dashboard,
    add_section,
    add_sous_section,
    producteurs,
    cooperative,
    prod_update,
    prod_delete,
    parcelles,
    parcelle_delete,
    planting,
    planting_update,
    formation,
    detail_formation,
    pepiniere,
    detail_pepiniere,
    localisation,
    Stats_coop,
    # use Ajax and jquery request
    my_section,
    export_producteur_csv,
    export_prod_xls,
    export_parcelle_xls,
    export_plant_xls, suivi_planting, edit_semence, Stats_semence, Editpepiniere, site_pepiniere, Editformation,
    delete_semence, parcelle_update, update_section, delete_section, export_section_xls, update_sous_section,
    ParcellesView, export_sous_section_xls, export_formation_xls,
    # delete_sous_section, export_sous_section_xls, export_formation_xls, my_parcelles, ParcellesView,
    # load_section
)

app_name='cooperatives'

urlpatterns = [
    # Patient
    path('cooperative/<int:id>', cooperative, name='cooperative'),
    path('producteur/<str:code>/modifier', prod_update, name='modifier'),
    path('producteur/<str:code>/supprimer', prod_delete, name='del_producteur'),
    # path('parcelle/<int:id>', parcelle_delete, name='del_parcelle'),
    path('parcelle/<int:id>/modifier', parcelle_update, name='edit_parcelle'),
    path('parcelle/<int:id>/supprimer', parcelle_delete, name='parcelle_delete'),
    path('section/<int:id>/modifier', update_section, name='update_section'),
    path('section/<int:id>/delete', delete_section, name='delete_section'),
    path('sous_section/<int:id>/modifier', update_sous_section, name='update_sous_section'),
    #path('sous_section/<int:id>/delete', delete_sous_section, name='delete_sous_section'),
    path('dashboard/', coop_dashboard, name='dashboard'),
    path('sections/', add_section, name='section'),
    path('sous_sections/', add_sous_section, name='sous_sections'),
    path('formation/', formation, name='formations'),
    path('Editformation/<int:id>', Editformation, name='Editformation'),
    path('formation/<int:id>', detail_formation, name='formation'),
    path('pepiniere/', pepiniere, name='pepinieres'),
    path('pepiniere/<int:id>', detail_pepiniere, name='pepiniere'),
    path('Editpepiniere/<int:id>', Editpepiniere, name='Editpepiniere'),
    path('delete_semence/<int:id>/supprimer', delete_semence, name='delete_semence'),
    path('semence/<int:id>', edit_semence, name='edit_semence'),
    path('producteurs/', producteurs, name='producteurs'),
    path('parcelles/', parcelles, name='parcelles'),
    #path('my_parcelles/', my_parcelles, name='my_parcelles'),
    path('plantings/', planting, name='planting'),
    path('Stats_coop/', Stats_coop, name='stats_coop'),
    path('Stats_semence/', Stats_semence, name='Stats_semence'),
    path('plantings/<int:id>/', suivi_planting, name='suivi_planting'),
    path('localisation/', localisation, name='localisation'),
    path('site_pepiniere/', site_pepiniere, name='site_pepiniere'),
    path('plantings/<int:id>', planting_update, name='planting_update'),

    #get Ajax Data
    path('parcelles/data', ParcellesView.as_view(), name="parcelles_data"),

    #path('my-section/', my_section, name='my_section'),
    # path('ajax/load-section/', load_section, name='ajax_load_section'),

    #Exportation de Données En Excel
    # path('export/csv/', export_producteur_csv, name='export_producteur_csv'),
    path('producteurs/xls/', export_prod_xls, name='export_prod_xls'),
    path('sections/xls/', export_section_xls, name='export_section_xls'),
    path('sous_sections/xls/', export_sous_section_xls, name='export_sous_section_xls'),
    path('parcelles/xls/', export_parcelle_xls, name='export_parcelle_xls'),
    path('plants/xls/', export_plant_xls, name='export_plant_xls'),
    path('formations/xls/', export_formation_xls, name='export_formation_xls'),

    # path('settings/', profile_setting, name='settings'),
    # path('add_patient/', add_patient, name="add_patient"),
    # path('rdv/', rdv_patient, name="checkout"),
]