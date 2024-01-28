from rest_framework import serializers
from core.models import Utilisateur, Abonne, Commande, LigneCommande

class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class AbonneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Abonne
        fields = '__all__'

class SetNewPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    reset_code = serializers.CharField(max_length=4)
    new_password = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        fields = ['email', 'reset_code', 'new_password']

class CommandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commande 
        fields = '__all__'

class LigneCommandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LigneCommande 
        fields = '__all__'
