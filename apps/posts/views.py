from django.shortcuts import render
from apps.posts.forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from .models import Noticia
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.contrib import messages
from .forms import PostForm, CommentForm
def home(request):
    # 1. Capturar parámetros del formulario
    q = request.GET.get('q', '')               # texto de búsqueda
    categoria_id = request.GET.get('categoria', '')  # id categoría
    fecha = request.GET.get('fecha', '')       # asc / desc

    # 2. Iniciar el queryset base
    noticias = Noticia.objects.all()

    # 3. Filtrar por búsqueda en título o contenido
    if q:
        noticias = noticias.filter(titulo__icontains=q) | noticias.filter(contenido__icontains=q)

    # 4. Filtrar por categoría
    if categoria_id:
        noticias = noticias.filter(categoria_id=categoria_id)

    # 5. Ordenar por fecha
    if fecha == "asc":
        noticias = noticias.order_by("fecha")
    elif fecha == "desc":
        noticias = noticias.order_by("-fecha")
    else:
        noticias = noticias.order_by("-fecha")  # por defecto recientes

    # 6. Paginar resultados (ej: 5 por página)
    paginator = Paginator(noticias, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 7. Pasar categorías para el dropdown
    from .models import Categoria
    categorias = Categoria.objects.all()

    return render(request, 'posts/home.html', {
        'categorias': categorias,
        'page_obj': page_obj
    })
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
@login_required
def post_detail(request, pk):
    post = get_object_or_404(Noticia, pk=pk)
    liked = False
    if request.user.is_authenticated:
        liked = post.likes.filter(id=request.user.id).exists()
    return render(request, 'posts/post_detail.html', {
        'post': post,
        'liked': liked
    })
@login_required
def like_post(request, pk):
    post = get_object_or_404(Noticia, pk=pk)

    # Si el usuario ya dio like, lo quitamos; si no, lo añadimos
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('post_detail', pk=pk)
def logout_view(request):
    logout(request)
    return redirect('home')
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.contrib import messages
from .models import Noticia

class NoticiaDeleteView(DeleteView):
    model = Noticia
    template_name = 'posts/confirmar_borrado.html'
    success_url = reverse_lazy('home')

    def get_queryset(self):
        qs = super().get_queryset()
        # Si es staff/admin, ve todos los posts
        if self.request.user.is_staff:
            return qs
        # Si no es staff, solo ve sus propios posts
        return qs.filter(autor=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "El post fue borrado con éxito ✅")
        return super().delete(request, *args, **kwargs)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView, DeleteView
from .models import Comment

class CommentEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['content']  # Campo editable
    template_name = 'comments/edit_comment.html'

    def test_func(self):
        # Permite acceso si es el autor o un admin/staff
        comment = self.get_object()
        return self.request.user == comment.author or self.request.user.is_staff
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'comments/confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = self.object.post
        return context

    def test_func(self):
        # Igual que en edición, controla permisos
        comment = self.get_object()
        return self.request.user == comment.author or self.request.user.is_staff

    def get_success_url(self):
        # Después de borrar, vuelve al detalle de la noticia
        return self.object.post.get_absolute_url()

def post_detail(request, pk):
    post = get_object_or_404(Noticia, pk=pk)
    liked = post.likes.filter(id=request.user.id).exists()
    comments = post.comments.all().order_by('-created_at')

    if request.method == 'POST':
        # Procesar comentario nuevo
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('home')  # 🔹 Redirige al inicio después de comentar
    else:
        form = CommentForm()

    return render(request, 'posts/post_detail.html', {
        'post': post,
        'liked': liked,
        'comments': comments,
        'form': form
    })   
template_name = 'posts/edit_comment.html'
template_name = 'posts/confirm_delete_comment.html'
