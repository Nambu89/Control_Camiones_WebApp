# Funcionalidades del Sistema

El Sistema de Control Logístico de Camiones ofrece un conjunto completo de funcionalidades para gestionar el flujo de vehículos en instalaciones logísticas. A continuación, se detallan las principales funcionalidades del sistema.

## Índice de Funcionalidades

1. [Registro de Entradas/Salidas](./registro_entradas_salidas.md)
2. [Listado de Camiones](./listado_camiones.md)
3. [Búsqueda de Registros](./busqueda.md)
4. [Generación de Reportes](./reportes.md)
5. [Exportación de Datos](./exportacion.md)
6. [Edición de Registros](./edicion_registros.md)
7. [Eliminación de Registros](./eliminacion_registros.md)
8. [Duplicación de Registros](./duplicacion_registros.md)

## Resumen de Funcionalidades

### Registro de Entradas/Salidas

Permite registrar la entrada y salida de camiones en las instalaciones. El sistema detecta automáticamente si se trata de una entrada o una salida basándose en la matrícula del vehículo.

### Listado de Camiones

Muestra todos los camiones que actualmente se encuentran dentro de las instalaciones (sin fecha de salida registrada). Permite filtrar por almacén (S1 o S6).

### Búsqueda de Registros

Facilita la búsqueda de registros históricos por matrícula (tractora o remolque), empresa o número de envío.

### Generación de Reportes

Permite generar informes de actividad por rango de fechas, mostrando todos los movimientos de vehículos en ese período.

### Exportación de Datos

Ofrece la posibilidad de exportar los reportes generados a formato CSV para su análisis en herramientas externas.

### Edición de Registros

Permite modificar la información de un registro existente, como matrículas, empresa, número de envío, almacén o tipo de operación.

### Eliminación de Registros

Proporciona la capacidad de eliminar registros erróneos o no deseados del sistema.

### Duplicación de Registros

Facilita la creación de nuevos registros basados en registros existentes, útil para camiones que realizan múltiples operaciones similares.

## Flujos de Trabajo Comunes

### Flujo de Registro de Entrada y Salida

1. El usuario introduce la matrícula de la tractora en la página principal
2. Si el camión no está registrado como "dentro", se muestra el formulario para registrar entrada
3. El usuario completa los datos y registra la entrada
4. Cuando el camión sale, se busca nuevamente por matrícula
5. El sistema detecta que el camión está dentro y ofrece registrar la salida
6. El usuario confirma la salida y se actualiza el registro

### Flujo de Generación de Reportes

1. El usuario accede a la sección de reportes
2. Selecciona el rango de fechas deseado
3. El sistema muestra todos los registros en ese período
4. El usuario puede exportar los resultados a CSV si lo desea

## Limitaciones Actuales

- No se implementa un sistema de autenticación de usuarios
- No hay paginación para grandes volúmenes de datos
- No se incluye un sistema de notificaciones
- La aplicación no tiene funcionalidades de estadísticas avanzadas

## Próximas Funcionalidades Planificadas

- Sistema de autenticación y roles de usuario
- Estadísticas y gráficos de actividad
- Notificaciones por correo electrónico
- Aplicación móvil para registro desde dispositivos portátiles
- Integración con sistemas de control de acceso físico
