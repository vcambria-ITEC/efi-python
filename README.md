# EFI: API REST Miniblog

API REST para un miniblog desarrollada en Python y Flask. Este proyecto sirve como un backend robusto para gestionar contenido y usuarios, implementando características clave de seguridad y arquitectura moderna.

### Características Principales
* **Autenticación:** Sistema seguro basado en **JWT (JSON Web Tokens)**.
* **Roles:** Gestión de permisos con tres niveles: `admin`, `moderador`, y `usuario`.
* **Permisos:** Control de acceso detallado por endpoint según el rol del usuario.
* **Vistas:** Implementación de Vistas Basadas en Clases (Flask's `MethodView`).
* **Arquitectura:** Diseño basado en el patrón **Service-Repository** para una lógica de negocio desacoplada y mantenible.

---

## Tecnologías y Prerrequisitos

Antes de comenzar, asegúrate de tener instalado lo siguiente en tu sistema:

* **Python 3.10+** (Puedes descargarlo desde [python.org](https://www.python.org/downloads/))
* **XAMPP** (Necesario para la base de datos MySQL. Puedes descargarlo desde [apachefriends.org](https://www.apachefriends.org/index.html))

---

## Instalación y Configuración

Sigue estos pasos para poner en marcha el proyecto localmente.

### 1. Clonar el Repositorio
```
git clone https://github.com/vcambria-ITEC/efi-python.git
```
```
cd efi-python
```
### 2. Configurar la Base de Datos (XAMPP / MySQL)
1. Inicia XAMPP (o tu servicio de MySQL).


Ejemplo para iniciar XAMPP en Linux
```
sudo /opt/lampp/xampp start
```
2. Abre un gestor de base de datos (como phpMyAdmin en http://localhost/phpmyadmin).

3. Inicia sesión (usualmente el usuario por defecto es root sin contraseña).

4. Crea una nueva base de datos vacía. Puedes llamarla db_miniblog o como prefieras. No necesitas crear ninguna tabla, solo la base de datos.

 ### 3. Configurar el Entorno de Python
1. Crea un entorno virtual:


```
python3 -m venv venv
```
2. Activa el entorno:
```
source venv/bin/activate
```
3. Instala todas las dependencias del proyecto:

```
pip install -r requirements.txt
```
### 4. Conectar la Base de Datos

1. Abre el archivo app.py en tu editor de código.

Localiza la línea app.config:

['SQLALCHEMY_DATABASE_URI'].

2. Actualízala para que coincida con tu usuario, contraseña (si tienes) y el nombre de la base de datos que creaste en el paso 2.


#### Ejemplo de cambio en app.py

app.config['SQLALCHEMY_DATABASE_URI'] = (
    # Cambia 'db_miniblog' por el nombre de tu BD
    "mysql+pymysql://root:@localhost/db_miniblog"
)

### 5. Aplicar las Migraciones
Ejecuta los siguientes comandos en orden para crear toda la estructura de tablas en tu base de datos:


Inicializa las migraciones (solo la primera vez)
```
flask db init
```
 Crea el script de migración basado en tus Modelos
 ```
flask db migrate
```
Aplica los cambios a la base de datos
```
flask db upgrade
```
### 6. Ejecutar el Proyecto

Una vez completada la instalación, puedes iniciar el servidor de desarrollo:

```
flask run --reload
```
El flag --reload reiniciará automáticamente el servidor cada vez que detecte un cambio en el código.

La API estará disponible y corriendo en: http://127.0.0.1:5000

# Documentación de endpoints (Swagger)

Una vez que el servidor esté en ejecución (flask run --reload), puedes acceder a la documentación interactiva de la API (generada con Swagger) desde tu navegador.

URL de la Documentación: http://127.0.0.1:5000/api/docs/swagger


si usa la base de datos remota, los datos de prueba para cada tipo de usuario son:

admin:

    "username": 'admin'
    "password": 'admin'

moderator:

    "username": 'moderator'
    "password": 'moderator'

user:

    "username": 'user'
    "password": 'user'




