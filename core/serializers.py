from rest_framework import serializers
from .models import Fleur, Fichesoin

class FleurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fleur
        fields = '__all__'

class FichesoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fichesoin
        fields = '__all__'        