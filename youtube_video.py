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
    statuses = {
        "public": 0,
        "unlisted": 0,
        "private": 0,
        "other": 0
    }
    total_views = 0
    total_likes = 0

    next_page_token = None
    while True:
        request = youtube.search().list(
            part="id",
            channelId=channel_id,
            maxResults=50,
            type="video",
            pageToken=next_page_token
        )
        response = request.execute()

        video_ids = [item['id']['videoId'] for item in response['items']]

        for video_id in video_ids:
            request = youtube.videos().list(
                part="status,statistics",
                id=video_id
            )
            response = request.execute()
            if 'items' in response and response['items']:
                status = response['items'][0]['status']['privacyStatus']
                if status in statuses:
                    statuses[status] += 1
                else:
                    statuses["other"] += 1

                total_views += int(response['items'][0]['statistics'].get('viewCount', 0))
                total_likes += int(response['items'][0]['statistics'].get('likeCount', 0))

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    return statuses, total_views, total_likes
