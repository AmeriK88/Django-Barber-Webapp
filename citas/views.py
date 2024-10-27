from datetime import datetime
from django.utils import timezone
from django.contrib.auth import logout as auth_logout, login as auth_login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count

from .models import Servicio, Resena, Imagen, Cita, UserProfile
from .forms import CitaForm, ResenaForm, CustomUserCreationForm, UserProfileForm, UserForm
from .utils import (enviar_confirmacion_cita, 
                    enviar_notificacion_modificacion_cita, 
                    enviar_notificacion_eliminacion_cita)
from .decorators import handle_exceptions

def home(request):
    return render(request, 'citas/home.html')

def servicios(request):
    servicios = Servicio.objects.all()
    
    return render(request, 'citas/servicios.html', {'servicios': servicios})

# Manejo de excepciones
@handle_exceptions
def register(request):
    # Verifica si solicitud es un POST
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        # Si el formulario es válido - se guarda el user y autentica
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            # Mensaje de éxito en UI
            messages.success(request, f'¡Échale mojo! Bienvenido a Ca\'Bigote, {user.username}! Cuenta operativa.')
            return redirect('citas:perfil_usuario')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})

# Manejo de excepciones
@handle_exceptions
def login_view(request):
    # Verifica si solicitud es un POST
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Obtenemos usuario del form e inicio de sesión
            user = form.get_user()
            auth_login(request, user)
            # Mensaje de éxito en UI
            messages.success(request, f'¡¿Qué pasó loco?! Bienvenido de nuevo, {user.username}!')
            return redirect('citas:perfil_usuario')
        else:
            # Mensaje de error en UI
            messages.error(request, '¡Eres un tolete! Nombre de usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
@handle_exceptions
def reservar_cita(request):
    # Obtener fechas completamente reservadas & excluye la opción vacía
    horas_por_dia = Cita.objects.values('fecha__date').annotate(total_citas=Count('hora')).filter(total_citas=len(CitaForm.HORA_CHOICES) - 1) 
    fechas_ocupadas = [entry['fecha__date'].isoformat() for entry in horas_por_dia]
    
    # Crea dicct de horas ocupadas por fecha
    horas_ocupadas_por_fecha = {cita.fecha.date().isoformat(): [] for cita in Cita.objects.all()}
    for cita in Cita.objects.all():
        horas_ocupadas_por_fecha[cita.fecha.date().isoformat()].append(cita.fecha.strftime("%H:%M"))
    # Valida formulario y muestra mensaje
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.usuario = request.user
            cita.fecha = timezone.make_aware(datetime.combine(form.cleaned_data['fecha'], form.cleaned_data['hora']))
            cita.save()
            enviar_confirmacion_cita(request.user.email, cita)
            messages.success(request, '¡Viejito! Ya tienes tu cita confirmada.')
            return redirect('citas:perfil_usuario')
    else:
        form = CitaForm()
    
    if not request.user.is_anonymous:
        messages.success(request, f'¡Mi niño¡ ¡Bienvenido {request.user.username}!')

    return render(request, 'citas/reservar_cita.html', {
        'form': form,
        'fechas_ocupadas': fechas_ocupadas,
        'horas_ocupadas_por_fecha': horas_ocupadas_por_fecha
    })

# Función ver citas & historial 
@login_required
@handle_exceptions
def ver_citas(request):
    citas_activas = Cita.objects.filter(usuario=request.user, fecha__gte=timezone.now())  
    citas_pasadas = Cita.objects.filter(usuario=request.user, fecha__lt=timezone.now()) 
    return render(request, 'citas/ver_citas.html', {'citas_activas': citas_activas, 'citas_pasadas': citas_pasadas})

# Editar citas según disponibilidad & manejo excepciones
@login_required
@handle_exceptions
def editar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id, usuario=request.user)
    # Verifica si la fecha ya ha pasado
    if cita.fecha < timezone.now():
        messages.error(request, '¡Ñooosss! ¡Se te fue el baifo! La fecha ya pasó.')
        return redirect('citas:ver_citas')
    
     # Obtiene las fechas ocupadas en las que todas las horas están reservadas
    horas_por_dia = Cita.objects.values('fecha__date').annotate(total_citas=Count('hora')).filter(total_citas=len(CitaForm.HORA_CHOICES))
    fechas_ocupadas = [entry['fecha__date'].isoformat() for entry in horas_por_dia]

    # Crea un diccionario para almacenar las horas ocupadas
    horas_ocupadas_por_fecha = {cita_existente.fecha.date().isoformat(): [] for cita_existente in Cita.objects.all()}
    for cita_existente in Cita.objects.all():
        horas_ocupadas_por_fecha[cita_existente.fecha.date().isoformat()].append(cita_existente.fecha.strftime("%H:%M"))

    # Verifica si el método de la petición es POST
    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            fecha = form.cleaned_data['fecha']
            hora = form.cleaned_data['hora']
            # Convierte  fecha y hora a aware si es necesario
            fecha_hora = timezone.make_aware(datetime.combine(fecha, hora)) if timezone.is_naive(datetime.combine(fecha, hora)) else datetime.combine(fecha, hora)

            # Verifica existencia de cita en la fecha y hora seleccionada excluyendo la editada
            if Cita.objects.filter(fecha=fecha_hora).exclude(id=cita_id).exists():
                form.add_error(None, "Ya existe una cita reservada en esa fecha y hora.")
            else:
                # Actualiza la fecha y hora de la cita
                cita.fecha = fecha_hora
                form.save()
                 # Envía una notificación via email
                enviar_notificacion_modificacion_cita(request.user.email, cita)
                messages.success(request, '¡Eres un puntal! Actualizaste tu cita.')
                return redirect('citas:ver_citas')
    else:
        form = CitaForm(instance=cita)
    
    return render(request, 'citas/editar_cita.html', {
        'form': form,
        'fechas_ocupadas': fechas_ocupadas,
        'horas_ocupadas_por_fecha': horas_ocupadas_por_fecha,
    })

