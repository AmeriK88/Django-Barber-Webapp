from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import editar_perfil_usuario

app_name = 'citas'


urlpatterns = [
    path('', views.home, name='home'),  
    path('servicios/', views.servicios, name='servicios'),
    path('reservar/', views.reservar_cita, name='reservar_cita'),
    path('resenas/', views.ver_resenas, name='resenas'),
    path('agregar_resena/', views.agregar_resena, name='agregar_resena'),
    path('imagenes/', views.ver_imagenes, name='imagenes'),
    path('register/', views.register, name='register'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),  
    path('citas/', views.ver_citas, name='ver_citas'),
    path('citas/editar/<int:cita_id>/', views.editar_cita, name='editar_cita'),
    path('citas/eliminar/<int:cita_id>/', views.eliminar_cita, name='eliminar_cita'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('perfil/editar/', editar_perfil_usuario, name='editar_perfil_usuario'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    
]

