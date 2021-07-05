import csv
import datetime
from itertools import product

import folium
import pandas as pd
import xlwt
from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login, get_user_model, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template.loader import get_template
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from django_pandas.io import read_frame
from folium import plugins, raster_layers
from folium.plugins import MarkerCluster
from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.views import APIView
from xhtml2pdf import pisa

from communaute.models import Communaute
from .models import (
    Sous_Prefecture,
    Origine,
    Prime,
    Projet,
    # Pepiniere,
    Activite,
    Region,
    # Campagne, Detail_Pepiniere, Detail_Retrait,
    # Formations,
)

from cooperatives.models import (
    Cooperative,
    Producteur,
    Parcelle,
    Planting,
    # Details_planting,
    Section,
    Sous_Section, Detail_Retrait_plant, Semence_Pepiniere, Formation, Detail_Formation, Pepiniere, DetailPlanting,
    Monitoring,
)

from .forms import UserForm, LoginForm, ProjetForm
from .serializers import ProducteurSerializer, ParcelleSerializer, PepiniereSerializer, FormationSerializer, \
    DetailPlantingSerializer


def connexion(request):
    login_form = LoginForm(request.POST or None)
    if login_form.is_valid():
        username = login_form.cleaned_data.get("username")
        password = login_form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user != None:
            #utilisateur valide et actif(is_active=True)
            #"request.user == user"
            dj_login(request, user)
            group = request.user.groups.filter(user=request.user)[0]
            if group.name == "COOPERATIVES":
                messages.success(request, "Bienvenue : {}".format(username))
                return HttpResponseRedirect(reverse('cooperatives:dashboard'))
            if group.name == "COMMUNAUTES":
                messages.success(request, "Bienvenue : {}".format(username))
                return HttpResponseRedirect(reverse('communautes:dashboard'))
            elif group.name == "ADMIN":
                messages.success(request, "Bienvenue : {}".format(username))
                return HttpResponseRedirect(reverse('accueil'))
            elif group.name == "CLIENTS":
                messages.success(request, "Bienvenue : {}".format(username))
                return HttpResponseRedirect(reverse('clients:dashboard'))
            else:
                messages.error(request, "Désolé vous n'estes pas encore enregistrer dans notre Sytème")
                return HttpResponseRedirect(reverse('connexion'))
        else:
            request.session['invalid_user'] = 1 # 1 == True
            messages.error(request, "Echec de Connexion, Assurez-vous d'avoir entrer le bon login et le bon Mot de Passe SVP !")
            return HttpResponseRedirect(reverse('connexion'))
    return render(request, 'parametres/login.html', {'login_form': login_form})

def loggout(request):
    logout(request)
    return HttpResponseRedirect(reverse('connexion'))

def index(request):
    cooperatives = Cooperative.objects.all()
    communautes = Communaute.objects.all()
    nb_communautes = Communaute.objects.all().count()
    nb_cooperatives = Cooperative.objects.all().count()
    nb_producteurs = Producteur.objects.all().count()
    nb_parcelles = Parcelle.objects.all().count()
    Superficie = Parcelle.objects.aggregate(total=Sum('superficie'))['total']
    Total_plant = Planting.objects.aggregate(total=Sum('plant_total'))['total']
    # plantings = Planting.objects.values("espece__libelle").filter(parcelle__producteur__cooperative_id=cooperative).annotate(plante=Sum('plant_recus'))

    context = {
        'cooperatives':cooperatives,
        'communautes':communautes,
        'nb_cooperatives': nb_cooperatives,
        'nb_producteurs': nb_producteurs,
        'nb_parcelles': nb_parcelles,
        'Superficie': Superficie,
        'Total_plant': Total_plant,
        # 'coop_nb_producteurs': coop_nb_producteurs,
        # 'coop_nb_parcelles': coop_nb_parcelles,
        # 'coop_superficie': coop_superficie,
        # 'plants': plants,
        # 'coop_plants_total': coop_plants_total,
    }
    return render(request, 'index.html', context)

