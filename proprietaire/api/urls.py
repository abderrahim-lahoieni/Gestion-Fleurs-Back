from django.urls import path
from core.api.views import login
from . import views

urlpatterns = [
    path('login',login,name='proprietaireLogin'),
    path('ChangePasswordVendeur/<int:vendeur_id>/',views.change_password_vendeur),
]