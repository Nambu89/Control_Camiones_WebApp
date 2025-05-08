# Eliminación de Registros

## Descripción General

La funcionalidad de eliminación de registros permite a los usuarios eliminar entradas de camiones del sistema. Esta característica es útil para eliminar registros erróneos, duplicados o que ya no son relevantes para el sistema.

## Interfaz de Usuario

Esta funcionalidad se accede desde la página de listado de camiones, a través del botón "Borrar" disponible para cada registro. No existe una interfaz dedicada para esta funcionalidad, ya que se ejecuta directamente desde la lista.

![Eliminación de Registros](../imagenes/eliminacion_registros.png)

## Características Principales

### Eliminación Directa

- La eliminación se realiza con un solo clic en el botón "Borrar"
- No hay confirmación adicional antes de eliminar el registro
- La eliminación es permanente y no puede deshacerse

### Accesibilidad

- La opción de borrado está disponible para todos los camiones que aparecen en la lista (aquellos que están actualmente dentro de las instalaciones)
- No es posible eliminar registros históricos directamente desde la interfaz de búsqueda o reportes

## Flujo de Trabajo

1. El usuario accede a la página de listado de camiones (`/list`)
2. Localiza el registro que desea eliminar
3. Hace clic en el botón "Borrar" para ese registro
4. El sistema:
   - Elimina el registro de la base de datos
   - Actualiza la página de listado
   - Muestra la lista actualizada sin el registro eliminado

## Código Relacionado

### Función Principal (app.py)

```python
@app.route('/delete/<int:camion_id>', methods=['POST'])
def delete_camion(camion_id):
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('DELETE FROM camiones WHERE id = ?', (camion_id,))
        conn.commit()
    return redirect(url_for('list_camiones'))
```

### Formulario en la Plantilla HTML (templates/list.html)

```html
<form method="post" action="{{ url_for('delete_camion', camion_id=c[0]) }}" style="display:inline-block; margin-left:5px;">
    <button type="submit" class="btn btn-warning">Borrar</button>
</form>
```

## Consulta SQL Utilizada

La eliminación de registros utiliza una consulta SQL DELETE:

```sql
DELETE FROM camiones WHERE id = ?
```

## Consideraciones Especiales

### Irreversibilidad

La eliminación de registros es permanente y no puede deshacerse. No existe una papelera de reciclaje o sistema de recuperación para registros eliminados.

### Ausencia de Confirmación

En la implementación actual, no hay un diálogo de confirmación antes de eliminar un registro. Esto podría llevar a eliminaciones accidentales.

### Integridad Referencial

La base de datos SQLite no implementa restricciones de integridad referencial en este sistema. Si en el futuro se añaden tablas relacionadas, será necesario gestionar la eliminación en cascada o restricciones.

### Seguridad

- La implementación utiliza parámetros en las consultas SQL para prevenir ataques de inyección SQL
- No hay restricciones de acceso a esta funcionalidad en la versión actual

## Impacto en el Sistema

La eliminación de registros puede afectar a:
- Reportes históricos (los registros eliminados no aparecerán en futuros reportes)
- Estadísticas y análisis de datos
- Trazabilidad de operaciones

## Mejoras Potenciales

- Implementar un diálogo de confirmación antes de eliminar registros
- Añadir una "papelera" temporal donde los registros eliminados puedan recuperarse
- Implementar un sistema de "eliminación lógica" (soft delete) en lugar de eliminación física
- Crear un registro de auditoría para las eliminaciones
- Restringir la capacidad de eliminar registros a usuarios con permisos específicos
- Permitir la eliminación masiva de registros basada en criterios (por ejemplo, todos los registros más antiguos que cierta fecha)
