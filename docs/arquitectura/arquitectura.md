# Arquitectura del Sistema

## Estructura General

El Sistema de Control Logístico de Camiones sigue una arquitectura de aplicación web tradicional basada en el patrón MVC (Modelo-Vista-Controlador) implementado con Flask. A continuación, se detalla cada componente de la arquitectura:

### Diagrama de Arquitectura

```
+------------------+     +------------------+     +------------------+
|                  |     |                  |     |                  |
|    Cliente Web   | <-> |  Servidor Flask  | <-> |   Base de Datos  |
|    (Navegador)   |     |    (Backend)     |     |     (SQLite)     |
|                  |     |                  |     |                  |
+------------------+     +------------------+     +------------------+
```

## Componentes Principales

### 1. Frontend

- **Tecnologías**: HTML, CSS, JavaScript, Bootstrap 5
- **Estructura**: 
  - Plantillas Jinja2 para la generación dinámica de HTML
  - Sistema de herencia de plantillas con base.html como plantilla principal
  - Componentes de Bootstrap para la interfaz de usuario
  - Datepicker para la selección de fechas en reportes

### 2. Backend

- **Framework**: Flask (Python)
- **Estructura**:
  - Rutas (routes) para gestionar las peticiones HTTP
  - Funciones para el procesamiento de datos
  - Lógica de negocio para el registro de entradas/salidas
  - Generación de reportes y exportación de datos

### 3. Base de Datos

- **Sistema**: SQLite
- **Estructura**:
  - Tabla principal `camiones` para almacenar todos los registros
  - Campos para almacenar información de matrículas, empresas, fechas, etc.
  - Consultas SQL para recuperar y manipular datos

## Flujo de Datos

1. **Registro de Entrada/Salida**:
   - El usuario introduce los datos en el formulario web
   - El servidor procesa la petición y determina si es una entrada o salida
   - Se actualiza la base de datos con la información correspondiente
   - Se redirige al usuario a la página principal con confirmación

2. **Consulta de Camiones Activos**:
   - El usuario accede a la página de listado
   - El servidor consulta la base de datos para obtener camiones sin fecha de salida
   - Se genera la vista con la información recuperada

3. **Búsqueda de Registros**:
   - El usuario introduce términos de búsqueda
   - El servidor realiza consultas SQL con operadores LIKE
   - Se muestran los resultados que coinciden con los criterios

4. **Generación de Reportes**:
   - El usuario selecciona un rango de fechas
   - El servidor consulta registros dentro de ese rango
   - Se muestran los resultados y se ofrece opción de exportación

## Seguridad y Rendimiento

- **Seguridad**:
  - Validación de datos de entrada en el servidor
  - Protección contra inyección SQL mediante parámetros en consultas
  - No se implementa autenticación de usuarios en la versión actual

- **Rendimiento**:
  - Uso de SQLite para aplicaciones con carga moderada
  - Consultas optimizadas para recuperación rápida de datos
  - Paginación no implementada en la versión actual (potencial mejora)

## Escalabilidad

La arquitectura actual es adecuada para instalaciones individuales con volumen moderado de tráfico. Para escalar el sistema a múltiples ubicaciones o mayor volumen de datos, se recomendaría:

- Migrar a una base de datos más robusta como PostgreSQL
- Implementar un sistema de autenticación y autorización
- Añadir paginación para grandes volúmenes de datos
- Considerar una arquitectura de microservicios para funcionalidades específicas
