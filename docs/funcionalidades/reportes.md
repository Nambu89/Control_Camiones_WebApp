# Generación de Reportes

## Descripción General

La funcionalidad de generación de reportes permite a los usuarios obtener informes detallados de la actividad de camiones en un período específico. Esta herramienta es fundamental para el análisis de operaciones, auditorías y toma de decisiones basada en datos históricos.

## Interfaz de Usuario

Esta funcionalidad se encuentra en la ruta `/report` de la aplicación. La interfaz consta de un formulario para seleccionar el rango de fechas y una tabla que muestra los resultados.

![Generación de Reportes](../imagenes/reportes.png)

## Características Principales

### Selección de Rango de Fechas

- Permite especificar una fecha de inicio y una fecha de fin para el reporte
- Utiliza un selector de fechas (datepicker) para facilitar la entrada de datos
- El formato de fecha es DD-MM-YYYY para mayor claridad

### Visualización de Resultados

Los resultados se muestran en una tabla ordenada cronológicamente (de más antiguo a más reciente), incluyendo:
- Matrícula de la tractora
- Matrícula del remolque
- Empresa
- Fecha de entrada
- Fecha de salida (o "Aún dentro" si no ha salido)
- Número de envío
- Almacén
- Tipo de operación

### Exportación a CSV

- Incluye un botón para exportar los resultados del reporte a un archivo CSV
- El archivo CSV contiene los mismos datos que se muestran en la tabla
- Útil para análisis posterior en herramientas como Excel o para compartir datos

## Flujo de Trabajo

1. El usuario accede a la página de reportes (`/report`)
2. Selecciona la fecha de inicio y la fecha de fin utilizando el datepicker
3. Al hacer clic en "Filtrar", el sistema:
   - Convierte las fechas al formato adecuado para la consulta
   - Consulta la base de datos para obtener registros en ese rango de fechas
   - Muestra los resultados en la tabla
4. Si desea exportar los datos, el usuario hace clic en "Exportar a CSV"
5. El sistema genera un archivo CSV con los resultados y lo ofrece para descarga

## Código Relacionado

### Función Principal (app.py)

```python
@app.route('/report', methods=['GET', 'POST'])
def report():
    resultados = []
    start_date = ''
    end_date = ''

    if request.method == 'POST':
        start_date = request.form.get('start_date', '').strip()
        end_date = request.form.get('end_date', '').strip()

        def convert_date_format(d):
            day, month, year = d.split('-')
            return f"{year}-{month}-{day}"

        if start_date and end_date:
            start_date_iso = convert_date_format(start_date)
            end_date_iso = convert_date_format(end_date)

            with sqlite3.connect('database.db') as conn:
                c = conn.cursor()
                c.execute('''
                    SELECT matricula_tractora, matricula_remolque, empresa, fecha_entrada, fecha_salida, numero_envio, almacen, tipo
                    FROM camiones
                    WHERE fecha_entrada BETWEEN ? AND ?
                    ORDER BY fecha_entrada ASC
                ''', (start_date_iso + " 00:00:00", end_date_iso + " 23:59:59"))
                resultados = c.fetchall()

    return render_template('report.html', resultados=resultados, start_date=start_date, end_date=end_date)
```

### Función de Exportación a CSV

```python
@app.route('/export.csv', methods=['GET'])
def export_csv():
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')
    results = []

    def convert_date_format(d):
        day, month, year = d.split('-')
        return f"{year}-{month}-{day}"

    if start_date and end_date:
        start_date_iso = convert_date_format(start_date)
        end_date_iso = convert_date_format(end_date)

        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute('''
                SELECT matricula_tractora, matricula_remolque, empresa, fecha_entrada, fecha_salida, numero_envio, almacen, tipo
                FROM camiones
                WHERE fecha_entrada BETWEEN ? AND ?
                ORDER BY fecha_entrada ASC
            ''', (start_date_iso + " 00:00:00", end_date_iso + " 23:59:59"))
            results = c.fetchall()

    output = StringIO()
    writer = csv.writer(output, delimiter=',')
    writer.writerow(['Matrícula Tractora', 'Matrícula Remolque', 'Empresa', 'Fecha Entrada', 'Fecha Salida', 'Numero Envio', 'Almacén', 'Tipo'])
    for r in results:
        writer.writerow(r)

    csv_data = output.getvalue()
    output.close()

    response = Response(
        csv_data.encode('utf-8'),
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment; filename=report.csv'}
    )
    return response
```

### Plantilla HTML (templates/report.html)

La plantilla `report.html` contiene el formulario para seleccionar fechas y la tabla de resultados. Los elementos clave son:

- Formulario con campos de fecha (utilizando datepicker)
- Tabla para mostrar los resultados
- Botón para exportar a CSV
- Scripts para inicializar el datepicker

```html
<form method="post" class="mb-4">
    <div class="row g-3 align-items-center mb-3">
        <div class="col-auto">
            <label for="start_date" class="col-form-label">Fecha Inicio (DD-MM-YYYY):</label>
        </div>
        <div class="col-auto">
            <input type="text" id="start_date" name="start_date" class="form-control datepicker" 
                   value="{{ start_date }}" placeholder="DD-MM-YYYY" required>
        </div>
        <div class="col-auto">
            <label for="end_date" class="col-form-label">Fecha Fin (DD-MM-YYYY):</label>
        </div>
        <div class="col-auto">
            <input type="text" id="end_date" name="end_date" class="form-control datepicker" 
                   value="{{ end_date }}" placeholder="DD-MM-YYYY" required>
        </div>
        <div class="col-auto">
            <button type="submit" class="btn btn-primary">Filtrar</button>
        </div>
    </div>
</form>

{% if resultados %}
    <p>Mostrando resultados entre {{ start_date }} y {{ end_date }}</p>
    <table class="table table-striped table-bordered">
        <!-- Estructura de la tabla -->
    </table>

    <a class="btn btn-success" href="{{ url_for('export_csv', start_date=start_date, end_date=end_date) }}">Exportar a CSV</a>
{% endif %}
```

## Consulta SQL Utilizada

La generación de reportes utiliza una consulta SQL para filtrar registros por rango de fechas:

```sql
SELECT matricula_tractora, matricula_remolque, empresa, fecha_entrada, fecha_salida, numero_envio, almacen, tipo
FROM camiones
WHERE fecha_entrada BETWEEN 'fecha_inicio 00:00:00' AND 'fecha_fin 23:59:59'
ORDER BY fecha_entrada ASC
```

## Consideraciones Especiales

### Formato de Fechas

El sistema utiliza diferentes formatos de fecha:
- En la interfaz de usuario: DD-MM-YYYY (más intuitivo para usuarios)
- En la base de datos: YYYY-MM-DD HH:MM:SS (formato estándar ISO)

La función `convert_date_format` se encarga de convertir entre estos formatos.

### Datepicker

El sistema utiliza Bootstrap Datepicker para facilitar la selección de fechas. Este componente se inicializa mediante JavaScript:

```javascript
$(document).ready(function(){
    $('.datepicker').datepicker({
        format: 'dd-mm-yyyy',
        todayHighlight: true,
        autoclose: true
    });
});
```

## Mejoras Potenciales

- Implementar paginación para grandes volúmenes de resultados
- Añadir filtros adicionales (por empresa, almacén, tipo de operación)
- Incluir estadísticas básicas en el reporte (total de entradas, tiempo promedio de estancia, etc.)
- Permitir guardar reportes frecuentes como favoritos
- Implementar gráficos y visualizaciones de datos
- Añadir opción para exportar a otros formatos (Excel, PDF)
