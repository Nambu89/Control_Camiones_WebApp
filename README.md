# Sistema de Control Logístico de Camiones

Sistema web para gestionar y monitorizar la entrada y salida de camiones en instalaciones logísticas.

## Descripción

El Sistema de Control Logístico de Camiones es una aplicación web desarrollada con Flask que permite registrar y controlar el flujo de vehículos en almacenes logísticos. La aplicación facilita el registro de entradas y salidas, búsqueda de registros históricos, generación de reportes y exportación de datos.

## Características Principales

- Registro de entradas y salidas de camiones
- Listado de camiones actualmente dentro de las instalaciones
- Búsqueda por matrícula, empresa o número de envío
- Reportes por rango de fechas
- Exportación de datos a formato CSV
- Diferenciación por almacén (S1/S6)
- Clasificación por tipo de operación (Carga/Descarga)

## Tecnologías Utilizadas

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Base de Datos**: SQLite
- **Despliegue**: Docker, Gunicorn

## Instalación y Ejecución

### Requisitos Previos

- Python 3.10 o superior
- pip (gestor de paquetes de Python)

### Instalación Local

1. Clonar o descargar el repositorio
2. Crear un entorno virtual (recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Ejecutar la aplicación:
   ```bash
   python app.py
   ```
5. Acceder a la aplicación en `http://localhost:5000`

### Instalación con Docker

1. Construir la imagen:
   ```bash
   docker build -t control-camiones .
   ```
2. Ejecutar el contenedor:
   ```bash
   docker run -p 5000:5000 control-camiones
   ```
3. Acceder a la aplicación en `http://localhost:5000`

## Estructura del Proyecto

```
.
├── app.py                 # Archivo principal de la aplicación Flask
├── database.db            # Base de datos SQLite
├── database.sqbpro        # Archivo de proyecto SQLite Browser
├── requirements.txt       # Dependencias del proyecto
├── dockerfile             # Configuración para Docker
├── Procfile               # Configuración para despliegue en Heroku
├── static/                # Archivos estáticos (CSS, JS)
└── templates/             # Plantillas HTML
    ├── base.html          # Plantilla base con estructura común
    ├── edit.html          # Formulario de edición
    ├── index.html         # Página principal (registro entradas/salidas)
    ├── list.html          # Listado de camiones activos
    ├── report.html        # Generación de reportes
    └── search.html        # Búsqueda de registros
```

## Documentación

La documentación completa del sistema se encuentra en la carpeta `docs/`. Incluye:

- [Visión General](./docs/general/vision_general.md)
- [Arquitectura](./docs/arquitectura/arquitectura.md)
- [Instalación](./docs/instalacion/instalacion.md)
- [Funcionalidades](./docs/funcionalidades/funcionalidades.md)
- [Base de Datos](./docs/base_datos/base_datos.md)
- [Despliegue](./docs/despliegue/despliegue.md)
- [Guía de Usuario](./docs/guia_usuario/guia_usuario.md)
- [API y Endpoints](./docs/api/api.md)
- [Mantenimiento](./docs/mantenimiento/mantenimiento.md)

## Contribución

Si desea contribuir al proyecto, por favor:

1. Haga un fork del repositorio
2. Cree una rama para su funcionalidad (`git checkout -b feature/nueva-funcionalidad`)
3. Haga commit de sus cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Haga push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Cree un Pull Request

## Licencia

Este proyecto está licenciado bajo [MIT License](LICENSE).

## Contacto

Para preguntas o soporte, contacte a [nombre@email.com](mailto:nombre@email.com).
