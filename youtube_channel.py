def get_channel_id(youtube, channel_id=None, username=None):
    if channel_id:
        return channel_id
    request = youtube.channels().list(
        part="id",
        forUsername=username
    )
    response = request.execute()
    if response["items"]:
        return response["items"][0]["id"]
    return None

def get_channel_stats(youtube, channel_id):
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=channel_id
    )
    response = request.execute()
    if 'items' not in response or not response['items']:
        print(f"No se pudieron obtener las estadísticas del canal con ID '{channel_id}'.")
        return None
    return response['items'][0]
