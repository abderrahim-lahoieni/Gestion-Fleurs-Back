from django.shortcuts import render, redirect, get_object_or_404
from core.models import Fleur, Famille
from .forms import FleurForm
from django.http import JsonResponse

# create and update a flower view
def cuFleur(request, id=None):
    if id:
        fleur_instance = get_object_or_404(Fleur, pk=id)
    else:
        fleur_instance = Fleur()

    if request.method == 'POST':
        form = FleurForm(request.POST, request.FILES, instance=fleur_instance)
        if form.is_valid():
            famille_nom = form.cleaned_data.get('famille_nom')
            form.save()

            if famille_nom:
                famille_instance, created = Famille.objects.get_or_create(nom=famille_nom)

                fleur_instance.famille = famille_instance
                fleur_instance.save()
            response_data = {'status': 'success', 'message': 'La fleur a été créée avec succès.'}
            return JsonResponse(response_data)
        else:
            response_data = {'status': 'error', 'message': 'Erreur lors de la création de la fleur. Veuillez vérifier les informations fournies.'}
            return JsonResponse(response_data)                

            return redirect("proprietaire:fleursList")
    else:
        form = FleurForm(instance=fleur_instance)

    return render(request, 'core/testForm.html', {'formTitle': 'Veuillez remplir le formulaire ', 'btntext': 'Ajouter', 'form': form})

def FleursList(request):
    fleurs = Fleur.objects.all()
    return render(request, 'proprietaire/fleurs_list.html', {'fleurs': fleurs})



def deleteFleur(request, id):
    fleur = get_object_or_404(Fleur, pk=id)

    try:
        fleur.delete()
        response_data = {'status': 'success', 'message': 'La fleur a été supprimée avec succès.'}
    except Exception as e:
        response_data = {'status': 'error', 'message': f"Erreur lors de la suppression de la fleur : {str(e)}"}

    return JsonResponse(response_data)

