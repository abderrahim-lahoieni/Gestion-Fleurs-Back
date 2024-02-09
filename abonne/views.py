from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny,IsAuthenticated
from core.models import Abonne,Magasin,Commande,LigneCommande
from core.serializers import UtilisateurSerializer,AbonneSerializer,CommandeSerializer,LigneCommandeSerializer
from rest_framework import status, serializers
from rest_framework import status
from django.db.models import Q
from django.db import transaction
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    if request.method == 'POST':
        if request.data.get('confirm_password')!=request.data.get('password'):
            return Response({"error": "Les mots de passe ne correspondent pas"}, status=status.HTTP_400_BAD_REQUEST)
        utilisateur_data = {
            'username': request.data.get('username'),
            'password': request.data.get('password'),
            'type': 3,  # Définir le type d'utilisateur
        }

        utilisateur_serializer = UtilisateurSerializer(data=utilisateur_data, context={'request': request})
        if utilisateur_serializer.is_valid():
            utilisateur = utilisateur_serializer.save()
            id_utilisateur = utilisateur.id_user

            abonne_data = {
                'nom': request.data.get('nom'),
                'prenom': request.data.get('prenom'),
                'numero': request.data.get('numero'),
                'email': request.data.get('email'),
                'id_user': id_utilisateur,
            }

            try:
                with transaction.atomic():
                    # Vérifier si l'abonné existe déjà
                    abonne_instance = Abonne.objects.filter(Q(email=abonne_data['email']) | Q(numero=abonne_data['numero'])).first()

                    if abonne_instance:
                        # Si l'abonné existe déjà, déterminer s'il s'agit de l'email ou du numéro
                        if abonne_instance.email == abonne_data['email']:
                            raise serializers.ValidationError({
                                "abonne": ["L'abonné avec cet email existe déjà. Veuillez fournir une adresse email unique."]
                            })
                        else:
                            raise serializers.ValidationError({
                                "abonne": ["L'abonné avec ce numéro existe déjà. Veuillez fournir un numéro unique."]
                            })

                    # Création d'un nouvel abonné
                    abonne_serializer = AbonneSerializer(data=abonne_data)

                    if abonne_serializer.is_valid():
                        abonne_serializer.save()
                    else:
                        # Si la création de l'abonné échoue, supprimer l'utilisateur correspondant
                        utilisateur.delete()
                        return Response({
                            "message": "Erreur lors de la création de l'abonné",
                            "errors": abonne_serializer.errors
                        }, status=status.HTTP_400_BAD_REQUEST)

                    # Créer ou récupérer le token existant
                    token = Token.objects.create(user=utilisateur)

                    return Response({
                        "token": token.key,
                        "utilisateur": utilisateur_serializer.data,
                        "abonne": abonne_serializer.data
                    }, status=status.HTTP_201_CREATED)

            except serializers.ValidationError as e:
                # Gérer l'erreur explicative levée dans le cas d'un abonné existant
                utilisateur.delete()
                return Response({"message": "Erreur lors de l'enregistrement", "errors": e.detail}, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                # Gérer toute autre exception pendant la transaction
                utilisateur.delete()
                return Response({"message": "Erreur lors de l'enregistrement", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"message": "Méthode non autorisée"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([AllowAny])
def contact_us(request):
    if request.method == 'POST':
        nom = request.data.get('nom')
        prenom = request.data.get('prenom')
        email = request.data.get('email')
        message = request.data.get('message')

        # Récupérer l'adresse e-mail du magasin depuis la base de données
        magasin = Magasin.objects.first()
        email_magasin = magasin.email if magasin else None

        if not email_magasin:
            return Response({"error": "L'adresse e-mail du magasin est indisponible"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        sujet = 'Contact depuis le site web'
        contenu = f'Nom: {nom}\nPrénom: {prenom}\nEmail: {email}\n\nMessage:\n{message}'

        try:
            # Envoie de l'e-mail
            send_mail(sujet, contenu, email, [email_magasin])
            return Response({"message": "Votre message a été envoyé avec succès"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Une erreur s'est produite lors de l'envoi de l'e-mail: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"message": "Méthode non autorisée"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)      

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lister_commandes_abonne(request):
    try:
        # Assurez-vous que l'utilisateur connecté est authentifié
        user = request.user

        # Vérifiez que l'utilisateur est un abonné (type 3)
        if user.type != 3:
            return Response({'message': 'Vous n\'êtes pas un abonné'},
                            status=status.HTTP_403_FORBIDDEN)

        # Obtenez les commandes de l'abonné actuel
        commandes_abonne = Commande.objects.filter(id_commandant=user).exclude(statut='Livré')

        # Sérialisez les commandes
        serializer = CommandeSerializer(commandes_abonne, many=True)

        return Response(serializer.data)

    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_commande(request, commande_id):
    try:
        # Assurez-vous que l'utilisateur connecté est authentifié
        user = request.user

        # Obtenez l'instance de la commande
        commande = Commande.objects.get(id_commande=commande_id)

        # Vérifiez que l'utilisateur est un abonné (type 3) et que la commande est en attente de livraison
        if user.type != 3 or commande.statut != 'En attente':
            return Response({'message': 'Vous n\'avez pas les permissions nécessaires pour modifier cette commande'},
                            status=status.HTTP_403_FORBIDDEN)

        # Mettez à jour les détails de la commande
        serializer = CommandeSerializer(commande, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            # Envoyez une alerte (notification ou email) au vendeur indiquant que la commande a été modifiée
            # (Implémentez la logique d'envoi d'alerte ici)

            return Response({'message': f"La commande {commande_id} a été modifiée."})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Commande.DoesNotExist:
        return Response({'message': f'Commande avec ID {commande_id} n\'existe pas'},
                        status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def supprimer_ligne_commande(request, ligne_commande_id):
    try:
        # Assurez-vous que l'utilisateur connecté est authentifié et est un abonné (type 3)
        user = request.user

        if user.type != 3:
            return Response({'message': 'Vous n\'êtes pas un abonné'},
                            status=status.HTTP_403_FORBIDDEN)

        # Obtenez l'instance de la ligne de commande
        ligne_commande = LigneCommande.objects.get(id_ligne_commande=ligne_commande_id)
        commande = ligne_commande.commande

        # Vérifiez que l'utilisateur est autorisé à modifier cette commande
        if user != commande.id_commandant:
            return Response({'message': 'Vous n\'avez pas les permissions nécessaires'},
                            status=status.HTTP_403_FORBIDDEN)

        # Supprimez la ligne de commande de la base de données
        ligne_commande.delete()

        return Response({'message': 'La ligne de commande a été supprimée avec succès'})

    except LigneCommande.DoesNotExist:
        return Response({'message': f'Ligne de commande avec ID {ligne_commande_id} n\'existe pas'},
                        status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def modifier_ligne_commande(request, ligne_commande_id):
    try:
        # Assurez-vous que l'utilisateur connecté est authentifié et est un abonné (type 3)
        user = request.user

        if user.type != 3:
            return Response({'message': 'Vous n\'êtes pas un abonné'},
                            status=status.HTTP_403_FORBIDDEN)

        # Obtenez l'instance de la ligne de commande
        ligne_commande = LigneCommande.objects.get(id_ligne_commande=ligne_commande_id)
        commande = ligne_commande.commande

        # Vérifiez que l'utilisateur est autorisé à modifier cette commande
        if user != commande.id_commandant:
            return Response({'message': 'Vous n\'avez pas les permissions nécessaires'},
                            status=status.HTTP_403_FORBIDDEN)

        # Mettez à jour les détails de la ligne de commande
        serializer = LigneCommandeSerializer(ligne_commande, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except LigneCommande.DoesNotExist:
        return Response({'message': f'Ligne de commande avec ID {ligne_commande_id} n\'existe pas'},
                        status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def annuler_commande(request, commande_id):
    try:
        # Assurez-vous que l'utilisateur connecté est authentifié
        user = request.user

        # Obtenez l'instance de la commande
        commande = Commande.objects.get(id_commande=commande_id)

        # Vérifiez que l'utilisateur est un abonné (type 3) et que la commande est en attente de livraison
        if user.type != 3 or commande.statut != 'En attente':
            return Response({'message': 'Vous n\'avez pas les permissions nécessaires pour annuler cette commande'},
                            status=status.HTTP_403_FORBIDDEN)

        # Mettez à jour le statut de la commande pour indiquer que l'abonné a demandé une annulation
        commande.statut = 'Demande annulation'
        commande.save()

        return Response({'message': 'Demande d\'annulation envoyée avec succès'})

    except Commande.DoesNotExist:
        return Response({'message': f'Commande avec ID {commande_id} n\'existe pas'},
                        status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
