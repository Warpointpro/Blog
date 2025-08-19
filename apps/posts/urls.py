from django.urls import path
from . import views
from .views import NoticiaDeleteView
urlpatterns = [
    path('', views.home, name='home'),
   path('acerca_de/', views.about, name='acerca_de'),
    path('register/', views.register, name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('contacto/', views.contacto, name='contacto'),
    path('crear/', views.crear_post, name='crear_post'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    path('logout/', views.logout_view, name='logout'),
    path('post/<int:pk>/borrar/', NoticiaDeleteView.as_view(), name='borrar_post'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
]

        