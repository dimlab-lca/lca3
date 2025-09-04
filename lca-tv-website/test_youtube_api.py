#!/usr/bin/env python3
"""
Test script to verify YouTube API functionality for LCA TV channel
"""

import requests
import json

# YouTube API configuration
YOUTUBE_API_KEY = 'AIzaSyC-9RCCz6mRrNWbUBhmrp37l3uXN09vXo0'

def search_channel():
    """Search for LCA TV channel"""
    print("🔍 Searching for LCA TV channel...")
    
    search_terms = ['LCATV', 'LCA TV', 'LCA Television Burkina']
    
    for term in search_terms:
        print(f"\n📺 Searching for: {term}")
        
        url = f"https://www.googleapis.com/youtube/v3/search"
        params = {
            'part': 'snippet',
            'q': term,
            'type': 'channel',
            'key': YOUTUBE_API_KEY,
            'maxResults': 5
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if 'items' in data and data['items']:
                for item in data['items']:
                    channel_title = item['snippet']['title']
                    channel_id = item['snippet']['channelId']
                    description = item['snippet'].get('description', '')[:100]
                    
                    print(f"  ✅ Found: {channel_title}")
                    print(f"     ID: {channel_id}")
                    print(f"     Description: {description}...")
                    
                    # Check if this looks like LCA TV
                    if 'lca' in channel_title.lower() or 'burkina' in description.lower():
                        print(f"  🎯 This looks like LCA TV!")
                        return channel_id
            else:
                print(f"  ❌ No channels found for '{term}'")
                if 'error' in data:
                    print(f"     Error: {data['error']}")
                    
        except Exception as e:
            print(f"  ❌ Error searching for '{term}': {e}")
    
    return None

def get_channel_videos(channel_id):
    """Get videos from channel"""
    print(f"\n📹 Getting videos from channel: {channel_id}")
    
    # First get the uploads playlist ID
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
            print(f"  📋 Uploads playlist ID: {uploads_playlist_id}")
            
            # Get videos from uploads playlist
            playlist_url = f"https://www.googleapis.com/youtube/v3/playlistItems"
            playlist_params = {
                'part': 'snippet',
                'playlistId': uploads_playlist_id,
                'maxResults': 10,
                'key': YOUTUBE_API_KEY
            }
            
            playlist_response = requests.get(playlist_url, params=playlist_params)
            playlist_data = playlist_response.json()
            
            if 'items' in playlist_data:
                videos = playlist_data['items']
                print(f"  ✅ Found {len(videos)} videos")
                
                for i, video in enumerate(videos[:5]):  # Show first 5
                    title = video['snippet']['title']
                    video_id = video['snippet']['resourceId']['videoId']
                    published = video['snippet']['publishedAt'][:10]
                    
                    print(f"    {i+1}. {title}")
                    print(f"       ID: {video_id}")
                    print(f"       Published: {published}")
                
                return videos
            else:
                print(f"  ❌ No videos found in playlist")
                if 'error' in playlist_data:
                    print(f"     Error: {playlist_data['error']}")
        else:
            print(f"  ❌ Channel not found")
            if 'error' in data:
                print(f"     Error: {data['error']}")
                
    except Exception as e:
        print(f"  ❌ Error getting videos: {e}")
    
    return []

def test_specific_videos():
    """Test the specific video IDs mentioned"""
    print("\n🎬 Testing specific video IDs...")
    
    video_ids = ['ixQEmhTbvTI', 'zjWu0nZyBCY']
    
    for video_id in video_ids:
        url = f"https://www.googleapis.com/youtube/v3/videos"
        params = {
            'part': 'snippet,statistics',
            'id': video_id,
            'key': YOUTUBE_API_KEY
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if 'items' in data and data['items']:
                video = data['items'][0]
                title = video['snippet']['title']
                channel_title = video['snippet']['channelTitle']
                published = video['snippet']['publishedAt'][:10]
                view_count = video['statistics'].get('viewCount', 'N/A')
                
                print(f"  ✅ {video_id}: {title}")
                print(f"     Channel: {channel_title}")
                print(f"     Published: {published}")
                print(f"     Views: {view_count}")
            else:
                print(f"  ❌ Video {video_id} not found")
                
        except Exception as e:
            print(f"  ❌ Error testing video {video_id}: {e}")

def main():
    print("🚀 Testing YouTube API for LCA TV")
    print("=" * 50)
    
    # Test API key
    print(f"🔑 API Key: {YOUTUBE_API_KEY[:20]}...")
    
    # Search for channel
    channel_id = search_channel()
    
    if channel_id:
        # Get videos from channel
        videos = get_channel_videos(channel_id)
        
        if videos:
            print(f"\n✅ Successfully found LCA TV channel and videos!")
            print(f"   Channel ID: {channel_id}")
            print(f"   Videos found: {len(videos)}")
        else:
            print(f"\n⚠️  Found channel but no videos")
    else:
        print(f"\n❌ Could not find LCA TV channel")
    
    # Test specific videos
    test_specific_videos()
    
    print("\n" + "=" * 50)
    print("🏁 Test completed!")

if __name__ == "__main__":
    main()