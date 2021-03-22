from itertools import product
import datetime
import xlwt
from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login, get_user_model, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.http import JsonResponse
from twisted.words.protocols.jabber.jstrports import client

from chocolotiers.models import Client
from parametres.models import (
    Sous_Prefecture,
    Origine,
    Prime,
    Projet,
    Activite,
    Region,
    Campagne
)

from cooperatives.models import (
    Cooperative,
    Producteur,
    Parcelle,
    Planting,
    Section,
    Sous_Section, Details_planting, Semence_Pepiniere, Detail_Retrait_plant, Formation, Detail_Formation, Pepiniere
)

def client_index(request, id=None):
    cooperatives = Cooperative.objects.all()
    nb_cooperatives = Cooperative.objects.all().count()
    nb_producteurs = Producteur.objects.all().count()
    nb_parcelles = Parcelle.objects.all().count()
    Superficie = Parcelle.objects.aggregate(total=Sum('superficie'))['total']
    Total_plant = Planting.objects.aggregate(total=Sum('nb_plant'))['total']

    context = {
        'cooperatives':cooperatives,
        'nb_cooperatives': nb_cooperatives,
        'nb_producteurs': nb_producteurs,
        'nb_parcelles': nb_parcelles,
        'Superficie': Superficie,
        'Total_plant': Total_plant,
    }
    return render(request, 'chocolatiers/client_index.html', context)