# Función para eliminar cita
@login_required
@handle_exceptions
def eliminar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id, usuario=request.user)
    
    if not cita.puede_cancelar():
        return render(request, 'citas/eliminar_cita.html', {
            'cita': cita,
            'error_message': "¡Mi niño! No puedes cancelar citas con 24hrs de antelación."
        })

    if request.method == 'POST':
        cita_detalle = {
            'email': request.user.email,
            'servicio': cita.servicio.nombre,
            'fecha': cita.fecha,
            'hora': cita.hora
        }
        
        cita.delete()
        # Envía una notificación via email
        enviar_notificacion_eliminacion_cita(cita_detalle['email'], cita_detalle)
        messages.success(request, "¡Fuerte loco! Has cancelado tu cita.")
        return redirect('citas:ver_citas')

    return render(request, 'citas/eliminar_cita.html', {'cita': cita})

@login_required
@handle_exceptions
def logout_view(request):
    username = request.user.username
    auth_logout(request)
    messages.success(request, f'¡Nos vemos, {username}, vuelve pronto puntalillo!')
    return redirect('citas:home')

@handle_exceptions
def ver_resenas(request):
    form = ResenaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        resena = form.save(commit=False)
        resena.usuario = request.user
        resena.save()
        return redirect('citas:resenas')
    
    resenas = Resena.objects.all()
    estrellas = list(range(1, 6))
    return render(request, 'citas/resenas.html', {'form': form, 'resenas': resenas, 'estrellas': estrellas})

@login_required
@handle_exceptions
def agregar_resena(request):
    form = ResenaForm(request.POST or None)
    if form.is_valid():
        resena = form.save(commit=False)
        resena.usuario = request.user
        resena.save()
        messages.success(request, "¡Viva la virgen del Carmen! ¡Aguita papá la reseña!.")
        return redirect('citas:resenas')

    return render(request, 'citas/agregar_resena.html', {'form': form})

@handle_exceptions
def ver_imagenes(request):
    imagenes = Imagen.objects.all()
    return render(request, 'citas/imagenes.html', {'imagenes': imagenes})

@handle_exceptions
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Imagen, id=producto_id)
    return render(request, 'citas/detalle_producto.html', {'producto': producto})

@login_required
@handle_exceptions
def perfil_usuario(request):
    citas_activas = Cita.objects.filter(usuario=request.user, fecha__gte=timezone.now()).order_by('fecha')
    return render(request, 'citas/perfil_usuario.html', {'citas': citas_activas})

@login_required
@handle_exceptions
def editar_perfil_usuario(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=user_profile)
        user_form = UserForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)
        
        if profile_form.is_valid() and user_form.is_valid() and password_form.is_valid():
            user_form.save()
            profile_form.save()
            password_form.save()
            update_session_auth_hash(request, request.user)  
            messages.success(request, '¡Esa es niñote! Tu perfil ha sido actualizado.')
            return redirect('citas:editar_perfil_usuario')
        else:
            if not password_form.is_valid():
                messages.error(request, '¡Ños! Tú o el servidor están en la parra. Prueba de nuevo puntal.')
    else:
        profile_form = UserProfileForm(instance=user_profile)
        user_form = UserForm(instance=request.user)
        password_form = PasswordChangeForm(user=request.user)

    context = {
        'profile_form': profile_form,
        'user_form': user_form,
        'password_form': password_form,
        'username': request.user.username,
        'current_email': request.user.email,
        'current_phone': user_profile.telefono
    }

    return render(request, 'citas/editar_perfil.html', context)