# Registro de Entradas y Salidas

## Descripción General

La funcionalidad de registro de entradas y salidas es el componente central del Sistema de Control Logístico de Camiones. Permite registrar cuándo un camión entra a las instalaciones y cuándo sale, manteniendo un registro detallado de todos los movimientos.

## Interfaz de Usuario

Esta funcionalidad se encuentra en la página principal de la aplicación (`/`). La interfaz consta de un formulario que adapta su comportamiento según el estado del camión (dentro o fuera de las instalaciones).

![Registro de Entradas/Salidas](../imagenes/registro_entradas_salidas.png)

## Flujo de Trabajo

### Registro de Entrada

1. El usuario introduce la matrícula de la tractora en el formulario
2. Si el camión no está registrado como "dentro" (no tiene un registro con entrada sin salida), el sistema muestra el formulario completo para registrar entrada
3. El usuario completa los campos requeridos:
   - Matrícula de la tractora (obligatorio)
   - Matrícula del remolque (opcional)
   - Empresa (obligatorio)
   - Número de envío (opcional)
   - Almacén (S1 o S6, obligatorio)
   - Tipo (Carga o Descarga, obligatorio)
4. Al hacer clic en "Registrar entrada", el sistema:
   - Registra la fecha y hora actual como fecha de entrada
   - Crea un nuevo registro en la base de datos
   - Muestra la información del registro creado

### Registro de Salida

1. El usuario introduce la matrícula de la tractora en el formulario
2. Si el camión está registrado como "dentro" (tiene un registro con entrada sin salida), el sistema:
   - Muestra la información del registro existente
   - Cambia el botón a "Registrar salida"
3. Al hacer clic en "Registrar salida", el sistema:
   - Registra la fecha y hora actual como fecha de salida
   - Actualiza el registro existente en la base de datos
   - Muestra la información actualizada con la fecha de salida

## Código Relacionado

### Función Principal (app.py)

```python
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        matricula_tractora = request.form.get('matricula_tractora')
        matricula_remolque = request.form.get('matricula_remolque', '')
        empresa = request.form.get('empresa')
        numero_envio = request.form.get('numero_envio', '')
        almacen = request.form.get('almacen')
        tipo = request.form.get('tipo')

        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute('SELECT id, fecha_entrada, fecha_salida FROM camiones WHERE matricula_tractora = ? ORDER BY id DESC LIMIT 1', 
                     (matricula_tractora,))
            row = c.fetchone()

        if not row or (row and row[2] is not None):
            # Registrar entrada
            fecha_entrada = get_current_datetime()
            with sqlite3.connect('database.db') as conn:
                c = conn.cursor()
                c.execute('''
                    INSERT INTO camiones 
                    (matricula_tractora, matricula_remolque, empresa, fecha_entrada, numero_envio, almacen, tipo) 
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (matricula_tractora, matricula_remolque, empresa, fecha_entrada, numero_envio, almacen, tipo))
                conn.commit()
            return redirect(url_for('index', matricula_tractora=matricula_tractora))
        else:
            # Registrar salida
            cam_id = row[0]
            fecha_salida = get_current_datetime()
            with sqlite3.connect('database.db') as conn:
                c = conn.cursor()
                c.execute('UPDATE camiones SET fecha_salida = ? WHERE id = ?', (fecha_salida, cam_id))
                conn.commit()
            return redirect(url_for('index', matricula_tractora=matricula_tractora))
```

## Plantilla HTML (templates/index.html)

La plantilla `index.html` contiene el formulario que se adapta según el estado del camión. Los elementos clave son:

- Campos de entrada para la información del camión
- Lógica condicional para mostrar "Registrar entrada" o "Registrar salida"
- Sección para mostrar la información del camión consultado

## Consideraciones Especiales

### Zona Horaria

El sistema utiliza la zona horaria de España (Europe/Madrid) para registrar las fechas y horas:

```python
def get_current_datetime():
    """Obtiene la fecha y hora actual en la zona horaria de España"""
    return datetime.now(TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')
```

### Validación de Datos

El formulario incluye validación básica:
- Campos obligatorios marcados con `required`
- Selección obligatoria de almacén y tipo de operación

### Comportamiento de Salida Masiva

Cuando se registra la salida de un camión desde la página de listado, el sistema actualiza todos los registros del mismo camión (misma matrícula tractora) que entraron el mismo día:

```python
c.execute('''
    UPDATE camiones
    SET fecha_salida = ?
    WHERE matricula_tractora = ?
    AND DATE(fecha_entrada) = ?
    AND fecha_salida IS NULL
''', (fecha_salida, matricula_tractora, fecha_solo))
```

## Mejoras Potenciales

- Implementar validación más robusta de matrículas (formato, caracteres permitidos)
- Añadir confirmación antes de registrar salida
- Permitir especificar manualmente la fecha/hora en casos especiales
- Implementar un sistema de escaneo de matrículas para automatizar el proceso
