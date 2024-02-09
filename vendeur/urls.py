from django.urls import path
from . import views
from core.views import login

urlpatterns = [
    ## path('login',login ,name='vendeurLogin'),
    path('modifier_statut_commande/<int:commande_id>/', views.modifier_statut_commande),
    path('commandesEnattente', views.commandesEnattente),
    path('find_product/<str:code>/', views.FindProduct),
]  