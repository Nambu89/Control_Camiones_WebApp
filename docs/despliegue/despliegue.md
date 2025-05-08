# Guía de Despliegue

## Descripción General

Esta guía proporciona instrucciones detalladas para desplegar el Sistema de Control Logístico de Camiones en diferentes entornos de producción. El sistema está diseñado para ser desplegado utilizando Docker o directamente en un servidor con Python.

## Opciones de Despliegue

### 1. Despliegue con Docker

El despliegue con Docker es la opción recomendada, ya que proporciona un entorno aislado y consistente, facilitando la gestión de dependencias y la configuración del entorno.

#### Requisitos Previos

- Docker instalado en el servidor
- Acceso a Internet para descargar imágenes base
- Permisos para ejecutar contenedores Docker

#### Pasos para el Despliegue

1. **Construir la Imagen Docker**

   Navegue al directorio raíz del proyecto donde se encuentra el Dockerfile y ejecute:

   ```bash
   docker build -t control-camiones .
   ```

2. **Ejecutar el Contenedor**

   Una vez construida la imagen, puede ejecutar el contenedor:

   ```bash
   docker run -d -p 5000:5000 --name control-camiones-app control-camiones
   ```

   Esto iniciará la aplicación en modo demonio (-d) y mapeará el puerto 5000 del contenedor al puerto 5000 del host.

3. **Verificar el Despliegue**

   Acceda a la aplicación a través de un navegador web:

   ```
   http://[dirección-ip-del-servidor]:5000
   ```

#### Persistencia de Datos

Por defecto, la base de datos SQLite se almacena dentro del contenedor. Para mantener los datos persistentes entre reinicios, se recomienda montar un volumen:

```bash
docker run -d -p 5000:5000 -v /ruta/en/host:/app/data --name control-camiones-app control-camiones
```

Y modificar la aplicación para usar `/app/data/database.db` como ruta de la base de datos.

### 2. Despliegue Directo en Servidor

#### Requisitos Previos

- Python 3.10 o superior instalado
- pip (gestor de paquetes de Python)
- Servidor web (opcional, para producción)

#### Pasos para el Despliegue

1. **Preparar el Entorno**

   Cree un entorno virtual e instale las dependencias:

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configurar el Servidor Web**

   Para entornos de producción, se recomienda utilizar Gunicorn como servidor WSGI:

   ```bash
   gunicorn --bind 0.0.0.0:5000 app:app
   ```

   El archivo `Procfile` incluido en el proyecto ya está configurado para usar Gunicorn.

3. **Configurar un Proxy Inverso (Recomendado)**

   Para mayor seguridad y rendimiento, configure un proxy inverso como Nginx:

   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

### 3. Despliegue en Plataformas PaaS

El sistema también puede desplegarse en plataformas como Heroku, Railway o Render.

#### Despliegue en Heroku

1. **Crear una Aplicación en Heroku**

   ```bash
   heroku create nombre-de-tu-app
   ```

2. **Configurar el Buildpack de Python**

   ```bash
   heroku buildpacks:set heroku/python
   ```

3. **Desplegar la Aplicación**

   ```bash
   git push heroku main
   ```

   El archivo `Procfile` incluido en el proyecto ya está configurado para Heroku.

## Configuración Post-Despliegue

### Zona Horaria

La aplicación está configurada para utilizar la zona horaria de España (Europe/Madrid). Si necesita cambiar esto, modifique la constante `TIMEZONE` en el archivo `app.py`:

```python
# Configuración de zona horaria
TIMEZONE = timezone('Europe/Madrid')  # Cambie a su zona horaria según sea necesario
```

### Respaldo de la Base de Datos

Configure respaldos periódicos de la base de datos SQLite:

```bash
# Ejemplo de script de respaldo
#!/bin/bash
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
cp /ruta/a/database.db /ruta/a/respaldos/database_$TIMESTAMP.db
```

Añada este script a un cron job para ejecutarlo regularmente.

## Monitorización y Mantenimiento

### Logs

Si utiliza Docker, puede ver los logs con:

```bash
docker logs control-camiones-app
```

Para un despliegue directo con Gunicorn, los logs se mostrarán en la salida estándar o en los archivos configurados.

### Actualizaciones

Para actualizar la aplicación:

1. **Con Docker**:

   ```bash
   # Detener el contenedor actual
   docker stop control-camiones-app
   docker rm control-camiones-app
   
   # Construir la nueva imagen
   docker build -t control-camiones .
   
   # Iniciar un nuevo contenedor
   docker run -d -p 5000:5000 -v /ruta/en/host:/app/data --name control-camiones-app control-camiones
   ```

2. **Despliegue Directo**:

   ```bash
   # Actualizar el código
   git pull
   
   # Actualizar dependencias
   pip install -r requirements.txt
   
   # Reiniciar el servicio
   # Depende de cómo esté configurado su servicio (systemd, supervisor, etc.)
   ```

## Solución de Problemas Comunes

### Problemas de Conexión

Si no puede acceder a la aplicación después del despliegue:

1. Verifique que el puerto 5000 esté abierto en el firewall
2. Compruebe que la aplicación esté en ejecución (`docker ps` o `ps aux | grep gunicorn`)
3. Revise los logs en busca de errores

### Problemas de Base de Datos

Si encuentra errores relacionados con la base de datos:

1. Verifique los permisos del archivo `database.db`
2. Compruebe que el directorio donde se almacena la base de datos sea escribible
3. Considere restaurar desde un respaldo si la base de datos está corrupta

## Consideraciones de Seguridad

- La aplicación no implementa autenticación de usuarios. Considere añadir un sistema de autenticación antes del despliegue en producción.
- Configure HTTPS utilizando certificados SSL/TLS para proteger la comunicación.
- Restrinja el acceso a la aplicación utilizando firewalls o redes privadas si es para uso interno.
- Realice respaldos regulares de la base de datos.