def detail_coop(request, id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    coop_producteurs = Producteur.objects.all().filter(section__cooperative_id=cooperative)
    coop_nb_producteurs = Producteur.objects.all().filter(cooperative_id=cooperative).count()
    coop_parcelles = Parcelle.objects.all().filter(producteur__section__cooperative_id=cooperative)
    nb_formations = Formation.objects.all().filter(cooperative_id=cooperative).count()
    coop_nb_parcelles = Parcelle.objects.all().filter(producteur__section__cooperative_id=cooperative).count()
    coop_superficie = Parcelle.objects.all().filter(producteur__cooperative_id=cooperative).aggregate(total=Sum('superficie'))['total']
    plants = Details_planting.objects.values("espece__libelle").filter(planting__parcelle__producteur__cooperative_id=cooperative).annotate(plante=Sum('plante'))
    coop_plants_total = Planting.objects.all().filter(parcelle__producteur__cooperative_id=cooperative).aggregate(total=Sum('nb_plant'))['total']

    context = {
        'cooperative': cooperative,
        'coop_nb_producteurs': coop_nb_producteurs,
        'coop_nb_parcelles': coop_nb_parcelles,
        'coop_superficie': coop_superficie,
        'plants': plants,
        'nb_formations':nb_formations,
        'coop_plants_total': coop_plants_total,
    }
    return render(request, 'chocolatiers/Coop/cooperative.html', context)

def section_coop(request, id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    coop_sections = Section.objects.all().filter(cooperative_id=cooperative)
    context = {
        'cooperative': cooperative,
        'coop_sections': coop_sections,
    }
    return render(request, 'chocolatiers/Coop/coop_sections.html', context)

def sous_section_coop(request, id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    coop_sous_sections = Sous_Section.objects.all().filter(section__cooperative_id=cooperative)
    context = {
        'cooperative': cooperative,
        'coop_sous_sections': coop_sous_sections,
    }
    return render(request, 'chocolatiers/Coop/coop_sous_sections.html', context)

def prod_coop(request, id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    coop_producteurs = Producteur.objects.all().filter(cooperative_id=cooperative)
    # coop_parcelles = Parcelle.objects.all().filter(producteur__section__cooperative_id=cooperative)
    context = {
        'cooperative': cooperative,
        'coop_producteurs': coop_producteurs,
    }
    return render(request, 'chocolatiers/Coop/coop_producteurs.html', context)

def parcelle_coop(request, id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    # coop_producteurs = Producteur.objects.all().filter(cooperative_id=cooperative)
    coop_parcelles = Parcelle.objects.all().filter(producteur__section__cooperative_id=cooperative)
    context = {
        'cooperative': cooperative,
        'coop_parcelles' : coop_parcelles,
    }
    return render(request, 'chocolatiers/Coop/coop_parcelle.html', context)

def planting_coop(request, id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    # coop_producteurs = Producteur.objects.all().filter(cooperative_id=cooperative)
    coop_plants = Planting.objects.all().filter(parcelle__producteur__cooperative_id=cooperative)
    context = {
        'cooperative': cooperative,
        'coop_plants' : coop_plants,
    }
    return render(request, 'chocolatiers/Coop/coop_plantings.html', context)

def projet(request):
    client = Client.objects.get(user_id=request.user.id)
    projets = Projet.objects.all().filter(client_id=client)
    context = {
        'client': client,
        'projets': projets,
    }
    return render(request, 'chocolatiers/projets.html', context)

def detail_proj(request, id=None):
    client = Client.objects.get(user_id=request.user.id)
    instance = get_object_or_404(Projet, id=id)
    pepinieres = Pepiniere.objects.all().filter(projet__client_id=client)
    nb_formations = Formation.objects.all().filter(projet_id=instance).count()
    # producteurs_proj = Parcelle.objects.all().filter(projet_id=instance).count()
    # parcelles = Parcelle.objects.all().filter(projet_id=instance)
    #     # parcelles = Parcelle.objects.all().filter(projet_id=instance)
    #     # nb_parcelles_proj = Parcelle.objects.all().filter(projet_id=instance).count()
    #     # plants = Planting.objects.all().filter(parcelle__projet_id=instance)
    #     # nb_plants_proj = Planting.objects.all().filter(parcelle__projet_id = instance).count()
    #     # superficie_proj = Parcelle.objects.all().filter(projet_id=instance).aggregate(total=Sum('superficie'))['total']
    context = {
        'instance': instance,
        # 'parcelles':parcelles,
        # 'nb_parcelles_proj':nb_parcelles_proj,
        # 'nb_plants_proj':nb_plants_proj,
        # 'plants':plants,
        # 'superficie_proj':superficie_proj,
        'pepinieres':pepinieres,
        'nb_formations':nb_formations,
    }
    return render(request, 'chocolatiers/projet.html', context)

def formations(request, id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    coop_formations = Formation.objects.all().filter(cooperative_id=cooperative)
    context = {
        'cooperative': cooperative,
        'coop_formations': coop_formations,
    }
    return render(request, 'chocolatiers/Coop/coop_formations.html', context)

def detail_formation(request, id=None, _id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    instance = get_object_or_404(Formation, id=_id)
    # instance = Formation.objects.all().filter(cooperative_id=cooperative)
    participants = Detail_Formation.objects.all().filter(formation_id=instance)
    # participants = Producteur.objects.all().filter(cooperative_id=cooperative)
    context = {
        'cooperative':cooperative,
        'instance':instance,
        'participants':participants,
        # 'detailFormation':detailFormation,
        # 'participants': participants,
    }
    return render(request, 'chocolatiers/Coop/detail_formation1.html', context)

def localisation(request):
    parcelles = Parcelle.objects.all()
    context = {
        'parcelles' : parcelles
    }
    return render(request, 'cooperatives/carte.html', context)

def localisation_coop(request, id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    # coop_producteurs = Producteur.objects.all().filter(cooperative_id=cooperative)
    points_coop = Parcelle.objects.all().filter(producteur__section__cooperative_id=cooperative)
    context = {
        'points_coop' : points_coop
    }
    return render(request, 'carte1.html', context)

def site_pepinieres(request):
    pepinieres = Pepiniere.objects.all()
    pepinieres_count = pepinieres.count()
    context = {
        'pepinieres': pepinieres,
        'parcelle_count': pepinieres_count,
    }
    return render(request, 'cooperatives/carte_pepinieres.html', context)

def coop_pepiniere(request, id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    pepinieres = Pepiniere.objects.all().filter(cooperative_id=cooperative)
    context = {
        'pepinieres' : pepinieres
    }
    return render(request, 'cooperatives/carte_pepinieres.html', context)

def pepiniere(request, id=None):
    client = Client.objects.get(user_id=request.user.id)
    cooperative = get_object_or_404(Cooperative, id=id)
    pepinieres = Pepiniere.objects.all().filter(cooperative_id=cooperative)
    context = {
        'cooperative': cooperative,
        'pepinieres': pepinieres,
    }
    return render(request, 'client/pepinieres.html', context)

#Statistiques Charts

def Stats_semences(request):
    querysets = Semence_Pepiniere.objects.values("pepiniere__cooperative__sigle").annotate(qte_recu=Sum('qte_recu'))
    labels = []
    data = []
    for stat in querysets:
        labels.append(stat['pepiniere__cooperative__sigle'])
        data.append(stat['qte_recu'])

    return JsonResponse(data= {
        'labels':labels,
        'data':data,
    })

def Production_plan(request):
    querysets = Semence_Pepiniere.objects.values("pepiniere__cooperative__sigle").annotate(production=Sum('production'))
    labels = []
    data = []
    for stat in querysets:
        labels.append(stat['pepiniere__cooperative__sigle'])
        data.append(stat['production'])

    return JsonResponse(data= {
        'labels':labels,
        'data':data,
    })

def Stats_coop(request):
    querysets = Detail_Retrait_plant.objects.values("retait__pepiniere__cooperative__sigle").annotate(plant_retire=Sum('plant_retire'))
    labels = []
    data = []
    for stat in querysets:
        labels.append(stat['retait__pepiniere__cooperative__sigle'])
        data.append(stat['plant_retire'])

    return JsonResponse(data= {
        'labels':labels,
        'data':data,
    })

def plants_coop(request, id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    querysets = Detail_Retrait_plant.objects.values("espece__libelle").filter(retait__pepiniere__cooperative_id=cooperative).annotate(plant_retire=Sum('plant_retire'))
    labels = []
    data = []
    for stat in querysets:
        labels.append(stat['espece__libelle'])
        data.append(stat['plant_retire'])

    return JsonResponse(data= {
        'labels':labels,
        'data':data,
    })

def semences_coop(request, id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    semences = Semence_Pepiniere.objects.values("espece_recu__libelle").filter(pepiniere__cooperative_id=cooperative).annotate(qte_recu=Sum('qte_recu'))
    labels = []
    data = []
    for stat in semences:
        labels.append(stat['espece_recu__libelle'])
        data.append(stat['qte_recu'])

    return JsonResponse(data= {
        'labels':labels,
        'data':data,
    })

#------------------------------------------------------------------------------------#
# Export to Excel

def export_prod_xls(request, id=None):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="producteurs.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Producteurs')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['COOPERATIVE' ,'CODE', 'TYPE', 'SECTION', 'GENRE', 'NOM', 'PRENOMS', 'CONTACTS', 'LOCALITE']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    cooperative = get_object_or_404(Cooperative, id=id)
    rows = Producteur.objects.all().filter(cooperative_id=cooperative.id).values_list(
        'cooperative__sigle',
        'code',
        'type_producteur',
        'section__libelle',
        'genre',
        'nom',
        'prenoms',
        'contacts',
        'localite',
    )
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def export_parcelle_xls(request, id=None):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Parcelles.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Parcelles')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['COOPERATIVE', 'CODE', 'P.NOM', 'P.PRENOMS', 'CERTIFI', 'CULTURE', 'SUPER', 'LONG', 'LAT', 'SECTION']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    cooperative = get_object_or_404(Cooperative, id=id)
    rows = Parcelle.objects.all().filter(producteur__cooperative_id=cooperative.id).values_list(
        'producteur__cooperative__sigle',
        'code',
        'producteur__nom',
        'producteur__prenoms',
        'certification',
        'culture',
        'superficie',
        'longitude',
        'latitude',
        'sous_section__section__libelle',
    )
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def export_formation_xls(request, id=None):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Formations.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Formations')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['COOPERATIVE', 'PROJET', 'FORMATEUR', 'INTITULE', 'DEBUT', 'FIN']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    cooperative = get_object_or_404(Cooperative, id=id)
    # format2 = xlwt.Workbook({'num_format': 'dd/mm/yy'})
    rows = Formation.objects.all().filter(cooperative_id=cooperative.id).values_list(
        'cooperative__sigle',
        'projet__titre',
        'formateur',
        'libelle',
        'debut',
        'fin',
    )
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            if isinstance(row[col_num], datetime.datetime):
                DEBUT = row[col_num].strftime('%d/%m/%Y')
                FIN = row[col_num].strftime('%d/%m/%Y')
                ws.write(row_num, col_num, DEBUT, FIN, font_style)
            else:
                ws.write(row_num, col_num, row[col_num], font_style)
            # ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def export_plant_xls(request, id=None):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Planting.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Plants')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['COOPERATIVE', 'P.CODE', 'P.NOM', 'P.PRENOMS', 'PARCELLE', 'ESPECE', 'NOMBRE', 'DATE']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    cooperative = get_object_or_404(Cooperative, id=id)
    rows = Planting.objects.all().filter(parcelle__propietaire__cooperative_id=cooperative.id).values_list(
        'parcelle__producteur__cooperative__sigle',
        'parcelle__propietaire__code',
        'parcelle__propietaire__nom',
        'parcelle__propietaire__prenoms',
        'parcelle__code',
        'espece',
        'nb_plant',
        'date',
    )
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


# Create your views here.
