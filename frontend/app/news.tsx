import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  Image,
  TouchableOpacity,
  ActivityIndicator,
  Alert,
  RefreshControl,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { StatusBar } from 'expo-status-bar';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';

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

interface NewsArticle {
  _id: string;
  title: string;
  content: string;
  excerpt: string;
  image_url?: string;
  category: string;
  published_at: string;
  author: string;
  view_count: number;
}

const categories = [
  { id: 'all', name: 'Tout', icon: 'grid' },
  { id: 'national', name: 'National', icon: 'flag' },
  { id: 'international', name: 'International', icon: 'globe' },
  { id: 'sport', name: 'Sport', icon: 'football' },
  { id: 'culture', name: 'Culture', icon: 'library' },
  { id: 'economie', name: 'Économie', icon: 'trending-up' },
];

export default function NewsScreen() {
  const [news, setNews] = useState<NewsArticle[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const router = useRouter();

  useEffect(() => {
    loadNews();
  }, [selectedCategory]);

  const loadNews = async () => {
    try {
      setLoading(true);
      const categoryParam = selectedCategory === 'all' ? '' : `?category=${selectedCategory}`;
      const response = await fetch(`${process.env.EXPO_PUBLIC_BACKEND_URL}/api/news${categoryParam}`);
      const data = await response.json();
      
      if (response.ok) {
        setNews(data.news || []);
      } else {
        console.error('Error loading news:', data);
      }
    } catch (error) {
      console.error('Error fetching news:', error);
      Alert.alert('Erreur', 'Impossible de charger les actualités');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    loadNews();
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffHours = Math.floor(diffTime / (1000 * 60 * 60));
    const diffDays = Math.floor(diffHours / 24);
    
    if (diffHours < 1) return 'Il y a quelques minutes';
    if (diffHours < 24) return `Il y a ${diffHours} heure${diffHours > 1 ? 's' : ''}`;
    if (diffDays === 1) return 'Hier';
    if (diffDays < 7) return `Il y a ${diffDays} jours`;
    
    return date.toLocaleDateString('fr-FR', {
      day: 'numeric',
      month: 'long',
      year: 'numeric'
    });
  };

  const getCategoryColor = (category: string) => {
    switch (category.toLowerCase()) {
      case 'national': return colors.primary;
      case 'international': return colors.blue;
      case 'sport': return colors.primaryLight;
      case 'culture': return colors.secondary;
      case 'economie': return '#f59e0b';
      default: return colors.gray;
    }
  };

  const shareArticle = (article: NewsArticle) => {
    Alert.alert(
      'Partager l\'article',
      `Partager "${article.title}"`,
      [
        { text: 'WhatsApp', onPress: () => console.log('Share WhatsApp') },
        { text: 'Facebook', onPress: () => console.log('Share Facebook') },
        { text: 'Twitter', onPress: () => console.log('Share Twitter') },
        { text: 'Annuler', style: 'cancel' }
      ]
    );
  };

  const navigateToArticle = (article: NewsArticle) => {
    router.push(`/news/${article._id}`);
  };

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
            size={16} 
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

  const renderNewsItem = ({ item, index }: { item: NewsArticle; index: number }) => {
    const isFirst = index === 0;
    
    return (
      <TouchableOpacity 
        style={[styles.newsCard, isFirst && styles.featuredCard]}
        onPress={() => navigateToArticle(item)}
      >
        {item.image_url && (
          <Image 
            source={{ uri: item.image_url }} 
            style={[styles.newsImage, isFirst && styles.featuredImage]}
            resizeMode="cover"
          />
        )}
        
        <View style={[styles.newsContent, isFirst && styles.featuredContent]}>
          <View style={styles.newsHeader}>
            <View 
              style={[
                styles.categoryBadge, 
                { backgroundColor: getCategoryColor(item.category) }
              ]}
            >
              <Text style={styles.categoryBadgeText}>{item.category.toUpperCase()}</Text>
            </View>
            
            <TouchableOpacity onPress={() => shareArticle(item)}>
              <Ionicons name="share-social" size={20} color={colors.gray} />
            </TouchableOpacity>
          </View>
          
          <Text 
            style={[styles.newsTitle, isFirst && styles.featuredTitle]} 
            numberOfLines={isFirst ? 3 : 2}
          >
            {item.title}
          </Text>
          
          <Text 
            style={[styles.newsExcerpt, isFirst && styles.featuredExcerpt]} 
            numberOfLines={isFirst ? 3 : 2}
          >
            {item.excerpt}
          </Text>
          
          <View style={styles.newsMeta}>
            <View style={styles.authorInfo}>
              <Ionicons name="person-circle" size={16} color={colors.primaryLight} />
              <Text style={styles.authorName}>{item.author}</Text>
            </View>
            
            <View style={styles.articleStats}>
              <Ionicons name="eye" size={14} color={colors.gray} />
              <Text style={styles.viewCount}>{item.view_count}</Text>
              <Text style={styles.publishedDate}>{formatDate(item.published_at)}</Text>
            </View>
          </View>
        </View>
        
        {isFirst && (
          <View style={styles.breakingBadge}>
            <Ionicons name="flash" size={16} color={colors.white} />
            <Text style={styles.breakingText}>À LA UNE</Text>
          </View>
        )}
      </TouchableOpacity>
    );
  };

  if (loading && !refreshing) {
    return (
      <SafeAreaView style={styles.container}>
        <StatusBar style="light" backgroundColor={colors.primary} />
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color={colors.primaryLight} />
          <Text style={styles.loadingText}>Chargement des actualités...</Text>
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
          <Text style={styles.headerTitle}>Actualités</Text>
          <Text style={styles.headerSubtitle}>Toute l'info du Burkina Faso</Text>
        </View>
        
        <TouchableOpacity onPress={() => router.push('/notifications')} style={styles.notificationButton}>
          <Ionicons name="notifications" size={24} color={colors.white} />
          <View style={styles.notificationBadge}>
            <Text style={styles.notificationBadgeText}>3</Text>
          </View>
        </TouchableOpacity>
      </View>

      {/* Category Filter */}
      {renderCategoryFilter()}

      {/* News List */}
      <FlatList
        data={news}
        keyExtractor={(item) => item._id}
        renderItem={renderNewsItem}
        contentContainerStyle={styles.newsList}
        showsVerticalScrollIndicator={false}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Ionicons name="newspaper-outline" size={64} color={colors.gray} />
            <Text style={styles.emptyText}>Aucune actualité</Text>
            <Text style={styles.emptySubtext}>
              Vérifiez votre connexion internet et réessayez
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
  notificationButton: {
    padding: 5,
    position: 'relative',
  },
  notificationBadge: {
    position: 'absolute',
    top: 0,
    right: 0,
    backgroundColor: colors.error,
    borderRadius: 8,
    width: 16,
    height: 16,
    justifyContent: 'center',
    alignItems: 'center',
  },
  notificationBadgeText: {
    color: colors.white,
    fontSize: 10,
    fontWeight: 'bold',
  },
  categoriesContainer: {
    paddingHorizontal: 15,
    paddingVertical: 10,
    backgroundColor: colors.lightGray,
  },
  categoryButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.white,
    borderRadius: 20,
    paddingHorizontal: 12,
    paddingVertical: 6,
    marginRight: 8,
    borderWidth: 1,
    borderColor: colors.primary,
  },
  categoryButtonActive: {
    backgroundColor: colors.primary,
  },
  categoryButtonText: {
    fontSize: 12,
    fontWeight: '600',
    color: colors.primary,
    marginLeft: 4,
  },
  categoryButtonTextActive: {
    color: colors.white,
  },
  newsList: {
    paddingHorizontal: 20,
    paddingTop: 10,
  },
  newsCard: {
    backgroundColor: colors.white,
    borderRadius: 12,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
    position: 'relative',
  },
  featuredCard: {
    borderWidth: 2,
    borderColor: colors.primaryLight,
    marginBottom: 25,
  },
  newsImage: {
    width: '100%',
    height: 150,
    borderTopLeftRadius: 12,
    borderTopRightRadius: 12,
  },
  featuredImage: {
    height: 200,
  },
  newsContent: {
    padding: 15,
  },
  featuredContent: {
    padding: 20,
  },
  newsHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 10,
  },
  categoryBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 6,
  },
  categoryBadgeText: {
    color: colors.white,
    fontSize: 10,
    fontWeight: 'bold',
  },
  newsTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: colors.black,
    marginBottom: 8,
    lineHeight: 22,
  },
  featuredTitle: {
    fontSize: 18,
    lineHeight: 25,
  },
  newsExcerpt: {
    fontSize: 14,
    color: colors.gray,
    marginBottom: 12,
    lineHeight: 20,
  },
  featuredExcerpt: {
    fontSize: 15,
    lineHeight: 22,
  },
  newsMeta: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  authorInfo: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  authorName: {
    fontSize: 12,
    color: colors.primaryLight,
    fontWeight: '600',
    marginLeft: 4,
  },
  articleStats: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  viewCount: {
    fontSize: 12,
    color: colors.gray,
    marginLeft: 4,
    marginRight: 10,
  },
  publishedDate: {
    fontSize: 12,
    color: colors.gray,
  },
  breakingBadge: {
    position: 'absolute',
    top: 15,
    left: 15,
    backgroundColor: colors.error,
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
  },
  breakingText: {
    color: colors.white,
    fontSize: 10,
    fontWeight: 'bold',
    marginLeft: 4,
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