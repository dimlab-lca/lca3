import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Image,
  TouchableOpacity,
  Dimensions,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { StatusBar } from 'expo-status-bar';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useRouter } from 'expo-router';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';

const { width: screenWidth } = Dimensions.get('window');

// Theme colors LCA TV
const colors = {
  primary: '#2d5016',
  primaryLight: '#22c55e',
  secondary: '#16a34a',
  blue: '#3b82f6',
  darkGreen: '#22543d',
  lightGreen: '#166534',
  white: '#ffffff',
  gray: '#6b7280',
  lightGray: '#f3f4f6',
  black: '#111827',
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
}

export default function HomeScreen() {
  const [user, setUser] = useState(null);
  const [featuredVideos, setFeaturedVideos] = useState<Video[]>([]);
  const [loading, setLoading] = useState(true);
  const [isLiveStreamActive, setIsLiveStreamActive] = useState(true);
  const router = useRouter();

  useEffect(() => {
    checkUserSession();
    loadFeaturedContent();
  }, []);

  const checkUserSession = async () => {
    try {
      const userData = await AsyncStorage.getItem('user');
      if (userData) {
        setUser(JSON.parse(userData));
      }
    } catch (error) {
      console.error('Error checking user session:', error);
    }
  };

  const loadFeaturedContent = async () => {
    try {
      setLoading(true);
      // Simulated content - in real app, fetch from YouTube API
      const mockVideos: Video[] = [
        {
          id: 'eSApphrRKWg',
          title: 'Journal LCA TV - Édition du Soir',
          description: 'Retrouvez l\'actualité nationale et internationale.',
          thumbnail: 'https://i.ytimg.com/vi/eSApphrRKWg/hqdefault.jpg',
          published_at: '2024-12-15T19:00:00Z',
          category: 'actualites',
          view_count: '15420',
          like_count: '234'
        },
        {
          id: 'xJatmbxIaIM',
          title: 'Franc-Parler - Débat Économie',
          description: 'Débat sur les enjeux économiques du Burkina Faso.',
          thumbnail: 'https://i.ytimg.com/vi/xJatmbxIaIM/hqdefault.jpg',
          published_at: '2024-12-14T20:30:00Z',
          category: 'debats',
          view_count: '8750',
          like_count: '156'
        },
        {
          id: '8aIAKRe4Spo',
          title: 'Festival des Masques - Culture',
          description: 'Découvrez la richesse culturelle du Burkina Faso.',
          thumbnail: 'https://i.ytimg.com/vi/8aIAKRe4Spo/hqdefault.jpg',
          published_at: '2024-12-13T18:00:00Z',
          category: 'culture',
          view_count: '12300',
          like_count: '298'
        }
      ];
      setFeaturedVideos(mockVideos);
    } catch (error) {
      console.error('Error loading content:', error);
      Alert.alert('Erreur', 'Impossible de charger le contenu');
    } finally {
      setLoading(false);
    }
  };

  const navigateToLogin = () => {
    router.push('/login');
  };

  const navigateToLive = () => {
    router.push('/live');
  };

  const navigateToReplay = () => {
    router.push('/replay');
  };

  const navigateToVideo = (videoId: string) => {
    router.push(`/video/${videoId}`);
  };

  const EmissionCard = ({ icon, title, onPress }: { icon: string, title: string, onPress: () => void }) => (
    <TouchableOpacity style={styles.emissionCard} onPress={onPress}>
      <LinearGradient
        colors={[colors.primary, colors.secondary]}
        style={styles.emissionGradient}
      >
        <Ionicons name={icon as any} size={24} color={colors.white} />
        <Text style={styles.emissionText}>{title}</Text>
      </LinearGradient>
    </TouchableOpacity>
  );

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <StatusBar style="light" backgroundColor={colors.primary} />
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color={colors.primaryLight} />
          <Text style={[styles.text, { marginTop: 16 }]}>Chargement...</Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar style="light" backgroundColor={colors.primary} />
      
      {/* Header */}
      <View style={styles.header}>
        <View style={styles.logoContainer}>
          <Text style={styles.logoText}>LCA</Text>
          <View style={styles.logoCircle}>
            <Text style={styles.logoSubText}>TV</Text>
          </View>
        </View>
        <Text style={styles.tagline}>La Chaîne Africaine de télévision</Text>
        {!user && (
          <TouchableOpacity onPress={navigateToLogin} style={styles.loginButton}>
            <Text style={styles.loginButtonText}>Se connecter</Text>
          </TouchableOpacity>
        )}
      </View>

      <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
        {/* Live Section */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Ionicons name="radio" size={24} color={colors.primaryLight} />
            <Text style={styles.sectionTitle}>Direct</Text>
            {isLiveStreamActive && (
              <View style={styles.liveIndicator}>
                <Text style={styles.liveText}>LIVE</Text>
              </View>
            )}
          </View>
          
          <TouchableOpacity onPress={navigateToLive} style={styles.liveContainer}>
            <Image
              source={{ uri: 'https://i.ytimg.com/vi/ixQEmhTbvTI/maxresdefault.jpg' }}
              style={styles.liveImage}
              resizeMode="cover"
            />
            <LinearGradient
              colors={['transparent', 'rgba(0,0,0,0.7)']}
              style={styles.liveOverlay}
            >
              <Ionicons name="play-circle" size={60} color={colors.white} />
              <Text style={styles.liveTitle}>Regarder en direct</Text>
            </LinearGradient>
          </TouchableOpacity>
        </View>

        {/* Featured Programs */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Ionicons name="star" size={24} color={colors.primaryLight} />
            <Text style={styles.sectionTitle}>Programmes populaires</Text>
            <TouchableOpacity onPress={navigateToReplay}>
              <Text style={styles.seeAllText}>Voir tout</Text>
            </TouchableOpacity>
          </View>
          
          <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.horizontalScroll}>
            {featuredVideos.map((video) => (
              <TouchableOpacity
                key={video.id}
                style={styles.videoCard}
                onPress={() => navigateToVideo(video.id)}
              >
                <Image source={{ uri: video.thumbnail }} style={styles.videoThumbnail} />
                <View style={styles.videoInfo}>
                  <Text style={styles.videoTitle} numberOfLines={2}>{video.title}</Text>
                  <Text style={styles.videoStats}>{video.view_count} vues • {video.like_count} likes</Text>
                </View>
              </TouchableOpacity>
            ))}
          </ScrollView>
        </View>

        {/* Our Programs Grid */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Ionicons name="grid" size={24} color={colors.primaryLight} />
            <Text style={styles.sectionTitle}>Nos émissions</Text>
          </View>
          
          <View style={styles.emissionsGrid}>
            <EmissionCard 
              icon="newspaper" 
              title="Journal LCA TV" 
              onPress={() => router.push('/category/actualites')} 
            />
            <EmissionCard 
              icon="chatbubbles" 
              title="Franc-Parler" 
              onPress={() => router.push('/category/debats')} 
            />
            <EmissionCard 
              icon="woman" 
              title="Questions de Femmes" 
              onPress={() => router.push('/category/femmes')} 
            />
            <EmissionCard 
              icon="sunny" 
              title="Soleil d'Afrique" 
              onPress={() => router.push('/category/culture')} 
            />
            <EmissionCard 
              icon="football" 
              title="Sports & Étalons" 
              onPress={() => router.push('/category/sport')} 
            />
            <EmissionCard 
              icon="people" 
              title="Jeunesse Avenir" 
              onPress={() => router.push('/category/jeunesse')} 
            />
            <EmissionCard 
              icon="flag" 
              title="Burkina Faso" 
              onPress={() => router.push('/category/national')} 
            />
            <EmissionCard 
              icon="musical-notes" 
              title="Danse des Masques" 
              onPress={() => router.push('/category/musique')} 
            />
          </View>
        </View>

        {/* News Section */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Ionicons name="newspaper-outline" size={24} color={colors.primaryLight} />
            <Text style={styles.sectionTitle}>Actualités</Text>
            <TouchableOpacity onPress={() => router.push('/news')}>
              <Text style={styles.seeAllText}>Voir tout</Text>
            </TouchableOpacity>
          </View>
          
          <View style={styles.newsContainer}>
            <TouchableOpacity style={styles.newsCard}>
              <Image 
                source={{ uri: 'https://via.placeholder.com/300x200?text=Breaking+News' }}
                style={styles.newsImage}
              />
              <View style={styles.newsContent}>
                <Text style={styles.newsTitle}>Actualités nationales - Flash info</Text>
                <Text style={styles.newsExcerpt}>Les dernières nouvelles du Burkina Faso...</Text>
                <Text style={styles.newsDate}>Il y a 2 heures</Text>
              </View>
            </TouchableOpacity>
          </View>
        </View>

        {/* Publicity Section */}
        <View style={styles.section}>
          <TouchableOpacity 
            style={styles.publicityBanner}
            onPress={() => router.push('/publicity')}
          >
            <LinearGradient
              colors={[colors.blue, colors.primaryLight]}
              style={styles.publicityGradient}
            >
              <Ionicons name="megaphone" size={32} color={colors.white} />
              <View style={styles.publicityContent}>
                <Text style={styles.publicityTitle}>Programme Publicitaire</Text>
                <Text style={styles.publicitySubtitle}>Boostez votre visibilité avec LCA TV</Text>
              </View>
              <Ionicons name="arrow-forward" size={24} color={colors.white} />
            </LinearGradient>
          </TouchableOpacity>
        </View>
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
    backgroundColor: colors.white,
  },
  header: {
    backgroundColor: colors.primary,
    paddingHorizontal: 20,
    paddingVertical: 15,
    borderBottomLeftRadius: 20,
    borderBottomRightRadius: 20,
  },
  logoContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 5,
  },
  logoText: {
    fontSize: 32,
    fontWeight: 'bold',
    color: colors.white,
    marginRight: 10,
  },
  logoCircle: {
    width: 30,
    height: 30,
    borderRadius: 15,
    backgroundColor: colors.blue,
    justifyContent: 'center',
    alignItems: 'center',
  },
  logoSubText: {
    fontSize: 12,
    fontWeight: 'bold',
    color: colors.white,
  },
  tagline: {
    fontSize: 14,
    color: colors.white,
    opacity: 0.9,
    marginBottom: 10,
  },
  loginButton: {
    alignSelf: 'flex-end',
    backgroundColor: colors.primaryLight,
    paddingHorizontal: 15,
    paddingVertical: 8,
    borderRadius: 15,
  },
  loginButtonText: {
    color: colors.white,
    fontWeight: 'bold',
    fontSize: 14,
  },
  content: {
    flex: 1,
  },
  section: {
    marginVertical: 15,
    paddingHorizontal: 20,
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 15,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: colors.black,
    marginLeft: 10,
    flex: 1,
  },
  seeAllText: {
    color: colors.primaryLight,
    fontWeight: 'bold',
    fontSize: 14,
  },
  liveContainer: {
    height: 200,
    borderRadius: 15,
    overflow: 'hidden',
    position: 'relative',
  },
  liveImage: {
    width: '100%',
    height: '100%',
  },
  liveOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    justifyContent: 'center',
    alignItems: 'center',
  },
  liveTitle: {
    color: colors.white,
    fontSize: 18,
    fontWeight: 'bold',
    marginTop: 10,
  },
  liveIndicator: {
    backgroundColor: '#ff4444',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 10,
    marginLeft: 10,
  },
  liveText: {
    color: colors.white,
    fontSize: 12,
    fontWeight: 'bold',
  },
  horizontalScroll: {
    marginHorizontal: -20,
    paddingHorizontal: 20,
  },
  videoCard: {
    width: 200,
    marginRight: 15,
    backgroundColor: colors.white,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  videoThumbnail: {
    width: '100%',
    height: 120,
    borderTopLeftRadius: 12,
    borderTopRightRadius: 12,
  },
  videoInfo: {
    padding: 10,
  },
  videoTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    color: colors.black,
    marginBottom: 5,
  },
  videoStats: {
    fontSize: 12,
    color: colors.gray,
  },
  emissionsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  emissionCard: {
    width: (screenWidth - 60) / 2,
    marginBottom: 15,
    borderRadius: 12,
    overflow: 'hidden',
  },
  emissionGradient: {
    padding: 20,
    alignItems: 'center',
    minHeight: 100,
    justifyContent: 'center',
  },
  emissionText: {
    color: colors.white,
    fontWeight: 'bold',
    fontSize: 14,
    textAlign: 'center',
    marginTop: 8,
  },
  newsContainer: {
    marginTop: 10,
  },
  newsCard: {
    backgroundColor: colors.white,
    borderRadius: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
    overflow: 'hidden',
  },
  newsImage: {
    width: '100%',
    height: 150,
  },
  newsContent: {
    padding: 15,
  },
  newsTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: colors.black,
    marginBottom: 5,
  },
  newsExcerpt: {
    fontSize: 14,
    color: colors.gray,
    marginBottom: 10,
  },
  newsDate: {
    fontSize: 12,
    color: colors.primaryLight,
    fontWeight: 'bold',
  },
  publicityBanner: {
    borderRadius: 15,
    overflow: 'hidden',
    marginTop: 10,
  },
  publicityGradient: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 20,
  },
  publicityContent: {
    flex: 1,
    marginLeft: 15,
  },
  publicityTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: colors.white,
    marginBottom: 5,
  },
  publicitySubtitle: {
    fontSize: 14,
    color: colors.white,
    opacity: 0.9,
  },
  text: {
    color: colors.black,
  },
});