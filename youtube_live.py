import os
import googleapiclient
import logging

from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
# from log import log_error




load_dotenv()
YOUTUBE_API = os.getenv('YOUTUBE_API')
CHANNEL_ID = os.getenv('CHANNEL_ID')
youtube = build(serviceName='youtube',version='v3', developerKey=YOUTUBE_API)


def get_channel():
    try:
        channel = youtube.channels().list(
            part='snippet,contentDetails,statistics',
            id=CHANNEL_ID,
            maxResults=1
        ).execute()

        # Kiểm tra xem kênh có custom URL không
        channel_info = channel['items'][0]
        custom_url = channel_info['snippet'].get('customUrl')

        if custom_url:
            return f"https://www.youtube.com/{custom_url}"
        else:
            # Trả về URL kênh dựa trên CHANNEL_ID nếu không có custom URL
            return f"https://www.youtube.com/channel/{CHANNEL_ID}"
    except HttpError as e:
        print(e)
    return None 

def get_list_live_video():
    try:
        list_live_video = youtube.search().list(
            part='snippet',
            channelId=CHANNEL_ID,
            type='video',
            eventType='live',
        ).execute()
        return list_live_video
    except HttpError as e:
        print(e)
    return None


def get_live_video_id(list_live_video):
    if list_live_video is not None:
        if len(list_live_video['items']) > 0:
            return list_live_video['items'][0]['id']['videoId']
        return None
    return None

def get_live_chat_comment(live_video_id):
    if live_video_id is not None:
        video = youtube.videos().list(
            part='snippet,liveStreamingDetails,statistics',
            id=live_video_id
        ).execute()

        if 'liveStreamingDetails' in video['items'][0]:
            activeLiveChatId = video['items'][0]['liveStreamingDetails']['activeLiveChatId']
            # get comment
            return youtube.liveChatMessages().list(
                part='snippet,authorDetails',
                liveChatId=activeLiveChatId,
                maxResults=20
            ).execute()
    return None


def get_comment(live_chat_comment):
    if live_chat_comment is not None:
        comments = []
        if live_chat_comment is not None:
            for comment in live_chat_comment['items']:
                comment_data = {
                    'name': comment['authorDetails']['displayName'],
                    'comment': comment['snippet']['displayMessage']
                    }
                comments.append(comment_data)
        return comments
    return None

list_live_video = get_list_live_video()
live_video_id = get_live_video_id(list_live_video)
live_chat_comment = get_live_chat_comment(live_video_id)
comments = get_comment(live_chat_comment)

