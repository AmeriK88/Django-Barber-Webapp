# Proyecto de Gestión de Citas

Este es un proyecto de gestión de citas desarrollado con Django. La aplicación permite a los usuarios registrar, iniciar sesión, reservar citas, ver y gestionar sus citas (editar y eliminar), recepción de confirmación via email de cita generada, y agregar reseñas, edición de perfil y datos del perfil como contraseña, email y teléfono, sección de productos con vista detallada del producto seleccionado. Manejo de errores y excepciones así como vistas personalizada de plantillas de error. También proporciona un panel de administración mejorado mediante el uso de la biblioteca Grappelli. 

# Estructura del Proyecto

## Models
- **Servicio**: Modela los servicios disponibles con nombre, descripción, precio e imagen.
- **Resena**: Permite a los usuarios dejar reseñas sobre los servicios.
- **Imagen**: Almacena imágenes relacionadas con los productos.
- **Cita**: Modela las citas que los usuarios pueden reservar.
- **UserProfile**: Almacena información adicional del usuario como correo electrónico y teléfono.

## Forms
- **CitaForm**: Formulario para reservar o editar citas con validación de fecha y hora.
- **ResenaForm**: Formulario para agregar reseñas.
- **CustomUserCreationForm**: Formulario de registro personalizado que incluye correo electrónico y teléfono.
- **UserProfileForm**: Formulario para editar el perfil del usuario.
- **UserForm**: Formulario para actualizar el correo electrónico del usuario.

## Views
- **home**: Página de inicio.
- **servicios**: Muestra todos los servicios y las citas del usuario si está autenticado.
- **register**: Registro de nuevos usuarios.
- **login_view**: Inicio de sesión de usuarios.
- **reservar_cita**: Reserva de una cita.
- **ver_citas**: Visualización de las citas del usuario.
- **editar_cita**: Edición de una cita.
- **eliminar_cita**: Eliminación de una cita.
- **logout_view**: Cierre de sesión.
- **ver_resenas**: Visualización y adición de reseñas.
- **agregar_resena**: Adición de una nueva reseña.
- **ver_imagenes**: Visualización de imágenes.
- **detalle_producto**: Detalle de un producto.
- **perfil_usuario**: Perfil del usuario con citas asociadas.
- **editar_perfil_usuario**: Edición del perfil del usuario.

## Contribución
Las contribuciones son bienvenidas. Si deseas contribuir a este proyecto, por favor sigue estos pasos:

1. **Haz un fork** del repositorio.
2. **Crea una nueva rama** para tu funcionalidad o corrección de errores.
3. **Realiza tus cambios** y haz commit.
4. **Envía un pull request** con una descripción clara de tus cambios.

## Características

- **Registro y Autenticación de Usuarios**: Los usuarios pueden registrarse, iniciar sesión y actualizar su perfil.
- **Gestión de Citas**: Permite a los usuarios reservar, ver, editar y cancelar citas.
- **Reseñas de Servicios**: Los usuarios pueden agregar reseñas a los servicios y ver las reseñas existentes.
- **Galería de Imágenes**: Los usuarios pueden ver detalles de productos a través de imágenes.
- **Panel de Administración Mejorado**: Utiliza Grappelli para una interfaz de administración más intuitiva y atractiva.

## Requisitos

-asgiref==3.8.1
-Django==5.1
-django-admin-interface==0.28.8
-django-colorfield==0.11.0
-django-environ==0.11.2
-django-grappelli==4.0.1
-mysqlclient==2.2.4
-pillow==10.4.0
-python-dateutil==2.9.0
-python-slugify==8.0.4
-six==1.16.0
-sqlparse==0.5.1
-text-unidecode==1.3
-tzdata==2024.1

## Instalación

1. **Clona el Repositorio**

   ```bash
   git clone https://github.com/<username>/<repo-name>.git
   cd <repo-name>

2. **Configura un Entorno Virtual

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows usa `venv\Scripts\activate`

3. **Instala las Dependencias
   
     ```bash
     pip install -r requirements.txt

4. Configura la Base de Datos

  Asegúrate de tener MariaDB instalado (o la base de datos que utilices) y crea una base de datos para tu proyecto. Luego, ajusta la configuración en settings.py.

5. **Aplica las Migraciones

   ```bash
   python manage.py migrate

6. Crea un Superusuario

   ```bash
   python manage.py createsuperuser

7. Inicia el Servidor de Desarrollo

     ```bash
     python manage.py runserver


Ahora puedes acceder a la aplicación en http://127.0.0.1:8000/. Si quieres acceder utilizando la misma red a través del código Qr, permite todas las conexiones de hosts en settings: ALLOWED_HOSTS = ['*']


## Panel de Administración
  El panel de administración se ha mejorado utilizando Grappelli. Puedes acceder al panel de administración en http://127.0.0.1:8000/admin/ con las credenciales del superusuario que creaste.

**Instalación de Grappelli
  Asegúrate de tener Grappelli instalado en tu entorno y de añadir 'grappelli' a la lista de INSTALLED_APPS en settings.py antes de 'django.contrib.admin'. Puedes instalarlo con:  pip install django-grappelli


## Imágenes

![Captura de pantalla 2024-08-25 214350](https://github.com/user-attachments/assets/cb95dd76-de42-48a6-96df-981eb3193f16)
![Captura de pantalla 2024-08-25 214229](https://github.com/user-attachments/assets/54537808-36a9-4fa4-a4da-5783ad205d93)
![Captura de pantalla 2024-08-25 214214](https://github.com/user-attachments/assets/e778de0b-6cf6-458f-bfd5-936cad30f8f1)
![Captura de pantalla 2024-08-25 214205](https://github.com/user-attachments/assets/de19901e-7005-463e-a755-7b16e52f579c)
![Captura de pantalla 2024-08-25 214156](https://github.com/user-attachments/assets/67ac5dcb-d7c6-4fed-a45c-95cefdbe16df)
![Captura de pantalla 2024-08-25 214144](https://github.com/user-attachments/assets/60ddc3b6-a46a-4d35-8e63-473721d4df5c)
![Captura de pantalla 2024-08-25 214116](https://github.com/user-attachments/assets/4962b5de-ea2d-414a-8a49-05318c57a29c)
![Captura de pantalla 2024-08-25 214108](https://github.com/user-attachments/assets/dd03fe4b-a399-4875-82bb-66913599d997)
![Captura de pantalla 2024-08-25 214630](https://github.com/user-attachments/assets/ae862245-037e-4c99-a23a-4039359668ab)
![Captura de pantalla 2024-08-25 214618](https://github.com/user-attachments/assets/a4917a93-0045-4488-a0b2-9f24e2786840)
![Captura de pantalla 2024-08-25 214559](https://github.com/user-attachments/assets/fd6bca65-4ff8-4a38-a258-bbfbf7a72014)
![Captura de pantalla 2024-08-25 214551](https://github.com/user-attachments/assets/dfb0718f-b7c9-49c0-af47-121159d57b78)
![Captura de pantalla 2024-08-25 214543](https://github.com/user-attachments/assets/a1116bd9-3c47-48c3-ac28-f9876eeea3b1)
![Captura de pantalla 2024-08-25 214528](https://github.com/user-attachments/assets/c6c2e1a3-7b8f-41f4-ad23-5b985490deb0)

![Captura de pantalla 2024-08-25 214528](https://github.com/user-attachments/assets/02651725-54c3-48c9-bda8-b94d4e24142b)

