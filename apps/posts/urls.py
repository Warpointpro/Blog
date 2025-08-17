from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
   path('acerca_de/', views.about, name='acerca_de'),
    path('register/', views.register, name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('contacto/', views.contacto, name='contacto'),
    path('crear/', views.crear_post, name='crear_post'),
]

        