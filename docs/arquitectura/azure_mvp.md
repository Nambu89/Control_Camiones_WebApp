# Arquitectura Azure MVP

## Objetivo

Definir una postura sencilla pero defendible para desplegar esta aplicación como MVP en Azure sin reescribirla ni introducir una migración compleja de base de datos.

## Arquitectura recomendada

```text
Usuarios internos o sedes controladas
            |
            v
Azure App Service for Containers o Azure Container Apps
            |
            v
Contenedor Flask + Gunicorn
            |
            v
SQLite en volumen persistente
```

## Medidas ya soportadas por el repositorio

- configuración mediante variables de entorno
- carga automática de `.env` en desarrollo local
- endpoint `/health` para sondas de plataforma
- contenedor ejecutado como usuario no-root
- logs por salida estándar
- índices SQLite básicos para sostener el piloto
- cabeceras HTTP defensivas en respuestas

## Límites aceptados del MVP

- no hay autenticación ni autorización integrada
- SQLite es válido para piloto o alcance contenido, no para alta concurrencia
- `app.py` sigue siendo monolítico, aunque con helpers de configuración, base de datos y validación

## Controles operativos recomendados en Azure

1. Restringir exposición pública mediante red corporativa, VPN, Access Restrictions o Application Gateway/WAF.
2. Persistir la base de datos en un volumen montado y monitorizar permisos y capacidad.
3. Mantener `FLASK_DEBUG=0` y `LOG_LEVEL=INFO` en producción.
4. Configurar alertas básicas usando el `health check` y logs de contenedor.

## Evolución recomendada

1. Añadir autenticación con Microsoft Entra ID o Azure Easy Auth.
2. Migrar de SQLite a Azure SQL si aumenta el número de usuarios o la criticidad.
3. Incorporar Application Insights con OpenTelemetry.
4. Separar progresivamente la lógica de aplicación si el producto deja de ser un MVP.
