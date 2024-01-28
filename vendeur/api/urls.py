from django.urls import path
from core.api.views import login

urlpatterns = [
    path('login',login ,name='vendeurLogin'),
]