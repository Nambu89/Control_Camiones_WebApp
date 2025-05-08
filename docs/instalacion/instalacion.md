# Guía de Instalación

Esta guía proporciona instrucciones detalladas para instalar y configurar el Sistema de Control Logístico de Camiones en diferentes entornos.

## Requisitos Previos

Antes de comenzar la instalación, asegúrese de tener instalados los siguientes componentes:

- Python 3.10 o superior
- pip (gestor de paquetes de Python)
- Git (opcional, para clonar el repositorio)

## Instalación en Entorno Local

### 1. Obtener el Código Fuente

Puede obtener el código fuente clonando el repositorio (si está disponible en un sistema de control de versiones) o descargando los archivos directamente.

```bash
# Opción 1: Clonar desde repositorio Git (si está disponible)
git clone [URL_DEL_REPOSITORIO]
cd [NOMBRE_DEL_DIRECTORIO]

# Opción 2: Descargar y descomprimir los archivos
# (Proceda según corresponda para su sistema operativo)
```

### 2. Crear un Entorno Virtual (Recomendado)

Es recomendable utilizar un entorno virtual para aislar las dependencias de la aplicación:

```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

Instale todas las dependencias necesarias utilizando pip:

```bash
pip install -r requirements.txt
```

### 4. Inicializar la Base de Datos

La aplicación inicializará automáticamente la base de datos SQLite al arrancar por primera vez. No se requieren pasos adicionales.

### 5. Ejecutar la Aplicación en Modo Desarrollo

Para iniciar la aplicación en modo desarrollo:

```bash
# En Windows
python app.py

# En macOS/Linux
python3 app.py
```

La aplicación estará disponible en `http://localhost:5000`.

## Instalación con Docker

### 1. Requisitos Previos para Docker

- Docker instalado en su sistema
- Docker Compose (opcional, para configuraciones más complejas)

### 2. Construir la Imagen Docker

```bash
docker build -t control-camiones .
```

### 3. Ejecutar el Contenedor

```bash
docker run -p 5000:5000 control-camiones
```

La aplicación estará disponible en `http://localhost:5000`.

## Configuración Adicional

### Zona Horaria

La aplicación está configurada para utilizar la zona horaria de España (Europe/Madrid). Si necesita cambiar esto, modifique la constante `TIMEZONE` en el archivo `app.py`:

```python
# Configuración de zona horaria
TIMEZONE = timezone('Europe/Madrid')  # Cambie a su zona horaria según sea necesario
```

### Personalización de Almacenes

Los almacenes disponibles (S1 y S6) están definidos en los formularios HTML. Si necesita modificar estas opciones, edite los archivos:

- `templates/index.html`
- `templates/edit.html`

Busque los elementos `<select>` con `id="almacen"` y modifique las opciones según sea necesario.

## Solución de Problemas

### Base de Datos

Si encuentra problemas con la base de datos, puede reiniciarla eliminando el archivo `database.db` y reiniciando la aplicación. La aplicación creará una nueva base de datos automáticamente.

### Dependencias

Si encuentra errores relacionados con dependencias, asegúrese de que todas las dependencias estén instaladas correctamente:

```bash
pip install -r requirements.txt --force-reinstall
```

### Problemas de Puerto

Si el puerto 5000 ya está en uso, puede cambiar el puerto en el archivo `app.py`:

```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Cambie 5001 por el puerto deseado
```

O al ejecutar el contenedor Docker:

```bash
docker run -p 8080:5000 control-camiones  # Mapea el puerto 8080 del host al 5000 del contenedor
```
