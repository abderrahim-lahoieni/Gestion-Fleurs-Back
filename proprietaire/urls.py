from django.urls import path, re_path
from . import views
app_name = 'proprietaire'
urlpatterns = [
    path('fleur/create/', views.cuFleur, name='createFleur'),
    path('fleur/update/<int:id>/', views.cuFleur, name='updateFleur'),
    path('fleur/delete/<int:id>/', views.deleteFleur, name='deleteFleur'),
    path('fleur/list/', views.FleursList, name='fleursList'),

    path('fichesoin/create/', views.cuFicheSoin, name='createfichesoin'),
    path('fichesoin/update/<int:id>/', views.cuFicheSoin, name='updatefichesoin'),
    path('fichesoin/delete/<int:id>/', views.deleteFicheSoin, name='deletefichesoin'),
    path('fichesoin/list/', views.FichesSoinList, name='fichesoinList'),    

    path('famille/create/', views.cuFamille, name='createfamille'),
    path('famille/update/<int:id>/', views.cuFamille, name='updatefamille'),

    path('magasin/create/', views.cuMagasin, name='create_magasin'),
    path('magasin/list/', views.MagasinList, name='create_magasin'),
    path('magasin/update/<int:id>/', views.cuMagasin, name='update_magasin'),
    path('magasin/delete/<int:id>/', views.deleteMagasin, name='delete_magasin'),


]