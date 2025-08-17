from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Noticia(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)
    imagen = models.ImageField(upload_to='posts/', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='noticia_likes', blank=True)
imagen = models.ImageField(upload_to='posts/', blank=True, null=True)
def __str__(self):
        return self.titulo

def total_likes(self):
        return self.likes.count()
