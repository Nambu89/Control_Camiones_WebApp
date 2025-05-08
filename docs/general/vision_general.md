# Visión General del Sistema

## Introducción

El Sistema de Control Logístico de Camiones es una aplicación web desarrollada para gestionar y monitorizar la entrada y salida de vehículos en instalaciones logísticas. La aplicación está diseñada específicamente para controlar el flujo de camiones en almacenes, proporcionando un registro detallado de cada movimiento.

## Propósito

El propósito principal de esta aplicación es:

- Registrar la entrada y salida de camiones en las instalaciones
- Mantener un historial de todos los movimientos de vehículos
- Facilitar la búsqueda de información histórica
- Generar reportes por rangos de fechas
- Exportar datos para análisis externos
- Diferenciar entre diferentes almacenes (S1 y S6)
- Clasificar operaciones por tipo (Carga y Descarga)

## Tecnologías Utilizadas

El sistema está desarrollado utilizando las siguientes tecnologías:

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Base de Datos**: SQLite
- **Despliegue**: Docker, Gunicorn

## Características Principales

1. **Registro de Entradas/Salidas**: Permite registrar la entrada y salida de camiones con información detallada.
2. **Listado de Camiones Activos**: Muestra todos los camiones que actualmente se encuentran dentro de las instalaciones.
3. **Búsqueda de Registros**: Facilita la búsqueda de camiones por matrícula, empresa o número de envío.
4. **Generación de Reportes**: Permite generar reportes por rango de fechas.
5. **Exportación de Datos**: Posibilidad de exportar datos a formato CSV.
6. **Gestión por Almacén**: Diferenciación entre almacenes S1 y S6.
7. **Clasificación por Tipo**: Categorización de operaciones como Carga o Descarga.

## Usuarios Objetivo

Esta aplicación está diseñada para ser utilizada por:

- Personal de seguridad en entradas de instalaciones logísticas
- Coordinadores de logística
- Administradores de almacenes
- Personal de gestión y planificación

## Beneficios

- **Eficiencia Operativa**: Agiliza el proceso de registro de entradas y salidas.
- **Trazabilidad**: Proporciona un historial completo de todos los movimientos.
- **Análisis de Datos**: Facilita la generación de informes y análisis de patrones.
- **Control de Acceso**: Mejora la seguridad al mantener un registro detallado de todos los vehículos.
- **Organización**: Permite clasificar las operaciones por almacén y tipo.
