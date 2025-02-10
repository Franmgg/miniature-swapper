FROM python:3.8-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos necesarios
COPY requirements.txt .
COPY main.py .
COPY youtube_client.py .
COPY youtube_channel.py .
COPY youtube_video.py .
COPY .env .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos del proyecto
COPY . .

# Comando para ejecutar el script
CMD ["python", "main.py"]
