"""
Static content loader for improved performance
"""
import json
import os
from datetime import datetime

class StaticContentManager:
    """Manages static content to reduce API calls"""
    
    def __init__(self):
        self.static_data_file = 'static_data.json'
        self.load_static_data()
    
    def load_static_data(self):
        """Load static data from file"""
        try:
            if os.path.exists(self.static_data_file):
                with open(self.static_data_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            else:
                self.data = self.get_default_data()
                self.save_static_data()
        except Exception as e:
            print(f"Error loading static data: {e}")
            self.data = self.get_default_data()
    
    def save_static_data(self):
        """Save static data to file"""
        try:
            with open(self.static_data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving static data: {e}")
    
    def get_default_data(self):
        """Get default static data"""
        return {
            "featured_videos": [
                {
                    'id': 'eSApphrRKWg',
                    'title': 'Journal LCA TV - Édition du Soir',
                    'description': 'Retrouvez l\'actualité nationale et internationale.',
                    'thumbnail': 'https://i.ytimg.com/vi/eSApphrRKWg/hqdefault.jpg',
                    'published_at': '2024-12-15T19:00:00Z',
                    'category': 'actualites',
                    'channel_title': 'LCA TV'
                },
                {
                    'id': 'xJatmbxIaIM',
                    'title': 'Franc-Parler - Débat Économique',
                    'description': 'Débat sur les enjeux économiques du Burkina Faso.',
                    'thumbnail': 'https://i.ytimg.com/vi/xJatmbxIaIM/hqdefault.jpg',
                    'published_at': '2024-12-14T20:30:00Z',
                    'category': 'debats',
                    'channel_title': 'LCA TV'
                },
                {
                    'id': '8aIAKRe4Spo',
                    'title': 'Festival des Masques - Culture',
                    'description': 'Découvrez la richesse culturelle du Burkina Faso.',
                    'thumbnail': 'https://i.ytimg.com/vi/8aIAKRe4Spo/hqdefault.jpg',
                    'published_at': '2024-12-13T18:00:00Z',
                    'category': 'culture',
                    'channel_title': 'LCA TV'
                }
            ],
            "about_content": {
                "title": "À propos de LCA TV",
                "description": "LCA TV est votre chaîne de télévision burkinabè de référence.",
                "mission": "Informer, éduquer et divertir le public burkinabè.",
                "vision": "Être la première chaîne de télévision du Burkina Faso."
            },
            "contact_info": {
                "address": "Ouagadougou, Burkina Faso",
                "phone": "+226 XX XX XX XX",
                "email": "contact@lcatv.bf",
                "social_media": {
                    "facebook": "https://facebook.com/lcatv",
                    "twitter": "https://twitter.com/lcatv",
                    "youtube": "https://youtube.com/@lcatv"
                }
            },
            "last_updated": datetime.now().isoformat()
        }
    
    def get_featured_videos(self):
        """Get featured videos for homepage"""
        return self.data.get('featured_videos', [])
    
    def get_about_content(self):
        """Get about page content"""
        return self.data.get('about_content', {})
    
    def get_contact_info(self):
        """Get contact information"""
        return self.data.get('contact_info', {})
    
    def update_featured_videos(self, videos):
        """Update featured videos"""
        self.data['featured_videos'] = videos[:6]  # Keep only 6 featured videos
        self.data['last_updated'] = datetime.now().isoformat()
        self.save_static_data()

# Global instance
static_content = StaticContentManager()