from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

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
 
    def __str__(self):
        return self.titulo

    def total_likes(self):
        return self.likes.count()
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey('Noticia', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} - {self.post.titulo[:20]}"

    def get_absolute_url(self):
        # Esto permite que UpdateView sepa a dónde ir tras editar
        return reverse('post_detail', kwargs={'pk': self.post.pk})



