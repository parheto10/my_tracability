import datetime

import datetime

import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
# from django.contrib.gis.serializers import geojson
from django.core.serializers import serialize
from django.core import serializers
from django.http import HttpResponse
from django.db.models import Sum
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
import folium
import json
from django.template.loader import get_template
from django.views.generic import TemplateView
from xhtml2pdf import pisa
from django.views import View
from xlrd.formatting import Format

# Import django Serializer Features #
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from parametres.forms import UserForm
from parametres.models import Projet
from .forms import CoopForm, ProdForm, EditProdForm, ParcelleForm, PlantingForm, SectionForm, Sous_SectionForm, \
    PepiniereForm, SuiviPlantingForm, SemenceForm, RetraitForm, DetailRetraitForm, EditSemenceForm, FormationForm, \
    DetailFormation, EditPepiniereForm, EditFormationForm, EditParcelleForm, Edit_Sous_SectionForm
from .models import Cooperative, Section, Sous_Section, Producteur, Parcelle, Planting, Formation, Detail_Formation, \
    Pepiniere, Semence_Pepiniere, Retrait_plant, Detail_Retrait_plant, Details_planting


def is_cooperative(user):
    return user.groups.filter(name='COOPERATIVES').exists()

#@login_required(login_url='connexion')
#@user_passes_test(is_cooperative)
def cooperative(request, id=None):
    coop = get_object_or_404(Cooperative, pk=id)
    producteurs = Producteur.objects.all().filter(section__cooperative_id= coop)
    nb_producteurs = Producteur.objects.all().filter(section__cooperative_id= coop).count()
    parcelles = Parcelle.objects.all().filter(propietaire__section__cooperative_id=coop)
    nb_parcelles = Parcelle.objects.all().filter(propietaire__section__cooperative_id=coop).count()
    context = {
        "coop": coop,
        'cooperative': cooperative,
        'producteurs': producteurs,
        'nb_producteurs': nb_producteurs,
        'parcelles': parcelles,
        'nb_parcelles': nb_parcelles,
    }
    return render(request, "cooperatives/dashboard.html", context)


def coop_dashboard(request):
    cooperative= Cooperative.objects.get(user_id=request.user.id)
    producteurs = Producteur.objects.all().filter(cooperative_id=cooperative)
    nb_producteurs = Producteur.objects.all().filter(cooperative_id=cooperative).count()
    nb_formations = Formation.objects.all().filter(cooperative_id=cooperative).count()
    parcelles = Parcelle.objects.all().filter(producteur__cooperative_id=cooperative)
    nb_parcelles = Parcelle.objects.all().filter(producteur__cooperative_id=cooperative).count()
    Superficie = Parcelle.objects.all().filter(producteur__cooperative_id=cooperative).aggregate(total=Sum('superficie'))['total']
    Plants = Planting.objects.all().filter(parcelle__producteur__cooperative_id=cooperative).aggregate(total=Sum('nb_plant'))['total']
    # querysets = Detail_Retrait_plant.objects.values("espece__libelle").filter(retait__pepiniere__cooperative_id=cooperative).annotate(plant_retire=Sum('plant_retire'))
    semences = Semence_Pepiniere.objects.values("espece_recu__libelle").filter(pepiniere__cooperative_id=cooperative).annotate(qte_recu=Sum('qte_recu'))

    context={
    'cooperative':cooperative,
    'producteurs': producteurs,
    'nb_formations': nb_formations,
    'nb_producteurs': nb_producteurs,
    'parcelles': parcelles,
    'nb_parcelles': nb_parcelles,
    'Superficie' : Superficie,
    'Plants': Plants,
    # 'labels': labels,
    # 'data': data,
    # 'mylabels': mylabels,
    # 'mydata': mydata,
    }
    return render(request,'cooperatives/dashboard.html',context=context)

def Stats_coop(request):
    cooperative = Cooperative.objects.get(user_id=request.user.id)
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

def Stats_semence(request):
    cooperative = Cooperative.objects.get(user_id=request.user.id)
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

# def prod_section(request):
#     cooperative = Cooperative.objects.get(user_id=request.user.id)
#     semences = Semence_Pepiniere.objects.values("espece_recu__libelle").filter(pepiniere__cooperative_id=cooperative).annotate(qte_recu=Sum('qte_recu'))
#     labels = []
#     data = []
#     for stat in semences:
#         labels.append(stat['espece_recu__libelle'])
#         data.append(stat['qte_recu'])
#
#     return JsonResponse(data= {
#         'labels':labels,
#         'data':data,
#     })

