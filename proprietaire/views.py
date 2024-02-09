from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes 
from core.models import Utilisateur
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def change_password_vendeur(request, vendeur_id):
    proprietaire = request.user

    if proprietaire.type != Utilisateur.PROPRIETAIRE:
        return Response({"error": "Vous n'avez pas la permission de changer le mot de passe du vendeur"}, status=status.HTTP_403_FORBIDDEN)

    try:
        vendeur = Utilisateur.objects.get(id_user=vendeur_id, type=Utilisateur.VENDEUR)
    except Utilisateur.DoesNotExist:
        return Response({"error": "Vendeur non trouvé"}, status=status.HTTP_404_NOT_FOUND)

    new_password = request.data.get('new_password')
    confirm_password = request.data.get('confirm_password')

    if new_password != confirm_password:
        return Response({"error": "Les mots de passe ne correspondent pas"}, status=status.HTTP_400_BAD_REQUEST)

    vendeur.set_password(new_password)
    vendeur.save()

    return Response({"message": "Le mot de passe du vendeur a été modifié avec succès"}, status=status.HTTP_200_OK)      
