# Edición de Registros

## Descripción General

La funcionalidad de edición de registros permite a los usuarios modificar la información de camiones ya registrados en el sistema. Esta característica es esencial para corregir errores de entrada, actualizar información o ajustar detalles después de que se haya creado un registro.

## Interfaz de Usuario

Esta funcionalidad se accede desde la página de listado de camiones, a través del botón "Editar" disponible para cada registro. La interfaz presenta un formulario con los datos actuales del camión seleccionado, permitiendo modificar cualquiera de sus campos.

![Edición de Registros](../imagenes/edicion_registros.png)

## Características Principales

### Campos Editables

La funcionalidad permite editar los siguientes campos:
- Matrícula de la tractora
- Matrícula del remolque
- Empresa
- Número de envío
- Almacén (S1 o S6)
- Tipo de operación (Carga o Descarga)

### Preservación de Datos

- Los campos se cargan con los valores actuales del registro
- Si un campo opcional está vacío en la base de datos, se muestra un valor vacío
- Las fechas de entrada y salida no son editables a través de esta interfaz

## Flujo de Trabajo

1. El usuario accede a la página de listado de camiones (`/list`)
2. Hace clic en el botón "Editar" para el registro que desea modificar
3. El sistema:
   - Recupera la información actual del registro
   - Muestra un formulario con los datos cargados
4. El usuario modifica los campos según sea necesario
5. Al hacer clic en "Guardar", el sistema:
   - Valida los datos ingresados
   - Actualiza el registro en la base de datos
   - Redirige al usuario a la página de listado

## Código Relacionado

### Función Principal (app.py)

```python
@app.route('/edit/<int:camion_id>', methods=['GET', 'POST'])
def edit_camion(camion_id):
    if request.method == 'POST':
        # Ahora recogemos todos los campos
        matricula_tractora = request.form.get('matricula_tractora', '')
        matricula_remolque = request.form.get('matricula_remolque', '')
        empresa = request.form.get('empresa', '')
        numero_envio = request.form.get('numero_envio', '')
        almacen = request.form.get('almacen', '')
        tipo = request.form.get('tipo', '')
        
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute('''
                UPDATE camiones 
                SET matricula_tractora = ?, 
                    matricula_remolque = ?, 
                    empresa = ?, 
                    numero_envio = ?,
                    almacen = ?,
                    tipo = ?
                WHERE id = ?
            ''', (matricula_tractora, matricula_remolque, empresa, numero_envio, almacen, tipo, camion_id))
            conn.commit()
        return redirect(url_for('list_camiones'))
    else:
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute('SELECT matricula_tractora, matricula_remolque, empresa, numero_envio, almacen, tipo FROM camiones WHERE id = ?', (camion_id,))
            row = c.fetchone()
            
        # Establecer valores predeterminados si son NULL
        almacen = row[4] if row[4] else ''
        tipo = row[5] if row[5] else ''
            
        return render_template('edit.html', 
                             camion_id=camion_id, 
                             matricula_tractora=row[0],
                             matricula_remolque=row[1], 
                             empresa=row[2], 
                             numero_envio=row[3],
                             almacen=almacen,
                             tipo=tipo)
```

### Plantilla HTML (templates/edit.html)

La plantilla `edit.html` contiene el formulario para editar los datos del camión. Los elementos clave son:

- Formulario con campos para cada atributo editable
- Valores precargados con la información actual
- Botón para guardar los cambios

```html
{% extends "base.html" %}

{% block title %}Editar Camión{% endblock %}

{% block content %}
<h1>Editar Camión</h1>
<form method="post" class="border p-4 rounded">
    <div class="mb-3">
        <label for="matricula_tractora" class="form-label">Matrícula Tractora:</label>
        <input type="text" class="form-control" id="matricula_tractora" name="matricula_tractora" value="{{ matricula_tractora }}" required>
    </div>
    
    <div class="mb-3">
        <label for="matricula_remolque" class="form-label">Matrícula Remolque:</label>
        <input type="text" class="form-control" id="matricula_remolque" name="matricula_remolque" value="{{ matricula_remolque }}">
    </div>
    
    <div class="mb-3">
        <label for="empresa" class="form-label">Empresa:</label>
        <input type="text" class="form-control" id="empresa" name="empresa" value="{{ empresa }}" required>
    </div>
    
    <div class="mb-3">
        <label for="numero_envio" class="form-label">Número de envío:</label>
        <input type="text" class="form-control" id="numero_envio" name="numero_envio" value="{{ numero_envio }}">
    </div>
    
    <div class="mb-3">
        <label for="almacen" class="form-label">Almacén:</label>
        <select class="form-select" id="almacen" name="almacen" required>
            <option value="" {% if not almacen %}selected{% endif %}>Seleccione...</option>
            <option value="S1" {% if almacen == 'S1' %}selected{% endif %}>S1</option>
            <option value="S6" {% if almacen == 'S6' %}selected{% endif %}>S6</option>
        </select>
    </div>
    
    <div class="mb-3">
        <label for="tipo" class="form-label">Tipo:</label>
        <select class="form-select" id="tipo" name="tipo" required>
            <option value="" {% if not tipo %}selected{% endif %}>Seleccione...</option>
            <option value="Carga" {% if tipo == 'Carga' %}selected{% endif %}>Carga</option>
            <option value="Descarga" {% if tipo == 'Descarga' %}selected{% endif %}>Descarga</option>
        </select>
    </div>
    
    <button type="submit" class="btn btn-primary">Guardar</button>
</form>
{% endblock %}
```

## Consulta SQL Utilizada

La actualización de registros utiliza una consulta SQL UPDATE:

```sql
UPDATE camiones 
SET matricula_tractora = ?, 
    matricula_remolque = ?, 
    empresa = ?, 
    numero_envio = ?,
    almacen = ?,
    tipo = ?
WHERE id = ?
```

## Consideraciones Especiales

### Validación de Datos

El formulario incluye validación básica:
- Campos obligatorios marcados con `required`
- Selección obligatoria de almacén y tipo de operación

### Limitaciones

- No es posible editar las fechas de entrada y salida a través de esta interfaz
- No se mantiene un historial de cambios realizados a los registros

### Seguridad

- La implementación utiliza parámetros en las consultas SQL para prevenir ataques de inyección SQL
- No hay confirmación adicional antes de guardar los cambios
- No hay restricciones de acceso a esta funcionalidad en la versión actual

## Mejoras Potenciales

- Implementar un historial de cambios para auditoría
- Añadir la posibilidad de editar fechas de entrada/salida para administradores
- Implementar validación más robusta de datos (formato de matrículas, etc.)
- Añadir confirmación antes de guardar cambios importantes
- Implementar control de acceso basado en roles
- Añadir la posibilidad de cancelar la edición y volver al listado sin guardar cambios