def add_section(request):
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    sections = Section.objects.all().filter(cooperative_id=cooperative)
    form = SectionForm()
    if request.method == 'POST':
        form = SectionForm(request.POST)
        if form.is_valid():
            section = form.save(commit=False)
            section.cooperative_id = cooperative.id
            section = section.save()
            # print()
        messages.success(request, "Section Ajoutée avec succès")
        return HttpResponseRedirect(reverse('cooperatives:section'))
    context = {
        "cooperative": cooperative,
        "sections": sections,
        'form': form,
    }
    return render(request, "cooperatives/sections.html", context)

def update_section(request, id=None):
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    instance = get_object_or_404(Section, id=id)
    form = SectionForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.cooperative_id = cooperative.id
        instance.save()
        messages.success(request, "Section Modifié Avec Succès", extra_tags='html_safe')
        return HttpResponseRedirect(reverse('cooperatives:section'))
    context = {
        'instance' : instance,
        'form' : form,
    }
    return render(request, "cooperatives/section_edit.html", context)

def delete_section(request, id=None):
    item = get_object_or_404(Section, id=id)
    if request.method == "POST":
        item.delete()
        messages.error(request, "Section Supprimée Avec Succès")
        return redirect('cooperatives:section')
    context = {
        # 'pepiniere': pepiniere,
        'item': item,
    }
    return render(request, 'cooperatives/section_delete.html', context)
    # item.delete()
    # messages.success(request, "Section Supprimer avec Succès")
    # return HttpResponseRedirect(reverse('cooperatives:section'))

def add_sous_section(request):
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    sections = Section.objects.all().filter(cooperative_id=cooperative)
    sous_sections = Sous_Section.objects.all().filter(section__cooperative_id=cooperative)
    form = Sous_SectionForm()
    if request.method == 'POST':
        form = Sous_SectionForm(request.POST)
        if form.is_valid():
            sous_section = form.save(commit=False)
            for section in sections:
                sous_section.section_id = section.id
            sous_section = sous_section.save()
            # print()
        messages.success(request, "Sous Section Ajoutée avec succès")
        return HttpResponseRedirect(reverse('cooperatives:sous_sections'))
    context = {
        "cooperative": cooperative,
        "sous_sections": sous_sections,
        "sections": sections,
        'form': form,
    }
    return render(request, "cooperatives/sous_sections.html", context)

def update_sous_section(request, id=None):
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    instance = get_object_or_404(Sous_Section, id=id)
    form = Edit_Sous_SectionForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        # instance.cooperative_id = cooperative.id
        instance.save()
        messages.success(request, "Sous Section Modifié Avec Succès", extra_tags='html_safe')
        return HttpResponseRedirect(reverse('cooperatives:sous_sections'))
    context = {
        'instance' : instance,
        'form' : form,
    }
    return render(request, "cooperatives/sous_section_edit.html", context)

def delete_sous_section(request, id=None):
    item = get_object_or_404(Sous_Section, id=id)
    if request.method == "POST":
        item.delete()
        messages.error(request, "Sous Section Supprimée Avec Succès")
        return redirect('cooperatives:sous_sections')
    context = {
        # 'pepiniere': pepiniere,
        'item': item,
    }
    return render(request, 'cooperatives/sous_section_delete.html', context)

def my_section(request):
    cooperative = request.GET.get("user_id")#Cooperative.objects.get(user_id=request.user.id)
    coop_sections = Section.objects.filter(cooperative_id=cooperative)
    context = {'coop_sections': coop_sections}
    return render(request, 'cooperatives/section.html', context)

def producteurs(request):
    cooperative = request.user.cooperative #Cooperative.objects.get(user_id=request.user.id)
    producteurs = Producteur.objects.all().filter(cooperative_id=cooperative).order_by("-add_le")
    sections = Section.objects.filter(cooperative_id=cooperative)
    sous_sections = Sous_Section.objects.all().filter(section__cooperative_id=cooperative)

    prodForm = ProdForm()
    if request.method == 'POST':
        prodForm = ProdForm(request.POST, request.FILES)
        if prodForm.is_valid():
            producteur = prodForm.save(commit=False)
            producteur.cooperative_id = cooperative.id
            for section in sections:
                producteur.section_id = section.id
            for sous_section in sous_sections:
                producteur.sous_section_id = sous_section.id
            producteur = producteur.save()
            print(producteur)   
        messages.success(request, "Producteur Ajouté avec succès")
        return HttpResponseRedirect(reverse('cooperatives:producteurs'))

    context = {
        "cooperative":cooperative,
        "producteurs": producteurs,
        'prodForm': prodForm,
        'sections':sections,
        'sous_sections':sous_sections,

    }
    return render(request, "cooperatives/producteurs.html", context)