def Stats_coop(request):
    querysets = Detail_Retrait_plant.objects.values("retait__pepiniere__cooperative__sigle").annotate(plant_recus=Sum('plant_recus'))
    labels = []
    data = []
    for stat in querysets:
        labels.append(stat['retait__pepiniere__cooperative__sigle'])
        data.append(stat['plant_recus'])

    return JsonResponse(data= {
        'labels':labels,
        'data':data,
    })

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

def Plantings(request):
    querysets = Planting.objects.values("parcelle__producteur__cooperative__sigle").annotate(plant_recus=Sum('plant_recus'))
    labels = []
    data = []
    for stat in querysets:
        labels.append(stat['parcelle__producteur__cooperative__sigle'])
        data.append(stat['plant_recus'])

    return JsonResponse(data= {
        'labels':labels,
        'data':data,
    })

def detailPlantings(request):
    querysets = DetailPlanting.objects.values("espece__libelle").annotate(nb_plante=Sum('nb_plante'))
    labels = []
    data = []
    for stat in querysets:
        labels.append(stat['espece__libelle'])
        data.append(stat['nb_plante'])

    return JsonResponse(data= {
        'labels':labels,
        'data':data,
    })


# def coopProducteur(request):
#     nb_prod_coop =
#     querysets = Producteur.objects.values("cooperative_id").annotate(nb_plante=Sum('nb_plante'))
#     labels = []
#     data = []
#     for stat in querysets:
#         labels.append(stat['espece__libelle'])
#         data.append(stat['nb_plante'])
#
#     return JsonResponse(data= {
#         'labels':labels,
#         'data':data,
#     })

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

