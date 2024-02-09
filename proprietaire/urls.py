from django.urls import path, re_path
from . import views
from core.views import ParfumDetail, FleurDetail, BouquetDetail, FichesoinDetail, FamilleDetail, MagasinDetail

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
    path('famille/list/', views.FamilleList, name='list_famille'),
    path('famille/delete/<int:id>/', views.deleteFamille, name='delete_famille'),

    path('magasin/create/', views.cuMagasin, name='create_magasin'),
    path('magasin/update/<int:id>/', views.cuMagasin, name='update_magasin'),
#    path('magazin/details/', views.DetailMagasin, name='details_magasin'),



    path('parfum/create/', views.cuParfum, name='create_parfum'),
    path('parfum/list/', views.ParfumList, name='create_parfum'),
    path('parfum/update/<int:id>/', views.cuParfum, name='update_parfum'),
    path('parfum/delete/<int:id>/', views.deletParfum, name='delete_parfum'),

    path('bouquet/create/', views.cuBouquet, name='create_bouquet'),
    path('bouquet/list/', views.BouquetList, name='create_bouquet'),
    path('bouquet/update/<int:id>/', views.cuBouquet, name='update_bouquet'),
    path('bouquet/delete/<int:id>/', views.deleteBouquet, name='delete_bouquet'),  

    path('parfum/<int:pk>/', ParfumDetail.as_view(), name='parfum-detail'),
    path('fleur/<int:pk>/', FleurDetail.as_view(), name='fleur-detail'),
    path('bouquet/<int:pk>/', BouquetDetail.as_view(), name='bouquet-detail'),
    path('fichesoin/<int:pk>/', FichesoinDetail.as_view(), name='fichesoin-detail'),          
    path('famille/<int:pk>/', FamilleDetail.as_view(), name='famille-detail'),          
    path('magasin/<int:pk>/', MagasinDetail.as_view(), name='magasin-detail'),          


]