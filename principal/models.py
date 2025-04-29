from django.db import models

# Create your models here.


# esto es nuevo
class Post(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    categoria = models.CharField(max_length=50)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.titulo


# fin de nuevo
