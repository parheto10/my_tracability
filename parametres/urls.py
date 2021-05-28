from django.urls import path

from cooperatives.views import parcelle_list
from .views import (
    index,
    connexion,
    loggout,
    projet,
    # pepiniere,
    # detail_pepiniere,
    # formation,
    detail_proj,
    localisation,
    detail_coop,
    # chart,
    prod_coop,
    parcelle_coop,
    localisation_coop,
    section_coop,
    sous_section_coop,
    Stats_coop, Production_plan,
    Stats_semences, stat_prod_coop, plants_coop, semences_coop, formations, detail_formation, site_pepinieres,
    coop_pepiniere, pepiniere, pepiniere_coop, export_prods_to_pdf, export_parcelles_to_pdf, export_prod_xls,
    export_parcelle_xls, export_plant_xls, export_formation_xls, ParcellesMapView, ProducteurApiView, ParcelleApiView,
    ParcelleJson, PepiniereJson, PepiniereApiView, FormationApiView, folium_map,
    planting_coop, planting_list, produteur_list, parcelles_list, details_planting_list  # , ParcelleCooperativeApi
    # detail_formation,
)

urlpatterns = [
    path('', connexion, name='connexion'),
    path('logout', loggout, name='logout'),
    path('index/', index, name='accueil'),
    path('projets/', projet, name='projets'),
    path('pepinieres/', pepiniere, name='pepinieres'),
    path('pepiniere_coop/<int:id>', pepiniere_coop, name='pepiniere_coop'),
    path('formation/<int:id>', formations, name='formations'),
    path('formation/<int:id>/<int:_id>', detail_formation, name='formation'),
    path('Stats_coop/', Stats_coop, name='stats_coop'),
    path('Stats_semences/', Stats_semences, name='stats_semences'),
    path('Production_plan/', Production_plan, name='production_plan'),
    path('stat_prod_coop/', stat_prod_coop, name='stat_prod_coop'),
    path('plants_coop/<int:id>', plants_coop, name='plants_coop'),
    path('semences_coop/<int:id>', semences_coop, name='semences_coop'),
    # path('pepiniere/', pepiniere, name='pepiniere'),
    # path('formations/', formation, name='formations'),
    path('producteurs/<int:id>', prod_coop, name='prod_coop'),
    path('parcelles/<int:id>', parcelle_coop, name='parcelle_coop'),
    path('sections/<int:id>', section_coop, name='section_coop'),
    path('sous_sections/<int:id>', sous_section_coop, name='sous_section_coop'),
    path('planting/<int:id>', planting_coop, name='planting_coop'),
    path('coordonnes/<int:id>', localisation_coop, name='localisation_coop'),
    path('localisation/', localisation, name='localisation'),
    path('detail_proj/<int:id>', detail_proj, name='detail_proj'),
    path('site_pepinieres/', site_pepinieres, name='site_pepinieres'),
    path('coop_pepiniere/<int:id>', coop_pepiniere, name='coop_pepiniere'),
    # path('detail_pepiniere/<int:id>', detail_pepiniere, name='detail_pepiniere'),
    # path('formation/<int:id>', detail_formation, name='formation'),
    path('detail_coop/<int:id>', detail_coop, name='detail_coop'),
    # path('chart/<int:id>', chart, name='chart'),

#Export to Excel
    path('cooperative/<int:id>/producteurs/xls/', export_prod_xls, name='export_prod_xls'),
    # path('sections/xls/', export_section_xls, name='export_section_xls'),
    # path('sous_sections/xls/', export_sous_section_xls, name='export_sous_section_xls'),
    path('cooperative/<int:id>/parcelles/xls/', export_parcelle_xls, name='export_parcelle_xls'),
    path('cooperative/<int:id>/plants/xls/', export_plant_xls, name='export_plant_xls'),
    path('cooperative/<int:id>/formations/xls/', export_formation_xls, name='export_formation_xls'),

    # Export Données EN PDF
    path('producteurs/pdf/<int:id>', export_prods_to_pdf, name='export_prods_to_pdf'),
    path('parcelles/pdf/<int:id>', export_parcelles_to_pdf, name='export_parcelles_to_pdf'),

    #Api Urls
    path('api/producteurs', ProducteurApiView.as_view(), name="producteurs_api"),
    path('api/parcelles', ParcelleApiView.as_view(), name="parcelles_api"),
    # path('api/parcelles_coop', ParcelleCooperativeApi.as_view(), name="coop_parcelles_api"),
    path('api/pepinieres', PepiniereApiView.as_view(), name="pepinieres_api"),
    path('api/formations', FormationApiView.as_view(), name="formations_api"),

    #map leaflet
    path('pepinieres_json/', PepiniereJson.as_view(), name="pepinieres_json"),
    path('geolocalisation/', ParcelleJson.as_view(), name='geolocalisation'),
    # path('parcelles/data', ParcellesView.as_view(), name="data"),
    path('parcelles/data', parcelle_list, name="data"),

    #Folium Map
    path('folium_map/', folium_map, name="folium_map"),

    # Api
    # path('plantings/api/v1/', planting_list, name="plantings"),
    path('producteurs/api/v1/', produteur_list, name="producteurs"),
    path('parcelles/api/v1/', parcelles_list, name="parcelles"),
    path('plantings/api/v1/', planting_list, name="plantings"),
    path('details_plantings/api/v1/', details_planting_list, name="details_plantings"),




]
