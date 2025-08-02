from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone

class Categoria(models.Model):
    """
    Define la tabla de Categorías en la base de datos.
    Una noticia (Post) puede pertenecer a una de estas categorías.
    """
    nombre = models.CharField(max_length=50, null=False)

    def str(self):
        return self.nombre

class Post(models.Model):
    """
    Define la tabla de Posts en la base de datos.
    Aquí se almacenará toda la información de las noticias.
    """
    titulo = models.CharField(max_length=100, null=False)
    sub_titulo = models.CharField(max_length=100, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True)
    texto = models.TextField(null=False)
    activo = models.BooleanField(default=True)
    # Relación: Un post tiene una categoría. Si se borra la categoría, el campo en el post se pone nulo.
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True)
    imagen = models.ImageField(null=True, blank=True, upload_to='posts', default='posts/default.png')
    publicado = models.DateTimeField(default=timezone.now)

    def str(self):
        return self.titulo

    def delete(self, using=None, keep_parents=False):
        # Borra el archivo de imagen asociado al post antes de borrar el post.
        self.imagen.storage.delete(self.imagen.name)
        super().delete()

    class Meta:
        ordering = ('-publicado',)