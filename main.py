import os
import time
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

def change_thumbnail(youtube, video_id, thumbnail_path):
    request = youtube.thumbnails().set(
        videoId=video_id,
        media_body=MediaFileUpload(thumbnail_path)
    )
    response = request.execute()
    return response

def get_videos_from_channel(youtube, channel_id):
    request = youtube.search().list(
        part="id,snippet",
        channelId=channel_id,
        maxResults=50,
        type="video",
        order="date"
    )
    response = request.execute()
    video_ids = []
    three_weeks_ago = datetime.now() - timedelta(weeks=3)
    for item in response['items']:
        video_id = item['id']['videoId']
        published_at = datetime.strptime(item['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%SZ")
        if published_at >= three_weeks_ago:
            video_ids.append(video_id)
    return video_ids

def get_channel_id(youtube, channel_id, username):
    if channel_id:
        request = youtube.channels().list(
            part="id",
            id=channel_id
        )
        response = request.execute()
        if 'items' in response and response['items']:
            return response['items'][0]['id']
        else:
            print(f"El canal con el ID '{channel_id}' no existe o no se pudo obtener.")
    
    if username:
        request = youtube.channels().list(
            part="id",
            forUsername=username
        )
        response = request.execute()
        if 'items' in response and response['items']:
            return response['items'][0]['id']
        else:
            print(f"El canal con el nombre de usuario '{username}' no existe o no se pudo obtener.")
    
    return None

def main():
    # Configuración de la API de YouTube
    api_service_name = "youtube"
    api_version = "v3"
    developer_key = os.getenv("DEVELOPER_KEY")
    channel_id = os.getenv("CHANNEL_ID")
    username = os.getenv("CHANNEL_USERNAME")

    youtube = build(api_service_name, api_version, developerKey=developer_key)

    # Obtener ID del canal
    channel_id = get_channel_id(youtube, channel_id, username)
    if not channel_id:
        return

    # Obtener videos del canal
    video_ids = get_videos_from_channel(youtube, channel_id)
    if not video_ids:
        print("El canal no tiene videos recientes.")
        return

    # Directorio de videos
    videos_dir = "/c:/Users/0xc/projects/miniature-swapper/videos"

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