def detail_coop(request, id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    # coop_nb_producteurs =
    section = Section.objects.all().filter(cooperative_id=cooperative)
    # section_prod = Producteur.objects.all().filter(section_id__in=section).count()
    prod_section = Producteur.objects.all().filter(section_id__in=section).count()
    coop_nb_producteurs = Producteur.objects.filter(cooperative_id=cooperative).count()
    nb_formations = Formation.objects.all().filter(cooperative_id=cooperative).count()
    parcelles_section = Parcelle.objects.filter(producteur__section_id__in=section).count()
    coop_nb_parcelles = Parcelle.objects.filter(producteur__section__cooperative_id=cooperative).count()
    coop_superficie = Parcelle.objects.all().filter(producteur__cooperative_id=cooperative).aggregate(total=Sum('superficie'))['total']
    section_superf = Parcelle.objects.filter(producteur__section_id__in=section).aggregate(total=Sum('superficie'))['total']
    section_plating = Planting.objects.filter(parcelle__producteur__section_id__in=section).aggregate(total=Sum('plant_recus'))['total']
    # plantings = Planting.objects.values("espece__libelle").filter(parcelle__producteur__cooperative_id=cooperative).annotate(plante=Sum('plant_recus'))
    coop_plants_total = DetailPlanting.objects.filter(planting__parcelle__producteur__cooperative_id=cooperative).aggregate(total=Sum('nb_plante'))['total']

    context = {
        'cooperative': cooperative,
        'coop_nb_producteurs': coop_nb_producteurs,
        'coop_nb_parcelles': coop_nb_parcelles,
        'coop_superficie': coop_superficie,
        'nb_formations': nb_formations,
        'section': section,
        'prod_section': prod_section,
        'parcelles_section': parcelles_section,
        # 'plantings': plantings,
        'coop_plants_total': coop_plants_total,
        'section_superf': section_superf,
        'section_plating': section_plating,
        # 'labels': labels,
        # 'data': data,
    }
    return render(request, 'Coop/cooperative.html', context)

def section_coop(request, id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    coop_sections = Section.objects.all().filter(cooperative_id=cooperative)
    context = {
        'cooperative': cooperative,
        'coop_sections': coop_sections,
    }
    return render(request, 'Coop/coop_sections.html', context)

def sous_section_coop(request):
    cooperative = get_object_or_404(Cooperative, id=id)
    coop_sous_sections = Sous_Section.objects.all().filter(section__cooperative_id=cooperative)
    context = {
        'cooperative': cooperative,
        'coop_sous_sections': coop_sous_sections,
    }
    return render(request, 'Coop/coop_sous_sections.html', context)

def prod_coop(request, id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    coop_producteurs = Producteur.objects.all().filter(cooperative_id=cooperative) #.order_by("-update_le")
    # coop_parcelles = Parcelle.objects.all().filter(producteur__section__cooperative_id=cooperative)
    context = {
        'cooperative': cooperative,
        'coop_producteurs' : coop_producteurs,
    }
    return render(request, 'Coop/coop_producteurs.html', context)

def stat_prod_coop(request, id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    # nb_producteurs = Producteur.objects.all().filter(cooperative_id=cooperative).count()
    querysets = Producteur.objects.values("cooperative__sigle").filter(cooperative_id=cooperative).annotate(tot_prod_coop=Sum('tot_prod_coop'))
    labels = []
    data = []
    for stat in querysets:
        labels.append(stat['cooperative__sigle'])
        data.append(stat['tot_prod_coop'])

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

def plantings_coop(request, id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    querysets = DetailPlanting.objects.filter(planting__parcelle__producteur__cooperative_id=cooperative).values("espece__libelle").annotate(nb_plante=Sum('nb_plante'))
    labels = []
    data = []
    for stat in querysets:
        labels.append(stat['espece__libelle'])
        data.append(stat['nb_plante'])

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

def parcelle_coop(request, id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    # coop_producteurs = Producteur.objects.all().filter(cooperative_id=cooperative)
    coop_parcelles = Parcelle.objects.all().filter(producteur__section__cooperative_id=cooperative)
    context = {
        'cooperative': cooperative,
        'coop_parcelles' : coop_parcelles,
    }
    return render(request, 'Coop/coop_parcelle.html', context)

def planting_coop(request, id=None, p_id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    # planting = Planting.objects.filter(parcelle__producteur__cooperative_id=cooperative)
    plantings = DetailPlanting.objects.filter(planting__parcelle__producteur__cooperative_id=cooperative)
    context = {
        'cooperative': cooperative,
        'plantings' : plantings,
    }
    return render(request, 'cooperatives/planting_coop_update.html', context)


def detail_planting(request, id=None, _id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    instance = get_object_or_404(Planting, id=_id)
    # instance = Planting.objects.get(id=_id)
    Details_Planting = DetailPlanting.objects.filter(planting_id=instance)
    monitorings = Monitoring.objects.filter(planting_id=instance)

    context = {
        'cooperative':cooperative,
        'instance':instance,
        'Details_Planting':Details_Planting,
        'monitorings':monitorings,
    }
    return render(request, 'Coop/detail_planting.html', context)

def projet(request):
    projets = Projet.objects.all()
    form = ProjetForm()
    if request.method == 'POST':
        form = ProjetForm(request.POST)
        if form.is_valid():
            projet = form.save(commit=False)
            projet = projet.save()
        messages.success(request, "Projet Ajoutée avec succès")
        return HttpResponseRedirect(reverse('projets'))
    context = {
        'projets': projets,
        'form': form,
    }
    return render(request, 'projets.html', context)

def update_projet(request, id=None):
    instance = get_object_or_404(Projet, id=id)
    form = ProjetForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.info(request, "Projet Modifié Avec Succès", extra_tags='html_safe')
        return HttpResponseRedirect(reverse('projets'))
    context = {
        'instance':instance,
        'form':form,
    }
    return render(request, "projet_edit.html", context)

def delete_projet(request, id=None):
    item = get_object_or_404(Projet, id=id)
    if request.method == "POST":
        item.delete()
        messages.error(request, "Projet Supprimée Avec Succès")
        return redirect('projets')
    context = {
        # 'pepiniere': pepiniere,
        'item': item,
    }
    return render(request, 'projet_delete.html', context)
    # item.delete()
    # messages.success(request, "Section Supprimer avec Succès")
    # return HttpResponseRedirect(reverse('cooperatives:section'))

def detail_proj(request, id=None):
    instance = get_object_or_404(Projet, id=id)
    # cooperatives = Cooperative.objects.filter(cooperative__projet__i).count()
    producteurs_proj = Producteur.objects.filter(cooperative__projet=instance).count()
    parcelles = Parcelle.objects.filter(producteur__cooperative__projet=instance)
    # parcelles = Planting.objects.all().filter(projet_id=instance)
    nb_parcelles_proj = Parcelle.objects.filter(producteur__cooperative__projet=instance).count()
    plants = DetailPlanting.objects.filter(planting__projet_id=instance).aggregate(total=Sum('nb_plante'))['total']
    #nb_plants_proj = Planting.objects.all().filter(projet_id = instance).count()
    superficie_proj = Parcelle.objects.filter(producteur__cooperative__projet=instance).aggregate(total=Sum('superficie'))['total']

    # print(superficie_proj)
    context = {
        'instance': instance,
        'parcelles': parcelles,
        # 'cooperatives': cooperatives,
        'plants':plants,
        # 'parcelles':plants,
        'nb_parcelles_proj':nb_parcelles_proj,
        #'nb_plants_proj':nb_plants_proj,
        #'plants':plants,
        'superficie_proj':superficie_proj,
        'producteurs_proj':producteurs_proj,
    }
    return render(request, 'projet.html', context)

def formations(request, id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    coop_formations = Formation.objects.all().filter(cooperative_id=cooperative)
    context = {
        'cooperative': cooperative,
        'coop_formations': coop_formations,
    }
    return render(request, 'Coop/coop_formations.html', context)

def detail_formation(request, id=None, _id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    instance = get_object_or_404(Formation, id=_id)
    # instance = Formation.objects.all().filter(cooperative_id=cooperative)
    participants = Detail_Formation.objects.filter(formation_id=instance)
    # participants = Producteur.objects.all().filter(cooperative_id=cooperative)
    context = {
        'cooperative':cooperative,
        'instance':instance,
        'participants':participants,
        # 'detailFormation':detailFormation,
        # 'participants': participants,
    }
    return render(request, 'Coop/detail_formation.html', context)

def pepiniere(request):
    pepinieres = Pepiniere.objects.all()
    context = {
        'pepinieres': pepinieres,
    }
    return render(request, 'pepinieres.html', context)

def pepiniere_coop(request, id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    pepinieres = Pepiniere.objects.all().filter(cooperative_id=cooperative)
    context = {
        'cooperative': cooperative,
        'pepinieres': pepinieres,
        # 'details_retraits': details_retraits,
    }
    return render(request, 'pepinieres.html', context)

def localisation(request):
    parcelles = Parcelle.objects.all()
    parcelle_count = parcelles.count()
    context = {
        'parcelles' : parcelles,
        'parcelle_count':parcelle_count,
        # 'parcelle_count':parcelle_count
    }
    return render(request, 'carte_update.html', context)

def localisation_coop(request, id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    # coop_producteurs = Producteur.objects.all().filter(cooperative_id=cooperative)
    parcelles = Parcelle.objects.filter(producteur__section__cooperative_id=cooperative)
    context = {
        'parcelles' : parcelles
    }
    return render(request, 'cooperatives/carte_update.html', context)

def plantingcoop(request, id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    # coop_producteurs = Producteur.objects.all().filter(cooperative_id=cooperative)
    plantings = Planting.objects.filter(parcelle__producteur__cooperative_id=cooperative)
    context = {
        'plantings' : plantings
    }
    return render(request, 'cooperatives/planting_coop_update.html', context)

def site_pepinieres(request):
    pepinieres = Pepiniere.objects.all()
    pepinieres_count = pepinieres.count()
    context = {
        'pepinieres': pepinieres,
        'parcelle_count': pepinieres_count,
        # 'parcelle_count':parcelle_count
    }
    return render(request, 'cooperatives/carte_pepinieres.html', context)

def coop_pepiniere(request, id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    pepinieres = Pepiniere.objects.all().filter(cooperative_id=cooperative)
    context = {
        'pepinieres' : pepinieres
    }
    return render(request, 'cooperatives/carte_pepinieres.html', context)
#----------------------------------------------------------#
#EXPORT TO EXECL
#----------------------------------------------------------#
def export_producteur_csv(request, id=None):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="producteurs.csv"'

    writer = csv.writer(response)
    writer.writerow(['CODE', 'TYPE', 'SECTION', 'GENRE', 'NOM', 'PRENOMS', 'CONTACTS'])
    cooperative = get_object_or_404(Cooperative, id=id)
    producteurs = Producteur.objects.all().filter(cooperative_id=cooperative.id).values_list(
        'code',
        'type_producteur',
        'section__libelle',
        'genre',
        'nom',
        'prenoms',
        'contacts',
    )
    for p in producteurs:
        writer.writerow(p)

    return response
def export_prod_xls(request, id=None):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="producteurs.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Producteurs')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['COOPERATIVE', 'SECTION','LOCALITE', 'CODE', 'TYPE',  'GENRE', 'NOM', 'PRENOMS', 'CONTACTS']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    cooperative = get_object_or_404(Cooperative, id=id)
    rows = Producteur.objects.all().filter(cooperative_id=cooperative.id).values_list(
        'cooperative__sigle',
        'section__libelle',
        'localite',
        'code',
        'type_producteur',
        'genre',
        'nom',
        'prenoms',
        'contacts',
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

    columns = ['COOPERATIVE','SECTION', 'CODE', 'NOM', 'PRENOMS', 'CERTIF', 'CULTURE', 'SUPER', 'LONG', 'LAT']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    cooperative = get_object_or_404(Cooperative, id=id)
    rows = Parcelle.objects.all().filter(producteur__cooperative_id=cooperative.id).values_list(
        'producteur__cooperative__sigle',
        'producteur__section__libelle',
        'code',
        'producteur__nom',
        'producteur__prenoms',
        'certification',
        'culture',
        'superficie',
        'longitude',
        'latitude',
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

#Export To PDF
def export_prods_to_pdf(request, id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    producteurs = Producteur.objects.all().filter(cooperative_id=cooperative)
    template_path = 'cooperatives/prods_pdf.html'
    context = {
        'cooperative':cooperative,
        'producteurs':producteurs,
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/csv')
    #response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Producteurs.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('Une Erreure est Survenue, Réessayer SVP... <pre>' + html + '</pre>')
    return response

def export_parcelles_to_pdf(request, id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    parcelles = Parcelle.objects.all().filter(producteur__cooperative_id=cooperative)
    template_path = 'cooperatives/parcelles_pdf.html'
    context = {
        'cooperative':cooperative,
        'parcelles':parcelles,
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/csv')
    #response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Parcelles.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('Une Erreure est Survenue, Réessayer SVP... <pre>' + html + '</pre>')
    return response

import json

from django.core.serializers import serialize
from django.views.generic.base import TemplateView

from cooperatives.models import Parcelle


class ParcellesMapView(TemplateView):
    """Markers map view."""

    template_name = "map.html"

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["parcelles"] = json.loads(serialize("geojson", Parcelle.objects.all()))
        return context

class ProducteurApiView(ListAPIView):
    queryset = Producteur.objects.all()
    serializer_class = ProducteurSerializer

class ParcelleJson(TemplateView):
    template_name = 'new_map.html'
    # template_name = 'parametres/parcelles.html'

class PepiniereApiView(ListAPIView):
    queryset = Pepiniere.objects.all()
    serializer_class = PepiniereSerializer

class DetailPlantingJson(TemplateView):
    template_name = 'map_plantings.html'
    # template_name = 'parametres/parcelles.html'

class DetailPlantingApiView(ListAPIView):
    queryset = DetailPlanting.objects.all()
    serializer_class = DetailPlantingSerializer


class PepiniereJson(TemplateView):
    template_name = 'pepinieres_json.html'
    # template_name = 'parametres/parcelles.html'

class ParcelleApiView(ListAPIView):
    queryset = Parcelle.objects.all()
    p_count = queryset.count()
    # print(p_count)
    serializer_class = ParcelleSerializer

class FormationApiView(ListCreateAPIView):
    queryset = Formation.objects.all()
    serializer_class = FormationSerializer

# Django rest framework Detail view
# class CooperativeDetail(APIView):
#     def get_object(self, category_slug):
#         try:
#             return Category.objects.get(slug=category_slug)
#         except Product.DoesNotExist:
#             raise Http404
#
#     def get(self, request, category_slug, format=None):
#         category = self.get_object(category_slug)
#         serializer = CategorySerializer(category)
#         return Response(serializer.data)
# class ParcelleCooperativeApi(ListAPIView, ):
#     # cooperative = get_object_or_404(Cooperative, id=id)
#     # queryset = Parcelle.objects.all().filter(producteur__section__cooperative_id=cooperative)
#     # serializer_class = ParcelleSerializer
#     # filter_backends = [DjangoFilterBackend]
#     # filterset_fields = ['cooperative']
#     serializer_class = ParcelleSerializer
#     def get_queryset(self, id):
#         cooperative = get_object_or_404(Cooperative, id=id)
#         user = self.request.user
#         return Parcelle.objects.filter(producteur__section__cooperative_id=cooperative)
#
# class ReportFieldDetail(APIView):
#     cooperative = get_object_or_404(Cooperative, id=id)
#     def get_object(self, cooperative):
#         try:
#             # return ReportField.objects.get(pk=pk)
#             return Parcelle.objects.filter(producteur__section__cooperative_id=cooperative)
#         except Parcelle.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         report_field = self.get_object(pk)
#         serialized_report_field = ReportFieldSerializers(report_field)
#         return Response(serialized_report_field.data)
# Create your views here.

def folium_map(request):
    # cooperative = Cooperative.objects.get(user_id=request.user.id)
    # m = folium.Map(
    #     location=[5.34939, -4.01705], zoom_start=1,
    #     tiles=None, crs='EPSG3857',
    #     control_scale=True, attributionControl=False,
    #     # max_zoom=22,min_zoom=2,
    #     min_lot=-179,
    #     max_lot=179, min_lat=-65,
    #     max_lat=179, max_bounds=True
    # )
    m = folium.Map(
        location=[5.34939, -4.01705],zoom_start=6,
        # tiles="CartoDB Dark_Matter",

    )
    marker_cluster = MarkerCluster().add_to(m)

    map1 = raster_layers.TileLayer(tiles="CartoDB Dark_Matter").add_to(m)
    map2 = raster_layers.TileLayer(tiles="CartoDB Positron").add_to(m)
    map3 = raster_layers.TileLayer(tiles="Stamen Terrain").add_to(m)
    map4 = raster_layers.TileLayer(tiles="Stamen Toner").add_to(m)
    map5 = raster_layers.TileLayer(tiles="Stamen Watercolor").add_to(m)
    folium.LayerControl().add_to(m)
    parcelles = Parcelle.objects.all()
    # df = pd.DataFrame(
    #     data=parcelles,
    #     columns=[
    #             'code',
    #             'producteur',
    #             'sous_section',
    #             'acquisition',
    #             'latitude',
    #             'longitude',
    #             'superficie',
    #             'culture',
    #             'certification',
    #         ]
    # )

    # html = df.to_html(
    #     classes="table table-striped table-hover table-condensed table-responsive"
    # )
    #
    # for (index, row) in df.iterrows():
    #     popup = folium.Popup(html)
    #
    #     folium.Marker([
    #         row.loc['latitude'],
    #         row.loc['longitude']],
    #         popup=popup,
    #         icon = folium.Icon(color="green", icon="ok-sign"),
    #     ).add_to(marker_cluster)
    #     plugins.Fullscreen().add_to(m)
    #     # plugins.MarkerCluster.add_to()
    #     m = m._repr_html_()

    df = read_frame(parcelles,
        fieldnames=
        [
            'code',
            'producteur',
            'latitude',
            'longitude',
        ]
    )
    html = df.to_html(
        classes="table table-striped table-hover table-condensed table-responsive"
    )

    # print(df)
    for (index, row) in df.iterrows():
        folium.Marker(
            location=[
                row.loc['latitude'],
                row.loc['longitude']
            ],
            popup=folium.Popup(html),
            # popup=[
            #     # row.loc['producteur.cooperative'],
            #     # '<strong>' + row_values['code'] + '</strong>',
            #     #     '<strong>' + row_values['code'] + '</strong>',
            #     # row.loc['code'],
            #     row.loc['code'],
            #     '<strong>'+row.loc['producteur']+'</strong><br><br>',
            #     '<strong>'+row.loc['sous_section']+'</strong><br><br>',
            #     row.loc['acquisition'],
            #     row.loc['culture'],
            #     row.loc['certification'],
            #     row.loc['superficie'],
            # ],
            icon=folium.Icon(color="green", icon="ok-sign"),
        ).add_to(marker_cluster)
    plugins.Fullscreen().add_to(m)
    # plugins.MarkerCluster.add_to()
    m = m._repr_html_()

    context = {
        "m":m
    }
    return render(request, "cooperatives/folium_map.html", context)


def folium_palntings_map(request):
    m = folium.Map(
        location=[5.34939, -4.01705],zoom_start=6,
    )
    marker_cluster = MarkerCluster().add_to(m)

    map1 = raster_layers.TileLayer(tiles="CartoDB Dark_Matter").add_to(m)
    map2 = raster_layers.TileLayer(tiles="CartoDB Positron").add_to(m)
    map3 = raster_layers.TileLayer(tiles="Stamen Terrain").add_to(m)
    map4 = raster_layers.TileLayer(tiles="Stamen Toner").add_to(m)
    map5 = raster_layers.TileLayer(tiles="Stamen Watercolor").add_to(m)
    folium.LayerControl().add_to(m)
    plantings = DetailPlanting.objects.all()
    parcelles = Parcelle.objects.all()

    df1 = read_frame(parcelles,
        fieldnames=
        [
            'code',
            'producteur',
            'latitude',
            'longitude',

        ]
    )
    df = read_frame(plantings,
        fieldnames=
        [
            'planting',
            'espece',
            'nb_plante',
            'add_le'
        ]
    )
    # print(df)
    html = df.to_html(
        classes="table table-striped table-hover table-condensed table-responsive"
    )

    # print(df)
    for (index, row) in df1.iterrows():
        folium.Marker(
            location=[
                row.loc['latitude'],
                row.loc['longitude']
            ],
            popup=folium.Popup(html),
            icon=folium.Icon(color="green", icon="ok-sign"),
        ).add_to(marker_cluster)
    plugins.Fullscreen().add_to(m)
    m = m._repr_html_()

    context = {
        "m":m
    }
    return render(request, "folium_planting_map.html", context)

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

def planting_list(request):
    plantings = Planting.objects.all()
    planting_data = serializers.serialize("json", plantings)
    response = HttpResponse(content=planting_data)
    return response
    # print(response)

def produteur_list(request):
    producteurs = Producteur.objects.all()
    producteur_data = serializers.serialize("json", producteurs)
    response = HttpResponse(content=producteur_data)
    return response
    # print(response)

def parcelles_list(request):
    parcelles = Parcelle.objects.all()
    p_count = parcelles.count()
    # print(p_count)
    parcelle_data = serializers.serialize("json", parcelles)
    response = HttpResponse(content=parcelle_data)
    return response
    # print(response)

def planting_list(request):
    plantings = Planting.objects.all()
    plantings_data = serializers.serialize("json", plantings)
    response = HttpResponse(content=plantings_data)
    return response
    # print(response)

def details_planting_list(request):
    details_plantings = DetailPlanting.objects.all()
    data = serializers.serialize("json", details_plantings)
    response = HttpResponse(content=data)
    return response
    # print(response)