from django import forms
from django.contrib.auth import get_user_model
#from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import fields
from django.http import request
from django_select2 import forms as s2forms
from django_select2.forms import ModelSelect2Widget

class CooperativeWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "sigle__icontains",
        #"email__icontains",
    ]

class SectionWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "libelle__icontains",
        #"email__icontains",
    ]

from cooperatives.models import Cooperative, Producteur, Section, Sous_Section, Parcelle, Planting, Formation, \
    Detail_Formation, Pepiniere, Semence_Pepiniere, Retrait_plant, Detail_Retrait_plant
# from cooperatives.views import cooperative
from parametres.models import Region, Projet, Activite, Origine, Sous_Prefecture, Espece
from ajax_select.fields import AutoCompleteSelectMultipleField, AutoCompleteField

User = get_user_model()
non_allowed_username = ["abc", "123", "admin1", "admin12"]

class UserForm(forms.ModelForm):
    last_name = forms.CharField(label="Nom")
    first_name = forms.CharField(label="Prénoms")
    username = forms.CharField(label="Nom d’utilisateur")
    email = forms.EmailField(label="Adresse électronique")
    password = forms.CharField(widget=forms.PasswordInput(attrs={"id": "password", "class": "form-control"}), label="Mot de Passe")

    class Meta:
        model=User
        fields=['last_name','first_name','username', 'email', 'password']

class CoopForm(forms.ModelForm):
    #this is the extrafield for linking patient and their assigend doctor
    #this will show dropdown __str__ method doctor model is shown on html so override it
    #to_field_name this will fetch corresponding value  user_id present in Doctor model and return it
    region=forms.ModelChoiceField(queryset=Region.objects.all(),empty_label="Région")
    projet=forms.ModelChoiceField(queryset=Projet.objects.all(),empty_label="Projet")
    activite=forms.ModelChoiceField(queryset=Activite.objects.all(),empty_label="Natures Activités")
    class Meta:
        model=Cooperative
        fields=[
            'region',
            'sigle',
            'activite',
            'projet',
            'contacts',
            'logo',
        ]

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        widgets = {
            "cooperative": CooperativeWidget,
            #"co_authors": CoAuthorsWidget,
        }
        fields = [
            'libelle',
            'responsable',
            'contacts',
        ]

class Sous_SectionForm(forms.ModelForm):
    class Meta:
        model = Sous_Section
        fields = [
            # 'section',
            'libelle',
            'responsable',
            'contacts',
        ]

class Edit_Sous_SectionForm(forms.ModelForm):
    class Meta:
        model = Sous_Section
        fields = [
            'section',
            'libelle',
            'responsable',
            'contacts',
        ]

class ProdForm(forms.ModelForm):
    # origine = forms.ModelChoiceField(queryset=Origine.objects.all(), empty_label="Origine")
    sous_prefecture = forms.ModelChoiceField(queryset=Sous_Prefecture.objects.all())
    # section = forms.ModelChoiceField(queryset=Section.objects.all().fil, empty_label="Section")
    sous_section = forms.ModelChoiceField(queryset=Sous_Section.objects.all(), empty_label="Sous Section", required=False)
    class Meta:
        model = Producteur
        fields = [
            'code',
            'origine',
            'sous_prefecture',
            'type_producteur',
            'nom',
            'prenoms',
            'dob',
            'genre',
            'contacts',
            'localite',
            # 'section',
            'sous_section',
            'nb_parcelle',
            'image',
            'type_document',
            'num_document',
            'document',
        ]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['section'].queryset = Section.objects.none()
    #
    #     if 'section' in self.data:
    #         try:
    #             cooperative_id = int(self.data.get('cooperative'))
    #             self.fields['section'].queryset = Section.objects.filter(cooperative_id=cooperative_id).order_by('libelle')
    #         except (ValueError, TypeError):
    #             pass  # invalid input from the client; ignore and fallback to empty City queryset
    #     elif self.instance.pk:
    #         self.fields['section'].queryset = self.instance.cooperative.section_set.order_by('libelle')
    # def __init__(self, user=None, *args, **kwargs):
    #     super(ProdForm, self).__init__(*args, **kwargs)
        # access object through self.instance...
        # self.fields['cooperative'].queryset = Cooperative.objects.all().filter(user_id=user)
        # self.fields['section'].queryset = Section.objects.filter(cooperative_id=self.instance.cooperative.user_id).all()
        # self.fields['sous_section'].queryset = Sous_Section.objects.all().filter(section__cooperative=self.instance.cooperative.user_id)
    # def __init__(self, user=None, **kwargs):
    #     super(ProdForm, self).__init__(**kwargs)
    #     if user:
    #         cooperative = Cooperative.objects.get(user_id=user)
    #         # self.fields['propietaire'].queryset = Parcelle.objects.filter(propietaire__cooperative_id=cooperative)
    #         # self.fields['sous_prefecture'].queryset = Cooperative.objects.filter(prefe)
    #         self.fields['section'].queryset = Section.objects.filter(cooperative=cooperative.user)
    #         self.fields['sous_section'].queryset = Sous_Section.objects.filter(section__cooperative=cooperative.user)
    #         # self.fields['sous_section']= Parcelle.objects.filter(section__cooperative_id=cooperative)

