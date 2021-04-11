from rest_framework import serializers

from cooperatives.models import Producteur, Parcelle, Section, Sous_Section, Cooperative, Pepiniere, Formation
from parametres.models import Projet, Projet_Cat
from chocolotiers.models import Client

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'user',
            'sigle',
            'contacts',
            'libelle',
            'pays',
            'adresse',
            'telephone1',
            'telephone2',
            'email',
            'siteweb',
            'logo',
        ]

class CategorieProjetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projet_Cat
        fields = ["libelle"]


class ProjetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projet
        fields = [
            "client",
            "categorie",
            "accronyme",
            "titre",
            "chef",
            "debut",
            "fin",
            "etat",
        ]
        depth = 1
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['client'] = ClientSerializer(instance.client).data
        response['categorie'] = CategorieProjetSerializer(instance.categorie).data
        return response



class CooperativeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cooperative
        fields = [
            'region',
            'sigle',
            'activite',
            'projet',
            'contacts',
            'logo',
        ]

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Section
        fields = [
            "cooperative",
            'libelle',
            'responsable',
            'contacts',
        ]
        depth = 1
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['cooperative'] = CooperativeSerializer(instance.cooperative).data
        # response['sous_section'] = SousSectionSerializer(instance.sous_section).data
        return response

class SousSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sous_Section
        fields = [
            'libelle',
            'responsable',
            'contacts',
            'section',
        ]
        depth = 1
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['section'] = SectionSerializer(instance.section).data
        # response['sous_section'] = SousSectionSerializer(instance.sous_section).data
        return response

class ProducteurSerializer(serializers.ModelSerializer):
    # parcelles = ParcelleSerializer(many=True)
    # parcelles = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    # parcelles = serializers.StringRelatedField(many=True)
    # parcelles = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='details'
    # )

    class Meta:
        model = Producteur
        fields = [
            'id',
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
            # 'parcelles',
        ]
        depth = 1
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['section'] = SectionSerializer(instance.section).data
        response['sous_section'] = SousSectionSerializer(instance.sous_section).data
        return response

class ParcelleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Parcelle
        fields = [
            'id',
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
        depth = 1

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['producteur'] = ProducteurSerializer(instance.producteur).data
        # response['sous_section'] = SousSectionSerializer(instance.sous_section).data
        return response

class PepiniereSerializer(serializers.ModelSerializer):
    class Meta:
        model=Pepiniere
        fields = [
            'cooperative',
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
        depth = 1
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['cooperative'] = CooperativeSerializer(instance.cooperative).data
        # response['sous_section'] = SousSectionSerializer(instance.sous_section).data
        return response

class FormationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formation
        fields = [
            'cooperative',
            'projet',
            'formateur',
            'libelle',
            'details',
            'observation',
            'debut',
            'fin',
        ]
        depth = 1
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['cooperative'] = CooperativeSerializer(instance.cooperative).data
        response['projet'] = ProjetSerializer(instance.projet).data
        return response





