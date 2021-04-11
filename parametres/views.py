import csv
import datetime
from itertools import product

import xlwt
from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login, get_user_model, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.http import JsonResponse
from rest_framework.generics import ListCreateAPIView, ListAPIView
from xhtml2pdf import pisa

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
    Details_planting,
    Section,
    Sous_Section, Detail_Retrait_plant, Semence_Pepiniere, Formation, Detail_Formation, Pepiniere,
)

from .forms import UserForm, LoginForm
from .serializers import ProducteurSerializer, ParcelleSerializer, PepiniereSerializer, FormationSerializer


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

def index(request, id=None):
    cooperatives = Cooperative.objects.all()
    nb_cooperatives = Cooperative.objects.all().count()
    nb_producteurs = Producteur.objects.all().count()
    nb_parcelles = Parcelle.objects.all().count()
    Superficie = Parcelle.objects.aggregate(total=Sum('superficie'))['total']
    Total_plant = Planting.objects.aggregate(total=Sum('nb_plant'))['total']
    # cooperative = get_object_or_404(Cooperative, id=id)
    # coop_nb_producteurs = Producteur.objects.all().filter(cooperative_id=cooperative).count()
    # coop_parcelles = Parcelle.objects.all().filter(producteur__section__cooperative_id=cooperative)
    # coop_nb_parcelles = Parcelle.objects.all().filter(producteur__section__cooperative_id=cooperative).count()
    # coop_superficie = Parcelle.objects.all().filter(producteur__cooperative_id=cooperative).aggregate(total=Sum('superficie'))['total']
    # plants = Details_planting.objects.all().filter(planting__parcelle__producteur__cooperative_id=cooperative).order_by('-espece')
    # coop_plants_total = Planting.objects.all().filter(parcelle__producteur__cooperative_id=cooperative).aggregate(total=Sum('nb_plant'))['total']

    context = {
        'cooperatives':cooperatives,
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

def detail_coop(request, id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    coop_producteurs = Producteur.objects.all().filter(section__cooperative_id=cooperative)
    coop_nb_producteurs = Producteur.objects.all().filter(cooperative_id=cooperative).count()
    nb_formations = Formation.objects.all().filter(cooperative_id=cooperative).count()
    coop_parcelles = Parcelle.objects.all().filter(producteur__section__cooperative_id=cooperative)
    coop_nb_parcelles = Parcelle.objects.all().filter(producteur__section__cooperative_id=cooperative).count()
    coop_superficie = Parcelle.objects.all().filter(producteur__cooperative_id=cooperative).aggregate(total=Sum('superficie'))['total']
    plants = Details_planting.objects.values("espece__libelle").filter(planting__parcelle__producteur__cooperative_id=cooperative).annotate(plante=Sum('plante'))
    coop_plants_total = Planting.objects.all().filter(parcelle__producteur__cooperative_id=cooperative).aggregate(total=Sum('nb_plant'))['total']

    context = {
        'cooperative': cooperative,
        'coop_nb_producteurs': coop_nb_producteurs,
        'coop_nb_parcelles': coop_nb_parcelles,
        'coop_superficie': coop_superficie,
        'nb_formations': nb_formations,
        'plants': plants,
        'coop_plants_total': coop_plants_total,
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
    coop_producteurs = Producteur.objects.all().filter(cooperative_id=cooperative).order_by("-update_le")
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

def planting_coop(request, id=None):
    cooperative = get_object_or_404(Cooperative, id=id)
    # coop_producteurs = Producteur.objects.all().filter(cooperative_id=cooperative)
    coop_plants = Planting.objects.all().filter(parcelle__producteur__cooperative_id=cooperative)
    context = {
        'cooperative': cooperative,
        'coop_plants' : coop_plants,
    }
    return render(request, 'Coop/coop_plantings.html', context)

def projet(request):
    projets = Projet.objects.all()
    context = {
        'projets': projets,
    }
    return render(request, 'projets.html', context)

def detail_proj(request, id=None):
    instance = get_object_or_404(Projet, id=id)
    # producteurs_proj = Parcelle.objects.all().filter(projet_id=instance).count()
 #   parcelles = Planting.objects.all().filter(projet_id=instance)
    # parcelles = Planting.objects.all().filter(projet_id=instance)
    #nb_parcelles_proj = Planting.objects.all().filter(projet_id=instance).count()
 #   plants = Planting.objects.all().filter(projet_id=instance)
    #nb_plants_proj = Planting.objects.all().filter(projet_id = instance).count()
    # superficie_proj = Planting.objects.all(parcelle).filter().aggregate(total=Sum('superficie'))['total']
    context = {
        'instance': instance,
        # 'parcelles':parcelles,
        # 'nb_parcelles_proj':nb_parcelles_proj,
        #'nb_plants_proj':nb_plants_proj,
        #'plants':plants,
        # 'superficie_proj':superficie_proj,
        # 'producteurs_proj':producteurs_proj,
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
    participants = Detail_Formation.objects.all().filter(formation_id=instance)
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

class PepiniereJson(TemplateView):
    template_name = 'pepinieres_json.html'
    # template_name = 'parametres/parcelles.html'

class ParcelleApiView(ListAPIView):
    queryset = Parcelle.objects.all()
    serializer_class = ParcelleSerializer

class FormationApiView(ListCreateAPIView):
    queryset = Formation.objects.all()
    serializer_class = FormationSerializer

# Create your views here.