class EditProdForm(forms.ModelForm):
    origine = forms.ModelChoiceField(queryset=Origine.objects.all(), empty_label="Origine")
    sous_prefecture = forms.ModelChoiceField(queryset=Sous_Prefecture.objects.all())
    section = forms.ModelChoiceField(queryset=Section.objects.all(), empty_label="Section")
    sous_section = forms.ModelChoiceField(queryset=Sous_Section.objects.all(), empty_label="Sous Section", required=False)
    class Meta:
        model = Producteur
        fields = [
            'code',
            'origine',
            'sous_prefecture',
            'type_producteur',
            'nom',
            'prenoms',
            'dob',
            'genre',
            'contacts',
            'localite',
            'section',
            'sous_section',
            'nb_enfant',
            'nb_parcelle',
            'image',
            'type_document',
            'num_document',
            'document',
        ]
    # def get_cooperative(self, request, *args, **kwargs):
    #     cooperative = Cooperative.objects.get(user_id=request.user.id)
    #     producteur_obj = Producteur.objects.filter(cooperative_id=cooperative)
    #     return producteur_obj

class ParcelleForm(forms.ModelForm):
    #this is the extrafield for linking patient and their assigend doctor
    #this will show dropdown __str__ method doctor model is shown on html so override it
    #to_field_name this will fetch corresponding value  user_id present in Doctor model and return it
    # projet = forms.ModelChoiceField(queryset=Projet.objects.all(), empty_label="Projet")
    # section = forms.ModelChoiceField(queryset=Section.objects.all(), empty_label="Section")
    # producteur = forms.ModelChoiceField(queryset=Producteur.objects.all(), empty_label="Propriétaires")
    # sous_section = forms.ModelChoiceField(queryset=Sous_Section.objects.all(), empty_label="Sous Section",required=False)

    class Meta:
        model=Parcelle
        fields=[
            'code',
            # 'producteur',
            # 'sous_section',
            'acquisition',
            'latitude',
            'longitude',
            'culture',
            'certification',
            'superficie'
        ]

    #producteur = AutoCompleteField('producteur')
    # def __init__(self, user=None, **kwargs):
    #     super(ParcelleForm, self).__init__(**kwargs)
    #     if user:
    #         cooperative = Cooperative.objects.get(user_id=user)
    #         self.fields['propietaire'].queryset = Parcelle.objects.filter(propietaire__cooperative_id=cooperative)
    #         self.fields['section'].queryset = Parcelle.objects.filter(section__cooperative_id=cooperative)
    #         # self.fields['sous_section']= Parcelle.objects.filter(section__cooperative_id=cooperative)

class EditParcelleForm(forms.ModelForm):

    class Meta:
        model=Parcelle
        fields=[
            'code',
            'producteur',
            'sous_section',
            'acquisition',
            'latitude',
            'longitude',
            'culture',
            'certification',
            'superficie'
        ]

