import os
import time
from dotenv import load_dotenv
from youtube_client import build_youtube_client
from youtube_channel import get_channel_id, get_channel_stats
from youtube_video import get_video_statuses, get_videos_from_channel, change_thumbnail

# Cargar variables de entorno desde el archivo .env
load_dotenv()

def main():
    # Configuración de la API de YouTube
    developer_key = os.getenv("DEVELOPER_KEY")
    channel_id = os.getenv("CHANNEL_ID")
    username = os.getenv("CHANNEL_USERNAME")

    youtube = build_youtube_client(developer_key)

    # Obtener ID del canal
    channel_id = get_channel_id(youtube, channel_id, username)
    if not channel_id:
        return

    # Obtener estadísticas del canal
    channel_stats = get_channel_stats(youtube, channel_id)
    if channel_stats:        
        print("Estadísticas del canal:")
        print(f"Nombre: {channel_stats['snippet']['title']}")
        print(f"Suscriptores: {channel_stats['statistics']['subscriberCount']}")
        print(f"Total de videos: {channel_stats['statistics']['videoCount']}")        
        print("-----------")

    # Obtener estados de los videos y sumar visitas y likes
    video_statuses, total_views, total_likes = get_video_statuses(youtube, channel_id)
    if video_statuses:        
        print("-Estados de los videos:")
        print(f"--Videos públicos: {video_statuses['public']}")
        print(f"--Videos no listados: {video_statuses['unlisted']}")
        print(f"--Videos privados: {video_statuses['private']}")
        print(f"--Otros estados: {video_statuses['other']}")
        print("-----------")
        print(f"Total de vistas: {total_views}")
        print(f"Total de likes: {total_likes}")

    # Obtener videos del canal
    video_ids = get_videos_from_channel(youtube, channel_id)
    if not video_ids:
        print("El canal no tiene videos recientes.")
        return

    # Directorio de videos
    videos_dir = os.getenv("VIDEOS_DIR")

    while True:
        for video_id in video_ids:
            video_path = os.path.join(videos_dir, video_id)
            thumbnails = sorted([f for f in os.listdir(video_path) if f.endswith('.png')])

            for thumbnail in thumbnails:
                thumbnail_path = os.path.join(video_path, thumbnail)
                change_thumbnail(youtube, video_id, thumbnail_path)
                time.sleep(2 * 24 * 60 * 60)  # Esperar 2 días

if __name__ == "__main__":
    main()
