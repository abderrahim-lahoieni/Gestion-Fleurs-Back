from django.urls import path
from core.views import login
from . import views

urlpatterns = [
    path('register',views.register),
    #path('login', login ,name='abonneLogin'),
    path('ContactUs',views.contact_us),
    path('ListerCommande',views.lister_commandes_abonne),
]