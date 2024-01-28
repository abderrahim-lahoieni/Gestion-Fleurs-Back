from django.urls import path
from . import views

urlpatterns = [
    path('modifier_statut_commande/<int:commande_id>/', views.modifier_statut_commande),
    path('commandes_par_statut/<str:statut>/', views.commandes_par_statut),

]  