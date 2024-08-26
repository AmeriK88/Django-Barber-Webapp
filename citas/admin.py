from django.contrib import admin
from django.utils.html import format_html
from .models import Servicio, Cita, Resena, Imagen

# Register your models here.
@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'precio')  # Muestra estos campos en la lista
    search_fields = ('nombre',)  # Permite buscar por nombre

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'servicio', 'fecha')  # Muestra estos campos en la lista
    list_filter = ('fecha',)  # Permite filtrar por fecha
    search_fields = ('usuario__username', 'servicio__nombre')  # Permite buscar por usuario y servicio

@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'servicio', 'texto', 'fecha', 'puntuacion')  # Muestra estos campos en la lista
    search_fields = ('usuario__username', 'servicio__nombre', 'texto')  # Permite buscar por usuario, servicio y texto
    list_filter = ('fecha', 'puntuacion')  # Permite filtrar por fecha y puntuación

@admin.register(Imagen)
class ImagenAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'mostrar_imagen')  # Muestra título y miniatura de la imagen

    def mostrar_imagen(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.imagen.url)
        return 'No image'
    mostrar_imagen.allow_tags = True
    mostrar_imagen.short_description = 'Imagen'
