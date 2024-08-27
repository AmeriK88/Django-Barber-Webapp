from django.contrib import admin
from django.utils.html import format_html
from .models import Servicio, Cita, Resena, Imagen

# Register your models here.
@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'precio')  
    search_fields = ('nombre',)  

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'servicio', 'fecha')  
    list_filter = ('fecha',)  
    search_fields = ('usuario__username', 'servicio__nombre')  

@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'servicio', 'texto', 'fecha', 'puntuacion')  
    search_fields = ('usuario__username', 'servicio__nombre', 'texto')  
    list_filter = ('fecha', 'puntuacion')  

@admin.register(Imagen)
class ImagenAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'mostrar_imagen')  
    def mostrar_imagen(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.imagen.url)
        return 'No image'
    mostrar_imagen.allow_tags = True
    mostrar_imagen.short_description = 'Imagen'
