from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes 
from .serializers import UtilisateurSerializer, CommandeSerializer, LigneCommandeSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from core.models import Utilisateur, Commande, Fleur, Bouquet, Parfum, LigneCommande

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    # Analyser l'URL pour déterminer le type
    path_parts = request.path.split('/')
    if 'proprietaire' in path_parts:
        type_utilisateur = 1
    elif 'vendeur' in path_parts:
        type_utilisateur = 2
    elif 'abonne' in path_parts:
        type_utilisateur = 3
    else:
        return Response({"error": "Type d'utilisateur non spécifié"}, status=status.HTTP_400_BAD_REQUEST)

    # Récupérer les données de connexion depuis la requête
    username = request.data.get('username')
    password = request.data.get('password')

    # Rechercher l'utilisateur dans la base de données
    try:
        utilisateur = Utilisateur.objects.get(username=username, type=type_utilisateur)
    except Utilisateur.DoesNotExist:
        return Response({"error": "Données d'authentification incorrecte"}, status=status.HTTP_404_NOT_FOUND)

    # Vérifier le mot de passe
    if utilisateur.check_password(password):
        # Authentification réussie, générer un token
        token, created = Token.objects.get_or_create(user=utilisateur)
        return Response({"token": token.key, "utilisateur": UtilisateurSerializer(utilisateur).data})
    else:
        return Response({"error": "Données incorrectes"}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        # Supprimer le jeton d'authentification
        request.auth.delete()
        return Response({"message": "Déconnexion réussie"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "Erreur lors de la déconnexion", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def change_password(request):
    if request.method == 'POST':
        old_password = request.data.get('old_password')
        utilisateur = request.user  

        if not utilisateur.check_password(old_password):
            return Response({"error": "Le mot de passe actuel est incorrect"}, status=status.HTTP_404_NOT_FOUND)
        
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if new_password != confirm_password:
            return Response({"error": "Les mots de passe ne correspondent pas"}, status=status.HTTP_400_BAD_REQUEST)
        
        if utilisateur.type not in [Utilisateur.ABONNE, Utilisateur.PROPRIETAIRE]:
            return Response({"error": "Vous n'avez pas la permission de changer le mot de passe"}, status=status.HTTP_403_FORBIDDEN)
        
        utilisateur.set_password(new_password)
        utilisateur.save()
        return Response({"message": "Le mot de passe a été modifié avec succès"}, status=status.HTTP_200_OK)

# Fonction pour vérifier la disponibilité du produit et la quantité en stock
def check_product_availability(type_produit, produit_id, quantite_demandee):
    try:
        if type_produit == 'Fleur':
            produit = Fleur.objects.get(id_fleur=produit_id)
        elif type_produit == 'Parfum':
            produit = Parfum.objects.get(id_parfum=produit_id)
        elif type_produit == 'Bouquet':
            produit = Bouquet.objects.get(id_bouquet=produit_id)
        else:
            # Invalid product type, cancel the order
            return Response({'message': f"Invalid product type for product {produit_id}"},
                            status=status.HTTP_400_BAD_REQUEST)

        quantite_en_stock = produit.qt_stock

        if quantite_demandee > quantite_en_stock:
            # Product quantity is insufficient, cancel the order
            return Response({'message': f"{type_produit} {produit_id} quantity insufisante in stock"},
                            status=status.HTTP_400_BAD_REQUEST)

    except (Fleur.DoesNotExist, Parfum.DoesNotExist, Bouquet.DoesNotExist):
        # Product does not exist, cancel the order
        return Response({'message': f"{type_produit} {produit_id} does not exist"},
                        status=status.HTTP_400_BAD_REQUEST)

    # Si tout est en ordre, retournez None
    return None

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated]) 
def add_Commande(request):
    user = request.user
    user_type = user.type  # Utilisez directement l'utilisateur connecté

    if user_type == 3:
        status_value = 'En attente'
    elif user_type == 2:
        status_value = request.data.get('statut')
    else:
        status_value = None

    request.data.update({
        'statut': status_value,
        'id_commandant': user.id_user,  # Utilisez l'ID de l'utilisateur connecté
        'telephone': None if status_value == 'livré' else request.data.get('telephone'),
        'adresse_livraison': None if status_value == 'livré' else request.data.get('adresse_livraison'),
    })

    ligne_commande_data = request.data.get('ligne_commande', [])

    # Check product availability and quantity in stock for each line of the order
    for ligne_data in ligne_commande_data:
        type_produit = ligne_data.get('type_produit', None)
        produit_id = ligne_data.get('produit_id', None)
        quantite_demandee = ligne_data.get('quantite_commande', 0)

        # Appeler la fonction de vérification
        result = check_product_availability(type_produit, produit_id, quantite_demandee)

        if result is not None:
            # La vérification a échoué, retourner la réponse d'erreur
            return result

    commande_serializer = CommandeSerializer(data=request.data)

    if commande_serializer.is_valid():
        # Enregistrer la commande principale
        commande = commande_serializer.save()

        # Traiter et enregistrer les lignes de commande
        for ligne_data in ligne_commande_data:
            ligne_data['commande'] = commande.id_commande
            ligne_serializer = LigneCommandeSerializer(data=ligne_data)

            if ligne_serializer.is_valid():
                ligne_serializer.save()
            else:
                # Rollback: Delete the main order if a line order fails to save
                commande.delete()
                return Response(ligne_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(commande_serializer.data)
    else:
        return Response(commande_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def details_commande(request, commande_id):
    try:
        # Assurez-vous que l'utilisateur connecté est authentifié
        user = request.user

        # Obtenez l'instance de la commande
        commande = Commande.objects.get(id_commande=commande_id)

        # Vérifiez si l'utilisateur est un abonné (type 3)
        if user.type == 3 and user != commande.id_commandant:
            return Response({'message': 'Vous n\'avez pas les permissions nécessaires'},
                            status=status.HTTP_403_FORBIDDEN)

        # Sérialisez la commande
        commande_serializer = CommandeSerializer(commande)

        # Obtenez les lignes de commande pour cette commande
        lignes_commande = LigneCommande.objects.filter(commande=commande)

        # Sérialisez les lignes de commande
        lignes_commande_serializer = LigneCommandeSerializer(lignes_commande, many=True)

        # Retournez la réponse avec les détails de la commande et ses lignes de commande
        return Response({
            'commande': commande_serializer.data,
            'lignes_commande': lignes_commande_serializer.data
        })

    except Commande.DoesNotExist:
        return Response({'message': f'Commande avec ID {commande_id} n\'existe pas'},
                        status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)