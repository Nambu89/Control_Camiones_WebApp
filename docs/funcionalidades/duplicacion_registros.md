# Duplicación de Registros

## Descripción General

La funcionalidad de duplicación de registros permite a los usuarios crear rápidamente una copia exacta de un registro existente. Esta característica es especialmente útil cuando un mismo camión realiza múltiples operaciones similares, evitando la necesidad de volver a introducir toda la información manualmente.

## Interfaz de Usuario

Esta funcionalidad se accede desde la página de listado de camiones, a través del botón "+" (más) disponible para cada registro. No existe una interfaz dedicada para esta funcionalidad, ya que se ejecuta directamente desde la lista.

![Duplicación de Registros](../imagenes/duplicacion_registros.png)

## Características Principales

### Duplicación Instantánea

- La duplicación se realiza con un solo clic en el botón "+"
- No hay formulario intermedio para modificar datos antes de duplicar
- El nuevo registro se crea inmediatamente con los mismos datos que el original

### Datos Duplicados

Los siguientes campos se copian del registro original al nuevo registro:
- Matrícula de la tractora
- Matrícula del remolque
- Empresa
- Fecha de entrada (se mantiene la misma)
- Número de envío
- Almacén
- Tipo

### Comportamiento de Fechas

- La fecha de entrada se copia exactamente igual que en el registro original
- El nuevo registro no tiene fecha de salida (se establece como NULL)

## Flujo de Trabajo

1. El usuario accede a la página de listado de camiones (`/list`)
2. Localiza el registro que desea duplicar
3. Hace clic en el botón "+" para ese registro
4. El sistema:
   - Recupera todos los datos del registro original
   - Crea un nuevo registro con esos datos
   - Actualiza la página de listado
   - Muestra la lista actualizada con el nuevo registro añadido

## Código Relacionado

### Función Principal (app.py)

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

### Formulario en la Plantilla HTML (templates/list.html)

```html
<form method="post" action="{{ url_for('replicate_camion', camion_id=c[0]) }}" style="display:inline-block; margin-left:5px;">
    <button type="submit" class="btn btn-success">+</button>
</form>
```

## Consultas SQL Utilizadas

La duplicación de registros utiliza dos consultas SQL:

1. Selección del registro original:
```sql
SELECT matricula_tractora, matricula_remolque, empresa, fecha_entrada, numero_envio, almacen, tipo 
FROM camiones 
WHERE id = ?
```

2. Inserción del nuevo registro:
```sql
INSERT INTO camiones 
(matricula_tractora, matricula_remolque, empresa, fecha_entrada, numero_envio, almacen, tipo) 
VALUES (?, ?, ?, ?, ?, ?, ?)
```

## Consideraciones Especiales

### Duplicación de Fecha de Entrada

Al duplicar un registro, la fecha de entrada se copia exactamente igual que en el registro original, lo que significa que el nuevo registro tendrá la misma fecha y hora de entrada que el original. Esto puede no reflejar la realidad si la duplicación se está utilizando para registrar una nueva entrada del mismo camión en un momento diferente.

### Valores Nulos

Si algún campo opcional (como `numero_envio`, `almacen` o `tipo`) es NULL en el registro original, se establece como una cadena vacía en el nuevo registro.

### Seguridad

- La implementación utiliza parámetros en las consultas SQL para prevenir ataques de inyección SQL
- No hay restricciones de acceso a esta funcionalidad en la versión actual

## Casos de Uso Comunes

- Duplicar registros para camiones que realizan múltiples cargas o descargas en el mismo día
- Crear rápidamente registros para camiones de la misma empresa con datos similares
- Facilitar la entrada de datos para operaciones repetitivas

## Mejoras Potenciales

- Implementar un formulario intermedio que permita modificar algunos datos antes de crear el duplicado
- Actualizar automáticamente la fecha de entrada al momento actual en lugar de copiar la fecha original
- Añadir un contador o sufijo al número de envío para diferenciar duplicados
- Permitir seleccionar qué campos duplicar y cuáles dejar en blanco o con valores predeterminados
- Implementar una opción de duplicación masiva para crear múltiples copias a la vez
