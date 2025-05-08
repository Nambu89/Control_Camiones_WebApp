# Guía de Mantenimiento

## Descripción General

Esta guía proporciona instrucciones detalladas para el mantenimiento y actualización del Sistema de Control Logístico de Camiones. Está dirigida a administradores de sistemas y desarrolladores responsables de mantener la aplicación en funcionamiento óptimo.

## Mantenimiento Rutinario

### Respaldo de la Base de Datos

Se recomienda realizar respaldos periódicos de la base de datos para prevenir pérdida de datos:

```bash
# Script de respaldo para sistemas Unix/Linux
#!/bin/bash
BACKUP_DIR="/ruta/a/respaldos"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
cp /ruta/a/database.db $BACKUP_DIR/database_$TIMESTAMP.db
# Opcional: Mantener solo los últimos 30 respaldos
find $BACKUP_DIR -name "database_*.db" -type f -mtime +30 -delete
```

Para Windows, puede crear un script PowerShell o una tarea programada similar.

### Rotación de Logs

Si ha configurado logs para la aplicación, implemente una política de rotación:

```bash
# Ejemplo usando logrotate en Linux
/ruta/a/logs/app.log {
    daily
    missingok
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 usuario grupo
}
```

### Monitorización del Espacio en Disco

La base de datos SQLite crecerá con el tiempo. Monitorice regularmente el espacio disponible:

```bash
# En Linux
df -h /ruta/donde/esta/la/aplicacion

# En Windows (PowerShell)
Get-PSDrive C | Select-Object Used,Free
```

## Optimización de la Base de Datos

### Compactación de la Base de Datos SQLite

SQLite puede fragmentarse con el tiempo. Ejecute periódicamente una compactación:

```python
# Script Python para compactar la base de datos
import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('database.db')
conn.execute("VACUUM")
conn.close()
```

### Análisis de Rendimiento

Si la aplicación se vuelve lenta, considere analizar las consultas:

```python
# Habilitar temporalmente el registro de consultas lentas
import sqlite3
import time

class TimingCursor(sqlite3.Cursor):
    def execute(self, sql, params=None):
        start = time.time()
        if params:
            result = super().execute(sql, params)
        else:
            result = super().execute(sql)
        duration = time.time() - start
        if duration > 0.1:  # Registrar consultas que toman más de 100ms
            print(f"Consulta lenta ({duration:.3f}s): {sql}")
        return result

conn = sqlite3.connect('database.db')
conn.row_factory = sqlite3.Row
conn.cursor_factory = TimingCursor
```

## Actualizaciones del Sistema

### Actualización del Código Fuente

Para actualizar el código de la aplicación:

1. Realice un respaldo completo antes de cualquier actualización
2. Si usa control de versiones, actualice desde el repositorio:
   ```bash
   git pull origin main
   ```
3. Actualice las dependencias:
   ```bash
   pip install -r requirements.txt --upgrade
   ```
4. Reinicie la aplicación

### Migración de la Base de Datos

Si necesita modificar la estructura de la base de datos:

1. Cree un script de migración:
   ```python
   import sqlite3
   
   def migrate():
       conn = sqlite3.connect('database.db')
       c = conn.cursor()
       
       # Ejemplo: Añadir una nueva columna
       try:
           c.execute('ALTER TABLE camiones ADD COLUMN nueva_columna TEXT')
           print("Migración completada: nueva_columna añadida")
       except sqlite3.OperationalError as e:
           print(f"Error o columna ya existe: {e}")
       
       conn.commit()
       conn.close()
   
   if __name__ == '__main__':
       migrate()
   ```

2. Ejecute el script:
   ```bash
   python migrate.py
   ```

## Solución de Problemas

### Problemas Comunes y Soluciones

#### La Aplicación No Inicia

1. Verifique los logs de error
2. Compruebe que todas las dependencias están instaladas:
   ```bash
   pip install -r requirements.txt
   ```
3. Verifique los permisos de archivos y directorios
4. Compruebe la conectividad a la base de datos

#### Base de Datos Corrupta

Si la base de datos se corrompe:

1. Detenga la aplicación
2. Restaure desde el último respaldo:
   ```bash
   cp /ruta/a/respaldos/database_ultimo.db database.db
   ```
3. Si no hay respaldo, intente recuperar la base de datos:
   ```bash
   sqlite3 database.db "PRAGMA integrity_check;"
   ```

#### Problemas de Rendimiento

1. Verifique el uso de recursos del servidor (CPU, memoria, disco)
2. Compacte la base de datos como se describió anteriormente
3. Considere añadir índices a columnas frecuentemente consultadas:
   ```python
   c.execute('CREATE INDEX IF NOT EXISTS idx_matricula ON camiones(matricula_tractora)')
   ```

## Seguridad

### Actualizaciones de Seguridad

Mantenga actualizadas todas las dependencias para prevenir vulnerabilidades:

```bash
pip install --upgrade pip
pip list --outdated
pip install --upgrade flask pytz
```

### Auditoría de Seguridad

Realice auditorías periódicas:

1. Revise los logs en busca de actividad sospechosa
2. Verifique los permisos de archivos y directorios
3. Considere implementar herramientas de monitorización de seguridad

## Mejoras Futuras

### Planificación de Actualizaciones

Considere las siguientes mejoras para futuras versiones:

1. **Autenticación de usuarios**: Implementar un sistema de login con diferentes niveles de acceso
2. **Paginación**: Para manejar grandes volúmenes de datos en listados y búsquedas
3. **API REST**: Para integración con otros sistemas
4. **Estadísticas avanzadas**: Implementar dashboards y gráficos
5. **Migración a una base de datos más robusta**: Considerar PostgreSQL o MySQL para mayor escala

### Procedimiento para Implementar Mejoras

1. Desarrolle las mejoras en un entorno de pruebas
2. Realice pruebas exhaustivas
3. Documente los cambios y actualice la documentación de usuario
4. Planifique la actualización en un momento de baja actividad
5. Realice un respaldo completo antes de la actualización
6. Implemente los cambios
7. Verifique el funcionamiento correcto después de la actualización
