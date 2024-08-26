from django.core.mail import send_mail
from django.conf import settings

def enviar_confirmacion_cita(usuario_email, cita):
    asunto = 'Confirmación de tu cita en Ca´Bigote Barber Shop'
    mensaje = f"""
    Estimado usuario,

    Gracias por reservar una cita con nosotros. Aquí están los detalles de tu cita:

    Servicio: {cita.servicio.nombre}
    Fecha: {cita.fecha}
    Hora: {cita.hora}
    Comentario: {cita.comentario}

    Si necesitas hacer algún cambio, por favor, contáctanos.

    ¡Te esperamos!

    Atentamente,
    Ca´Bigote Barber Shop
    """
    send_mail(
        asunto,
        mensaje,
        settings.EMAIL_HOST_USER,
        [usuario_email],
        fail_silently=False,
    )
