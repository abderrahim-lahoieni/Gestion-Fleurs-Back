from django.urls import path
from . import views

urlpatterns = [
    path('logout',views.logout),
    path('changePassword', views.change_password),
    path('Commander', views.add_Commande),
]