import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
  SafeAreaView,
  Image,
  Dimensions,
} from 'react-native';

const { width: screenWidth } = Dimensions.get('window');

// LCA TV Colors
const colors = {
  primary: '#2d5016',
  primaryLight: '#22c55e',
  blue: '#3b82f6',
  orange: '#f97316',
  red: '#ef4444',
  white: '#ffffff',
  gray: '#6b7280',
  lightGray: '#f3f4f6',
  black: '#111827',
};

export default function App() {
  const [currentPage, setCurrentPage] = useState('welcome');
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadVideos();
  }, []);

  const loadVideos = async () => {
    try {
      setLoading(true);
      // Use relative URL for API calls
      const response = await fetch('/api/videos');
      const data = await response.json();
      setVideos(data.videos || []);
    } catch (error) {
      console.log('Using demo data');
      setVideos([
        {
          id: '1',
          title: 'Journal LCA TV - Édition du Soir',
          thumbnail: 'https://i.ytimg.com/vi/eSApphrRKWg/hqdefault.jpg',
          view_count: '15K',
          duration: '25:30'
        },
        {
          id: '2', 
          title: 'Franc-Parler - Débat Économie',
          thumbnail: 'https://i.ytimg.com/vi/xJatmbxIaIM/hqdefault.jpg',
          view_count: '8.7K',
          duration: '45:12'
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  // Welcome Page
  const WelcomePage = () => (
    <ScrollView style={styles.container}>
      <View style={styles.welcomeHeader}>
        <Text style={styles.logo}>LCA TV</Text>
        <Text style={styles.tagline}>La Chaîne Africaine de télévision</Text>
      </View>
      
      <View style={styles.heroSection}>
        <Text style={styles.welcomeTitle}>🎬 Bienvenue sur LCA TV</Text>
        <Text style={styles.welcomeText}>
          Découvrez l'actualité, le divertissement et la culture du Burkina Faso 
          en direct et en replay avec une qualité exceptionnelle.
        </Text>
      </View>

      <View style={styles.featuresSection}>
        <View style={styles.featureCard}>
          <Text style={styles.featureIcon}>🔴</Text>
          <Text style={styles.featureTitle}>Direct 24/7</Text>
          <Text style={styles.featureText}>Suivez nos programmes en temps réel</Text>
        </View>
        
        <View style={styles.featureCard}>
          <Text style={styles.featureIcon}>▶️</Text>
          <Text style={styles.featureTitle}>Replays HD</Text>
          <Text style={styles.featureText}>Rattrapage de toutes vos émissions</Text>
        </View>
        
        <View style={styles.featureCard}>
          <Text style={styles.featureIcon}>📰</Text>
          <Text style={styles.featureTitle}>Actualités</Text>
          <Text style={styles.featureText}>Info nationale et internationale</Text>
        </View>
        
        <View style={styles.featureCard}>
          <Text style={styles.featureIcon}>🌍</Text>
          <Text style={styles.featureTitle}>Culture</Text>
          <Text style={styles.featureText}>Patrimoine burkinabè authentique</Text>
        </View>
      </View>

      <View style={styles.actionButtons}>
        <TouchableOpacity 
          style={styles.primaryButton}
          onPress={() => setCurrentPage('home')}
        >
          <Text style={styles.primaryButtonText}>🚀 Découvrir l'App</Text>
        </TouchableOpacity>
        
        <TouchableOpacity 
          style={styles.secondaryButton}
          onPress={() => Alert.alert('Connexion', 'Fonctionnalité de connexion disponible')}
        >
          <Text style={styles.secondaryButtonText}>Se connecter</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.statsSection}>
        <View style={styles.statCard}>
          <Text style={styles.statNumber}>🔥 500K+</Text>
          <Text style={styles.statLabel}>Téléspectateurs</Text>
        </View>
        <View style={styles.statCard}>
          <Text style={styles.statNumber}>📡 24/7</Text>
          <Text style={styles.statLabel}>Diffusion</Text>
        </View>
        <View style={styles.statCard}>
          <Text style={styles.statNumber}>🇧🇫 100%</Text>
          <Text style={styles.statLabel}>Burkinabè</Text>
        </View>
      </View>
    </ScrollView>
  );

  // Home Page
  const HomePage = () => (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => setCurrentPage('welcome')} style={styles.backButton}>
          <Text style={styles.backButtonText}>← LCA TV</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.liveSection}>
        <Text style={styles.liveTitle}>🔴 EN DIRECT</Text>
        <Text style={styles.liveSubtitle}>Journal du soir - Édition spéciale</Text>
        <TouchableOpacity style={styles.playButton}>
          <Text style={styles.playButtonText}>▶️ Regarder en direct</Text>
        </TouchableOpacity>
        <Text style={styles.viewerCount}>👥 1,247 spectateurs connectés</Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>⭐ Programmes populaires</Text>
        
        {loading ? (
          <Text style={styles.loadingText}>Chargement des vidéos...</Text>
        ) : (
          <ScrollView horizontal showsHorizontalScrollIndicator={false}>
            {videos.map((video, index) => (
              <TouchableOpacity key={index} style={styles.videoCard}>
                <Image source={{ uri: video.thumbnail }} style={styles.videoThumbnail} />
                <View style={styles.videoInfo}>
                  <Text style={styles.videoTitle} numberOfLines={2}>{video.title}</Text>
                  <Text style={styles.videoMeta}>{video.view_count} vues • {video.duration}</Text>
                </View>
              </TouchableOpacity>
            ))}
          </ScrollView>
        )}
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>📱 Nos émissions</Text>
        <View style={styles.categoriesGrid}>
          <TouchableOpacity style={styles.categoryCard}>
            <Text style={styles.categoryIcon}>📰</Text>
            <Text style={styles.categoryText}>Actualités</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.categoryCard}>
            <Text style={styles.categoryIcon}>⚽</Text>
            <Text style={styles.categoryText}>Sports</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.categoryCard}>
            <Text style={styles.categoryIcon}>🌍</Text>
            <Text style={styles.categoryText}>Culture</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.categoryCard}>
            <Text style={styles.categoryIcon}>🗣️</Text>
            <Text style={styles.categoryText}>Débats</Text>
          </TouchableOpacity>
        </View>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>📢 Programme Publicitaire</Text>
        <TouchableOpacity style={styles.adBanner}>
          <Text style={styles.adTitle}>Boostez votre visibilité avec LCA TV</Text>
          <Text style={styles.adSubtitle}>Spots TV • Sponsoring • Digital</Text>
          <Text style={styles.adCta}>En savoir plus →</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.footer}>
        <Text style={styles.footerTitle}>LCA TV</Text>
        <Text style={styles.footerText}>
          Votre média de référence au Burkina Faso depuis 2018. 
          Information, culture, sport et divertissement de qualité.
        </Text>
      </View>
    </ScrollView>
  );

  return (
    <SafeAreaView style={styles.safeArea}>
      {currentPage === 'welcome' ? <WelcomePage /> : <HomePage />}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: colors.white,
  },
  container: {
    flex: 1,
    backgroundColor: colors.white,
  },
  
  // Welcome Page Styles
  welcomeHeader: {
    backgroundColor: colors.primary,
    padding: 40,
    alignItems: 'center',
  },
  logo: {
    fontSize: 48,
    fontWeight: 'bold',
    color: colors.white,
    marginBottom: 10,
  },
  tagline: {
    fontSize: 16,
    color: colors.white,
    opacity: 0.9,
  },
  heroSection: {
    padding: 30,
    alignItems: 'center',
  },
  welcomeTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: colors.black,
    textAlign: 'center',
    marginBottom: 20,
  },
  welcomeText: {
    fontSize: 16,
    color: colors.gray,
    textAlign: 'center',
    lineHeight: 24,
  },
  
  // Features Section
  featuresSection: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    marginBottom: 30,
  },
  featureCard: {
    width: (screenWidth - 60) / 2,
    backgroundColor: colors.lightGray,
    borderRadius: 15,
    padding: 20,
    marginBottom: 15,
    alignItems: 'center',
  },
  featureIcon: {
    fontSize: 32,
    marginBottom: 10,
  },
  featureTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: colors.black,
    marginBottom: 5,
  },
  featureText: {
    fontSize: 12,
    color: colors.gray,
    textAlign: 'center',
  },
  
  // Action Buttons
  actionButtons: {
    paddingHorizontal: 30,
    marginBottom: 30,
  },
  primaryButton: {
    backgroundColor: colors.primaryLight,
    borderRadius: 25,
    paddingVertical: 18,
    marginBottom: 15,
    alignItems: 'center',
  },
  primaryButtonText: {
    color: colors.white,
    fontSize: 18,
    fontWeight: 'bold',
  },
  secondaryButton: {
    borderWidth: 2,
    borderColor: colors.primary,
    borderRadius: 25,
    paddingVertical: 16,
    alignItems: 'center',
  },
  secondaryButtonText: {
    color: colors.primary,
    fontSize: 16,
    fontWeight: 'bold',
  },
  
  // Stats Section
  statsSection: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    paddingHorizontal: 20,
    marginBottom: 40,
  },
  statCard: {
    alignItems: 'center',
    backgroundColor: colors.lightGray,
    borderRadius: 15,
    padding: 20,
    minWidth: 90,
  },
  statNumber: {
    fontSize: 20,
    fontWeight: 'bold',
    color: colors.primary,
    marginBottom: 5,
  },
  statLabel: {
    fontSize: 12,
    color: colors.gray,
    textAlign: 'center',
  },
  
  // Home Page Styles
  header: {
    backgroundColor: colors.primary,
    padding: 20,
  },
  backButton: {
    alignSelf: 'flex-start',
  },
  backButtonText: {
    color: colors.white,
    fontSize: 18,
    fontWeight: 'bold',
  },
  
  // Live Section
  liveSection: {
    backgroundColor: colors.primary,
    padding: 30,
    alignItems: 'center',
    marginBottom: 20,
  },
  liveTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: colors.white,
    marginBottom: 10,
  },
  liveSubtitle: {
    fontSize: 16,
    color: colors.white,
    opacity: 0.9,
    textAlign: 'center',
    marginBottom: 20,
  },
  playButton: {
    backgroundColor: 'rgba(255,255,255,0.3)',
    borderRadius: 25,
    paddingHorizontal: 30,
    paddingVertical: 15,
    marginBottom: 15,
  },
  playButtonText: {
    color: colors.white,
    fontSize: 18,
    fontWeight: 'bold',
  },
  viewerCount: {
    color: colors.white,
    fontSize: 14,
  },
  
  // Sections
  section: {
    marginVertical: 20,
    paddingHorizontal: 20,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: colors.black,
    marginBottom: 15,
  },
  
  // Video Cards
  videoCard: {
    width: 200,
    marginRight: 15,
    backgroundColor: colors.white,
    borderRadius: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  videoThumbnail: {
    width: '100%',
    height: 120,
    borderTopLeftRadius: 15,
    borderTopRightRadius: 15,
    resizeMode: 'cover',
  },
  videoInfo: {
    padding: 12,
  },
  videoTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    color: colors.black,
    marginBottom: 5,
  },
  videoMeta: {
    fontSize: 12,
    color: colors.gray,
  },
  loadingText: {
    fontSize: 16,
    color: colors.gray,
    textAlign: 'center',
    padding: 20,
  },
  
  // Categories Grid
  categoriesGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  categoryCard: {
    width: (screenWidth - 60) / 4,
    alignItems: 'center',
    backgroundColor: colors.lightGray,
    borderRadius: 15,
    padding: 15,
    marginBottom: 15,
  },
  categoryIcon: {
    fontSize: 32,
    marginBottom: 8,
  },
  categoryText: {
    fontSize: 12,
    color: colors.black,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  
  // Ad Banner
  adBanner: {
    backgroundColor: colors.blue,
    borderRadius: 15,
    padding: 25,
    alignItems: 'center',
  },
  adTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: colors.white,
    textAlign: 'center',
    marginBottom: 10,
  },
  adSubtitle: {
    fontSize: 14,
    color: colors.white,
    textAlign: 'center',
    marginBottom: 15,
  },
  adCta: {
    fontSize: 16,
    color: colors.white,
    fontWeight: 'bold',
  },
  
  // Footer
  footer: {
    backgroundColor: colors.lightGray,
    padding: 30,
    alignItems: 'center',
    marginTop: 20,
  },
  footerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: colors.primary,
    marginBottom: 10,
  },
  footerText: {
    fontSize: 14,
    color: colors.gray,
    textAlign: 'center',
    lineHeight: 20,
  },
});