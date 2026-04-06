from django.db import models
from PIL import Image

class ImagenCarrusel(models.Model):
    imagen = models.ImageField(upload_to='carrusel/')

class RedSocial(models.Model):
    nombre = models.CharField(max_length=50)
    link = models.URLField()

class Sede(models.Model):
    ubicacion = models.CharField(max_length=200)
    fecha = models.DateField()
    hora = models.TimeField()
    horatermino = models.TimeField(null=True, blank=True)  # 👈 IMPORTANTE
    
class ImagenCarrusel(models.Model):
    imagen = models.ImageField(upload_to='carrusel/')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.imagen.path)

        # 🔥 TAMAÑO FIJO
        img = img.resize((1000, 1000), Image.Resampling.LANCZOS)

        img.save(self.imagen.path)