from django.shortcuts import get_object_or_404, render
from core.models import Fleur, Famille,Fichesoin, Magasin, Parfum, Bouquet
from .forms import FleurForm,FichesoinForm, FamilleForm, MagasinForm, ParfumForm, BouquetForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from core.serializers import FleurSerializer,FichesoinSerializer, FamilleSerializer, Magasinserializer, ParfumSerializer, BouquetSerializer
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view

# create and update
@csrf_exempt
@api_view(['POST'])
def cuFleur(request, id=None):
    response_data = {'status': 'error', 'message': 'Erreur lors du traitement de la requête.'}

    if id:
        fleur_instance = get_object_or_404(Fleur, pk=id)
    else:
        fleur_instance = Fleur()
    if request.method == 'POST':
        form = FleurForm(request.POST, request.FILES, instance=fleur_instance)
        if form.is_valid():
           form.save()
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
@api_view(['DELETE'])
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
@api_view(['POST'])
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

@api_view(['DELETE'])
@csrf_exempt
def deleteFicheSoin(request, id):
    fiche_soin = get_object_or_404(Fichesoin, pk=id)

    try:
        fiche_soin.delete()
        response_data = {'status': 'success', 'message': 'La fiche soin a été supprimée avec succès.'}
    except Exception as e:
        response_data = {'status': 'error', 'message': f"Erreur lors de la suppression de la fiche soin : {str(e)}"}

    return JsonResponse(response_data)


# create and update
@csrf_exempt
@api_view(['POST'])
def cuFamille(request, id=None):
    response_data = {'status': 'error', 'message': 'Erreur lors du traitement de la requête.'}

    if id:
        famille_instance = get_object_or_404(Famille, pk=id)
    else:
        famille_instance = Famille()

    if request.method == 'POST':
        form = FamilleForm(request.POST, request.FILES, instance=famille_instance)
        if form.is_valid():
           form.save()
           if id:
              response_data = {'status': 'success', 'message': 'La famille a été  mise à jour avec succès.'}
           else :
              response_data = {'status': 'success', 'message': 'La famille a été créée avec succès.'}

        else:
         if id:
             response_data['message'] = 'Erreur lors de la mise à jour de la famille. Veuillez vérifier les informations fournies.'
         else:
             response_data['message'] = 'Erreur lors de la création  de la famille. Veuillez vérifier les informations fournies.'
        response_data['errors'] = form.errors
    return JsonResponse(response_data)

@api_view(['GET'])
def FamilleList(request):
    famille = Famille.objects.all()
    serializer = FamilleSerializer(famille, many=True)
    content = JSONRenderer().render(serializer.data)  # Serialize the data using JSONRenderer
    return Response(content, content_type='application/json')

@api_view(['DELETE'])
@csrf_exempt
def deleteFamille(request, id):
    famille = get_object_or_404(Famille, pk=id)

    try:
        famille.delete()
        response_data = {'status': 'success', 'message': 'La famille a été supprimée avec succès.'}
    except Exception as e:
        response_data = {'status': 'error', 'message': f"Erreur lors mise a jour de la famille : {str(e)}"}

    return JsonResponse(response_data)

@api_view(['POST'])
@csrf_exempt
def cuMagasin(request, id=None):
    response_data = {'status': 'error', 'message': 'Erreur lors du traitement de la requête.'}

    if id:
        magasin_instance = get_object_or_404(Magasin, pk=id)
    else:
        magasin_instance = Magasin()

    if request.method == 'POST':
        form = MagasinForm(request.POST, instance=magasin_instance)
        if form.is_valid():
            form.save()
            if id:
                response_data = {'status': 'success', 'message': 'Le magasin a été mis à jour avec succès.'}
            else:
                response_data = {'status': 'success', 'message': 'Le magasin a été créé avec succès.'}
        else:
            if id:
                response_data['message'] = 'Erreur lors de la mise à jour du magasin. Veuillez vérifier les informations fournies.'
            else:
                response_data['message'] = 'Erreur lors de la création du magasin. Veuillez vérifier les informations fournies.'
            response_data['errors'] = form.errors
    return JsonResponse(response_data)


@api_view(['POST'])
@csrf_exempt
def cuBouquet(request, id=None):
    response_data = {'status': 'error', 'message': 'Erreur lors du traitement de la requête.'}

    if id:
        bouquet_instance = get_object_or_404(Bouquet, pk=id)
    else:
        bouquet_instance = Bouquet()

    if request.method == 'POST':
        form = BouquetForm(request.POST, request.FILES,instance=bouquet_instance)
        if form.is_valid():
            form.save()
            if id:
                response_data = {'status': 'success', 'message': 'Le bouquet a été mis à jour avec succès.'}
            else:
                response_data = {'status': 'success', 'message': 'Le bouquet a été créé avec succès.'}
        else:
            if id:
                response_data['message'] = 'Erreur lors de la mise à jour du bouquet. Veuillez vérifier les informations fournies.'
            else:
                response_data['message'] = 'Erreur lors de la création du bouquet. Veuillez vérifier les informations fournies.'
                response_data['errors'] = form.errors
    return JsonResponse(response_data)


@api_view(['GET'])
def BouquetList(request):
    bouquet = Bouquet.objects.all()
    serializer = BouquetSerializer(bouquet, many=True)
    content = JSONRenderer().render(serializer.data)  # Serialize the data using JSONRenderer
    return Response(content, content_type='application/json')

@api_view(['DELETE'])
@csrf_exempt
def deleteBouquet(request, id):
    bouquet = get_object_or_404(Bouquet, pk=id)

    try:
        bouquet.delete()
        response_data = {'status': 'success', 'message': 'Le bouquet a été supprimée avec succès.'}
    except Exception as e:
        response_data = {'status': 'error', 'message': f"Erreur lors du bouquet. : {str(e)}"}

    return JsonResponse(response_data)


@api_view(['POST'])
@csrf_exempt
def cuParfum(request, id=None):
    response_data = {'status': 'error', 'message': 'Erreur lors du traitement de la requête.'}

    if id:
        parfum_instance = get_object_or_404(Parfum, pk=id)
    else:
        parfum_instance = Parfum()

    if request.method == 'POST':
        form = ParfumForm(request.POST, request.FILES,instance=parfum_instance)
        if form.is_valid():
            form.save()
            if id:
                response_data = {'status': 'success', 'message': 'Le parfum a été mis à jour avec succès.'}
            else:
                response_data = {'status': 'success', 'message': 'Le parfum a été créé avec succès.'}
        else:
            if id:
                response_data['message'] = 'Erreur lors de la mise à jour du parfum. Veuillez vérifier les informations fournies.'
            else:
                response_data['message'] = 'Erreur lors de la création du parfum. Veuillez vérifier les informations fournies.'
                response_data['errors'] = form.errors
    return JsonResponse(response_data)


@api_view(['GET'])
def ParfumList(request):
    parfum = Parfum.objects.all()
    serializer = BouquetSerializer(parfum, many=True)
    content = JSONRenderer().render(serializer.data)  # Serialize the data using JSONRenderer
    return Response(content, content_type='application/json')

@api_view(['DELETE'])
@csrf_exempt
def deletParfum(request, id):
    parfum = get_object_or_404(Parfum, pk=id)

    try:
        parfum.delete()
        response_data = {'status': 'success', 'message': 'Le parfum a été supprimée avec succès.'}
    except Exception as e:
        response_data = {'status': 'error', 'message': f"Erreur lors du parfum. : {str(e)}"}

    return JsonResponse(response_data)
