import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Image,
  TouchableOpacity,
  Dimensions,
  Alert,
  TextInput,
  ActivityIndicator,
  SafeAreaView,
  StatusBar,
  Animated,
  Modal,
  FlatList,
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

const { width: screenWidth, height: screenHeight } = Dimensions.get('window');

// LCA TV Colors - Modern Style
const colors = {
  primary: '#2d5016',
  primaryLight: '#22c55e',
  secondary: '#16a34a',
  blue: '#3b82f6',
  darkBlue: '#1e40af',
  purple: '#8b5cf6',
  pink: '#ec4899',
  orange: '#f97316',
  yellow: '#eab308',
  cyan: '#06b6d4',
  red: '#ef4444',
  emerald: '#10b981',
  indigo: '#6366f1',
  white: '#ffffff',
  gray: '#6b7280',
  lightGray: '#f3f4f6',
  darkGray: '#374151',
  black: '#111827',
  cardShadow: 'rgba(0, 0, 0, 0.1)',
};

export default function App() {
  const [currentPage, setCurrentPage] = useState('welcome');
  const [user, setUser] = useState(null);
  const [videos, setVideos] = useState([]);
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [slideAnim] = useState(new Animated.Value(-screenWidth));

  useEffect(() => {
    checkExistingUser();
    loadInitialData();
  }, []);

  const checkExistingUser = async () => {
    try {
      const userData = await AsyncStorage.getItem('user');
      if (userData) {
        setUser(JSON.parse(userData));
        setCurrentPage('home');
      }
    } catch (error) {
      console.error('Error checking user:', error);
    }
  };

  const loadInitialData = async () => {
    try {
      await loadVideos();
      await loadNews();
    } catch (error) {
      console.error('Error loading initial data:', error);
    }
  };

  const loadVideos = async () => {
    try {
      const response = await fetch('https://lcatv-mobile.preview.emergentagent.com/api/videos');
      const data = await response.json();
      setVideos(data.videos || []);
    } catch (error) {
      console.error('Error loading videos:', error);
      setVideos([
        {
          id: 'eSApphrRKWg',
          title: 'Journal LCA TV - Édition du Soir',
          thumbnail: 'https://i.ytimg.com/vi/eSApphrRKWg/hqdefault.jpg',
          view_count: '15420',
          like_count: '234',
          category: 'actualites'
        },
        {
          id: 'xJatmbxIaIM',
          title: 'Franc-Parler - Débat Économie',
          thumbnail: 'https://i.ytimg.com/vi/xJatmbxIaIM/hqdefault.jpg',
          view_count: '8750',
          like_count: '156',
          category: 'debats'
        },
        {
          id: '8aIAKRe4Spo',
          title: 'Festival des Masques - Culture Burkinabè',
          thumbnail: 'https://i.ytimg.com/vi/8aIAKRe4Spo/hqdefault.jpg',
          view_count: '12300',
          like_count: '298',
          category: 'culture'
        }
      ]);
    }
  };

  const loadNews = async () => {
    try {
      const response = await fetch('https://lcatv-mobile.preview.emergentagent.com/api/news');
      const data = await response.json();
      setNews(data.news || []);
    } catch (error) {
      console.error('Error loading news:', error);
      setNews([
        {
          _id: '1',
          title: 'Flash Info - Burkina Faso',
          excerpt: 'Les dernières nouvelles du pays des hommes intègres...',
          image_url: 'https://images.unsplash.com/photo-1716399409349-e1a11a2d789f',
          published_at: new Date().toISOString(),
          category: 'national'
        },
        {
          _id: '2',
          title: 'Étalons du Burkina - Victoire historique',
          excerpt: 'L\'équipe nationale remporte un match décisif...',
          image_url: 'https://images.unsplash.com/photo-1613425295457-ff05c1b63e23',
          published_at: new Date(Date.now() - 2*60*60*1000).toISOString(),
          category: 'sport'
        },
        {
          _id: '3',
          title: 'Festival de la Culture - Ouagadougou',
          excerpt: 'Célébration de la richesse culturelle burkinabè...',
          image_url: 'https://images.unsplash.com/photo-1639572492198-98b45f2867d1',
          published_at: new Date(Date.now() - 4*60*60*1000).toISOString(),
          category: 'culture'
        }
      ]);
    }
  };

  const handleLogin = async (email, password) => {
    setLoading(true);
    try {
      const response = await fetch('https://lcatv-mobile.preview.emergentagent.com/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password, remember_me: true }),
      });

      const data = await response.json();
      if (response.ok) {
        await AsyncStorage.setItem('user', JSON.stringify(data.user));
        await AsyncStorage.setItem('access_token', data.access_token);
        setUser(data.user);
        Alert.alert('Connexion réussie', `Bienvenue ${data.user.prenom} !`);
        setCurrentPage('home');
      } else {
        Alert.alert('Erreur', data.detail || 'Email ou mot de passe incorrect');
      }
    } catch (error) {
      Alert.alert('Erreur', 'Problème de connexion');
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (userData) => {
    setLoading(true);
    try {
      const response = await fetch('https://lcatv-mobile.preview.emergentagent.com/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      const data = await response.json();
      if (response.ok) {
        await AsyncStorage.setItem('user', JSON.stringify(data.user));
        await AsyncStorage.setItem('access_token', data.access_token);
        setUser(data.user);
        Alert.alert('Inscription réussie !', `Bienvenue ${data.user.prenom} ! Vous avez reçu 100 points.`);
        setCurrentPage('home');
      } else {
        Alert.alert('Erreur', data.detail || 'Une erreur est survenue');
      }
    } catch (error) {
      Alert.alert('Erreur', 'Problème de connexion');
    } finally {
      setLoading(false);
    }
  };

  const toggleSidebar = () => {
    if (sidebarOpen) {
      Animated.timing(slideAnim, {
        toValue: -screenWidth,
        duration: 300,
        useNativeDriver: false,
      }).start(() => setSidebarOpen(false));
    } else {
      setSidebarOpen(true);
      Animated.timing(slideAnim, {
        toValue: 0,
        duration: 300,
        useNativeDriver: false,
      }).start();
    }
  };

  const navigateTo = (page) => {
    setCurrentPage(page);
    if (sidebarOpen) toggleSidebar();
  };

  const logout = async () => {
    await AsyncStorage.removeItem('user');
    await AsyncStorage.removeItem('access_token');
    setUser(null);
    setCurrentPage('welcome');
    if (sidebarOpen) toggleSidebar();
  };

  // Icon Component
  const Icon = ({ name, size = 24, color = colors.gray }) => {
    const icons = {
      home: '🏠', radio: '📡', play: '▶️', star: '⭐', grid: '⚏',
      newspaper: '📰', person: '👤', heart: '❤️', megaphone: '📢',
      arrow: '→', back: '←', live: '🔴', tv: '📺', video: '🎥',
      news: '📰', menu: '☰', close: '✕', logout: '🚪',
      settings: '⚙️', info: 'ℹ️', help: '❓', notification: '🔔',
      fire: '🔥', trending: '📈', clock: '🕐', location: '📍',
      search: '🔍', filter: '🎛️', share: '📤', download: '📥',
    };
    
    return (
      <Text style={{ fontSize: size, color }}>{icons[name] || '•'}</Text>
    );
  };

  // Modern Card Component
  const ModernCard = ({ children, style, color = colors.white, shadowLevel = 'medium' }) => {
    const shadowStyles = {
      light: { elevation: 2, shadowOpacity: 0.05 },
      medium: { elevation: 5, shadowOpacity: 0.1 },
      heavy: { elevation: 8, shadowOpacity: 0.15 }
    };

    return (
      <View style={[
        styles.modernCard,
        { backgroundColor: color },
        shadowStyles[shadowLevel],
        style
      ]}>
        {children}
      </View>
    );
  };

  // Welcome Page - Ultra Modern with Rich Content
  const WelcomePage = () => (
    <View style={styles.welcomeContainer}>
      <StatusBar barStyle="light-content" backgroundColor={colors.primary} />
      
      {/* Hero Background */}
      <View style={styles.welcomeBackground}>
        <Image 
          source={{ uri: 'https://images.unsplash.com/photo-1713453450934-ffa72b233597' }}
          style={styles.welcomeBackgroundImage}
          blurRadius={3}
        />
        <View style={styles.gradientOverlay} />
        
        {/* Floating Elements */}
        <View style={styles.floatingElement1} />
        <View style={styles.floatingElement2} />
        <View style={styles.floatingElement3} />
        
        {/* Hero Section */}
        <ScrollView style={styles.welcomeScroll} showsVerticalScrollIndicator={false}>
          <View style={styles.heroSection}>
            <ModernCard style={styles.logoHeroCard} shadowLevel="heavy">
              <View style={styles.logoHero}>
                <Text style={styles.logoHeroText}>LCA</Text>
                <View style={styles.logoHeroCircle}>
                  <Text style={styles.logoHeroSubText}>TV</Text>
                </View>
              </View>
            </ModernCard>
            
            <Text style={styles.welcomeTitle}>Bienvenue sur LCA TV</Text>
            <Text style={styles.welcomeSubtitle}>La Chaîne Africaine de télévision</Text>
            <Text style={styles.welcomeDescription}>
              Découvrez l'actualité, le divertissement et la culture du Burkina Faso 
              en direct et en replay. Plus de 500,000 téléspectateurs nous font confiance.
            </Text>

            {/* Features Preview Cards */}
            <View style={styles.featuresPreview}>
              <ModernCard style={[styles.featureCard, { backgroundColor: colors.red }]}>
                <Icon name="live" size={28} color={colors.white} />
                <Text style={styles.featureCardTitle}>Direct 24/7</Text>
                <Text style={styles.featureCardDesc}>Stream en continu</Text>
              </ModernCard>
              
              <ModernCard style={[styles.featureCard, { backgroundColor: colors.blue }]}>
                <Icon name="play" size={28} color={colors.white} />
                <Text style={styles.featureCardTitle}>Replays</Text>
                <Text style={styles.featureCardDesc}>Toutes nos émissions</Text>
              </ModernCard>
              
              <ModernCard style={[styles.featureCard, { backgroundColor: colors.orange }]}>
                <Icon name="news" size={28} color={colors.white} />
                <Text style={styles.featureCardTitle}>Actualités</Text>
                <Text style={styles.featureCardDesc}>Info en temps réel</Text>
              </ModernCard>
            </View>

            {/* Trending Shows */}
            <ModernCard style={styles.trendingSection}>
              <View style={styles.trendingSectionHeader}>
                <Icon name="fire" size={24} color={colors.orange} />
                <Text style={styles.trendingSectionTitle}>Émissions Populaires</Text>
              </View>
              
              <ScrollView horizontal showsHorizontalScrollIndicator={false}>
                <View style={styles.trendingShows}>
                  <ModernCard style={[styles.trendingShowCard, { backgroundColor: colors.purple }]}>
                    <Text style={styles.trendingShowTitle}>Journal LCA</Text>
                    <Text style={styles.trendingShowTime}>19h00</Text>
                  </ModernCard>
                  
                  <ModernCard style={[styles.trendingShowCard, { backgroundColor: colors.emerald }]}>
                    <Text style={styles.trendingShowTitle}>Franc-Parler</Text>
                    <Text style={styles.trendingShowTime}>20h30</Text>
                  </ModernCard>
                  
                  <ModernCard style={[styles.trendingShowCard, { backgroundColor: colors.cyan }]}>
                    <Text style={styles.trendingShowTitle}>Questions de Femmes</Text>
                    <Text style={styles.trendingShowTime}>21h15</Text>
                  </ModernCard>
                </View>
              </ScrollView>
            </ModernCard>

            {/* Action Buttons */}
            <View style={styles.welcomeActions}>
              <TouchableOpacity 
                style={styles.primaryActionButton}
                onPress={() => setCurrentPage('login')}
              >
                <ModernCard style={styles.primaryActionCard} color={colors.primaryLight}>
                  <Icon name="person" size={24} color={colors.white} />
                  <Text style={styles.primaryActionText}>Se connecter</Text>
                </ModernCard>
              </TouchableOpacity>
              
              <TouchableOpacity 
                style={styles.secondaryActionButton}
                onPress={() => setCurrentPage('register')}
              >
                <ModernCard style={styles.secondaryActionCard} color={colors.indigo}>
                  <Icon name="star" size={24} color={colors.white} />
                  <Text style={styles.secondaryActionText}>Créer un compte</Text>
                </ModernCard>
              </TouchableOpacity>
              
              <TouchableOpacity 
                style={styles.ghostActionButton}
                onPress={() => setCurrentPage('home')}
              >
                <ModernCard style={styles.ghostActionCard} color={colors.darkGray}>
                  <Icon name="arrow" size={20} color={colors.white} />
                  <Text style={styles.ghostActionText}>Continuer sans compte</Text>
                </ModernCard>
              </TouchableOpacity>
            </View>

            {/* Statistics Cards */}
            <View style={styles.statsSection}>
              <ModernCard style={[styles.statCard, { backgroundColor: colors.pink }]}>
                <Icon name="trending" size={32} color={colors.white} />
                <Text style={styles.statNumber}>500K+</Text>
                <Text style={styles.statLabel}>Téléspectateurs</Text>
              </ModernCard>
              
              <ModernCard style={[styles.statCard, { backgroundColor: colors.yellow }]}>
                <Icon name="clock" size={32} color={colors.white} />
                <Text style={styles.statNumber}>24/7</Text>
                <Text style={styles.statLabel}>Diffusion</Text>
              </ModernCard>
              
              <ModernCard style={[styles.statCard, { backgroundColor: colors.emerald }]}>
                <Icon name="location" size={32} color={colors.white} />
                <Text style={styles.statNumber}>100%</Text>
                <Text style={styles.statLabel}>Burkinabè</Text>
              </ModernCard>
            </View>

            {/* Partnership Section */}
            <ModernCard style={styles.partnershipSection}>
              <Text style={styles.partnershipTitle}>Nos Partenaires</Text>
              <View style={styles.partnersGrid}>
                <View style={[styles.partnerCard, { backgroundColor: colors.orange }]}>
                  <Text style={styles.partnerText}>TV5</Text>
                </View>
                <View style={[styles.partnerCard, { backgroundColor: colors.purple }]}>
                  <Text style={styles.partnerText}>RFI</Text>
                </View>
                <View style={[styles.partnerCard, { backgroundColor: colors.cyan }]}>
                  <Text style={styles.partnerText}>FRANCE24</Text>
                </View>
                <View style={[styles.partnerCard, { backgroundColor: colors.indigo }]}>
                  <Text style={styles.partnerText}>BBC</Text>
                </View>
              </View>
            </ModernCard>
          </View>
        </ScrollView>
      </View>
    </View>
  );

  // Enhanced Sidebar
  const Sidebar = () => (
    <Modal
      transparent={true}
      visible={sidebarOpen}
      animationType="none"
      onRequestClose={toggleSidebar}
    >
      <View style={styles.sidebarOverlay}>
        <TouchableOpacity 
          style={styles.sidebarBackdrop} 
          onPress={toggleSidebar}
        />
        
        <Animated.View style={[styles.sidebar, { transform: [{ translateX: slideAnim }] }]}>
          {/* Enhanced Sidebar Header */}
          <View style={styles.sidebarHeader}>
            {user ? (
              <ModernCard style={styles.sidebarUserCard} color={colors.primaryLight}>
                <View style={styles.sidebarUserInfo}>
                  <View style={styles.sidebarAvatar}>
                    <Text style={styles.sidebarAvatarText}>
                      {user.nom.charAt(0)}{user.prenom.charAt(0)}
                    </Text>
                  </View>
                  <View style={styles.sidebarUserDetails}>
                    <Text style={styles.sidebarUserName}>{user.prenom} {user.nom}</Text>
                    <Text style={styles.sidebarUserEmail}>{user.email}</Text>
                    <View style={styles.pointsBadge}>
                      <Icon name="star" size={16} color={colors.yellow} />
                      <Text style={styles.sidebarUserPoints}>{user.points || 0} points</Text>
                    </View>
                  </View>
                </View>
              </ModernCard>
            ) : (
              <ModernCard style={styles.sidebarGuestCard} color={colors.darkGray}>
                <View style={styles.sidebarGuestInfo}>
                  <View style={styles.sidebarGuestAvatar}>
                    <Icon name="person" size={32} color={colors.white} />
                  </View>
                  <Text style={styles.sidebarGuestText}>Visiteur</Text>
                  <TouchableOpacity 
                    style={styles.sidebarLoginBtn}
                    onPress={() => navigateTo('login')}
                  >
                    <Text style={styles.sidebarLoginText}>Se connecter</Text>
                  </TouchableOpacity>
                </View>
              </ModernCard>
            )}
          </View>

          {/* Enhanced Navigation Menu */}
          <ScrollView style={styles.sidebarMenu}>
            <View style={styles.menuSection}>
              <Text style={styles.menuSectionTitle}>Navigation</Text>
              
              <TouchableOpacity style={styles.menuItem} onPress={() => navigateTo('home')}>
                <View style={[styles.menuIcon, { backgroundColor: colors.primaryLight }]}>
                  <Icon name="home" size={20} color={colors.white} />
                </View>
                <Text style={styles.menuItemText}>Accueil</Text>
                <View style={styles.menuArrow}>
                  <Icon name="arrow" size={16} color={colors.gray} />
                </View>
              </TouchableOpacity>
              
              <TouchableOpacity style={styles.menuItem} onPress={() => navigateTo('live')}>
                <View style={[styles.menuIcon, { backgroundColor: colors.red }]}>
                  <Icon name="radio" size={20} color={colors.white} />
                </View>
                <Text style={styles.menuItemText}>Direct</Text>
                <View style={styles.liveBadge}>
                  <Text style={styles.liveBadgeText}>LIVE</Text>
                </View>
              </TouchableOpacity>
              
              <TouchableOpacity style={styles.menuItem} onPress={() => Alert.alert('Replays', 'Accédez aux replays')}>
                <View style={[styles.menuIcon, { backgroundColor: colors.blue }]}>
                  <Icon name="play" size={20} color={colors.white} />
                </View>
                <Text style={styles.menuItemText}>Replays</Text>
                <View style={styles.menuBadge}>
                  <Text style={styles.menuBadgeText}>+200</Text>
                </View>
              </TouchableOpacity>
              
              <TouchableOpacity style={styles.menuItem} onPress={() => Alert.alert('Actualités', 'Toute l\'info du Burkina')}>
                <View style={[styles.menuIcon, { backgroundColor: colors.orange }]}>
                  <Icon name="news" size={20} color={colors.white} />
                </View>
                <Text style={styles.menuItemText}>Actualités</Text>
                <View style={styles.newsBadge}>
                  <Text style={styles.newsBadgeText}>5 nouvelles</Text>
                </View>
              </TouchableOpacity>
            </View>
            
            <View style={styles.menuDivider} />
            
            <View style={styles.menuSection}>
              <Text style={styles.menuSectionTitle}>Personnel</Text>
              
              <TouchableOpacity style={styles.menuItem} onPress={() => navigateTo('profile')}>
                <View style={[styles.menuIcon, { backgroundColor: colors.purple }]}>
                  <Icon name="person" size={20} color={colors.white} />
                </View>
                <Text style={styles.menuItemText}>Mon Profil</Text>
              </TouchableOpacity>
              
              <TouchableOpacity style={styles.menuItem} onPress={() => Alert.alert('Favoris', 'Vos vidéos favorites')}>
                <View style={[styles.menuIcon, { backgroundColor: colors.pink }]}>
                  <Icon name="heart" size={20} color={colors.white} />
                </View>
                <Text style={styles.menuItemText}>Mes Favoris</Text>
              </TouchableOpacity>
            </View>
            
            <View style={styles.menuDivider} />
            
            <View style={styles.menuSection}>
              <Text style={styles.menuSectionTitle}>Services</Text>
              
              <TouchableOpacity style={styles.menuItem} onPress={() => Alert.alert('Publicité', 'Programme publicitaire')}>
                <View style={[styles.menuIcon, { backgroundColor: colors.indigo }]}>
                  <Icon name="megaphone" size={20} color={colors.white} />
                </View>
                <Text style={styles.menuItemText}>Programme Pub</Text>
              </TouchableOpacity>
              
              <TouchableOpacity style={styles.menuItem} onPress={() => Alert.alert('Notifications', 'Paramètres notifications')}>
                <View style={[styles.menuIcon, { backgroundColor: colors.cyan }]}>
                  <Icon name="notification" size={20} color={colors.white} />
                </View>
                <Text style={styles.menuItemText}>Notifications</Text>
              </TouchableOpacity>
              
              <TouchableOpacity style={styles.menuItem} onPress={() => Alert.alert('Paramètres', 'Paramètres app')}>
                <View style={[styles.menuIcon, { backgroundColor: colors.gray }]}>
                  <Icon name="settings" size={20} color={colors.white} />
                </View>
                <Text style={styles.menuItemText}>Paramètres</Text>
              </TouchableOpacity>
              
              <TouchableOpacity style={styles.menuItem} onPress={() => Alert.alert('À propos', 'LCA TV Mobile v1.0')}>
                <View style={[styles.menuIcon, { backgroundColor: colors.emerald }]}>
                  <Icon name="info" size={20} color={colors.white} />
                </View>
                <Text style={styles.menuItemText}>À propos</Text>
              </TouchableOpacity>
            </View>
            
            {user && (
              <>
                <View style={styles.menuDivider} />
                <TouchableOpacity style={styles.logoutMenuItem} onPress={logout}>
                  <View style={[styles.menuIcon, { backgroundColor: colors.red }]}>
                    <Icon name="logout" size={20} color={colors.white} />
                  </View>
                  <Text style={[styles.menuItemText, { color: colors.red }]}>Déconnexion</Text>
                </TouchableOpacity>
              </>
            )}
          </ScrollView>
        </Animated.View>
      </View>
    </Modal>
  );

  // Enhanced Header
  const Header = () => (
    <View style={styles.header}>
      <TouchableOpacity style={styles.menuButton} onPress={toggleSidebar}>
        <ModernCard style={styles.menuButtonCard} color={colors.primaryLight}>
          <Icon name="menu" size={20} color={colors.white} />
        </ModernCard>
      </TouchableOpacity>
      
      <ModernCard style={styles.logoHeaderCard} color={colors.white}>
        <View style={styles.logoContainer}>
          <Text style={styles.logoText}>LCA</Text>
          <View style={styles.logoCircle}>
            <Text style={styles.logoSubText}>TV</Text>
          </View>
        </View>
      </ModernCard>
      
      <TouchableOpacity style={styles.notificationButton}>
        <ModernCard style={styles.notificationButtonCard} color={colors.orange}>
          <Icon name="notification" size={20} color={colors.white} />
          <View style={styles.notificationDot} />
        </ModernCard>
      </TouchableOpacity>
    </View>
  );

  // Enhanced Home Page with Rich Content
  const HomePage = () => (
    <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
      {/* Hero Banner */}
      <ModernCard style={styles.heroBanner}>
        <Image 
          source={{ uri: 'https://images.unsplash.com/photo-1651465531201-7e430660fd82' }}
          style={styles.heroBannerImage}
        />
        <View style={styles.heroBannerOverlay}>
          <View style={styles.heroBannerContent}>
            <Text style={styles.heroBannerTitle}>LCA TV en Direct</Text>
            <Text style={styles.heroBannerSubtitle}>Votre chaîne préférée 24/7</Text>
          </View>
          <TouchableOpacity style={styles.heroBannerButton} onPress={() => setCurrentPage('live')}>
            <Icon name="play" size={24} color={colors.white} />
          </TouchableOpacity>
        </View>
      </ModernCard>

      {/* Quick Stats */}
      <View style={styles.quickStats}>
        <ModernCard style={[styles.quickStatCard, { backgroundColor: colors.red }]}>
          <Icon name="live" size={24} color={colors.white} />
          <Text style={styles.quickStatNumber}>1,247</Text>
          <Text style={styles.quickStatLabel}>En direct</Text>
        </ModernCard>
        
        <ModernCard style={[styles.quickStatCard, { backgroundColor: colors.blue }]}>
          <Icon name="video" size={24} color={colors.white} />
          <Text style={styles.quickStatNumber}>850+</Text>
          <Text style={styles.quickStatLabel}>Replays</Text>
        </ModernCard>
        
        <ModernCard style={[styles.quickStatCard, { backgroundColor: colors.emerald }]}>
          <Icon name="news" size={24} color={colors.white} />
          <Text style={styles.quickStatNumber}>24</Text>
          <Text style={styles.quickStatLabel}>News/jour</Text>
        </ModernCard>
      </View>

      {/* Featured Videos Section */}
      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Icon name="fire" size={24} color={colors.orange} />
          <Text style={styles.sectionTitle}>Programmes Populaires</Text>
          <TouchableOpacity onPress={() => Alert.alert('Voir tout', 'Plus de programmes')}>
            <Text style={styles.seeAllText}>Voir tout</Text>
          </TouchableOpacity>
        </View>
        
        <ScrollView horizontal showsHorizontalScrollIndicator={false}>
          {videos.slice(0, 3).map((video, index) => (
            <ModernCard key={index} style={styles.videoCard}>
              <Image source={{ uri: video.thumbnail }} style={styles.videoThumbnail} />
              <View style={styles.videoOverlay}>
                <View style={styles.videoPlayButton}>
                  <Icon name="play" size={16} color={colors.white} />
                </View>
                <View style={[styles.videoCategoryBadge, { 
                  backgroundColor: video.category === 'actualites' ? colors.red : 
                                  video.category === 'debats' ? colors.purple :
                                  colors.orange
                }]}>
                  <Text style={styles.videoCategoryText}>
                    {video.category === 'actualites' ? 'ACTU' : 
                     video.category === 'debats' ? 'DÉBAT' : 'CULTURE'}
                  </Text>
                </View>
              </View>
              <View style={styles.videoInfo}>
                <Text style={styles.videoTitle} numberOfLines={2}>{video.title}</Text>
                <View style={styles.videoMeta}>
                  <View style={styles.videoStats}>
                    <Icon name="trending" size={12} color={colors.gray} />
                    <Text style={styles.videoStatsText}>{video.view_count} vues</Text>
                  </View>
                  <View style={styles.videoLikes}>
                    <Icon name="heart" size={12} color={colors.red} />
                    <Text style={styles.videoStatsText}>{video.like_count}</Text>
                  </View>
                </View>
              </View>
            </ModernCard>
          ))}
        </ScrollView>
      </View>

      {/* Categories Grid */}
      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Icon name="grid" size={24} color={colors.purple} />
          <Text style={styles.sectionTitle}>Nos Émissions</Text>
        </View>
        
        <View style={styles.categoriesGrid}>
          <ModernCard style={[styles.categoryCard, { backgroundColor: colors.red }]}>
            <Icon name="news" size={32} color={colors.white} />
            <Text style={styles.categoryTitle}>Journal</Text>
            <Text style={styles.categorySubtitle}>LCA TV</Text>
          </ModernCard>
          
          <ModernCard style={[styles.categoryCard, { backgroundColor: colors.purple }]}>
            <Icon name="megaphone" size={32} color={colors.white} />
            <Text style={styles.categoryTitle}>Franc</Text>
            <Text style={styles.categorySubtitle}>Parler</Text>
          </ModernCard>
          
          <ModernCard style={[styles.categoryCard, { backgroundColor: colors.pink }]}>
            <Icon name="heart" size={32} color={colors.white} />
            <Text style={styles.categoryTitle}>Questions</Text>
            <Text style={styles.categorySubtitle}>de Femmes</Text>
          </ModernCard>
          
          <ModernCard style={[styles.categoryCard, { backgroundColor: colors.orange }]}>
            <Icon name="star" size={32} color={colors.white} />
            <Text style={styles.categoryTitle}>Soleil</Text>
            <Text style={styles.categorySubtitle}>d'Afrique</Text>
          </ModernCard>
          
          <ModernCard style={[styles.categoryCard, { backgroundColor: colors.emerald }]}>
            <Icon name="trending" size={32} color={colors.white} />
            <Text style={styles.categoryTitle}>Sports</Text>
            <Text style={styles.categorySubtitle}>& Étalons</Text>
          </ModernCard>
          
          <ModernCard style={[styles.categoryCard, { backgroundColor: colors.cyan }]}>
            <Icon name="star" size={32} color={colors.white} />
            <Text style={styles.categoryTitle}>Jeunesse</Text>
            <Text style={styles.categorySubtitle}>Avenir</Text>
          </ModernCard>
        </View>
      </View>

      {/* News Section */}
      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Icon name="notification" size={24} color={colors.orange} />
          <Text style={styles.sectionTitle}>Actualités Flash</Text>
          <TouchableOpacity onPress={() => Alert.alert('Actualités', 'Plus d\'actualités')}>
            <Text style={styles.seeAllText}>Voir tout</Text>
          </TouchableOpacity>
        </View>
        
        {news.slice(0, 3).map((article, index) => (
          <ModernCard key={index} style={styles.newsCard}>
            <Image source={{ uri: article.image_url }} style={styles.newsImage} />
            <View style={styles.newsContent}>
              <View style={[styles.newsCategoryBadge, { 
                backgroundColor: article.category === 'national' ? colors.emerald : 
                                article.category === 'sport' ? colors.blue :
                                colors.purple
              }]}>
                <Text style={styles.newsCategoryText}>
                  {article.category.toUpperCase()}
                </Text>
              </View>
              <Text style={styles.newsTitle} numberOfLines={2}>{article.title}</Text>
              <Text style={styles.newsExcerpt} numberOfLines={2}>{article.excerpt}</Text>
              <View style={styles.newsFooter}>
                <View style={styles.newsTime}>
                  <Icon name="clock" size={14} color={colors.gray} />
                  <Text style={styles.newsTimeText}>Il y a {index + 1}h</Text>
                </View>
                <TouchableOpacity style={styles.newsShareButton}>
                  <Icon name="share" size={16} color={colors.gray} />
                </TouchableOpacity>
              </View>
            </View>
          </ModernCard>
        ))}
      </View>

      {/* Publicity Banner */}
      <ModernCard style={styles.publicityBanner}>
        <View style={styles.publicityContent}>
          <View style={styles.publicityIcon}>
            <Icon name="megaphone" size={32} color={colors.white} />
          </View>
          <View style={styles.publicityText}>
            <Text style={styles.publicityTitle}>Programme Publicitaire</Text>
            <Text style={styles.publicitySubtitle}>Boostez votre visibilité avec LCA TV</Text>
            <Text style={styles.publicityDetails}>À partir de 50,000 FCFA/mois</Text>
          </View>
          <TouchableOpacity style={styles.publicityButton}>
            <Icon name="arrow" size={20} color={colors.white} />
          </TouchableOpacity>
        </View>
      </ModernCard>
    </ScrollView>
  );

  // Autres pages simplifiées pour l'espace...
  const LoginPage = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    return (
      <ScrollView style={styles.content}>
        <View style={styles.authContainer}>
          <TouchableOpacity onPress={() => setCurrentPage('welcome')} style={styles.backButton}>
            <Icon name="back" size={24} color={colors.primary} />
            <Text style={styles.backText}>Retour</Text>
          </TouchableOpacity>
          
          <ModernCard style={styles.authCard}>
            <Text style={styles.authTitle}>Connexion</Text>
            <Text style={styles.authSubtitle}>Connectez-vous pour accéder à vos favoris</Text>
            
            <View style={styles.inputContainer}>
              <TextInput
                style={styles.input}
                placeholder="Email"
                value={email}
                onChangeText={setEmail}
                keyboardType="email-address"
                autoCapitalize="none"
              />
            </View>
            
            <View style={styles.inputContainer}>
              <TextInput
                style={styles.input}
                placeholder="Mot de passe"
                value={password}
                onChangeText={setPassword}
                secureTextEntry
              />
            </View>
            
            <TouchableOpacity 
              style={styles.authButton} 
              onPress={() => handleLogin(email, password)}
              disabled={loading}
            >
              <ModernCard style={styles.authButtonCard} color={colors.primaryLight}>
                {loading ? (
                  <ActivityIndicator color={colors.white} />
                ) : (
                  <Text style={styles.authButtonText}>Se connecter</Text>
                )}
              </ModernCard>
            </TouchableOpacity>
            
            <TouchableOpacity onPress={() => setCurrentPage('register')}>
              <Text style={styles.linkText}>Créer un compte</Text>
            </TouchableOpacity>
          </ModernCard>
        </View>
      </ScrollView>
    );
  };

  const renderCurrentPage = () => {
    switch (currentPage) {
      case 'welcome':
        return <WelcomePage />;
      case 'home':
        return <HomePage />;
      case 'login':
        return <LoginPage />;
      default:
        return <WelcomePage />;
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      {currentPage !== 'welcome' && <Header />}
      <View style={styles.pageContainer}>
        {renderCurrentPage()}
      </View>
      <Sidebar />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.lightGray,
  },
  
  // Modern Card Base Style
  modernCard: {
    borderRadius: 16,
    shadowColor: colors.cardShadow,
    shadowOffset: { width: 0, height: 4 },
    shadowRadius: 12,
    elevation: 5,
    marginVertical: 4,
  },
  
  // Welcome Page Styles
  welcomeContainer: {
    flex: 1,
  },
  welcomeBackground: {
    flex: 1,
    position: 'relative',
  },
  welcomeBackgroundImage: {
    position: 'absolute',
    width: '100%',
    height: '100%',
  },
  gradientOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(45,80,22,0.85)',
  },
  floatingElement1: {
    position: 'absolute',
    top: 100,
    right: 30,
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: colors.primaryLight,
    opacity: 0.3,
  },
  floatingElement2: {
    position: 'absolute',
    top: 300,
    left: 40,
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: colors.blue,
    opacity: 0.4,
  },
  floatingElement3: {
    position: 'absolute',
    bottom: 200,
    right: 50,
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: colors.orange,
    opacity: 0.2,
  },
  welcomeScroll: {
    flex: 1,
  },
  heroSection: {
    padding: 20,
    paddingTop: 60,
  },
  logoHeroCard: {
    alignSelf: 'center',
    padding: 20,
    marginBottom: 30,
  },
  logoHero: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  logoHeroText: {
    fontSize: 48,
    fontWeight: 'bold',
    color: colors.primary,
    marginRight: 12,
  },
  logoHeroCircle: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: colors.blue,
    justifyContent: 'center',
    alignItems: 'center',
  },
  logoHeroSubText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: colors.white,
  },
  welcomeTitle: {
    fontSize: 32,
    fontWeight: 'bold',
    color: colors.white,
    textAlign: 'center',
    marginBottom: 10,
  },
  welcomeSubtitle: {
    fontSize: 18,
    color: colors.white,
    opacity: 0.9,
    textAlign: 'center',
    marginBottom: 15,
  },
  welcomeDescription: {
    fontSize: 16,
    color: colors.white,
    opacity: 0.8,
    textAlign: 'center',
    lineHeight: 24,
    marginBottom: 30,
  },
  featuresPreview: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 30,
  },
  featureCard: {
    width: (screenWidth - 60) / 3,
    padding: 15,
    alignItems: 'center',
  },
  featureCardTitle: {
    color: colors.white,
    fontSize: 14,
    fontWeight: 'bold',
    marginTop: 8,
  },
  featureCardDesc: {
    color: colors.white,
    fontSize: 11,
    opacity: 0.8,
    marginTop: 4,
    textAlign: 'center',
  },
  trendingSection: {
    padding: 20,
    marginBottom: 30,
  },
  trendingSectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 15,
  },
  trendingSectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: colors.black,
    marginLeft: 10,
  },
  trendingShows: {
    flexDirection: 'row',
  },
  trendingShowCard: {
    padding: 15,
    marginRight: 15,
    minWidth: 120,
    alignItems: 'center',
  },
  trendingShowTitle: {
    color: colors.white,
    fontSize: 14,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  trendingShowTime: {
    color: colors.white,
    fontSize: 12,
    opacity: 0.8,
    marginTop: 4,
  },
  welcomeActions: {
    marginBottom: 30,
  },
  primaryActionButton: {
    marginBottom: 15,
  },
  primaryActionCard: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 18,
  },
  primaryActionText: {
    color: colors.white,
    fontSize: 18,
    fontWeight: 'bold',
    marginLeft: 10,
  },
  secondaryActionButton: {
    marginBottom: 15,
  },
  secondaryActionCard: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 16,
  },
  secondaryActionText: {
    color: colors.white,
    fontSize: 16,
    fontWeight: 'bold',
    marginLeft: 10,
  },
  ghostActionButton: {
    marginBottom: 30,
  },
  ghostActionCard: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 14,
  },
  ghostActionText: {
    color: colors.white,
    fontSize: 14,
    marginLeft: 8,
  },
  statsSection: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 30,
  },
  statCard: {
    width: (screenWidth - 60) / 3,
    padding: 20,
    alignItems: 'center',
  },
  statNumber: {
    fontSize: 20,
    fontWeight: 'bold',
    color: colors.white,
    marginTop: 8,
  },
  statLabel: {
    fontSize: 12,
    color: colors.white,
    opacity: 0.8,
    marginTop: 4,
    textAlign: 'center',
  },
  partnershipSection: {
    padding: 20,
    marginBottom: 20,
  },
  partnershipTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: colors.black,
    textAlign: 'center',
    marginBottom: 15,
  },
  partnersGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  partnerCard: {
    width: (screenWidth - 80) / 2,
    padding: 15,
    alignItems: 'center',
    marginBottom: 10,
    borderRadius: 12,
  },
  partnerText: {
    color: colors.white,
    fontSize: 14,
    fontWeight: 'bold',
  },

  // Enhanced Sidebar Styles
  sidebarOverlay: {
    flex: 1,
    flexDirection: 'row',
  },
  sidebarBackdrop: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.6)',
  },
  sidebar: {
    width: screenWidth * 0.85,
    backgroundColor: colors.white,
    shadowColor: colors.cardShadow,
    shadowOffset: { width: 4, height: 0 },
    shadowOpacity: 0.3,
    shadowRadius: 15,
    elevation: 15,
  },
  sidebarHeader: {
    padding: 20,
    paddingTop: 50,
  },
  sidebarUserCard: {
    padding: 20,
  },
  sidebarUserInfo: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  sidebarAvatar: {
    width: 50,
    height: 50,
    borderRadius: 25,
    backgroundColor: colors.white,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 15,
  },
  sidebarAvatarText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: colors.primaryLight,
  },
  sidebarUserDetails: {
    flex: 1,
  },
  sidebarUserName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: colors.white,
    marginBottom: 4,
  },
  sidebarUserEmail: {
    fontSize: 14,
    color: colors.white,
    opacity: 0.8,
    marginBottom: 8,
  },
  pointsBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.white,
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
    alignSelf: 'flex-start',
  },
  sidebarUserPoints: {
    fontSize: 12,
    color: colors.primaryLight,
    fontWeight: 'bold',
    marginLeft: 4,
  },
  sidebarGuestCard: {
    padding: 20,
    alignItems: 'center',
  },
  sidebarGuestInfo: {
    alignItems: 'center',
  },
  sidebarGuestAvatar: {
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: colors.gray,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 10,
  },
  sidebarGuestText: {
    fontSize: 18,
    color: colors.white,
    marginBottom: 15,
  },
  sidebarLoginBtn: {
    backgroundColor: colors.white,
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 20,
  },
  sidebarLoginText: {
    color: colors.darkGray,
    fontWeight: 'bold',
  },
  sidebarMenu: {
    flex: 1,
    paddingHorizontal: 10,
  },
  menuSection: {
    marginBottom: 20,
  },
  menuSectionTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    color: colors.gray,
    marginLeft: 15,
    marginBottom: 10,
    textTransform: 'uppercase',
  },
  menuItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 15,
    paddingVertical: 12,
    marginVertical: 2,
    borderRadius: 12,
    backgroundColor: colors.lightGray,
  },
  menuIcon: {
    width: 36,
    height: 36,
    borderRadius: 18,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  menuItemText: {
    fontSize: 16,
    color: colors.black,
    fontWeight: '500',
    flex: 1,
  },
  menuArrow: {
    opacity: 0.5,
  },
  menuBadge: {
    backgroundColor: colors.blue,
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 10,
  },
  menuBadgeText: {
    color: colors.white,
    fontSize: 10,
    fontWeight: 'bold',
  },
  liveBadge: {
    backgroundColor: colors.red,
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 10,
  },
  liveBadgeText: {
    color: colors.white,
    fontSize: 10,
    fontWeight: 'bold',
  },
  newsBadge: {
    backgroundColor: colors.orange,
    paddingHorizontal: 8,
    paddingVertical: 2,
    borderRadius: 10,
  },
  newsBadgeText: {
    color: colors.white,
    fontSize: 10,
    fontWeight: 'bold',
  },
  menuDivider: {
    height: 1,
    backgroundColor: colors.lightGray,
    marginVertical: 10,
    marginHorizontal: 15,
  },
  logoutMenuItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 15,
    paddingVertical: 12,
    marginVertical: 2,
    borderRadius: 12,
    backgroundColor: colors.lightGray,
  },

  // Enhanced Header Styles
  header: {
    backgroundColor: colors.primary,
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 15,
    justifyContent: 'space-between',
  },
  menuButton: {},
  menuButtonCard: {
    padding: 8,
  },
  logoHeaderCard: {
    paddingHorizontal: 15,
    paddingVertical: 8,
  },
  logoContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  logoText: {
    fontSize: 20,
    fontWeight: 'bold',
    color: colors.primary,
    marginRight: 6,
  },
  logoCircle: {
    width: 20,
    height: 20,
    borderRadius: 10,
    backgroundColor: colors.blue,
    justifyContent: 'center',
    alignItems: 'center',
  },
  logoSubText: {
    fontSize: 8,
    fontWeight: 'bold',
    color: colors.white,
  },
  notificationButton: {},
  notificationButtonCard: {
    padding: 8,
    position: 'relative',
  },
  notificationDot: {
    position: 'absolute',
    top: 2,
    right: 2,
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: colors.red,
  },

  // Enhanced Home Page Styles
  pageContainer: {
    flex: 1,
  },
  content: {
    flex: 1,
  },
  heroBanner: {
    height: 200,
    margin: 20,
    overflow: 'hidden',
    position: 'relative',
  },
  heroBannerImage: {
    width: '100%',
    height: '100%',
  },
  heroBannerOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0,0,0,0.4)',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 20,
  },
  heroBannerContent: {},
  heroBannerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: colors.white,
    marginBottom: 5,
  },
  heroBannerSubtitle: {
    fontSize: 16,
    color: colors.white,
    opacity: 0.9,
  },
  heroBannerButton: {
    backgroundColor: colors.primaryLight,
    padding: 15,
    borderRadius: 30,
  },
  quickStats: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    marginBottom: 20,
  },
  quickStatCard: {
    width: (screenWidth - 60) / 3,
    padding: 15,
    alignItems: 'center',
  },
  quickStatNumber: {
    fontSize: 18,
    fontWeight: 'bold',
    color: colors.white,
    marginTop: 5,
  },
  quickStatLabel: {
    fontSize: 12,
    color: colors.white,
    opacity: 0.8,
    marginTop: 2,
  },
  section: {
    marginBottom: 25,
    paddingHorizontal: 20,
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 15,
  },
  sectionTitle: {
    fontSize: 20,
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
  videoCard: {
    width: 220,
    marginRight: 15,
    overflow: 'hidden',
  },
  videoThumbnail: {
    width: '100%',
    height: 130,
  },
  videoOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 130,
    flexDirection: 'row',
    justifyContent: 'space-between',
    padding: 10,
  },
  videoPlayButton: {
    backgroundColor: 'rgba(0,0,0,0.7)',
    padding: 8,
    borderRadius: 20,
    alignSelf: 'flex-end',
  },
  videoCategoryBadge: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 8,
    alignSelf: 'flex-start',
  },
  videoCategoryText: {
    color: colors.white,
    fontSize: 10,
    fontWeight: 'bold',
  },
  videoInfo: {
    padding: 15,
  },
  videoTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: colors.black,
    marginBottom: 8,
    lineHeight: 22,
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
  videoLikes: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  categoriesGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  categoryCard: {
    width: (screenWidth - 60) / 2,
    padding: 20,
    alignItems: 'center',
    marginBottom: 15,
  },
  categoryTitle: {
    color: colors.white,
    fontSize: 16,
    fontWeight: 'bold',
    marginTop: 10,
  },
  categorySubtitle: {
    color: colors.white,
    fontSize: 14,
    opacity: 0.8,
    marginTop: 2,
  },
  newsCard: {
    flexDirection: 'row',
    marginBottom: 15,
    overflow: 'hidden',
  },
  newsImage: {
    width: 100,
    height: 100,
  },
  newsContent: {
    flex: 1,
    padding: 15,
    position: 'relative',
  },
  newsCategoryBadge: {
    position: 'absolute',
    top: 10,
    right: 10,
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 8,
  },
  newsCategoryText: {
    color: colors.white,
    fontSize: 10,
    fontWeight: 'bold',
  },
  newsTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: colors.black,
    marginBottom: 8,
    marginRight: 60,
  },
  newsExcerpt: {
    fontSize: 14,
    color: colors.gray,
    marginBottom: 10,
    lineHeight: 20,
  },
  newsFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  newsTime: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  newsTimeText: {
    fontSize: 12,
    color: colors.gray,
    marginLeft: 4,
  },
  newsShareButton: {
    padding: 5,
  },
  publicityBanner: {
    margin: 20,
    backgroundColor: colors.indigo,
    overflow: 'hidden',
  },
  publicityContent: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 20,
  },
  publicityIcon: {
    marginRight: 15,
  },
  publicityText: {
    flex: 1,
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
    marginBottom: 3,
  },
  publicityDetails: {
    fontSize: 12,
    color: colors.yellow,
    fontWeight: 'bold',
  },
  publicityButton: {
    backgroundColor: colors.white,
    padding: 12,
    borderRadius: 25,
  },

  // Auth Styles
  authContainer: {
    padding: 20,
  },
  backButton: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 30,
  },
  backText: {
    fontSize: 16,
    color: colors.primary,
    marginLeft: 8,
  },
  authCard: {
    padding: 30,
  },
  authTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: colors.black,
    textAlign: 'center',
    marginBottom: 10,
  },
  authSubtitle: {
    fontSize: 16,
    color: colors.gray,
    textAlign: 'center',
    marginBottom: 30,
  },
  inputContainer: {
    marginBottom: 20,
  },
  input: {
    backgroundColor: colors.lightGray,
    borderRadius: 12,
    paddingHorizontal: 15,
    paddingVertical: 15,
    fontSize: 16,
    color: colors.black,
    borderWidth: 1,
    borderColor: colors.lightGray,
  },
  authButton: {
    marginTop: 10,
    marginBottom: 20,
  },
  authButtonCard: {
    padding: 18,
    alignItems: 'center',
  },
  authButtonText: {
    color: colors.white,
    fontSize: 18,
    fontWeight: 'bold',
  },
  linkText: {
    textAlign: 'center',
    color: colors.primaryLight,
    fontSize: 16,
    fontWeight: 'bold',
  },
});