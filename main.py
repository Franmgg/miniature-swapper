import os
import time
import json
import datetime
import random
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv
from youtube_client import build_youtube_client
from youtube_channel import get_channel_id, get_channel_stats
from youtube_video import get_video_statuses, get_videos_from_channel, change_thumbnail
from PIL import Image, ImageDraw, ImageFont

# Cargar variables de entorno desde el archivo .env
load_dotenv()

SCOPES = [
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/youtube',
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/youtubepartner',
    'https://www.googleapis.com/auth/youtubepartner-channel-audit',
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube.channel-memberships.creator'
]
TOKEN_FILE = 'token.json'

def authenticate_youtube():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
    return build('youtube', 'v3', credentials=creds)

def get_next_image(video_id):
    video_dir = os.path.join('videos', video_id)
    images = sorted([img for img in os.listdir(video_dir) if img.endswith('.png')])
    current_image_file = os.path.join(video_dir, 'current_image.txt')
    if os.path.exists(current_image_file):
        with open(current_image_file, 'r') as f:
            current_image = f.read().strip()
        next_image = images[(images.index(current_image) + 1) % len(images)]
    else:
        next_image = images[0]
    with open(current_image_file, 'w') as f:
        f.write(next_image)
    return os.path.join(video_dir, next_image)

def generate_placeholder_image(image_path, title):
    width, height = 1280, 720
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)

    # Generate two random colors for the gradient
    color1 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    color2 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # Create gradient background
    for y in range(height):
        ratio = y / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Load a font with 200px size
    font_path = "arial.ttf"  # Ensure this font file is available in your environment
    font = ImageFont.truetype(font_path, 200)

    # Calculate text size and position
    text_bbox = draw.textbbox((0, 0), title, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2

    # Draw the title text in the middle
    draw.text((text_x, text_y), title, fill="white", font=font)

    # Save the image
    image.save(image_path)

def main():
    # Configuración de la API de YouTube
    channel_id = os.getenv("CHANNEL_ID")
    username = os.getenv("CHANNEL_USERNAME")

    youtube = authenticate_youtube()

    # Obtener ID del canal
    channel_id = get_channel_id(youtube, channel_id, username)
    if not channel_id:
        return

    try:
        # Obtener estadísticas del canal
        channel_stats = get_channel_stats(youtube, channel_id)
        if channel_stats:        
            print("Estadísticas del canal:")
            print(f"Nombre: {channel_stats['snippet']['title']}")
            print(f"Suscriptores: {channel_stats['statistics']['subscriberCount']}")
            print(f"Total de videos: {channel_stats['statistics']['videoCount']}")        
            print("-----------")
    except HttpError as e:
        print(f"Error al obtener las estadísticas del canal: {e}")

    try:
        # Obtener estados de los videos y sumar visitas y likes
        video_statuses, total_views, total_likes = get_video_statuses(youtube, channel_id)
        if video_statuses:        
            print("-Estados de los videos:")
            print(f"--Videos públicos: {video_statuses['public']}")
            print("-----------")
            print(f"Total de vistas: {total_views}")
            print(f"Total de likes: {total_likes}")
    except HttpError as e:
        print(f"Error al obtener los estados de los videos: {e}")

    try:
        # Obtener videos del canal
        video_ids = get_videos_from_channel(youtube, channel_id)
        if not video_ids:
            print("El canal no tiene videos recientes.")
            return
    except HttpError as e:
        print(f"Error al obtener los videos del canal: {e}")
        video_ids = []

    # Directorio de videos
    videos_dir = os.getenv("VIDEOS_DIR")

    for video_id in video_ids:
        video_path = os.path.join(videos_dir, video_id)
        if not os.path.exists(video_path):
            print(f"El directorio {video_path} no existe. Creando directorio y archivos de imagen de marcador de posición.")
            os.makedirs(video_path)

            # Obtener el título del video
            try:
                video_response = youtube.videos().list(
                    part="snippet",
                    id=video_id
                ).execute()
                video_title = video_response['items'][0]['snippet']['title']
            except HttpError as e:
                print(f"Error al obtener el título del video {video_id}: {e}")
                video_title = "Placeholder"

            for i in range(1, 4):
                placeholder_image_path = os.path.join(video_path, f"{video_title}_0{i}.png")
                generate_placeholder_image(placeholder_image_path, video_title)

        try:
            thumbnail_path = get_next_image(video_id)
            change_thumbnail(youtube, video_id, thumbnail_path)
        except HttpError as e:
            print(f"Error al cambiar la miniatura del video {video_id}: {e}")

if __name__ == "__main__":
    main()
