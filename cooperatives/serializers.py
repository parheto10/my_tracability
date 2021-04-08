from rest_framework import serializers

from .models import Producteur, Parcelle, Section, Sous_Section, Cooperative

class CooperativeSerliazer(serializers.ModelSerializer):
    class Meta:
        model=Cooperative
        fields="__all__"

class SectionSerliazer(serializers.ModelSerializer):
    class Meta:
        model=Section
        fields="__all__"

    def to_representation(self, instance):
        response=super().to_representation(instance)
        response['cooperative']=CooperativeSerliazer(instance.cooperative_id).data
        return response

    
class Sous_SectionSerliazer(serializers.ModelSerializer):
    class Meta:
        model=Sous_Section
        fields="__all__"

    def to_representation(self, instance):
        response=super().to_representation(instance)
        response['section']=SectionSerliazer(instance.section_id).data
        return response

class ProducteurSerliazer(serializers.ModelSerializer):
    class Meta:
        model=Producteur
        fields="__all__"

    def to_representation(self, instance):
        response=super().to_representation(instance)
        response['section'] = SectionSerliazer(instance.section_id).data
        response['sous_section']=Sous_SectionSerliazer(instance.sous_section_id).data
        return response


class ParcelleSerliazer(serializers.ModelSerializer):
    class Meta:
        model=Parcelle
        fields="__all__"

    def to_representation(self, instance):
        response=super().to_representation(instance)
        response['section'] = SectionSerliazer(instance.section_id).data
        response['sous_section']=Sous_SectionSerliazer(instance.sous_section_id).data
        response['producteur']=Sous_SectionSerliazer(instance.producteur_id).data
        return response