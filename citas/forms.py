from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Cita, Resena
from datetime import datetime, time
from django.utils import timezone
from .models import UserProfile
from django_recaptcha.fields import ReCaptchaField

# Formulario cita
class CitaForm(forms.ModelForm):
    HORA_CHOICES = [
        ('', 'Seleccione una hora'),
        ('09:30', '09:30 AM'),
        ('10:00', '10:00 AM'),
        ('10:30', '10:30 AM'),
        ('11:00', '11:00 AM'),
        ('11:30', '11:30 AM'),
        ('12:00', '12:00 PM'),
        ('12:30', '12:30 PM'),
        ('16:00', '04:00 PM'),
        ('16:30', '04:30 PM'),
        ('17:00', '05:00 PM'),
        ('17:30', '05:30 PM'),
        ('18:00', '06:00 PM'),
        ('18:30', '06:30 PM'),
        ('19:00', '07:00 PM'),
        ('19:30', '07:30 PM'),
    ]

    hora = forms.ChoiceField(choices=HORA_CHOICES, label='Hora')
    # Campos para el formulario
    class Meta:
        model = Cita
        fields = ['servicio', 'fecha', 'hora', 'comentario']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }
    # Manejo errores formulario
    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        if fecha.weekday() >= 5:
            raise forms.ValidationError("¡Puntalillo! Te recuerdo que el finde no curro.")
        today = timezone.now().date() 

        if fecha.date() < today:
            raise forms.ValidationError("¡Ñooosss! ¡Se te fue el baifo! La fecha ya pasó.")
        return fecha

    def clean_hora(self):
        hora = self.cleaned_data['hora']
        hora = datetime.strptime(hora, '%H:%M').time()
        if hora < time(9, 30) or hora > time(19, 0):
            raise forms.ValidationError("¡Se te fue el baifo! La hora está fuera del rango.")
        return hora

    def clean_hora(self):
        hora = self.cleaned_data.get('hora')
        if not hora or hora == '':  
            raise forms.ValidationError("Por favor, selecciona una hora válida.")
        
        hora = datetime.strptime(hora, '%H:%M').time()
        if hora < time(9, 30) or hora > time(19, 0):
            raise forms.ValidationError("¡Se te fue el baifo! La hora está fuera del rango.")
        return hora


# Formulario reseñas
class ResenaForm(forms.ModelForm):
    class Meta:
        model = Resena
        fields = ['servicio', 'texto', 'puntuacion']
        widgets = {
            'servicio': forms.Select(attrs={'class': 'form-select'}),
            'texto': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'puntuacion': forms.RadioSelect(attrs={'class': 'rating'})
        }

# Formulario registro usuario
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Correo electrónico')
    phone = forms.CharField(max_length=15, required=True, label='Teléfono')
    captcha = ReCaptchaField() 

    class Meta:
        model = User
        fields = ("username", "email", "phone", "password1", "password2")

    # Majejo errores formulario
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("!Chacho¡ Este email ya está registrado puntal.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("¡Estás bonito! Las contraseñas no coinciden.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        phone = self.cleaned_data["phone"]
        UserProfile.objects.create(user=user, telefono=phone, email=user.email)
        return user

    
class CustomAuthenticationForm(AuthenticationForm):
    captcha = ReCaptchaField()
    
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email', 'telefono']
        widgets = {
            'email': forms.EmailInput(attrs={'autocomplete': 'email'}),
            'telefono': forms.TextInput(attrs={'autocomplete': 'tel'}),
        }

class UserForm(forms.ModelForm):
     class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'autocomplete': 'email', 'id': 'user-email'}),
        }