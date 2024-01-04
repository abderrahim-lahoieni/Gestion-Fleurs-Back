from django.urls import path, re_path
from proprietaire import views
app_name = 'Visiteur'
urlpatterns = [
    path('fleur/list',views.FleursList, name ='fleurList'),
    path('fichesoin/list',views.FichesSoinList, name ='FichesSoinList'),    

]