# class PlantingForm(forms.ModelForm):
#     #this is the extrafield for linking patient and their assigend doctor
#     #this will show dropdown __str__ method doctor model is shown on html so override it
#     #to_field_name this will fetch corresponding value  user_id present in Doctor model and return it
#     # parcelle = forms.ModelChoiceField(queryset=Parcelle.objects.all(), empty_label="Parcelle")
#     # espece = forms.ModelChoiceField(queryset=Espece.objects.all(), empty_label="Espèce")
#     # sous_section = forms.ModelChoiceField(queryset=Sous_Section.objects.all(), empty_label="Sous Section",required=False)
#
#     class Meta:
#         model=Planting
#         fields=[
#             # 'parcelle',
#             'date',
#             'nb_plant',
#             'details',
#             'observation',
#         ]
#
#     # def __init__(self, user=None, **kwargs):
#     #     super(PlantingForm, self).__init__(**kwargs)
#     #     if user:
#     #         cooperative = Cooperative.objects.get(user_id=user)
#     #         self.fields['parcelle'].queryset = Parcelle.objects.filter(section__cooperative_id=cooperative)

class PepiniereForm(forms.ModelForm):

    class Meta:
        model=Pepiniere
        fields=[
            # 'cooperative',
            'region',
            'ville',
            'site',
            'latitude',
            'longitude',
            'technicien',
            'contacts_technicien',
            'superviseur',
            'contacts_superviseur',
            'sachet_recus',
            'production_plant',
            'production_realise',
            'plant_mature',
            'plant_retire',
        ]

class EditPepiniereForm(forms.ModelForm):

    class Meta:
        model=Pepiniere
        fields=[
            # 'cooperative',
            'region',
            'ville',
            'site',
            'latitude',
            'longitude',
            'technicien',
            'contacts_technicien',
            'superviseur',
            'contacts_superviseur',
            'sachet_recus',
            'production_plant',
            'production_realise',
            'plant_mature',
            'plant_retire',
        ]

# class SuiviPlantingForm(forms.ModelForm):
#
#     class Meta:
#         model=Details_planting
#         fields=[
#             # 'planting',
#             'projet',
#             'espece',
#             'plante',
#             'date',
#             'mort',
#             'remplace',
#             'mature',
#         ]

class SemenceForm(forms.ModelForm):

    class Meta:
        model=Semence_Pepiniere
        fields=[
            # 'pepiniere',
            'espece_recu',
            'production',
            'qte_recu',
            'date',
        ]

class EditSemenceForm(forms.ModelForm):

    class Meta:
        model=Semence_Pepiniere
        fields=[
            'pepiniere',
            'espece_recu',
            'production',
            'qte_recu',
            'date',
        ]

class RetraitForm(forms.ModelForm):

    class Meta:
        model=Retrait_plant
        fields=[
            # 'pepiniere',
            'client',
            'destination',
            'plant_retire',
            'date',
        ]

class DetailRetraitForm(forms.ModelForm):

    class Meta:
        model= Detail_Retrait_plant
        fields=[
            # 'cooperative'
            'retait',
            'espece',
            'plant_retire',
            'date',
        ]

class FormationForm(forms.ModelForm):

    class Meta:
        model=Formation
        fields=[
            'projet',
            'formateur',
            'libelle',
            'details',
            'observation',
            'debut',
            'fin',
        ]

class EditFormationForm(forms.ModelForm):

    class Meta:
        model=Formation
        fields=[
            'projet',
            'formateur',
            'libelle',
            'details',
            'observation',
            'debut',
            'fin',
        ]

class DetailFormation(forms.ModelForm):
    # participant = forms.ModelMultipleChoiceField(queryset=Producteur.objects.all(), empty_label="Producteurs",required=False)
    participant = forms.ModelMultipleChoiceField(queryset=Producteur.objects.all())

    class Meta:
        model = Detail_Formation
        fields = [
            # 'formation',
            'participant',
        ]
        # widgets = {'participant': ModelSelect2Widget(
        #     queryset=Producteur.objects.all().distinct('participant'),
        #     search_fields=['participant_icontains']
        # )}


