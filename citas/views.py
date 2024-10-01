from django.contrib.auth import logout as auth_logout, login as auth_login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from datetime import datetime
from django.utils import timezone
from .models import Servicio, Resena, Imagen, Cita, UserProfile
from .forms import CitaForm, ResenaForm, CustomUserCreationForm, UserProfileForm, UserForm
from .utils import enviar_confirmacion_cita
from .decorators import handle_exceptions
from django.db.models import Count

def home(request):
    return render(request, 'citas/home.html')

def servicios(request):
    servicios = Servicio.objects.all()
    citas = Cita.objects.filter(usuario=request.user) if request.user.is_authenticated else None
    return render(request, 'citas/servicios.html', {'servicios': servicios, 'citas': citas})

@handle_exceptions
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user:
                auth_login(request, user)
                messages.success(request, f'¡Bienvenido a Ca\'Bigote, {username}! Tu cuenta ha sido creada con éxito.')

                return redirect('citas:perfil_usuario')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@handle_exceptions
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, f'Bienvenido de nuevo, {user.username}!')

            return redirect('citas:perfil_usuario')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
@handle_exceptions
def reservar_cita(request):
    # Obtener fechas donde las horas estén completamente ocupadas
    horas_por_dia = Cita.objects.values('fecha__date').annotate(total_citas=Count('hora')).filter(total_citas=len(CitaForm.HORA_CHOICES))
    fechas_ocupadas = [entry['fecha__date'].isoformat() for entry in horas_por_dia]  # Convertir a formato ISO para JavaScript

    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            fecha = form.cleaned_data['fecha']
            hora = form.cleaned_data['hora']
            fecha_hora = datetime.combine(fecha, hora)

            if timezone.is_naive(fecha_hora):
                fecha_hora = timezone.make_aware(fecha_hora, timezone.get_current_timezone())
            
            if Cita.objects.filter(fecha=fecha_hora).exists():
                form.add_error(None, "Ya existe una cita reservada en esa fecha y hora.")
            else:
                cita = form.save(commit=False)
                cita.usuario = request.user
                cita.fecha = fecha_hora
                cita.save()
                enviar_confirmacion_cita(request.user.email, cita)
                messages.success(request, '¡Cita reservada con éxito!')
                return redirect('citas:perfil_usuario')
    else:
        form = CitaForm()

    return render(request, 'citas/reservar_cita.html', {'form': form, 'fechas_ocupadas': fechas_ocupadas})


@login_required
@handle_exceptions
def ver_citas(request):
    citas = Cita.objects.filter(usuario=request.user)
    return render(request, 'citas/ver_citas.html', {'citas': citas})

@login_required
@handle_exceptions
def editar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id, usuario=request.user)

    # Verifica caducidad cita
    if cita.fecha < timezone.now():
        messages.error(request, 'No puedes editar una cita que ya ha finalizado.')
        return redirect('citas:ver_citas')
    
    # Obtener fechas con horas completamente ocupadas
    horas_por_dia = Cita.objects.values('fecha__date').annotate(total_citas=Count('hora')).filter(total_citas=len(CitaForm.HORA_CHOICES))
    fechas_ocupadas = [entry['fecha__date'].isoformat() for entry in horas_por_dia]

    if request.method == 'POST':
        form = CitaForm(request.POST, instance=cita)
        if form.is_valid():
            fecha = form.cleaned_data['fecha']
            hora = form.cleaned_data['hora']
            fecha_hora = datetime.combine(fecha, hora)

            # Convertir a timezone-aware si USE_TZ está habilitado
            if timezone.is_naive(fecha_hora):
                fecha_hora = timezone.make_aware(fecha_hora, timezone.get_current_timezone())
            
            cita.fecha = fecha_hora
            cita.hora = hora
            form.save()
            
            messages.success(request, '¡Cita actualizada con éxito!')
            return redirect('citas:ver_citas')
    else:
        form = CitaForm(instance=cita)
    
    return render(request, 'citas/editar_cita.html', {'form': form, 'fechas_ocupadas': fechas_ocupadas})


@login_required
@handle_exceptions
def eliminar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id, usuario=request.user)
    
    if not cita.puede_cancelar():
        return render(request, 'citas/eliminar_cita.html', {
            'cita': cita,
            'error_message': "No puedes cancelar la cita menos de 24 horas antes."
        })

    if request.method == 'POST':
        cita.delete()
        messages.success(request, "La cita ha sido cancelada.")
        return redirect('citas:ver_citas')

    return render(request, 'citas/eliminar_cita.html', {'cita': cita})
    

@login_required
@handle_exceptions
def logout_view(request):
    username = request.user.username
    auth_logout(request)
    messages.success(request, f'¡Hasta pronto, {username}!')
    return redirect('citas:home')

@handle_exceptions
def ver_resenas(request):
    form = None
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ResenaForm(request.POST)
            if form.is_valid():
                resena = form.save(commit=False)
                resena.usuario = request.user
                resena.save()
                return redirect('citas:resenas')
        else:
            form = ResenaForm()
    resenas = Resena.objects.all()
    estrellas = list(range(1, 6))
    context = {
        'form': form,
        'resenas': resenas,
        'estrellas': estrellas
    }
    return render(request, 'citas/resenas.html', context)

@login_required
@handle_exceptions
def agregar_resena(request):
    if request.method == 'POST':
        form = ResenaForm(request.POST)
        if form.is_valid():
            resena = form.save(commit=False)
            resena.usuario = request.user
            resena.save()
            return redirect('citas:resenas')
    else:
        form = ResenaForm()
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
    citas = Cita.objects.filter(usuario=request.user)
    return render(request, 'citas/perfil_usuario.html', {'citas': citas})

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
            messages.success(request, 'Tu perfil ha sido actualizado exitosamente.')
            return redirect('citas:editar_perfil_usuario')
        else:
            if not password_form.is_valid():
                messages.error(request, 'Hubo un problema con la actualización de la contraseña. Por favor, corrige los errores indicados.')
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

