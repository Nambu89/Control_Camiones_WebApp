# API y Endpoints

## Descripción General

El Sistema de Control Logístico de Camiones está implementado como una aplicación web basada en Flask. Aunque no ofrece una API REST formal, utiliza un conjunto de rutas (endpoints) para gestionar las diferentes funcionalidades. Este documento detalla todas las rutas disponibles, sus métodos HTTP asociados y su funcionalidad.

## Rutas Principales

### Página Principal - Registro de Entradas/Salidas

- **Ruta**: `/`
- **Métodos**: `GET`, `POST`
- **Función**: `index()`
- **Descripción**: Maneja el registro de entradas y salidas de camiones.
- **Comportamiento**:
  - `GET`: Muestra el formulario de registro y la información del último registro si se proporciona una matrícula.
  - `POST`: Procesa el formulario para registrar una entrada o salida.
- **Parámetros**:
  - `matricula_tractora`: Matrícula del vehículo tractor
  - `matricula_remolque`: Matrícula del remolque (opcional)
  - `empresa`: Nombre de la empresa transportista
  - `numero_envio`: Número de referencia del envío (opcional)
  - `almacen`: Identificador del almacén (S1 o S6)
  - `tipo`: Tipo de operación (Carga o Descarga)

### Health Check

- **Ruta**: `/health`
- **Métodos**: `GET`
- **Función**: `health()`
- **Descripción**: Verifica que la aplicación arranca correctamente y que la base de datos responde.
- **Comportamiento**:
  - `GET`: Devuelve JSON con el estado general, estado de base de datos, marca temporal y zona horaria configurada.
  - Si la base de datos no responde, devuelve `503 Service Unavailable`.

### Listado de Camiones Activos

- **Ruta**: `/list`
- **Métodos**: `GET`
- **Función**: `list_camiones()`
- **Descripción**: Muestra todos los camiones que actualmente están dentro de las instalaciones.
- **Comportamiento**:
  - `GET`: Consulta y muestra los camiones sin fecha de salida registrada.
- **Parámetros**:
  - `almacen`: Filtro opcional para mostrar solo camiones en un almacén específico.

### Registrar Salida

- **Ruta**: `/salida/<int:camion_id>`
- **Métodos**: `POST`
- **Función**: `registrar_salida(camion_id)`
- **Descripción**: Registra la salida de un camión específico.
- **Comportamiento**:
  - `POST`: Actualiza el registro del camión con la fecha y hora actual como fecha de salida.
- **Parámetros**:
  - `camion_id`: ID del registro del camión (en la URL).

### Duplicar Registro

- **Ruta**: `/replicate/<int:camion_id>`
- **Métodos**: `POST`
- **Función**: `replicate_camion(camion_id)`
- **Descripción**: Crea una copia exacta de un registro existente.
- **Comportamiento**:
  - `POST`: Crea un nuevo registro con los mismos datos que el original.
- **Parámetros**:
  - `camion_id`: ID del registro del camión a duplicar (en la URL).

### Eliminar Registro

- **Ruta**: `/delete/<int:camion_id>`
- **Métodos**: `POST`
- **Función**: `delete_camion(camion_id)`
- **Descripción**: Elimina un registro específico.
- **Comportamiento**:
  - `POST`: Elimina permanentemente el registro de la base de datos.
- **Parámetros**:
  - `camion_id`: ID del registro del camión a eliminar (en la URL).

### Búsqueda de Registros

- **Ruta**: `/search`
- **Métodos**: `GET`, `POST`
- **Función**: `search()`
- **Descripción**: Permite buscar registros históricos.
- **Comportamiento**:
  - `GET`: Muestra el formulario de búsqueda.
  - `POST`: Procesa la búsqueda y muestra los resultados.
- **Parámetros**:
  - `query`: Término de búsqueda para matrículas, empresa o número de envío.

### Generación de Reportes

- **Ruta**: `/report`
- **Métodos**: `GET`, `POST`
- **Función**: `report()`
- **Descripción**: Genera reportes por rango de fechas.
- **Comportamiento**:
  - `GET`: Muestra el formulario para seleccionar fechas.
  - `POST`: Genera y muestra el reporte para el rango de fechas seleccionado.
- **Parámetros**:
  - `start_date`: Fecha de inicio del reporte (formato DD-MM-YYYY).
  - `end_date`: Fecha de fin del reporte (formato DD-MM-YYYY).

### Exportación a CSV

- **Ruta**: `/export.csv`
- **Métodos**: `GET`
- **Función**: `export_csv()`
- **Descripción**: Exporta los datos de un reporte a formato CSV.
- **Comportamiento**:
  - `GET`: Genera y descarga un archivo CSV con los datos del reporte.
- **Parámetros**:
  - `start_date`: Fecha de inicio del reporte (formato DD-MM-YYYY).
  - `end_date`: Fecha de fin del reporte (formato DD-MM-YYYY).

### Edición de Registros

- **Ruta**: `/edit/<int:camion_id>`
- **Métodos**: `GET`, `POST`
- **Función**: `edit_camion(camion_id)`
- **Descripción**: Permite editar la información de un registro existente.
- **Comportamiento**:
  - `GET`: Muestra el formulario con los datos actuales del registro.
  - `POST`: Procesa los cambios y actualiza el registro.
- **Parámetros**:
  - `camion_id`: ID del registro del camión a editar (en la URL).
  - Campos del formulario: `matricula_tractora`, `matricula_remolque`, `empresa`, `numero_envio`, `almacen`, `tipo`.

## Funciones Auxiliares

### Obtener Fecha y Hora Actual

- **Función**: `get_current_datetime()`
- **Descripción**: Obtiene la fecha y hora actual en la zona horaria de España.
- **Retorno**: Cadena de texto con formato `YYYY-MM-DD HH:MM:SS`.

### Inicialización de Base de Datos

- **Función**: `init_db()`
- **Descripción**: Inicializa la estructura de la base de datos si no existe.
- **Comportamiento**: Crea la tabla `camiones` si no existe.

## Consideraciones para Desarrollo

### Convenciones de Rutas

- Las rutas siguen una estructura lógica y descriptiva
- Los IDs de recursos se incluyen directamente en la URL
- Se utilizan métodos HTTP apropiados para cada operación (GET para consultas, POST para modificaciones)

### Respuestas

- La mayoría de las rutas devuelven respuestas HTML renderizadas
- Solo la ruta de exportación a CSV devuelve un tipo de contenido diferente (text/csv)
- Las operaciones de modificación (POST) generalmente redirigen a otra página tras completarse

### Seguridad

- No se implementa autenticación ni autorización en la versión actual
- Las consultas SQL utilizan parámetros para prevenir inyección SQL
- La aplicación añade cabeceras HTTP defensivas en todas las respuestas
- No se implementa protección CSRF en los formularios

## Extensión de la API

Para convertir esta aplicación en una API REST formal, se podrían implementar los siguientes cambios:

1. Añadir rutas específicas para API con prefijo `/api/`
2. Implementar respuestas en formato JSON
3. Utilizar códigos de estado HTTP apropiados
4. Implementar autenticación mediante tokens
5. Documentar la API con herramientas como Swagger/OpenAPI
