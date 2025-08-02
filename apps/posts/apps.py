from django.contrib import admin
from .models import Categoria, Post

# --- Clase para personalizar la vista de Post en el admin ---
class PostAdmin(admin.ModelAdmin):
    """
    Personaliza la forma en que el modelo Post se muestra en el panel de administrador.
    """
    # Columnas que se mostrarán en la lista de posts
    list_display = ('titulo', 'publicado', 'categoria', 'activo')
    # Campos por los que se puede buscar
    search_fields = ('titulo', 'texto')
    # Filtros que aparecerán en la barra lateral
    list_filter = ('categoria', 'activo')

# --- Registramos los modelos en el sitio de administración ---
admin.site.register(Post, PostAdmin)