def prod_update(request, code=None):
	instance = get_object_or_404(Producteur, code=code)
	form = EditProdForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Producteur Modifié Avec Succès", extra_tags='html_safe')
		return HttpResponseRedirect(reverse('cooperatives:producteurs'))

	context = {
		"instance": instance,
		"form":form,
	}
	return render(request, "cooperatives/prod_edt.html", context)

def prod_delete(request, code=None):
    item = get_object_or_404(Producteur, code=code)
    if request.method == "POST":
        item.delete()
        messages.error(request, "Producteur Supprimer Avec Succès")
        return redirect('cooperatives:producteurs')
    context = {
        'item': item,
    }
    return render(request, 'cooperatives/prod_delete.html', context)

def parcelles(request):
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    prods = Producteur.objects.filter(cooperative_id=cooperative)
    s_sections = Sous_Section.objects.all().filter(section__cooperative_id=cooperative)
    parcelles = Parcelle.objects.all().filter(producteur__cooperative_id=cooperative).order_by("-add_le")
    parcelleForm = ParcelleForm(request.POST or None)
    if request.method == 'POST':
        parcelleForm = ParcelleForm(request.POST, request.FILES)
        if parcelleForm.is_valid():
            parcelle = parcelleForm.save(commit=False)
            # parcelle.producteur_id = prods
            for prod in prods:
                parcelle.producteur_id = prod.id

            for sect in s_sections:
                parcelle.sous_section_id = sect.id

            parcelle = parcelle.save()
            print(parcelle)
        messages.success(request, "Parcelle Ajoutés avec succès")
        return HttpResponseRedirect(reverse('cooperatives:parcelles'))

    context = {
        "cooperative":cooperative,
        "parcelles": parcelles,
        'parcelleForm': parcelleForm,
        'producteurs': prods,
        's_sections': s_sections,
    }
    return render(request, "cooperatives/parcelles.html", context)

def parcelle_update(request, id=None):
    instance = get_object_or_404(Parcelle, id=id)
    form = EditParcelleForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Parcelle Modifiée Avec Succès", extra_tags='html_safe')
        return HttpResponseRedirect(reverse('cooperatives:parcelles'))
    context = {
        'instance':instance,
        'form':form
    }
    return render(request, "cooperatives/parcelle_edit.html", context)

def parcelle_delete(request, id=None):
    parcelle = get_object_or_404(Parcelle, id=id)
    if request.method == "POST":
        parcelle.delete()
        messages.error(request, "Parcelle Supprimée Avec Succès")
        return redirect('cooperatives:parcelles')
    context = {
        'parcelle': parcelle,
    }
    return render(request, 'cooperatives/parcelle_delete.html', context)
    # parcelle.delete()
    # messages.success(request, "Parcelle Supprimer avec Succès")
    # return HttpResponseRedirect(reverse('cooperatives:parcelles'))

def planting(request):
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    # producteurs = Producteur.objects.all().filter(cooperative=cooperative)
    parcelles = Parcelle.objects.all().filter(producteur__cooperative_id=cooperative)
    plantings = Planting.objects.all().filter(parcelle__producteur__cooperative_id=cooperative)
    plantingForm = PlantingForm()
    if request.method == 'POST':
        plantingForm = PlantingForm(request.POST, request.FILES)
        if plantingForm.is_valid():
            planting = plantingForm.save(commit=False)
            for parcelle in parcelles.iterator():
                planting.parcelle_id = parcelle.id
            planting = planting.save()
            print(planting)
            # print(planting.parcelle.producteur)
        messages.success(request, "Parcelle Ajoutés avec succès")
        return HttpResponseRedirect(reverse('cooperatives:planting'))
    context = {
        "cooperative":cooperative,
        "parcelles": parcelles,
        "plantings": plantings,
        'plantingForm': plantingForm,
    }
    return render(request, "cooperatives/plantings.html", context)

