from django.urls import path
from . import views

urlpatterns = [
    path('login',views.login),  
    path('logout',views.logout),
    path('changePassword', views.change_password),
    path('Commander', views.add_Commande),
    path('DetailsCommande/<int:commande_id>/',views.details_commande),
]