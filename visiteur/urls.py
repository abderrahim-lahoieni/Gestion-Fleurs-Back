from django.urls import path
from proprietaire import views
from proprietaire.views import ParfumDetail, FleurDetail, BouquetDetail, FichesoinDetail, FamilleDetail, MagasinDetail

app_name = 'Visiteur'
urlpatterns = [
    path('fleur/list/',views.FleursList, name ='fleurList'),
    path('fichesoin/list/',views.FichesSoinList, name ='FichesSoinList'),    
    path('parfum/list/', views.ParfumList, name='create_parfum'),
    path('bouquet/list/', views.BouquetList, name='create_bouquet'),

    path('parfum/<int:pk>/', ParfumDetail.as_view(), name='parfum-detail'),
    path('fleur/<int:pk>/', FleurDetail.as_view(), name='fleur-detail'),
    path('bouquet/<int:pk>/', BouquetDetail.as_view(), name='bouquet-detail'),
    path('fichesoin/<int:pk>/', FichesoinDetail.as_view(), name='fichesoin-detail'),          
    path('famille/<int:pk>/', FamilleDetail.as_view(), name='famille-detail'),     

]