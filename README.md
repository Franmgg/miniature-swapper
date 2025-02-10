# Miniature Swapper

## Requisitos

- Python 3.8+
- pip
- [Google API Client Library for Python](https://developers.google.com/api-client-library/python/start/installation)
- [Pillow](https://pillow.readthedocs.io/en/stable/installation.html)
- [python-dotenv](https://pypi.org/project/python-dotenv/)

## Instalación

1. Clonar el repositorio:

   ```sh
   git clone https://github.com/tu_usuario/miniature-swapper.git
   cd miniature-swapper
   ```

2. Crear y activar un entorno virtual:

   ```sh
   python -m venv venv
   source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
   ```

3. Instalar las dependencias:

   ```sh
   pip install -r requirements.txt
   ```

4. Crear un archivo `.env` en la raíz del proyecto con el siguiente contenido:

   ```dotenv
   DEVELOPER_KEY=your_developer_key_here
   CHANNEL_ID=your_channel_id_here
   CHANNEL_USERNAME=your_channel_username_here
   CHANNEL_USER_ID=your_channel_user_id_here
   VIDEOS_DIR=./videos
   ```

5. Ejecutar el script:
   ```sh
   python main.py
   ```

## Uso

El script autentica con la API de YouTube, obtiene estadísticas del canal, estados de los videos y cambia las miniaturas de los videos.

## Ejecución con Docker

1. Construye la imagen de Docker:
   ```sh
   docker build -t miniature-swapper .
   ```
2. Ejecuta el contenedor de Docker:
   ```sh
   docker run --rm -v $(pwd)/credentials.json:/app/credentials.json -v $(pwd)/token.json:/app/token.json -v $(pwd)/videos:/app/videos miniature-swapper
   ```
