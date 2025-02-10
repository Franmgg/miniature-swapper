from googleapiclient.discovery import build

def build_youtube_client(developer_key):
    api_service_name = "youtube"
    api_version = "v3"
    return build(api_service_name, api_version, developerKey=developer_key)
