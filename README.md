# Miniature Swapper

Esta aplicación cambia la miniatura de un video en YouTube tres veces a la semana.

## Configuración

1. Clona este repositorio.
2. Instala las dependencias necesarias:
   ```sh
   pip install google-api-python-client python-dotenv
   ```
3. Crea una carpeta `videos` en el directorio del proyecto.
4. Dentro de la carpeta `videos`, crea una subcarpeta con el nombre o ID del video.
5. Dentro de cada subcarpeta, coloca tres imágenes con los nombres `nombredelvideo_01.png`, `nombredelvideo_02.png`, `nombredelvideo_03.png`.
6. Crea un archivo `.env` en el directorio del proyecto y agrega tu clave de desarrollador de la API de YouTube y el nombre de usuario del canal:
   ```env
   DEVELOPER_KEY=your_developer_key_here
   CHANNEL_USERNAME=canal_youtube
   ```

## Ejecución

1. Ejecuta el script:
   ```sh
   python main.py
   ```
