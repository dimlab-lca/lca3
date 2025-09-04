import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
  ActivityIndicator,
  Dimensions,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { StatusBar } from 'expo-status-bar';
import { Ionicons } from '@expo/vector-icons';
import { useRouter, useLocalSearchParams } from 'expo-router';
// import YoutubePlayer from 'react-native-youtube-iframe';
import AsyncStorage from '@react-native-async-storage/async-storage';

const { width: screenWidth, height: screenHeight } = Dimensions.get('window');

// LCA TV Theme colors
const colors = {
  primary: '#2d5016',
  primaryLight: '#22c55e',
  secondary: '#16a34a',
  blue: '#3b82f6',
  white: '#ffffff',
  gray: '#6b7280',
  lightGray: '#f3f4f6',
  black: '#111827',
  error: '#ef4444',
};

interface Video {
  id: string;
  title: string;
  description: string;
  thumbnail: string;
  published_at: string;
  category: string;
  view_count: string;
  like_count: string;
  duration: string;
  channel_title: string;
}

export default function VideoScreen() {
  const { id } = useLocalSearchParams();
  const [video, setVideo] = useState<Video | null>(null);
  const [playing, setPlaying] = useState(false);
  const [fullscreen, setFullscreen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [isFavorite, setIsFavorite] = useState(false);
  const [user, setUser] = useState(null);
  const [relatedVideos, setRelatedVideos] = useState<Video[]>([]);
  const router = useRouter();

  useEffect(() => {
    loadVideoDetails();
    loadUserData();
  }, [id]);

  const loadUserData = async () => {
    try {
      const userData = await AsyncStorage.getItem('user');
      if (userData) {
        const parsedUser = JSON.parse(userData);
        setUser(parsedUser);
        checkIfFavorite(parsedUser.favorites || []);
      }
    } catch (error) {
      console.error('Error loading user data:', error);
    }
  };

  const checkIfFavorite = (favorites: string[]) => {
    setIsFavorite(favorites.includes(id as string));
  };

  const loadVideoDetails = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${process.env.EXPO_PUBLIC_BACKEND_URL}/api/videos/${id}`);
      const data = await response.json();
      
      if (response.ok) {
        setVideo(data.video);
        await trackVideoWatch();
        loadRelatedVideos(data.video.category);
      } else {
        Alert.alert('Erreur', 'Vidéo non trouvée');
        router.back();
      }
    } catch (error) {
      console.error('Error loading video:', error);
      Alert.alert('Erreur', 'Impossible de charger la vidéo');
      router.back();
    } finally {
      setLoading(false);
    }
  };

  const loadRelatedVideos = async (category: string) => {
    try {
      const response = await fetch(`${process.env.EXPO_PUBLIC_BACKEND_URL}/api/videos?category=${category}`);
      const data = await response.json();
      
      if (response.ok) {
        // Filter out current video and limit to 3 related videos
        const filtered = data.videos.filter((v: Video) => v.id !== id).slice(0, 3);
        setRelatedVideos(filtered);
      }
    } catch (error) {
      console.error('Error loading related videos:', error);
    }
  };

  const trackVideoWatch = async () => {
    if (!user) return;
    
    try {
      const token = await AsyncStorage.getItem('access_token');
      const response = await fetch(`${process.env.EXPO_PUBLIC_BACKEND_URL}/api/user/watch-video/${id}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        console.log(`Points earned: ${data.points_earned}`);
      }
    } catch (error) {
      console.error('Error tracking video watch:', error);
    }
  };

  const toggleFavorite = async () => {
    if (!user) {
      Alert.alert('Connexion requise', 'Connectez-vous pour ajouter des favoris', [
        { text: 'Se connecter', onPress: () => router.push('/login') },
        { text: 'Annuler', style: 'cancel' }
      ]);
      return;
    }

    try {
      const token = await AsyncStorage.getItem('access_token');
      const method = isFavorite ? 'DELETE' : 'POST';
      
      const response = await fetch(`${process.env.EXPO_PUBLIC_BACKEND_URL}/api/user/favorites/${id}`, {
        method,
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        setIsFavorite(!isFavorite);
        
        if (!isFavorite) {
          Alert.alert('Favori ajouté', `${data.points_earned || 0} points gagnés !`);
        }
      }
    } catch (error) {
      console.error('Error toggling favorite:', error);
      Alert.alert('Erreur', 'Impossible de modifier les favoris');
    }
  };

  const shareVideo = () => {
    Alert.alert(
      'Partager la vidéo',
      `Partager "${video?.title}"`,
      [
        { text: 'WhatsApp', onPress: () => console.log('Share WhatsApp') },
        { text: 'Facebook', onPress: () => console.log('Share Facebook') },
        { text: 'Twitter', onPress: () => console.log('Share Twitter') },
        { text: 'Annuler', style: 'cancel' }
      ]
    );
  };

  const onStateChange = (state: string) => {
    if (state === 'ended') {
      setPlaying(false);
    }
  };

  const onReady = () => {
    console.log('Video player ready');
  };

  const onError = (error: string) => {
    console.error('YouTube Player Error:', error);
    Alert.alert('Erreur de lecture', 'Impossible de lire cette vidéo');
  };

  const toggleFullscreen = () => {
    setFullscreen(!fullscreen);
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR', {
      day: 'numeric',
      month: 'long',
      year: 'numeric'
    });
  };

  const formatViewCount = (count: string) => {
    const num = parseInt(count);
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}k`;
    return count;
  };

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <StatusBar style="light" backgroundColor={colors.primary} />
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color={colors.primaryLight} />
          <Text style={styles.loadingText}>Chargement de la vidéo...</Text>
        </View>
      </SafeAreaView>
    );
  }

  if (!video) {
    return (
      <SafeAreaView style={styles.container}>
        <StatusBar style="light" backgroundColor={colors.primary} />
        <View style={styles.errorContainer}>
          <Ionicons name="videocam-off" size={64} color={colors.gray} />
          <Text style={styles.errorText}>Vidéo non trouvée</Text>
          <TouchableOpacity onPress={() => router.back()} style={styles.backToListButton}>
            <Text style={styles.backToListText}>Retour aux vidéos</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  if (fullscreen) {
    return (
      <View style={styles.fullscreenContainer}>
        <StatusBar style="light" hidden />
        <YoutubePlayer
          height={screenHeight}
          width={screenWidth}
          play={playing}
          videoId={video.id}
          onChangeState={onStateChange}
          onReady={onReady}
          onError={onError}
          initialPlayerParams={{
            loop: false,
            controls: true,
            modestbranding: true,
            rel: false,
            showinfo: false,
          }}
        />
        <TouchableOpacity 
          style={styles.exitFullscreenButton}
          onPress={toggleFullscreen}
        >
          <Ionicons name="contract" size={24} color={colors.white} />
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar style="light" backgroundColor={colors.primary} />
      
      <ScrollView style={styles.scrollView} showsVerticalScrollIndicator={false}>
        {/* Video Player Placeholder */}
        <View style={styles.playerContainer}>
          <View style={styles.videoPlaceholder}>
            <Image source={{ uri: video.thumbnail }} style={styles.placeholderImage} />
            <View style={styles.videoOverlay}>
              <TouchableOpacity onPress={() => setPlaying(!playing)} style={styles.playButton}>
                <Ionicons 
                  name={playing ? "pause" : "play"} 
                  size={48} 
                  color={colors.white} 
                />
              </TouchableOpacity>
            </View>
          </View>
          
          <View style={styles.playerControls}>
            <TouchableOpacity onPress={toggleFullscreen} style={styles.fullscreenBtn}>
              <Ionicons name="expand" size={24} color={colors.white} />
            </TouchableOpacity>
          </View>
        </View>

        {/* Video Info */}
        <View style={styles.videoInfo}>
          <View style={styles.videoHeader}>
            <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
              <Ionicons name="arrow-back" size={24} color={colors.primary} />
            </TouchableOpacity>
            
            <View style={styles.videoActions}>
              <TouchableOpacity onPress={toggleFavorite} style={styles.actionButton}>
                <Ionicons 
                  name={isFavorite ? "heart" : "heart-outline"} 
                  size={24} 
                  color={isFavorite ? colors.error : colors.gray} 
                />
              </TouchableOpacity>
              
              <TouchableOpacity onPress={shareVideo} style={styles.actionButton}>
                <Ionicons name="share-social" size={24} color={colors.gray} />
              </TouchableOpacity>
            </View>
          </View>
          
          <Text style={styles.videoTitle}>{video.title}</Text>
          
          <View style={styles.videoMeta}>
            <View style={styles.videoStats}>
              <Ionicons name="eye" size={16} color={colors.gray} />
              <Text style={styles.statsText}>{formatViewCount(video.view_count)} vues</Text>
              <Ionicons name="heart" size={16} color={colors.gray} style={{ marginLeft: 15 }} />
              <Text style={styles.statsText}>{formatViewCount(video.like_count)} likes</Text>
            </View>
            <Text style={styles.publishedDate}>{formatDate(video.published_at)}</Text>
          </View>
          
          <View style={styles.categoryContainer}>
            <View style={styles.categoryBadge}>
              <Text style={styles.categoryText}>{video.category.toUpperCase()}</Text>
            </View>
          </View>
        </View>

        {/* Channel Info */}
        <View style={styles.channelInfo}>
          <View style={styles.channelHeader}>
            <View style={styles.channelLogo}>
              <Text style={styles.channelLogoText}>LCA</Text>
            </View>
            <View style={styles.channelDetails}>
              <Text style={styles.channelName}>{video.channel_title}</Text>
              <Text style={styles.channelDescription}>La Chaîne Africaine de télévision</Text>
            </View>
          </View>
        </View>

        {/* Description */}
        <View style={styles.descriptionContainer}>
          <Text style={styles.descriptionTitle}>Description</Text>
          <Text style={styles.descriptionText}>{video.description}</Text>
        </View>

        {/* Related Videos */}
        {relatedVideos.length > 0 && (
          <View style={styles.relatedContainer}>
            <Text style={styles.relatedTitle}>Vidéos similaires</Text>
            {relatedVideos.map((relatedVideo) => (
              <TouchableOpacity 
                key={relatedVideo.id}
                style={styles.relatedVideoCard}
                onPress={() => router.push(`/video/${relatedVideo.id}`)}
              >
                <View style={styles.relatedVideoInfo}>
                  <Text style={styles.relatedVideoTitle} numberOfLines={2}>
                    {relatedVideo.title}
                  </Text>
                  <View style={styles.relatedVideoMeta}>
                    <Text style={styles.relatedVideoStats}>
                      {formatViewCount(relatedVideo.view_count)} vues
                    </Text>
                    <Text style={styles.relatedVideoDate}>
                      {formatDate(relatedVideo.published_at)}
                    </Text>
                  </View>
                </View>
                <Ionicons name="play-circle" size={24} color={colors.primaryLight} />
              </TouchableOpacity>
            ))}
          </View>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.white,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    fontSize: 16,
    color: colors.gray,
    marginTop: 10,
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 40,
  },
  errorText: {
    fontSize: 18,
    color: colors.gray,
    textAlign: 'center',
    marginTop: 15,
    marginBottom: 20,
  },
  backToListButton: {
    backgroundColor: colors.primaryLight,
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 20,
  },
  backToListText: {
    color: colors.white,
    fontWeight: 'bold',
  },
  fullscreenContainer: {
    flex: 1,
    backgroundColor: colors.black,
    justifyContent: 'center',
    alignItems: 'center',
  },
  exitFullscreenButton: {
    position: 'absolute',
    top: 50,
    right: 20,
    backgroundColor: 'rgba(0,0,0,0.7)',
    borderRadius: 20,
    padding: 10,
  },
  scrollView: {
    flex: 1,
  },
  playerContainer: {
    position: 'relative',
    backgroundColor: colors.black,
  },
  videoPlaceholder: {
    height: 220,
    width: '100%',
    position: 'relative',
    backgroundColor: colors.black,
  },
  placeholderImage: {
    width: '100%',
    height: '100%',
  },
  videoOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0,0,0,0.3)',
  },
  playerControls: {
    position: 'absolute',
    bottom: 20,
    left: 20,
    right: 20,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  playButton: {
    backgroundColor: 'rgba(0,0,0,0.7)',
    borderRadius: 25,
    padding: 10,
  },
  fullscreenBtn: {
    backgroundColor: 'rgba(0,0,0,0.7)',
    borderRadius: 20,
    padding: 8,
  },
  videoInfo: {
    backgroundColor: colors.white,
    padding: 20,
  },
  videoHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
  },
  backButton: {
    padding: 5,
  },
  videoActions: {
    flexDirection: 'row',
  },
  actionButton: {
    padding: 8,
    marginLeft: 10,
  },
  videoTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: colors.black,
    lineHeight: 25,
    marginBottom: 10,
  },
  videoMeta: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
  },
  videoStats: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  statsText: {
    fontSize: 14,
    color: colors.gray,
    marginLeft: 5,
  },
  publishedDate: {
    fontSize: 14,
    color: colors.gray,
  },
  categoryContainer: {
    flexDirection: 'row',
  },
  categoryBadge: {
    backgroundColor: colors.primaryLight,
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 15,
  },
  categoryText: {
    color: colors.white,
    fontSize: 12,
    fontWeight: 'bold',
  },
  channelInfo: {
    backgroundColor: colors.lightGray,
    padding: 20,
    marginHorizontal: 20,
    borderRadius: 12,
    marginBottom: 20,
  },
  channelHeader: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  channelLogo: {
    width: 50,
    height: 50,
    borderRadius: 25,
    backgroundColor: colors.primary,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 15,
  },
  channelLogoText: {
    color: colors.white,
    fontSize: 18,
    fontWeight: 'bold',
  },
  channelDetails: {
    flex: 1,
  },
  channelName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: colors.black,
    marginBottom: 2,
  },
  channelDescription: {
    fontSize: 14,
    color: colors.gray,
  },
  descriptionContainer: {
    paddingHorizontal: 20,
    marginBottom: 20,
  },
  descriptionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: colors.black,
    marginBottom: 10,
  },
  descriptionText: {
    fontSize: 14,
    color: colors.gray,
    lineHeight: 20,
  },
  relatedContainer: {
    paddingHorizontal: 20,
    paddingBottom: 20,
  },
  relatedTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: colors.black,
    marginBottom: 15,
  },
  relatedVideoCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.lightGray,
    padding: 15,
    borderRadius: 12,
    marginBottom: 10,
  },
  relatedVideoInfo: {
    flex: 1,
    marginRight: 15,
  },
  relatedVideoTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: colors.black,
    marginBottom: 5,
  },
  relatedVideoMeta: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  relatedVideoStats: {
    fontSize: 12,
    color: colors.gray,
  },
  relatedVideoDate: {
    fontSize: 12,
    color: colors.gray,
  },
});