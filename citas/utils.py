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

    En caso de no poder asistir, puede editar su cita desde nuestra app!

    ¡Te esperamos!

    Atentamente,
    Ca´Bigote Barber Shop

    ---

    Dirección: Calle Ejemplo 123, Ciudad
    Teléfono: +123 456 789
    Instagram: @cabigote_barber_shop
    ¡Síguenos para más novedades!git a
    """
    send_mail(
        asunto,
        mensaje,
        settings.EMAIL_HOST_USER,
        [usuario_email],
        fail_silently=False,
    )
