from django import forms
from django.contrib.auth import get_user_model
#from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import fields
from django.http import request
from django_select2 import forms as s2forms
from django_select2.forms import ModelSelect2Widget

from .models import Parcelle, Formation

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
            'latitude',
            'longitude',
            'culture',
            'associee',
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
        fields = [
            'code',
            'latitude',
            'longitude',
            'culture',
            'associee',
            'superficie'
        ]