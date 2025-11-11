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

Para conectarte a la base de datos, necesitarás las siguientes variables de ambiente

#### Crear variables temporales (para la sesión actual de tu terminal)

```bash
export DB_NAME="db_miniblog"
export DB_USER="root"
export DB_PASSWORD=""
export DB_SERVER="localhost"
export DB_PORT="3306"
```

###### NOTA: las variables que se muestran son las que la API utiliza por defecto al inicializarse, si son las mismas que vas a utilizar en la base de datos no es necesario utilizar este código en tu terminal.


#### La app se conectará a la base de datos de la siguiente manera
```
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}:{DB_PORT}/{DB_NAME}"
)
```

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

# Probar la API

La API está deployada 24/7 en este servidor, puede acceder para probar los endpoints aprovechando los datos de la db interna.

```
http://18.223.136.198:5000/
```

Si se conecta a este servidor, los datos de prueba para cada tipo de usuario son:

admin:

    "username": 'admin'
    "password": 'admin'

moderator:

    "username": 'moderator'
    "password": 'moderator'

user:

    "username": 'user'
    "password": 'user'

