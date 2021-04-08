from rest_framework import serializers

from cooperatives.models import Producteur, Parcelle, Section, Sous_Section, Cooperative

class ProducteurSerializer(serializers.ModelSerializer):
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
            'nb_parcelle',
            'image',
            'type_document',
            'num_document',
            'document',
        ]

class ParcelleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcelle
        fields = [
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