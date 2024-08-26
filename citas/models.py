from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    imagen = models.ImageField(upload_to='servicios/', blank=True, null=True)

    def __str__(self):
        return self.nombre

class Resena(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    servicio = models.ForeignKey('Servicio', on_delete=models.CASCADE)
    texto = models.TextField()  
    fecha = models.DateTimeField(default=timezone.now)
    puntuacion = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=1) 
    
    def __str__(self):
        return f"Reseña de {self.usuario.username} - {self.servicio.nombre} - {self.texto[:50]} - {self.puntuacion} estrellas"

class Imagen(models.Model):
    titulo = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='productos/')
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.titulo

class Cita(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    fecha = models.DateTimeField()  
    hora = models.TimeField() 
    comentario = models.TextField(blank=True, null=True) 

    def __str__(self):
        return f'Cita para {self.usuario} el {self.fecha.date()} a las {self.hora}'
    
    def puede_cancelar(self):
        # Permitir cancelar hasta 24 horas antes de la cita
        limite_cancelacion = self.fecha - timezone.timedelta(days=1)
        return timezone.now() < limite_cancelacion
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)
    telefono = models.CharField(max_length=20, blank=True, null=True)  # Teléfono opcional

    def __str__(self):
        return self.user.username
