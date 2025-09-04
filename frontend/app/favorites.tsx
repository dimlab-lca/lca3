import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  Image,
  TouchableOpacity,
  Alert,
  ActivityIndicator,
  RefreshControl,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { StatusBar } from 'expo-status-bar';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';

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
  added_to_favorites?: string;
}

export default function FavoritesScreen() {
  const [favorites, setFavorites] = useState<Video[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [user, setUser] = useState(null);
  const router = useRouter();

  useEffect(() => {
    checkUserAndLoadFavorites();
  }, []);

  const checkUserAndLoadFavorites = async () => {
    try {
      const userData = await AsyncStorage.getItem('user');
      if (!userData) {
        Alert.alert(
          'Connexion requise',
          'Vous devez être connecté pour voir vos favoris',
          [
            { text: 'Se connecter', onPress: () => router.push('/login') },
            { text: 'Retour', onPress: () => router.back() }
          ]
        );
        return;
      }

      setUser(JSON.parse(userData));
      loadFavorites();
    } catch (error) {
      console.error('Error checking user:', error);
      router.push('/login');
    }
  };

  const loadFavorites = async () => {
    try {
      setLoading(true);
      const token = await AsyncStorage.getItem('access_token');
      
      if (!token) {
        router.push('/login');
        return;
      }

      const response = await fetch(`${process.env.EXPO_PUBLIC_BACKEND_URL}/api/user/favorites`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setFavorites(data.favorites || []);
      } else if (response.status === 401) {
        router.push('/login');
      } else {
        Alert.alert('Erreur', 'Impossible de charger vos favoris');
      }
    } catch (error) {
      console.error('Error loading favorites:', error);
      Alert.alert('Erreur', 'Problème de connexion');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    loadFavorites();
  };

  const removeFromFavorites = async (videoId: string) => {
    Alert.alert(
      'Retirer des favoris',
      'Voulez-vous retirer cette vidéo de vos favoris ?',
      [
        { text: 'Annuler', style: 'cancel' },
        { 
          text: 'Retirer', 
          style: 'destructive',
          onPress: async () => {
            try {
              const token = await AsyncStorage.getItem('access_token');
              const response = await fetch(`${process.env.EXPO_PUBLIC_BACKEND_URL}/api/user/favorites/${videoId}`, {
                method: 'DELETE',
                headers: {
                  'Authorization': `Bearer ${token}`,
                },
              });

              if (response.ok) {
                setFavorites(prev => prev.filter(video => video.id !== videoId));
              } else {
                Alert.alert('Erreur', 'Impossible de retirer cette vidéo');
              }
            } catch (error) {
              console.error('Error removing favorite:', error);
              Alert.alert('Erreur', 'Problème de connexion');
            }
          }
        }
      ]
    );
  };

  const navigateToVideo = (video: Video) => {
    router.push(`/video/${video.id}`);
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

  const renderFavoriteItem = ({ item }: { item: Video }) => (
    <TouchableOpacity 
      style={styles.favoriteCard}
      onPress={() => navigateToVideo(item)}
    >
      <View style={styles.thumbnailContainer}>
        <Image source={{ uri: item.thumbnail }} style={styles.thumbnail} />
        <View style={styles.durationBadge}>
          <Text style={styles.durationText}>{item.duration || '00:00'}</Text>
        </View>
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
          
          <TouchableOpacity 
            onPress={() => removeFromFavorites(item.id)}
            style={styles.removeButton}
          >
            <Ionicons name="heart" size={20} color={colors.error} />
          </TouchableOpacity>
        </View>
        
        <View style={styles.addedInfo}>
          <Ionicons name="time" size={12} color={colors.gray} />
          <Text style={styles.addedText}>
            Ajouté le {item.added_to_favorites ? formatDate(item.added_to_favorites) : 'récemment'}
          </Text>
        </View>
      </View>
    </TouchableOpacity>
  );

  const EmptyState = () => (
    <View style={styles.emptyContainer}>
      <Ionicons name="heart-outline" size={80} color={colors.gray} />
      <Text style={styles.emptyTitle}>Aucun favori</Text>
      <Text style={styles.emptyDescription}>
        Ajoutez des vidéos à vos favoris pour les retrouver facilement ici
      </Text>
      <TouchableOpacity 
        style={styles.exploreButton}
        onPress={() => router.push('/replay')}
      >
        <Text style={styles.exploreButtonText}>Explorer les vidéos</Text>
      </TouchableOpacity>
    </View>
  );

  if (loading && !refreshing) {
    return (
      <SafeAreaView style={styles.container}>
        <StatusBar style="light" backgroundColor={colors.primary} />
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color={colors.primaryLight} />
          <Text style={styles.loadingText}>Chargement de vos favoris...</Text>
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
          <Text style={styles.headerTitle}>Mes Favoris</Text>
          <Text style={styles.headerSubtitle}>
            {favorites.length} vidéo{favorites.length > 1 ? 's' : ''} sauvegardée{favorites.length > 1 ? 's' : ''}
          </Text>
        </View>
        
        {favorites.length > 0 && (
          <TouchableOpacity onPress={() => router.push('/profile')} style={styles.profileButton}>
            <Ionicons name="person-circle" size={24} color={colors.white} />
          </TouchableOpacity>
        )}
      </View>

      {/* Favorites List */}
      <FlatList
        data={favorites}
        keyExtractor={(item) => item.id}
        renderItem={renderFavoriteItem}
        contentContainerStyle={styles.favoritesList}
        showsVerticalScrollIndicator={false}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
            colors={[colors.primaryLight]}
            tintColor={colors.primaryLight}
          />
        }
        ListEmptyComponent={<EmptyState />}
      />

      {/* Bottom Info */}
      {favorites.length > 0 && (
        <View style={styles.bottomInfo}>
          <View style={styles.infoCard}>
            <Ionicons name="information-circle" size={20} color={colors.primaryLight} />
            <Text style={styles.infoText}>
              Regardez vos vidéos favorites pour gagner des points supplémentaires !
            </Text>
          </View>
        </View>
      )}
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
  profileButton: {
    padding: 5,
  },
  favoritesList: {
    paddingHorizontal: 20,
    paddingTop: 15,
    paddingBottom: 100,
  },
  favoriteCard: {
    backgroundColor: colors.white,
    borderRadius: 12,
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
    overflow: 'hidden',
  },
  thumbnailContainer: {
    position: 'relative',
  },
  thumbnail: {
    width: '100%',
    height: 180,
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
  videoInfo: {
    padding: 15,
  },
  videoTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: colors.black,
    marginBottom: 5,
    lineHeight: 22,
  },
  videoDescription: {
    fontSize: 14,
    color: colors.gray,
    marginBottom: 10,
    lineHeight: 20,
  },
  videoMeta: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
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
  removeButton: {
    padding: 5,
  },
  addedInfo: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  addedText: {
    fontSize: 12,
    color: colors.gray,
    marginLeft: 5,
  },
  emptyContainer: {
    alignItems: 'center',
    paddingVertical: 60,
    paddingHorizontal: 40,
  },
  emptyTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: colors.black,
    marginTop: 20,
    marginBottom: 10,
  },
  emptyDescription: {
    fontSize: 16,
    color: colors.gray,
    textAlign: 'center',
    lineHeight: 22,
    marginBottom: 30,
  },
  exploreButton: {
    backgroundColor: colors.primaryLight,
    paddingHorizontal: 30,
    paddingVertical: 15,
    borderRadius: 25,
  },
  exploreButtonText: {
    color: colors.white,
    fontSize: 16,
    fontWeight: 'bold',
  },
  bottomInfo: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    backgroundColor: colors.white,
    borderTopWidth: 1,
    borderTopColor: colors.lightGray,
  },
  infoCard: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 15,
    margin: 15,
    backgroundColor: colors.lightGray,
    borderRadius: 12,
  },
  infoText: {
    fontSize: 14,
    color: colors.black,
    marginLeft: 10,
    flex: 1,
    lineHeight: 18,
  },
});