def suivi_planting(request, id=None):
    instance = get_object_or_404(Planting, id=id)
    details = Details_planting.objects.all().filter(planting_id=instance)

    suiviForm = SuiviPlantingForm()
    if request.method == 'POST':
        suiviForm = SuiviPlantingForm(request.POST, request.FILES)
        if suiviForm.is_valid():
            suivi = suiviForm.save(commit=False)
            suivi.planting_id = instance.id
            suivi = suivi.save()
            print(suivi)
        messages.success(request, "Planting Ajouté avec succès")
        return HttpResponseRedirect(reverse('cooperatives:planting'))
    context = {
        'instance':instance,
        'details':details,
        'suiviForm':suiviForm,
    }
    return render(request, 'cooperatives/suivi_planting.html', context)

def planting_update(request, id=None):
	instance = get_object_or_404(Planting, id=id)
	form = PlantingForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Modification effectuée avec succès")
		return HttpResponseRedirect(reverse('cooperatives:planting'))

	context = {
		"instance": instance,
		"form":form,
	}
	return render(request, "cooperatives/planting_edit.html", context)

#-------------------------------------------------------------------------
## Export to Excel
#-------------------------------------------------------------------------

import csv

from django.http import HttpResponse
from django.contrib.auth.models import User

def export_producteur_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="producteurs.csv"'

    writer = csv.writer(response)
    writer.writerow(['CODE', 'TYPE', 'SECTION', 'GENRE', 'NOM', 'PRENOMS', 'CONTACTS'])
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    # producteurs = Producteur.objects.all().filter(cooperative=cooperative)

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

import xlwt

from django.http import HttpResponse
from django.contrib.auth.models import User

def export_prod_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="producteurs.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Producteurs')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['CODE', 'TYPE', 'SECTION', 'GENRE', 'NOM', 'PRENOMS', 'CONTACTS', 'LOCALITE']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    rows = Producteur.objects.all().filter(cooperative_id=cooperative.id).values_list(
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

def export_section_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Sections.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sections')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['LIBELLE', 'RESPONSABLE', 'CONTACTS']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    rows = Section.objects.all().filter(cooperative_id=cooperative.id).values_list(
        'libelle',
        'responsable',
        'contacts',
    )
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def export_sous_section_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Sous Sections.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sous Sections')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['SECTION', 'LIBELLE', 'RESPONSABLE', 'CONTACTS']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    rows = Sous_Section.objects.all().filter(section__cooperative_id=cooperative.id).values_list(
        'section__libelle',
        'libelle',
        'responsable',
        'contacts',
    )
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response

def export_parcelle_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Parcelles.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Parcelles')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['CODE', 'P.NOM', 'P.PRENOMS', 'CERTIFI', 'CULTURE', 'SUPER', 'LONG', 'LAT', 'SECTION']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    rows = Parcelle.objects.all().filter(producteur__cooperative_id=cooperative.id).values_list(
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

