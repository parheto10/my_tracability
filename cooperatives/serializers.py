from rest_framework import serializers

from .models import Producteur, Parcelle, Section, Sous_Section, Cooperative

class CooperativeSerliazer(serializers.ModelSerializer):
    class Meta:
        model=Cooperative
        fields="__all__"

class SectionSerliazer(serializers.ModelSerializer):
    class Meta:
        model=Section
        fields=[
            "id",
            "cooperative",
            "libelle",
            "responsable",
            "contacts",
        ]
        # fields="__all__"

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


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcelle
        fields="__all__"

class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True)

    class Meta:
        model = Cooperative
        fields="__all__"

    def create(self, validated_data):
        tracks_data = validated_data.pop('tracks')
        album = Cooperative.objects.create(**validated_data)
        for track_data in tracks_data:
            Parcelle.objects.create(album=album, **track_data)
        return album