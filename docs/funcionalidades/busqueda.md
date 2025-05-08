# Búsqueda de Registros

## Descripción General

La funcionalidad de búsqueda permite a los usuarios encontrar registros históricos de camiones utilizando diferentes criterios. Esta herramienta es esencial para consultar información sobre movimientos pasados, verificar la actividad de un camión específico o buscar registros relacionados con una empresa determinada.

## Interfaz de Usuario

Esta funcionalidad se encuentra en la ruta `/search` de la aplicación. La interfaz consta de un formulario de búsqueda simple y una tabla de resultados.

![Búsqueda de Registros](../imagenes/busqueda.png)

## Características Principales

### Búsqueda Flexible

La búsqueda permite encontrar registros basándose en varios criterios:
- Matrícula de la tractora
- Matrícula del remolque
- Nombre de la empresa
- Número de envío

El sistema utiliza búsqueda parcial (operador LIKE en SQL), lo que significa que el término de búsqueda puede estar contenido en cualquier parte del campo, no necesariamente al principio.

### Visualización de Resultados

Los resultados se muestran en una tabla ordenada cronológicamente (de más reciente a más antiguo), incluyendo:
- Matrícula de la tractora
- Matrícula del remolque
- Empresa
- Fecha de entrada
- Fecha de salida (o "Aún dentro" si no ha salido)
- Número de envío
- Almacén
- Tipo de operación

## Flujo de Trabajo

1. El usuario accede a la página de búsqueda (`/search`)
2. Introduce un término de búsqueda en el campo correspondiente
3. Al hacer clic en "Buscar", el sistema:
   - Consulta la base de datos buscando coincidencias parciales en los campos relevantes
   - Ordena los resultados por fecha de entrada (más recientes primero)
   - Muestra los resultados en la tabla
4. Si no hay resultados, se muestra un mensaje indicando que no se encontraron coincidencias

## Código Relacionado

### Función Principal (app.py)

```python
@app.route('/search', methods=['GET', 'POST'])
def search():
    resultados = []
    query = ''
    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute("""
                SELECT matricula_tractora, matricula_remolque, empresa, fecha_entrada, fecha_salida, numero_envio, almacen, tipo
                FROM camiones
                WHERE matricula_tractora LIKE ? 
                OR matricula_remolque LIKE ?
                OR empresa LIKE ? 
                OR numero_envio LIKE ?
                ORDER BY fecha_entrada DESC
            """, (f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"))
            resultados = c.fetchall()
    return render_template('search.html', query=query, resultados=resultados)
```

### Plantilla HTML (templates/search.html)

La plantilla `search.html` contiene el formulario de búsqueda y la tabla de resultados. Los elementos clave son:

- Formulario con campo de búsqueda
- Tabla para mostrar los resultados
- Lógica condicional para mostrar mensajes cuando no hay resultados

```html
<form method="post" class="mb-4">
    <div class="row g-3 align-items-center">
        <div class="col-auto">
            <label for="query" class="col-form-label">Matrícula, Empresa o Nº de envío:</label>
        </div>
        <div class="col-auto">
            <input type="text" id="query" name="query" class="form-control" value="{{ query }}" required>
        </div>
        <div class="col-auto">
            <button type="submit" class="btn btn-primary">Buscar</button>
        </div>
    </div>
</form>

{% if resultados %}
    <table class="table table-striped table-bordered">
        <!-- Estructura de la tabla -->
    </table>
{% elif query %}
    <p>No se encontraron resultados para <strong>{{ query }}</strong>.</p>
{% endif %}
```

## Consulta SQL Utilizada

La búsqueda utiliza una consulta SQL con operadores LIKE para encontrar coincidencias parciales:

```sql
SELECT matricula_tractora, matricula_remolque, empresa, fecha_entrada, fecha_salida, numero_envio, almacen, tipo
FROM camiones
WHERE matricula_tractora LIKE '%término%' 
OR matricula_remolque LIKE '%término%'
OR empresa LIKE '%término%' 
OR numero_envio LIKE '%término%'
ORDER BY fecha_entrada DESC
```

## Consideraciones Especiales

### Rendimiento

La búsqueda con operadores LIKE puede ser ineficiente en bases de datos grandes. En la implementación actual, esto no debería ser un problema para volúmenes moderados de datos, pero podría convertirse en una limitación si la base de datos crece significativamente.

### Seguridad

La implementación actual utiliza parámetros en las consultas SQL, lo que protege contra ataques de inyección SQL.

## Mejoras Potenciales

- Implementar búsqueda avanzada con múltiples criterios específicos
- Añadir filtros por rango de fechas en la búsqueda
- Implementar paginación para grandes volúmenes de resultados
- Permitir ordenar los resultados por diferentes columnas
- Añadir la posibilidad de exportar los resultados de búsqueda a CSV
- Implementar búsqueda por almacén y tipo de operación
