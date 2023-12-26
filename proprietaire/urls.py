from django.urls import path, re_path
from . import views
app_name = 'proprietaire'
urlpatterns = [
    path('create/', views.cuFleur, name='createFleur'),
    path('update/<int:id>/', views.cuFleur, name='updateFleur'),
    path('delete/<int:id>/', views.deleteFleur, name='deleteFleur'),
    path('fleurs_list/', views.FleursList, name='fleursList'),


]