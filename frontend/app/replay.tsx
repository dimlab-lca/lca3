import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  Image,
  TouchableOpacity,
  TextInput,
  ActivityIndicator,
  Alert,
  Dimensions,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { StatusBar } from 'expo-status-bar';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';

const { width: screenWidth } = Dimensions.get('window');

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

interface Category {
  id: string;
  name: string;
  icon: string;
}

const categories: Category[] = [
  { id: 'all', name: 'Tout', icon: 'grid' },
  { id: 'actualites', name: 'Actualités', icon: 'newspaper' },
  { id: 'debats', name: 'Franc-Parler', icon: 'chatbubbles' },
  { id: 'femmes', name: 'Questions de Femmes', icon: 'woman' },
  { id: 'culture', name: 'Culture', icon: 'sunny' },
  { id: 'sport', name: 'Sports', icon: 'football' },
  { id: 'jeunesse', name: 'Jeunesse', icon: 'people' },
];

export default function ReplayScreen() {
  const [videos, setVideos] = useState<Video[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [favorites, setFavorites] = useState<string[]>([]);
  const [user, setUser] = useState(null);
  const router = useRouter();

  useEffect(() => {
    loadVideos();
    loadUserData();
  }, [selectedCategory]);

  const loadUserData = async () => {
    try {
      const userData = await AsyncStorage.getItem('user');
      if (userData) {
        const parsedUser = JSON.parse(userData);
        setUser(parsedUser);
        setFavorites(parsedUser.favorites || []);
      }
    } catch (error) {
      console.error('Error loading user data:', error);
    }
  };

  const loadVideos = async () => {
    try {
      setLoading(true);
      const categoryParam = selectedCategory === 'all' ? '' : `?category=${selectedCategory}`;
      const response = await fetch(`${process.env.EXPO_PUBLIC_BACKEND_URL}/api/videos${categoryParam}`);
      const data = await response.json();
      
      if (response.ok) {
        setVideos(data.videos || []);
      } else {
        console.error('Error loading videos:', data);
      }
    } catch (error) {
      console.error('Error fetching videos:', error);
      Alert.alert('Erreur', 'Impossible de charger les vidéos');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    loadVideos();
  };

  const toggleFavorite = async (videoId: string) => {
    if (!user) {
      Alert.alert('Connexion requise', 'Connectez-vous pour ajouter des favoris', [
        { text: 'Se connecter', onPress: () => router.push('/login') },
        { text: 'Annuler', style: 'cancel' }
      ]);
      return;
    }

    try {
      const token = await AsyncStorage.getItem('access_token');
      const isFavorite = favorites.includes(videoId);
      const method = isFavorite ? 'DELETE' : 'POST';
      
      const response = await fetch(`${process.env.EXPO_PUBLIC_BACKEND_URL}/api/user/favorites/${videoId}`, {
        method,
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        if (isFavorite) {
          setFavorites(prev => prev.filter(id => id !== videoId));
        } else {
          setFavorites(prev => [...prev, videoId]);
          Alert.alert('Favori ajouté', `${data.points_earned || 0} points gagnés !`);
        }
      }
    } catch (error) {
      console.error('Error toggling favorite:', error);
      Alert.alert('Erreur', 'Impossible de modifier les favoris');
    }
  };

  const navigateToVideo = (video: Video) => {
    router.push(`/video/${video.id}`);
  };

  const formatDuration = (duration: string) => {
    // Convert ISO 8601 duration to readable format
    if (!duration) return '';
    return duration; // Simplified for now
  };

  const formatViewCount = (count: string) => {
    const num = parseInt(count);
    if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`;
    if (num >= 1000) return `${(num / 1000).toFixed(1)}k`;
    return count;
  };

  const formatPublishedDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 1) return 'Il y a 1 jour';
    if (diffDays < 7) return `Il y a ${diffDays} jours`;
    if (diffDays < 30) return `Il y a ${Math.ceil(diffDays / 7)} semaines`;
    return `Il y a ${Math.ceil(diffDays / 30)} mois`;
  };

  const filteredVideos = videos.filter(video => 
    video.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    video.description.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const renderCategoryFilter = () => (
    <FlatList
      horizontal
      showsHorizontalScrollIndicator={false}
      data={categories}
      keyExtractor={(item) => item.id}
      contentContainerStyle={styles.categoriesContainer}
      renderItem={({ item }) => (
        <TouchableOpacity
          style={[
            styles.categoryButton,
            selectedCategory === item.id && styles.categoryButtonActive
          ]}
          onPress={() => setSelectedCategory(item.id)}
        >
          <Ionicons 
            name={item.icon as any} 
            size={18} 
            color={selectedCategory === item.id ? colors.white : colors.primary} 
          />
          <Text style={[
            styles.categoryButtonText,
            selectedCategory === item.id && styles.categoryButtonTextActive
          ]}>
            {item.name}
          </Text>
        </TouchableOpacity>
      )}
    />
  );

  const renderVideoItem = ({ item }: { item: Video }) => (
    <TouchableOpacity 
      style={styles.videoCard}
      onPress={() => navigateToVideo(item)}
    >
      <View style={styles.thumbnailContainer}>
        <Image source={{ uri: item.thumbnail }} style={styles.thumbnail} />
        <View style={styles.durationBadge}>
          <Text style={styles.durationText}>{formatDuration(item.duration)}</Text>
        </View>
        <TouchableOpacity 
          style={styles.favoriteButton}
          onPress={() => toggleFavorite(item.id)}
        >
          <Ionicons 
            name={favorites.includes(item.id) ? "heart" : "heart-outline"} 
            size={20} 
            color={favorites.includes(item.id) ? colors.error : colors.white} 
          />
        </TouchableOpacity>
      </View>
      
      <View style={styles.videoInfo}>
        <Text style={styles.videoTitle} numberOfLines={2}>{item.title}</Text>
        <Text style={styles.videoDescription} numberOfLines={2}>{item.description}</Text>
        
        <View style={styles.videoMeta}>
          <View style={styles.videoStats}>
            <Ionicons name="eye" size={14} color={colors.gray} />
            <Text style={styles.videoStatsText}>{formatViewCount(item.view_count)}</Text>
            <Ionicons name="heart" size={14} color={colors.gray} style={{ marginLeft: 10 }} />
            <Text style={styles.videoStatsText}>{formatViewCount(item.like_count)}</Text>
          </View>
          <Text style={styles.publishedDate}>{formatPublishedDate(item.published_at)}</Text>
        </View>
      </View>
    </TouchableOpacity>
  );

  if (loading && !refreshing) {
    return (
      <SafeAreaView style={styles.container}>
        <StatusBar style="light" backgroundColor={colors.primary} />
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color={colors.primaryLight} />
          <Text style={styles.loadingText}>Chargement des replays...</Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar style="light" backgroundColor={colors.primary} />
      
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
          <Ionicons name="arrow-back" size={24} color={colors.white} />
        </TouchableOpacity>
        
        <View style={styles.headerContent}>
          <Text style={styles.headerTitle}>Replays</Text>
          <Text style={styles.headerSubtitle}>Revivez nos meilleures émissions</Text>
        </View>
        
        <TouchableOpacity onPress={() => router.push('/favorites')} style={styles.favoritesButton}>
          <Ionicons name="heart" size={24} color={colors.white} />
        </TouchableOpacity>
      </View>

      {/* Search Bar */}
      <View style={styles.searchContainer}>
        <View style={styles.searchBar}>
          <Ionicons name="search" size={20} color={colors.gray} />
          <TextInput
            style={styles.searchInput}
            placeholder="Rechercher une vidéo..."
            placeholderTextColor={colors.gray}
            value={searchQuery}
            onChangeText={setSearchQuery}
          />
          {searchQuery.length > 0 && (
            <TouchableOpacity onPress={() => setSearchQuery('')}>
              <Ionicons name="close-circle" size={20} color={colors.gray} />
            </TouchableOpacity>
          )}
        </View>
      </View>

      {/* Category Filter */}
      {renderCategoryFilter()}

      {/* Videos List */}
      <FlatList
        data={filteredVideos}
        keyExtractor={(item) => item.id}
        renderItem={renderVideoItem}
        contentContainerStyle={styles.videosList}
        showsVerticalScrollIndicator={false}
        onRefresh={onRefresh}
        refreshing={refreshing}
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Ionicons name="videocam-off" size={64} color={colors.gray} />
            <Text style={styles.emptyText}>Aucune vidéo trouvée</Text>
            <Text style={styles.emptySubtext}>
              {searchQuery ? 'Essayez d\'autres mots-clés' : 'Vérifiez votre connexion internet'}
            </Text>
          </View>
        }
      />
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
  header: {
    backgroundColor: colors.primary,
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 15,
  },
  backButton: {
    padding: 5,
  },
  headerContent: {
    flex: 1,
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: colors.white,
  },
  headerSubtitle: {
    fontSize: 14,
    color: colors.white,
    opacity: 0.8,
  },
  favoritesButton: {
    padding: 5,
  },
  searchContainer: {
    paddingHorizontal: 20,
    paddingVertical: 15,
    backgroundColor: colors.lightGray,
  },
  searchBar: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.white,
    borderRadius: 25,
    paddingHorizontal: 15,
    paddingVertical: 12,
  },
  searchInput: {
    flex: 1,
    marginLeft: 10,
    fontSize: 16,
    color: colors.black,
  },
  categoriesContainer: {
    paddingHorizontal: 15,
    paddingVertical: 10,
  },
  categoryButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.white,
    borderRadius: 20,
    paddingHorizontal: 15,
    paddingVertical: 8,
    marginRight: 10,
    borderWidth: 1,
    borderColor: colors.primary,
  },
  categoryButtonActive: {
    backgroundColor: colors.primary,
  },
  categoryButtonText: {
    fontSize: 14,
    fontWeight: '600',
    color: colors.primary,
    marginLeft: 5,
  },
  categoryButtonTextActive: {
    color: colors.white,
  },
  videosList: {
    paddingHorizontal: 20,
    paddingTop: 10,
  },
  videoCard: {
    backgroundColor: colors.white,
    borderRadius: 12,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  thumbnailContainer: {
    position: 'relative',
  },
  thumbnail: {
    width: '100%',
    height: 200,
    borderTopLeftRadius: 12,
    borderTopRightRadius: 12,
  },
  durationBadge: {
    position: 'absolute',
    bottom: 8,
    right: 8,
    backgroundColor: 'rgba(0,0,0,0.8)',
    borderRadius: 4,
    paddingHorizontal: 6,
    paddingVertical: 2,
  },
  durationText: {
    color: colors.white,
    fontSize: 12,
    fontWeight: 'bold',
  },
  favoriteButton: {
    position: 'absolute',
    top: 8,
    right: 8,
    backgroundColor: 'rgba(0,0,0,0.7)',
    borderRadius: 15,
    padding: 6,
  },
  videoInfo: {
    padding: 15,
  },
  videoTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: colors.black,
    marginBottom: 5,
  },
  videoDescription: {
    fontSize: 14,
    color: colors.gray,
    marginBottom: 10,
  },
  videoMeta: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  videoStats: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  videoStatsText: {
    fontSize: 12,
    color: colors.gray,
    marginLeft: 4,
  },
  publishedDate: {
    fontSize: 12,
    color: colors.gray,
  },
  emptyContainer: {
    alignItems: 'center',
    paddingVertical: 50,
  },
  emptyText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: colors.gray,
    marginTop: 15,
  },
  emptySubtext: {
    fontSize: 14,
    color: colors.gray,
    marginTop: 5,
    textAlign: 'center',
  },
});