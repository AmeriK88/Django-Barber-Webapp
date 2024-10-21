import qrcode

# URL a la que se redirigirá el código QR
url = 'http://192.168.0.14:8000/register/' 

# Crear una instancia del generador de QR
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

# Añadir la URL al QR
qr.add_data(url)
qr.make(fit=True)

# Crear una imagen del QR
img = qr.make_image(fill='black', back_color='white')

# Guardar la imagen del QR
img.save('registro_qr.png')
