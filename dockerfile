# Usa una imagen base con Python 3.10
FROM python:3.12-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos requirements.txt a la carpeta de trabajo
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de tu proyecto en el contenedor
COPY . .

# Expone el puerto en el que la app se ejecutará (por defecto Flask corre en el 5000)
EXPOSE 5000

# Comando para ejecutar la aplicación con gunicorn en modo producción
# Ajusta "app:app" según el nombre del fichero donde está tu instancia de Flask si es distinto
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
