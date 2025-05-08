# Documentación de la Base de Datos

## Estructura de la Base de Datos

El Sistema de Control Logístico de Camiones utiliza SQLite como sistema de gestión de base de datos. SQLite es una base de datos relacional liviana que almacena toda la información en un único archivo, lo que facilita su mantenimiento y respaldo.

### Archivo de Base de Datos

- **Nombre del archivo**: `database.db`
- **Ubicación**: Directorio raíz de la aplicación
- **Herramienta de gestión**: Se incluye un archivo `database.sqbpro` para gestionar la base de datos con SQLite Browser

## Esquema de la Base de Datos

### Tabla: `camiones`

Esta es la tabla principal que almacena todos los registros de entrada y salida de camiones.

| Columna | Tipo | Descripción | Restricciones |
|---------|------|-------------|---------------|
| id | INTEGER | Identificador único del registro | PRIMARY KEY, AUTOINCREMENT |
| matricula_tractora | TEXT | Matrícula del vehículo tractor | NOT NULL |
| matricula_remolque | TEXT | Matrícula del remolque | Puede ser NULL |
| empresa | TEXT | Nombre de la empresa transportista | NOT NULL |
| fecha_entrada | TEXT | Fecha y hora de entrada (formato YYYY-MM-DD HH:MM:SS) | NOT NULL |
| fecha_salida | TEXT | Fecha y hora de salida (formato YYYY-MM-DD HH:MM:SS) | Puede ser NULL |
| numero_envio | TEXT | Número de referencia del envío | Puede ser NULL |
| almacen | TEXT | Identificador del almacén (S1 o S6) | Puede ser NULL |
| tipo | TEXT | Tipo de operación (Carga o Descarga) | Puede ser NULL |

## Inicialización de la Base de Datos

La base de datos se inicializa automáticamente cuando se ejecuta la aplicación por primera vez. El código responsable de esta inicialización se encuentra en la función `init_db()` en el archivo `app.py`:

```python
def init_db():
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS camiones(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                matricula_tractora TEXT NOT NULL,
                matricula_remolque TEXT,
                empresa TEXT,
                fecha_entrada TEXT,
                fecha_salida TEXT,
                numero_envio TEXT,
                almacen TEXT,
                tipo TEXT
            )
        ''')
        conn.commit()
```

## Operaciones Principales

### Inserción de Registros

Cuando un camión entra a las instalaciones, se crea un nuevo registro con `fecha_entrada` establecida y `fecha_salida` como NULL:

```python
c.execute('''
    INSERT INTO camiones 
    (matricula_tractora, matricula_remolque, empresa, fecha_entrada, numero_envio, almacen, tipo) 
    VALUES (?, ?, ?, ?, ?, ?, ?)
''', (matricula_tractora, matricula_remolque, empresa, fecha_entrada, numero_envio, almacen, tipo))
```

### Actualización de Registros

Cuando un camión sale de las instalaciones, se actualiza el registro existente estableciendo `fecha_salida`:

```python
c.execute('UPDATE camiones SET fecha_salida = ? WHERE id = ?', (fecha_salida, cam_id))
```

### Consultas Principales

#### Listado de Camiones Actualmente Dentro

```python
c.execute("""
    SELECT id, matricula_tractora, matricula_remolque, empresa, fecha_entrada, numero_envio, almacen, tipo 
    FROM camiones 
    WHERE fecha_salida IS NULL
""")
```

#### Búsqueda por Criterios

```python
c.execute("""
    SELECT matricula_tractora, matricula_remolque, empresa, fecha_entrada, fecha_salida, numero_envio, almacen, tipo
    FROM camiones
    WHERE matricula_tractora LIKE ? 
    OR matricula_remolque LIKE ?
    OR empresa LIKE ? 
    OR numero_envio LIKE ?
    ORDER BY fecha_entrada DESC
""", (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"))
```

#### Reporte por Rango de Fechas

```python
c.execute('''
    SELECT matricula_tractora, matricula_remolque, empresa, fecha_entrada, fecha_salida, numero_envio, almacen, tipo
    FROM camiones
    WHERE fecha_entrada BETWEEN ? AND ?
    ORDER BY fecha_entrada ASC
''', (start_date_iso + " 00:00:00", end_date_iso + " 23:59:59"))
```

## Mantenimiento de la Base de Datos

### Respaldo

Para realizar un respaldo de la base de datos, simplemente copie el archivo `database.db` a una ubicación segura:

```bash
# En Windows
copy database.db database_backup_YYYYMMDD.db

# En macOS/Linux
cp database.db database_backup_YYYYMMDD.db
```

### Restauración

Para restaurar desde un respaldo, detenga la aplicación y reemplace el archivo `database.db` con el archivo de respaldo:

```bash
# En Windows
copy database_backup_YYYYMMDD.db database.db

# En macOS/Linux
cp database_backup_YYYYMMDD.db database.db
```

### Optimización

SQLite generalmente no requiere mucho mantenimiento, pero puede ejecutar la siguiente consulta periódicamente para optimizar la base de datos:

```sql
VACUUM;
```

## Consideraciones para Escalar

Si el volumen de datos crece significativamente, considere:

1. Implementar un sistema de archivado para registros antiguos
2. Migrar a un sistema de base de datos más robusto como PostgreSQL o MySQL
3. Implementar índices adicionales para mejorar el rendimiento de las consultas
