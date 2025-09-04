#!/usr/bin/env python3
"""
Get the correct LCA TV channel ID from the video IDs
"""

import requests

YOUTUBE_API_KEY = 'AIzaSyC-9RCCz6mRrNWbUBhmrp37l3uXN09vXo0'

def get_channel_from_video(video_id):
    """Get channel ID from a video ID"""
    url = f"https://www.googleapis.com/youtube/v3/videos"
    params = {
        'part': 'snippet',
        'id': video_id,
        'key': YOUTUBE_API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'items' in data and data['items']:
            video = data['items'][0]
            channel_id = video['snippet']['channelId']
            channel_title = video['snippet']['channelTitle']
            return channel_id, channel_title
    except Exception as e:
        print(f"Error: {e}")
    
    return None, None

def get_channel_videos(channel_id):
    """Get recent videos from the channel"""
    print(f"Getting videos from channel: {channel_id}")
    
    # Get uploads playlist
    url = f"https://www.googleapis.com/youtube/v3/channels"
    params = {
        'part': 'contentDetails',
        'id': channel_id,
        'key': YOUTUBE_API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        if 'items' in data and data['items']:
            uploads_playlist_id = data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            
            # Get videos from uploads playlist
            playlist_url = f"https://www.googleapis.com/youtube/v3/playlistItems"
            playlist_params = {
                'part': 'snippet',
                'playlistId': uploads_playlist_id,
                'maxResults': 15,
                'key': YOUTUBE_API_KEY
            }
            
            playlist_response = requests.get(playlist_url, params=playlist_params)
            playlist_data = playlist_response.json()
            
            if 'items' in playlist_data:
                return playlist_data['items']
    except Exception as e:
        print(f"Error getting videos: {e}")
    
    return []

# Get channel ID from one of the videos
video_id = 'ixQEmhTbvTI'
channel_id, channel_title = get_channel_from_video(video_id)

if channel_id:
    print(f"✅ Found LCA TV channel:")
    print(f"   Title: {channel_title}")
    print(f"   ID: {channel_id}")
    
    # Get recent videos
    videos = get_channel_videos(channel_id)
    print(f"\n📹 Found {len(videos)} recent videos:")
    
    for i, video in enumerate(videos[:10]):
        title = video['snippet']['title']
        video_id = video['snippet']['resourceId']['videoId']
        published = video['snippet']['publishedAt'][:10]
        
        print(f"  {i+1}. {title}")
        print(f"     ID: {video_id}")
        print(f"     Date: {published}")
        print()
else:
    print("❌ Could not find channel")