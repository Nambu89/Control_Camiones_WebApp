# Listado de Camiones

## Descripción General

La funcionalidad de listado de camiones permite visualizar todos los vehículos que actualmente se encuentran dentro de las instalaciones (aquellos que tienen fecha de entrada registrada pero no tienen fecha de salida). Esta vista proporciona una visión general del estado actual de las instalaciones y permite realizar acciones sobre los registros.

## Interfaz de Usuario

Esta funcionalidad se encuentra en la ruta `/list` de la aplicación. La interfaz presenta una tabla con todos los camiones actualmente dentro, con opciones para filtrar por almacén (S1 o S6).

![Listado de Camiones](../imagenes/listado_camiones.png)

## Características Principales

### Visualización de Camiones Activos

- Muestra todos los camiones que están actualmente dentro de las instalaciones
- Presenta información completa: matrículas, empresa, fecha de entrada, número de envío, almacén y tipo
- Ordena los camiones por fecha de entrada (implícito en la consulta SQL)

### Filtrado por Almacén

- Permite filtrar la lista para mostrar solo camiones en un almacén específico (S1 o S6)
- Incluye opción para ver todos los camiones independientemente del almacén

### Acciones Disponibles

Para cada camión en la lista, se ofrecen las siguientes acciones:

1. **Registrar salida**: Permite registrar la salida del camión de las instalaciones
2. **Borrar**: Elimina completamente el registro del camión
3. **Editar**: Permite modificar la información del registro
4. **Duplicar (+)**: Crea un nuevo registro con la misma información (útil para operaciones repetitivas)

## Flujo de Trabajo

1. El usuario accede a la página de listado (`/list`)
2. El sistema consulta la base de datos para obtener todos los camiones sin fecha de salida
3. Se muestra la tabla con los resultados
4. El usuario puede:
   - Filtrar por almacén usando el selector y botón "Filtrar"
   - Realizar acciones sobre cada registro (salida, borrar, editar, duplicar)

## Código Relacionado

### Función Principal (app.py)

```python
@app.route('/list', methods=['GET'])
def list_camiones():
    almacen_filter = request.args.get('almacen', '')
    
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        
        if almacen_filter:
            c.execute("""
                SELECT id, matricula_tractora, matricula_remolque, empresa, fecha_entrada, numero_envio, almacen, tipo 
                FROM camiones 
                WHERE fecha_salida IS NULL AND almacen = ?
            """, (almacen_filter,))
        else:
            c.execute("""
                SELECT id, matricula_tractora, matricula_remolque, empresa, fecha_entrada, numero_envio, almacen, tipo 
                FROM camiones 
                WHERE fecha_salida IS NULL
            """)
        
        camiones_dentro = c.fetchall()
    
    return render_template('list.html', camiones=camiones_dentro, almacen_filter=almacen_filter)
```

### Plantilla HTML (templates/list.html)

La plantilla `list.html` contiene la tabla de camiones y los formularios para las diferentes acciones. Los elementos clave son:

- Selector de filtro por almacén
- Tabla con información de camiones
- Formularios para cada acción (salida, borrar, editar, duplicar)

## Funciones Relacionadas

### Registrar Salida

```python
@app.route('/salida/<int:camion_id>', methods=['POST'])
def registrar_salida(camion_id):
    fecha_salida = get_current_datetime()

    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        # Primero obtenemos matricula_tractora y fecha_entrada de este camion_id
        c.execute('SELECT matricula_tractora, fecha_entrada FROM camiones WHERE id=?', (camion_id,))
        row = c.fetchone()
        if row:
            matricula_tractora = row[0]
            fecha_entrada_original = row[1]
            fecha_solo = fecha_entrada_original.split(' ')[0]

            # Actualizamos todos los registros que tengan la misma matrícula tractora y el mismo día de fecha_entrada
            c.execute('''
                UPDATE camiones
                SET fecha_salida = ?
                WHERE matricula_tractora = ?
                AND DATE(fecha_entrada) = ?
                AND fecha_salida IS NULL
            ''', (fecha_salida, matricula_tractora, fecha_solo))
            conn.commit()

    return redirect(url_for('list_camiones'))
```

### Borrar Registro

```python
@app.route('/delete/<int:camion_id>', methods=['POST'])
def delete_camion(camion_id):
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('DELETE FROM camiones WHERE id = ?', (camion_id,))
        conn.commit()
    return redirect(url_for('list_camiones'))
```

### Duplicar Registro

```python
@app.route('/replicate/<int:camion_id>', methods=['POST'])
def replicate_camion(camion_id):
    with sqlite3.connect('database.db') as conn:
        c = conn.cursor()
        c.execute('''
            SELECT matricula_tractora, matricula_remolque, empresa, fecha_entrada, numero_envio, almacen, tipo 
            FROM camiones 
            WHERE id = ?
        ''', (camion_id,))
        row = c.fetchone()

        if row:
            matricula_tractora = row[0]
            matricula_remolque = row[1]
            empresa = row[2]
            fecha_entrada = row[3]
            numero_envio = row[4] if row[4] else ''
            almacen = row[5] if row[5] else ''
            tipo = row[6] if row[6] else ''

            c.execute('''
                INSERT INTO camiones 
                (matricula_tractora, matricula_remolque, empresa, fecha_entrada, numero_envio, almacen, tipo) 
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (matricula_tractora, matricula_remolque, empresa, fecha_entrada, numero_envio, almacen, tipo))
            conn.commit()

        return redirect(url_for('list_camiones'))
```

## Consideraciones Especiales

### Comportamiento de Salida Masiva

Al registrar la salida de un camión, el sistema actualiza todos los registros del mismo camión (misma matrícula tractora) que entraron el mismo día. Esto es útil cuando un camión realiza múltiples operaciones en un mismo día.

### Seguridad

Las operaciones de borrado y edición no tienen confirmación adicional en la interfaz actual. Los usuarios deben tener cuidado al utilizar estas funciones ya que son irreversibles.

## Mejoras Potenciales

- Implementar paginación para manejar grandes volúmenes de datos
- Añadir confirmación antes de borrar registros
- Permitir ordenar la tabla por diferentes columnas
- Añadir más opciones de filtrado (por empresa, por tipo, etc.)
- Implementar un sistema de búsqueda dentro de la lista
