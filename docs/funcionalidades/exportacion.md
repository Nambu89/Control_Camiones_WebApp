# Exportación de Datos

## Descripción General

La funcionalidad de exportación de datos permite a los usuarios extraer información del sistema en formato CSV (Comma-Separated Values) para su análisis en herramientas externas como Microsoft Excel, Google Sheets u otras aplicaciones de análisis de datos. Esta característica es especialmente útil para generar informes personalizados, realizar análisis estadísticos o compartir datos con otros departamentos.

## Interfaz de Usuario

La exportación de datos está integrada en la funcionalidad de reportes y se accede a través de un botón "Exportar a CSV" que aparece después de generar un reporte por rango de fechas.

![Exportación de Datos](../imagenes/exportacion.png)

## Características Principales

### Formato de Exportación

- Los datos se exportan en formato CSV (valores separados por comas)
- El archivo incluye una cabecera con los nombres de las columnas
- La codificación utilizada es UTF-8 para garantizar la compatibilidad con caracteres especiales

### Datos Incluidos

El archivo CSV exportado incluye los siguientes campos:
- Matrícula Tractora
- Matrícula Remolque
- Empresa
- Fecha Entrada
- Fecha Salida
- Número de Envío
- Almacén
- Tipo

### Filtrado por Fechas

- La exportación se basa en el rango de fechas seleccionado en la pantalla de reportes
- Solo se exportan los registros cuya fecha de entrada está dentro del rango especificado

## Flujo de Trabajo

1. El usuario accede a la página de reportes (`/report`)
2. Selecciona un rango de fechas y genera el reporte
3. Una vez que se muestran los resultados, hace clic en el botón "Exportar a CSV"
4. El sistema:
   - Ejecuta la misma consulta que para el reporte
   - Genera un archivo CSV con los resultados
   - Configura las cabeceras HTTP para que el navegador descargue el archivo
5. El navegador descarga el archivo con el nombre "report.csv"

## Código Relacionado

### Función de Exportación a CSV (app.py)

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

### Enlace en la Plantilla HTML (templates/report.html)

```html
{% if resultados %}
    <p>Mostrando resultados entre {{ start_date }} y {{ end_date }}</p>
    <table class="table table-striped table-bordered">
        <!-- Estructura de la tabla -->
    </table>

    <a class="btn btn-success" href="{{ url_for('export_csv', start_date=start_date, end_date=end_date) }}">Exportar a CSV</a>
{% endif %}
```

## Detalles Técnicos

### Generación del CSV

El sistema utiliza las siguientes bibliotecas de Python para generar el archivo CSV:
- `csv`: Para escribir datos en formato CSV
- `StringIO`: Para crear un buffer en memoria donde escribir los datos
- `Response` (de Flask): Para generar una respuesta HTTP con el archivo adjunto

### Configuración de la Respuesta HTTP

Para que el navegador descargue el archivo, se configuran las siguientes cabeceras HTTP:
- `Content-Type: text/csv`: Indica que el contenido es un archivo CSV
- `Content-Disposition: attachment; filename=report.csv`: Indica al navegador que debe descargar el archivo con el nombre "report.csv"

## Consideraciones Especiales

### Formato de Fechas

Las fechas en el archivo CSV mantienen el formato original de la base de datos (YYYY-MM-DD HH:MM:SS), lo que facilita su procesamiento en herramientas de análisis.

### Manejo de Valores Nulos

Los valores nulos (NULL) en la base de datos se exportan como cadenas vacías en el CSV.

### Seguridad

La implementación utiliza parámetros en las consultas SQL para prevenir ataques de inyección SQL.

## Mejoras Potenciales

- Permitir seleccionar qué columnas incluir en la exportación
- Ofrecer diferentes formatos de exportación (Excel, PDF, JSON)
- Implementar opciones de filtrado adicionales para la exportación
- Añadir la posibilidad de programar exportaciones automáticas periódicas
- Incluir estadísticas calculadas en la exportación
- Permitir personalizar el nombre del archivo exportado
