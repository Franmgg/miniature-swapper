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
