from googleapiclient.http import MediaFileUpload
from datetime import datetime, timedelta

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

def get_video_statuses(youtube, channel_id):
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=50,
        order="date"
    )
    response = request.execute()

    video_statuses = {
        'public': 0,
        'unlisted': 0,
        'private': 0,
        'other': 0
    }
    total_views = 0
    total_likes = 0

    for item in response['items']:
        if item['id']['kind'] == 'youtube#video':
            video_id = item['id']['videoId']
            video_response = youtube.videos().list(
                part="status,statistics",
                id=video_id
            ).execute()

            for video in video_response['items']:
                status = video['status']['privacyStatus']
                if status in video_statuses:
                    video_statuses[status] += 1
                else:
                    video_statuses['other'] += 1

                total_views += int(video['statistics'].get('viewCount', 0))
                total_likes += int(video['statistics'].get('likeCount', 0))

    return video_statuses, total_views, total_likes
