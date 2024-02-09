from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from core.models import Commande,Magasin,Fleur,Bouquet,Parfum
from core.serializers import CommandeSerializer 
from django.core.mail import send_mail

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def modifier_statut_commande(request, commande_id):
    try:
        # Assurez-vous que l'utilisateur connecté est de type vendeur (type 2)
        user = request.user
        if user.type != 2:
            return Response({'message': 'Vous n\'avez pas les permissions nécessaires'},
                            status=status.HTTP_403_FORBIDDEN)

        # Obtenez l'instance de la commande
        commande = Commande.objects.get(id_commande=commande_id)

        # Obtenez le nouveau statut à partir des données de la requête
        nouveau_statut = request.data.get('nouveau_statut', None)

        if nouveau_statut is not None:
            # Mettez à jour directement le statut dans l'instance de la commande
            commande.statut = nouveau_statut
            commande.save()

            # Réponse réussie
            return Response({'message': f'Statut de la commande {commande_id} modifié avec succès'})

        else:
            # Si le nouveau statut n'est pas fourni dans la requête
            return Response({'message': 'Le nouveau statut n\'est pas spécifié'},
                            status=status.HTTP_400_BAD_REQUEST)

    except Commande.DoesNotExist:
        # Si la commande n'existe pas
        return Response({'message': f'Commande avec ID {commande_id} n\'existe pas'},
                        status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def commandesEnattente(request):
    try:
        # Assurez-vous que l'utilisateur connecté est de type vendeur (type 2)
        user = request.user
        if user.type != 2:
            return Response({'message': 'Vous n\'avez pas les permissions nécessaires'},
                            status=status.HTTP_403_FORBIDDEN)

        # Obtenez les commandes avec le statut spécifié
        commandes = Commande.objects.filter(statut='En attente')

        if not commandes.exists():
            return Response({'message': 'Aucune commande n\'est en attente de livraison'})

        # Sérialisez les commandes
        serializer = CommandeSerializer(commandes, many=True)

        return Response(serializer.data)

    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def valider_rejeter_annulation(request, commande_id):
    try:
        # Assurez-vous que l'utilisateur connecté est authentifié et est un vendeur (type 2)
        user = request.user

        if user.type != 2:
            return Response({'message': 'Vous n\'avez pas les permissions nécessaires'},
                            status=status.HTTP_403_FORBIDDEN)

        # Obtenez l'instance de la commande
        commande = Commande.objects.get(id_commande=commande_id)

        # Vérifiez que la commande est en attente d'annulation
        if commande.statut != 'Demande annulation':
            return Response({'message': 'La commande ne peut pas être annulée car elle n\'a pas fait l\'objet d\'une demande d\'annulation'},
                            status=status.HTTP_400_BAD_REQUEST)

        user_commande = commande.id_commandant
        email_abonne = user_commande.email if user_commande else None

        magasin = Magasin.objects.first()
        email_magasin = magasin.email if magasin else None
        sujet = 'Réponse concernant votre demande d\'annulation de commande'

        # Validez ou rejetez l'annulation en fonction de la demande du vendeur
        if 'valider' in request.data and request.data['valider']:
            # Valider l'annulation : Supprimez la commande et ses lignes de commande de la base de données
            commande.delete()
            message = 'L\'annulation de la commande a été validée par le vendeur.'
        else:
            message = 'L\'annulation de la commande a été refusée par le vendeur.'

        contenu = f'Bonjour Monsieur/Madame,\n\nMessage:\n{message}'

        try:
            # Envoie de l'e-mail à l'abonné
            send_mail(sujet, contenu, email_magasin, [email_abonne])
            return Response({"message": "La réponse à la demande d'annulation a été envoyée avec succès"},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Une erreur s'est produite lors de l'envoi de l'e-mail: {str(e)}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    except Commande.DoesNotExist:
        return Response({'message': f'Commande avec ID {commande_id} n\'existe pas'},
                        status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def FindProduct(request, code):
    try:
        # Assurez-vous que l'utilisateur connecté est authentifié et est un vendeur (type 2)
        user = request.user

        if user.type != 2:
            return Response({'message': 'Vous n\'avez pas les permissions nécessaires'},
                            status=status.HTTP_403_FORBIDDEN)
        
        product = None

        # Vérifiez le préfixe du code et recherchez dans la table appropriée
        if code.startswith('FL'):
            product = Fleur.objects.get(code=code)
        elif code.startswith('PF'):
            product = Parfum.objects.get(code=code)
        elif code.startswith('BQ'):
            product = Bouquet.objects.get(code=code)
        else:
            return Response({'message': 'Code de produit invalide'}, status=status.HTTP_400_BAD_REQUEST)

        # Si le produit est trouvé, renvoyez-le
        if product:
            return Response(product.nom)
        else:
            return Response({'message': 'Produit non trouvé'}, status=status.HTTP_404_NOT_FOUND)

    except Fleur.DoesNotExist:
        return Response({'message': 'Produit non trouvé'}, status=status.HTTP_404_NOT_FOUND)
    except Parfum.DoesNotExist:
        return Response({'message': 'Produit non trouvé'}, status=status.HTTP_404_NOT_FOUND)
    except Bouquet.DoesNotExist:
        return Response({'message': 'Produit non trouvé'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 