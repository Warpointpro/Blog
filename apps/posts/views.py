from django.shortcuts import render
from apps.posts.forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from .models import Noticia
def home(request):
    noticias = Noticia.objects.all().order_by('-fecha')
    return render(request, 'posts/home.html', {'noticias': noticias})
def about(request):
    return render(request, 'posts/acerca_de.html')

def contacto(request):
    return render(request, 'posts/contacto.html')
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') # Redirige al login después de un registro exitoso
    else:
        form = CustomUserCreationForm()
    return render(request, 'posts/register.html', {'form': form})

class UserLoginView(LoginView):
    template_name = 'posts/login.html'
    authentication_form = AuthenticationForm

class UserLogoutView(LogoutView):
    next_page = 'login' # Redirige a la página de login después del logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PostForm

@login_required
def crear_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            noticia = form.save(commit=False)
            noticia.autor = request.user
            noticia.save()
            return redirect('home')  # Ajusta al nombre de tu vista principal
    else:
        form = PostForm()
    return render(request, 'posts/crear_noticia.html', {'form': form})

    