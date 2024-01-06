from rest_framework import serializers
from .models import Fleur, Fichesoin, Famille, Magasin, Parfum

class FleurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fleur
        fields = '__all__'

class FichesoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fichesoin
        fields = '__all__' 

class FamilleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Famille
        fields = '__all__' 

class Magasinserializer(serializers.ModelSerializer):
    class Meta:
        model = Magasin
        fields = '__all__' 

class ParfumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parfum
        fields = '__all__'                        