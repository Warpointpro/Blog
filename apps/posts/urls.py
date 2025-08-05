from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
   path('acerca_de/', views.about, name='acerca_de'),
]