def export_formation_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Formations.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Formations')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['PROJET', 'FORMATEUR', 'INTITULE', 'DEBUT', 'FIN']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    # format2 = xlwt.Workbook({'num_format': 'dd/mm/yy'})
    rows = Formation.objects.all().filter(cooperative_id=cooperative.id).values_list(
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

def export_plant_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Planting.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Plants')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['P.CODE', 'P.NOM', 'P.PRENOMS', 'PARCELLE', 'ESPECE', 'NOMBRE', 'DATE']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    rows = Planting.objects.all().filter(parcelle__propietaire__cooperative_id=cooperative.id).values_list(
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

from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse

def export_prod_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="Producteurs.pdf"'

    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Start writing the PDF here
    p.drawString(100, 100, 'Hello world.')
    # End writing

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

from django.shortcuts import render
from django.core.serializers import serialize
from django.http import HttpResponse

def localisation(request):
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    parcelles = Parcelle.objects.all().filter(producteur__cooperative_id=cooperative)
    context = {
        'parcelles' : parcelles
    }
    return render(request, 'cooperatives/carte.html', context)

def site_pepiniere(request):
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    pepinieres = Pepiniere.objects.all().filter(cooperative_id=cooperative)
    context = {
        'pepinieres' : pepinieres
    }
    return render(request, 'cooperatives/carte_pepinieres.html', context)

def formation(request):
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    formations = Formation.objects.all().filter(cooperative_id=cooperative)
    formationForm = FormationForm()
    if request.method == 'POST':
        formationForm = FormationForm(request.POST, request.FILES)
        if formationForm.is_valid():
            formation = formationForm.save(commit=False)
            formation.cooperative_id = cooperative.id
            formation = formation.save()
            print(formation)
            # print(planting.parcelle.producteur)
        messages.success(request, "Formation Ajoutée avec succès")
        return HttpResponseRedirect(reverse('cooperatives:formations'))

    context = {
        'cooperative': cooperative,
        'formations': formations,
        'formationForm': formationForm,
    }
    return render(request, 'cooperatives/formations.html', context)

def Editformation(request, id=None):
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    instance = get_object_or_404(Formation, id=id)
    form = EditFormationForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.cooperative_id = cooperative.id
        instance.save()
        instance.save()
        messages.success(request, "Modification Effectuée Avec Succès", extra_tags='html_safe')
        return HttpResponseRedirect(reverse('cooperatives:formations'))

    context = {
        "cooperative":cooperative,
        "instance": instance,
        "form": form,
    }
    return render(request, "cooperatives/edit_formation.html", context)

def detail_formation(request, id=None):
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    instance = get_object_or_404(Formation, id=id)
    details = Detail_Formation.objects.all().filter(formation_id=instance)
    participants = Producteur.objects.all().filter(cooperative_id=cooperative)
    detailFormation = DetailFormation()
    if request.method == 'POST':
        detailFormation = DetailFormation(request.POST, request.FILES)
        if detailFormation.is_valid():
            detail = detailFormation.save(commit=False)
            detail.formation_id = instance.id
            # for p in participants:
                # detail.
            detail = detail.save()
            print(detail)
            # print(planting.parcelle.producteur)
        messages.success(request, "Formation Ajoutée avec succès")
        return HttpResponseRedirect(reverse('cooperatives:formations'))
    # participants = Producteur.objects.all().filter(formation_id=formation)
    context = {
        'instance':instance,
        'details':details,
        'detailFormation':detailFormation,
        # 'participants': participants,
    }
    return render(request, 'cooperatives/detail_formation.html', context)

def pepiniere(request):
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    pepinieres = Pepiniere.objects.all().filter(cooperative_id=cooperative)
    pepiForm = PepiniereForm()
    if request.method == 'POST':
        pepiForm = PepiniereForm(request.POST, request.FILES)
        if pepiForm.is_valid():
            pepiniere = pepiForm.save(commit=False)
            pepiniere.cooperative_id = cooperative.id
            pepiniere = pepiniere.save()
            print(pepiniere)
        messages.success(request, "Site Pépinière Ajouté avec succès")
        return HttpResponseRedirect(reverse('cooperatives:pepinieres'))

    context = {
        'cooperative': cooperative,
        'pepinieres': pepinieres,
        'pepiForm': pepiForm,
    }
    return render(request, 'cooperatives/pepinieres.html', context)

def Editpepiniere(request, id=None):
    cooperative = Cooperative.objects.get(user_id=request.user.id)
    instance = get_object_or_404(Pepiniere, id=id)
    form = EditPepiniereForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.cooperative_id = cooperative.id
        instance.save()
        instance.save()
        messages.success(request, "Modification Effectuée Avec Succès", extra_tags='html_safe')
        return HttpResponseRedirect(reverse('cooperatives:pepinieres'))

    context = {
        "cooperative":cooperative,
        "instance": instance,
        "form": form,
    }
    return render(request, "cooperatives/edit_pepiniere.html", context)

def detail_pepiniere(request, id=None, destination=None):
    # cooperative = Cooperative.objects.get(user_id=request.user.id)
    instance = get_object_or_404(Pepiniere, id=id)
    semences = Semence_Pepiniere.objects.all().filter(pepiniere_id=instance)
    retraits = Retrait_plant.objects.all().filter(pepiniere_id=instance)
    total_retraits = Retrait_plant.objects.all().filter(pepiniere_id=instance).aggregate(total=Sum('plant_retire'))['total']
    details_retraits = Detail_Retrait_plant.objects.all().filter(retait__pepiniere_id=instance)
    # detail_destination  = Detail_Retrait_plant.objects.all().filter()
    total_plants_a_produire = Semence_Pepiniere.objects.all().filter(pepiniere_id=instance).aggregate(total=Sum('production'))['total']

    retraitForm = RetraitForm()
    semenceForm = SemenceForm()
    detailRetraitForm = DetailRetraitForm()
    if request.method == 'POST':
        retraitForm = RetraitForm(request.POST, request.FILES)
        semenceForm = SemenceForm(request.POST, request.FILES)
        detailRetraitForm = DetailRetraitForm(request.POST, request.FILES)
        if retraitForm.is_valid():
            enlevement = retraitForm.save(commit=False)
            enlevement.pepiniere_id = instance.id
            enlevement = enlevement.save()
            print(enlevement)
            print(RetraitForm)
            messages.success(request, "Enregistrement effectué avec succès")
            return HttpResponse("Enregistrement effectué avec succès")

        elif semenceForm.is_valid():
            semence_recu = semenceForm.save(commit=False)
            semence_recu.pepiniere_id = instance.id
            semence_recu = semence_recu.save()
            print(semenceForm)
            messages.success(request, "Enregistrement effectué avec succès")
            return HttpResponse("Enregistrement effectué avec succès")


        elif detailRetraitForm.is_valid():
            detail_plant_retire = detailRetraitForm.save(commit=False)
            # detail_plant_retire.cooperative_id = cooperative.id
            detail_plant_retire.retait.pepiniere_id = instance.id
            detail_plant_retire = detail_plant_retire.save()
            print(detail_plant_retire)
            messages.success(request, "Enregistrement effectué avec succès")
            return HttpResponse("Enregistrement effectué avec succès")

        else:
            pass
    context = {
        # 'cooperative':cooperative,
        'instance':instance,
        'semences':semences,
        'retraits':retraits,
        'semenceForm':semenceForm,
        'retraitForm':retraitForm,
        'detailRetraitForm':detailRetraitForm,
        'details_retraits':details_retraits,
        'total_retraits':total_retraits,
        'total_plants_a_produire':total_plants_a_produire,
    }
    return render(request, 'cooperatives/detail_pepiniere.html', context)

def edit_semence(request, id=None):
    # pepiniere = get_object_or_404(Pepiniere, id=id)
    instance = get_object_or_404(Semence_Pepiniere, id=id)
    # instance = Semence_Pepiniere.objects.all().filter(pepiniere_id=pepiniere)
    form = EditSemenceForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        # instance.pepiniere_id = pepiniere.id
        instance.save()
        instance.save()
        messages.success(request, "Semence Modifiée Avec Succès", extra_tags='html_safe')
        return HttpResponseRedirect(reverse('cooperatives:pepinieres'))

    context = {
        # "pepiniere":pepiniere,
        "instance": instance,
        "form": form,
    }
    return render(request, "cooperatives/edit_semence.html", context)

def delete_semence(request, id=None):
    # pepiniere = get_object_or_404(Pepiniere, id=id)
    semence = get_object_or_404(Semence_Pepiniere, id=id)
    if request.method == "POST":
        semence.delete()
        messages.error(request, "Semence Supprimée Avec Succès")
        return redirect('cooperatives:detail_pepiniere')
    context = {
        # 'pepiniere': pepiniere,
        'semence': semence,
    }
    return render(request, 'cooperatives/semence_delete.html', context)
    # semence.delete()
    # messages.success(request, "Parcelle Supprimer avec Succès")
    # return HttpResponseRedirect(reverse('cooperatives:pepiniere'))

#Parcelle Json
# def my_parcelles(request):
#     parcelles = Parcelle.objects.all()
#     parcelles_list = serializers.serialize('json', parcelles)
#     return HttpResponse(parcelles_list, content_type="text/json-comment-filtered")

class ParcellesView(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            parcelles = Producteur.objects.all()
            parcelles_serializers = serializers.serialize('json', parcelles)
            return JsonResponse(parcelles_serializers, safe=False)
        return JsonResponse({'message': 'Erreure Lors du Chargement.....'})
    # parcelles = Parcelle.objects.all()
    # parcelles_list = serializers.serialize('json', parcelles)
    # return HttpResponse(parcelles_list, content_type="text/json-comment-filtered")

# DJango Serializer Views#
#@csrf_exempt
#def parcelle_list(request):
    # """
    # List all code snippets, or create a new snippet.
    # """
    # if request.method == 'GET':
    #     parcelles = Parcelle.objects.all()
    #     parcelles_serializers = serializers.serialize('json', parcelles)
    #     return JsonResponse(parcelles_serializers, safe=False)
class ParcellesMapView(TemplateView):

    template_name = "map.html"

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["parcelles"] = json.loads(serialize("geojson", Parcelle.objects.all()))
        return context




def ok(request):
    return render(request, 'ok.html')

def covid(request):
    response = requests.get('https://api.covid19api.com/countries').json()
    context = {
        'response': response
    }
    return render(request, 'covid.html', context)

#Export To PDF
def export_prods_to_pdf(request):
    cooperative = request.user.cooperative #Cooperative.objects.get(user_id=request.user.id)
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


def export_parcelles_to_pdf(request):
    cooperative = request.user.cooperative #Cooperative.objects.get(user_id=request.user.id)
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


