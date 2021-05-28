from django.contrib import messages
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from cooperatives.forms import EditParcelleForm
from .forms import ParcelleForm, EditParcelleForm
from .models import Organisation, Parcelle, Planting_Com, DetailPlanting, Monitoring


def com_dashboard(request):
    communaute = Organisation.objects.get(user_id=request.user.id)

    # nb_formations = Formation.objects.all().filter(cooperative_id=cooperative).count()
    parcelles = Parcelle.objects.filter(communaute_id=communaute)
    nb_parcelles = parcelles = Parcelle.objects.filter(communaute_id=communaute).count()
    Superficie = parcelles = Parcelle.objects.filter(communaute_id=communaute).aggregate(total=Sum('superficie'))['total']
    Plants = Planting_Com.objects.all().filter(parcelle__communaute_id=communaute).aggregate(total=Sum('plant_total'))['total']

    context={
    'communaute':communaute,
    # 'producteurs': producteurs,
    # 'nb_producteurs': nb_producteurs,
    # 'nb_formations': nb_formations,
    'parcelles': parcelles,
    'nb_parcelles': nb_parcelles,
    'Superficie' : Superficie,
    'Plants': Plants,
    # 'section': section,
    # 'section_plating': section_plating,
    # 'labels': labels,
    # 'data': data,
    # 'mylabels': mylabels,
    # 'mydata': mydata,
    }
    return render(request,'communautes/dashboard.html',context=context)

def parcelles(request):
    communaute = Organisation.objects.get(user_id=request.user.id)
    parcelles = Parcelle.objects.filter(communaute_id=communaute)
    parcelleForm = ParcelleForm(request.POST or None)
    if request.method == 'POST':
        parcelleForm = ParcelleForm(request.POST, request.FILES)
        if parcelleForm.is_valid():
            parcelle = parcelleForm.save(commit=False)
            parcelle.communaute_id = communaute.id
            # parcelle.producteur_id = prods
            if not parcelle.code:
                tot = Parcelle.objects.filter(communaute_id=communaute).count()
                parcelle.code = "%s-%s" % (parcelle.communaute.user.username, tot)
            parcelle = parcelle.save()
            # print(parcelle)
        messages.success(request, "Parcelle Ajoutés avec succès")
        return HttpResponseRedirect(reverse('communautes:parcelles'))

    context = {
        "communaute":communaute,
        "parcelles": parcelles,
        'parcelleForm': parcelleForm,
    }
    return render(request, "communautes/parcelles.html", context)

def parcelle_update(request, id=None):
    instance = get_object_or_404(Parcelle, id=id)
    form = EditParcelleForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Parcelle Modifiée Avec Succès", extra_tags='html_safe')
        return HttpResponseRedirect(reverse('communautes:parcelles'))
    context = {
        'instance':instance,
        'form':form
    }
    return render(request, "communautes/parcelle_edit.html", context)

def parcelle_delete(request, id=None):
    parcelle = get_object_or_404(Parcelle, id=id)
    if request.method == "POST":
        parcelle.delete()
        messages.error(request, "Parcelle Supprimée Avec Succès")
        return redirect('communautes:parcelles')
    context = {
        'parcelle': parcelle,
    }
    return render(request, 'communautes/parcelle_delete.html', context)
    # parcelle.delete()
    # messages.success(request, "Parcelle Supprimer avec Succès")
    # return HttpResponseRedirect(reverse('cooperatives:parcelles'))

# Create your views here.
