from flask import Flask, render_template, request, redirect, url_for, Response
import sqlite3
from datetime import datetime
from pytz import timezone
import csv
from io import StringIO
import os

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Configuration — all values are overridable via environment variables.
# Copy .env.example to .env and adjust as needed.
# ---------------------------------------------------------------------------
DATABASE_PATH = os.environ.get('DATABASE_PATH', 'database.db')
TIMEZONE_NAME = os.environ.get('APP_TIMEZONE', 'Europe/Madrid')
TIMEZONE = timezone(TIMEZONE_NAME)
DEBUG = os.environ.get('FLASK_DEBUG', '0').lower() in ('1', 'true', 'yes')
PORT = int(os.environ.get('PORT', '5000'))

def init_db():
    with sqlite3.connect(DATABASE_PATH) as conn:
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

init_db()

def get_current_datetime():
    """Obtiene la fecha y hora actual en la zona horaria de España"""
    return datetime.now(TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        matricula_tractora = request.form.get('matricula_tractora')
        matricula_remolque = request.form.get('matricula_remolque', '')
        empresa = request.form.get('empresa')
        numero_envio = request.form.get('numero_envio', '')
        almacen = request.form.get('almacen')  # Nuevo campo
        tipo = request.form.get('tipo')  # Nuevo campo

        with sqlite3.connect(DATABASE_PATH) as conn:
            c = conn.cursor()
            c.execute('SELECT id, fecha_entrada, fecha_salida FROM camiones WHERE matricula_tractora = ? ORDER BY id DESC LIMIT 1',
                     (matricula_tractora,))
            row = c.fetchone()

        if not row or (row and row[2] is not None):
            # Registrar entrada
            fecha_entrada = get_current_datetime()
            with sqlite3.connect(DATABASE_PATH) as conn:
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
            with sqlite3.connect(DATABASE_PATH) as conn:
                c = conn.cursor()
                c.execute('UPDATE camiones SET fecha_salida = ? WHERE id = ?', (fecha_salida, cam_id))
                conn.commit()
            return redirect(url_for('index', matricula_tractora=matricula_tractora))

    matricula_tractora = request.args.get('matricula_tractora', '')
    matricula_remolque = ''
    empresa = ''
    fecha_entrada = None
    fecha_salida = None
    entrada_registrada = False
    salida_registrada = False
    numero_envio = ''
    almacen = ''
    tipo = ''

    if matricula_tractora:
        with sqlite3.connect(DATABASE_PATH) as conn:
            c = conn.cursor()
            c.execute('''
                SELECT id, empresa, matricula_remolque, fecha_entrada, fecha_salida, numero_envio, almacen, tipo
                FROM camiones 
                WHERE matricula_tractora = ? 
                ORDER BY id DESC LIMIT 1
            ''', (matricula_tractora,))
            row = c.fetchone()
            if row:
                empresa = row[1]
                matricula_remolque = row[2]
                fecha_entrada = row[3]
                fecha_salida = row[4]
                numero_envio = row[5]
                almacen = row[6] if row[6] else ''
                tipo = row[7] if row[7] else ''
                if fecha_entrada and not fecha_salida:
                    entrada_registrada = True
                if fecha_salida:
                    salida_registrada = True

    return render_template('index.html',
                         matricula_tractora=matricula_tractora,
                         matricula_remolque=matricula_remolque,
                         empresa=empresa,
                         fecha_entrada=fecha_entrada,
                         fecha_salida=fecha_salida,
                         entrada_registrada=entrada_registrada,
                         salida_registrada=salida_registrada,
                         numero_envio=numero_envio,
                         almacen=almacen,
                         tipo=tipo)

@app.route('/list', methods=['GET'])
def list_camiones():
    almacen_filter = request.args.get('almacen', '')
    
    with sqlite3.connect(DATABASE_PATH) as conn:
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

@app.route('/salida/<int:camion_id>', methods=['POST'])
def registrar_salida(camion_id):
    fecha_salida = get_current_datetime()

    with sqlite3.connect(DATABASE_PATH) as conn:
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

@app.route('/replicate/<int:camion_id>', methods=['POST'])
def replicate_camion(camion_id):
    with sqlite3.connect(DATABASE_PATH) as conn:
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

@app.route('/delete/<int:camion_id>', methods=['POST'])
def delete_camion(camion_id):
    with sqlite3.connect(DATABASE_PATH) as conn:
        c = conn.cursor()
        c.execute('DELETE FROM camiones WHERE id = ?', (camion_id,))
        conn.commit()
    return redirect(url_for('list_camiones'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    resultados = []
    query = ''
    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        with sqlite3.connect(DATABASE_PATH) as conn:
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

            with sqlite3.connect(DATABASE_PATH) as conn:
                c = conn.cursor()
                c.execute('''
                    SELECT matricula_tractora, matricula_remolque, empresa, fecha_entrada, fecha_salida, numero_envio, almacen, tipo
                    FROM camiones
                    WHERE fecha_entrada BETWEEN ? AND ?
                    ORDER BY fecha_entrada ASC
                ''', (start_date_iso + " 00:00:00", end_date_iso + " 23:59:59"))
                resultados = c.fetchall()

    return render_template('report.html', resultados=resultados, start_date=start_date, end_date=end_date)

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

        with sqlite3.connect(DATABASE_PATH) as conn:
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
        
        with sqlite3.connect(DATABASE_PATH) as conn:
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
        with sqlite3.connect(DATABASE_PATH) as conn:
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

if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)