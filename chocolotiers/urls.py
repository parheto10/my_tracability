from django.urls import path

from .views import (
    client_index,
    projet,
    detail_proj,
    localisation,
    detail_coop,
    # chart,
    prod_coop,
    parcelle_coop,
    localisation_coop,
    section_coop,
    sous_section_coop,
    planting_coop, Stats_coop, Stats_semences, Production_plan, plants_coop, semences_coop, formations,
    detail_formation, site_pepinieres, coop_pepiniere, export_prod_xls,
    export_parcelle_xls, export_plant_xls, export_formation_xls
)

app_name='clients'

urlpatterns = [
    # path('', connexion, name='connexion'),
    # path('logout', loggout, name='logout'),
    path('client_index/', client_index, name='dashboard'),
    path('projets/', projet, name='projets'),
    path('formation/<int:id>', formations, name='formations'),
    path('formation/<int:id>/<int:_id>', detail_formation, name='formation'),
    path('producteurs/<int:id>', prod_coop, name='prod_coop'),
    path('parcelles/<int:id>', parcelle_coop, name='parcelle_coop'),
    path('sections/<int:id>', section_coop, name='section_coop'),
    path('sous_sections/<int:id>', sous_section_coop, name='sous_section_coop'),
    path('planting/<int:id>', planting_coop, name='planting_coop'),
    path('coordonnes/<int:id>', localisation_coop, name='localisation_coop'),
    path('localisation/', localisation, name='localisation'),
    path('site_pepinieres/', site_pepinieres, name='site_pepinieres'),
    path('coop_pepiniere/<int:id>', coop_pepiniere, name='coop_pepiniere'),
    path('detail_proj/<int:id>', detail_proj, name='detail_proj'),
    path('detail_coop/<int:id>', detail_coop, name='detail_coop'),
    #Charts
    path('Stats_coop/', Stats_coop, name='stats_coop'),
    path('Stats_semences/', Stats_semences, name='stats_semences'),
    path('Production_plan/', Production_plan, name='production_plan'),
    path('plants_coop/<int:id>', plants_coop, name='plants_coop'),
    path('semences_coop/<int:id>', semences_coop, name='semences_coop'),
    # path('chart/<int:id>', chart, name='chart'),

    #Export to Excel
    path('cooperative/<int:id>/producteurs/xls/', export_prod_xls, name='export_prod_xls'),
    # path('sections/xls/', export_section_xls, name='export_section_xls'),
    # path('sous_sections/xls/', export_sous_section_xls, name='export_sous_section_xls'),
    path('cooperative/<int:id>/parcelles/xls/', export_parcelle_xls, name='export_parcelle_xls'),
    path('cooperative/<int:id>/plants/xls/', export_plant_xls, name='export_plant_xls'),
    path('cooperative/<int:id>/formations/xls/', export_formation_xls, name='export_formation_xls'),
]
