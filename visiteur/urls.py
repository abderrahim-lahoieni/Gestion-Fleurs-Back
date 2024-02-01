from django.urls import path
from proprietaire import views
app_name = 'Visiteur'
urlpatterns = [
    path('fleur/list/',views.FleursList, name ='fleurList'),
    path('fichesoin/list/',views.FichesSoinList, name ='FichesSoinList'),    
    path('parfum/list/', views.ParfumList, name='create_parfum'),
    path('bouquet/list/', views.BouquetList, name='create_bouquet'),

]