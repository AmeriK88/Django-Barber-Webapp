from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Cita, Resena
from datetime import datetime, time
from django.utils import timezone
from .models import UserProfile
from django_recaptcha.fields import ReCaptchaField


class CitaForm(forms.ModelForm):
    HORA_CHOICES = [
        ('09:30', '09:30 AM'),
        ('10:30', '10:30 AM'),
        ('11:30', '11:30 AM'),
        ('12:30', '12:30 PM'),
        ('16:00', '04:00 PM'),
        ('17:00', '05:00 PM'),
        ('18:00', '06:00 PM'),
        ('19:00', '07:00 PM'),
    ]

    hora = forms.ChoiceField(choices=HORA_CHOICES, label='Hora')

    class Meta:
        model = Cita
        fields = ['servicio', 'fecha', 'hora', 'comentario']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_fecha(self):
        fecha = self.cleaned_data['fecha']
        if fecha.weekday() >= 5: 
            raise ValidationError("No se pueden seleccionar citas para fines de semana.")
        today = timezone.now().date() 

        if fecha.date() < today:
            raise ValidationError("La fecha de la cita no puede ser en el pasado.")
        return fecha
    
    def clean_hora(self):
        hora = self.cleaned_data['hora']
        hora = datetime.strptime(hora, '%H:%M').time()  
        if hora < time(9, 30) or hora > time(19, 0):
            raise ValidationError("La hora seleccionada está fuera del rango permitido.")
        return hora

class ResenaForm(forms.ModelForm):
    class Meta:
        model = Resena
        fields = ['servicio', 'texto', 'puntuacion']
        widgets = {
            'servicio': forms.Select(attrs={'class': 'form-select'}),
            'texto': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'puntuacion': forms.RadioSelect(attrs={'class': 'rating'})
        }

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Correo electrónico')
    phone = forms.CharField(max_length=15, required=True, label='Teléfono')
    captcha = ReCaptchaField() 

    class Meta:
        model = User
        fields = ("username", "email", "phone", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.phone = self.cleaned_data["phone"]  
        if commit:
            user.save()
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