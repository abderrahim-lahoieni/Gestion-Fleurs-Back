from django.shortcuts import get_object_or_404
from core.models import Fleur, Famille,Fichesoin
from .forms import FleurForm,FichesoinForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from core.serializers import FleurSerializer,FichesoinSerializer
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view

# create and update
@csrf_exempt
def cuFleur(request, id=None):
    response_data = {'status': 'error', 'message': 'Erreur lors du traitement de la requête.'}

    if id:
        fleur_instance = get_object_or_404(Fleur, pk=id)
    else:
        fleur_instance = Fleur()

    if request.method == 'POST':
        form = FleurForm(request.POST, request.FILES, instance=fleur_instance)
        if form.is_valid():
            famille_nom = form.cleaned_data.get('famille')
            fleur_instance = form.save(commit=False)

            if famille_nom:
                famille_instance, created = Famille.objects.get_or_create(nom=famille_nom)
                fleur_instance.famille = famille_instance

            fleur_instance.save()
            if id:
              response_data = {'status': 'success', 'message': 'La fleur a été  mise à jour avec succès.'}
            else :
              response_data = {'status': 'success', 'message': 'La fleur a été créée avec succès.'}

        else:
         if id:
             response_data['message'] = 'Erreur lors de la mise à jour de la fleur. Veuillez vérifier les informations fournies.'
         else:
             response_data['message'] = 'Erreur lors de la création  de la fleur. Veuillez vérifier les informations fournies.'
        response_data['errors'] = form.errors
    return JsonResponse(response_data)

@api_view(['GET'])
def FleursList(request):
    fleurs = Fleur.objects.all()
    serializer = FleurSerializer(fleurs, many=True)
    content = JSONRenderer().render(serializer.data)  # Serialize the data using JSONRenderer
    return Response(content, content_type='application/json')

@csrf_exempt
def deleteFleur(request, id):
    fleur = get_object_or_404(Fleur, pk=id)

    try:
        fleur.delete()
        response_data = {'status': 'success', 'message': 'La fleur a été supprimée avec succès.'}
    except Exception as e:
        response_data = {'status': 'error', 'message': f"Erreur lors de la suppression de la fleur : {str(e)}"}

    return JsonResponse(response_data)

# create & update fiche soin
@csrf_exempt
def cuFicheSoin(request, id=None):
    response_data = {'status': 'error', 'message': 'Erreur lors du traitement de la requête.'}

    if id:
        fiche_soin__instance = get_object_or_404(Fichesoin, pk=id)
    else:
        fiche_soin__instance = Fichesoin()

    if request.method == 'POST':
        form = FichesoinForm(request.POST, instance=fiche_soin__instance)
        if form.is_valid():
            form.save()
            if id:
              response_data = {'status': 'success', 'message': 'La fiche soin a été  mise à jour avec succès.'}
            else :
              response_data = {'status': 'success', 'message': 'La fiche soin a été créée avec succès.'}

        else:
         if id:
             response_data['message'] = 'Erreur lors de la mise à jour de la fiche soin. Veuillez vérifier les informations fournies.'
         else:
             response_data['message'] = 'Erreur lors de la création  de la fiche soin. Veuillez vérifier les informations fournies.'
        response_data['errors'] = form.errors
    return JsonResponse(response_data)

@api_view(['GET'])
def FichesSoinList(request):
    fichesSoin = Fichesoin.objects.all()
    serializer = FichesoinSerializer(fichesSoin, many=True)
    content = JSONRenderer().render(serializer.data)  # Serialize the data using JSONRenderer
    return Response(content, content_type='application/json')

@csrf_exempt
def deleteFicheSoin(request, id):
    fiche_soin = get_object_or_404(Fichesoin, pk=id)

    try:
        fiche_soin.delete()
        response_data = {'status': 'success', 'message': 'La fiche soin a été supprimée avec succès.'}
    except Exception as e:
        response_data = {'status': 'error', 'message': f"Erreur lors de la suppression de la fiche soin : {str(e)}"}

    return JsonResponse(response_data)

