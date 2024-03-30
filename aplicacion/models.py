from django.db import models
from django.contrib.auth.models import User

class Libro(models.Model):
    titulo = models.CharField(max_length=80)
    autor = models.CharField(max_length=60)
    descripcion = models.CharField(max_length=200, null=True) 
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    genero = models.CharField(max_length=40)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    fecha = models.DateTimeField(auto_now_add=True, null=True)
    imagen = models.ImageField(null=True, blank=True, upload_to="libros/", default=None)
    ubicacion = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f"{self.titulo}"

    class Meta:
        ordering = ['-fecha']

class Avatar(models.Model):
    imagen = models.ImageField(upload_to="avatares")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} {self.imagen}"

class Comentario(models.Model):
    objeto_comentado = models.ForeignKey(Libro, related_name='comentarios', on_delete=models.CASCADE, null=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    mensaje = models.TextField(null=True, blank=True)
    fechaComentario = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fechaComentario']

    def __str__(self):
        return f"Comentario por {self.usuario} en {self.fechaComentario}"

class Wishlist(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    libros = models.ManyToManyField(Libro)