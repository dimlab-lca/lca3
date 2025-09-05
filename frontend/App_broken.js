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
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

const { width: screenWidth, height: screenHeight } = Dimensions.get('window');

// LCA TV Colors - Modern & Vibrant
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
  accent: '#fbbf24',
};

export default function App() {
  const [currentPage, setCurrentPage] = useState('welcome');
  const [user, setUser] = useState(null);
  const [videos, setVideos] = useState([]);
  const [news, setNews] = useState([]);
  const [categories, setCategories] = useState([]);
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
      await loadCategories();
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
      // Fallback data
      setVideos([
        {
          id: 'eSApphrRKWg',
          title: 'Journal LCA TV - Édition du Soir',
          thumbnail: 'https://i.ytimg.com/vi/eSApphrRKWg/hqdefault.jpg',
          view_count: '15K',
          duration: '25:30'
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
          category: 'national'
        }
      ]);
    }
  };

  const loadCategories = async () => {
    try {
      const response = await fetch('https://lcatv-mobile.preview.emergentagent.com/api/categories');
      const data = await response.json();
      setCategories(data.categories || []);
    } catch (error) {
      console.error('Error loading categories:', error);
      setCategories([
        { id: 'actualites', name: '📰 Actualités' },
        { id: 'sport', name: '⚽ Sports' },
        { id: 'culture', name: '🌍 Culture' },
        { id: 'debats', name: '🗣️ Débats' }
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
    toggleSidebar();
  };

  const logout = async () => {
    await AsyncStorage.removeItem('user');
    await AsyncStorage.removeItem('access_token');
    setUser(null);
    setCurrentPage('welcome');
    toggleSidebar();
  };

  // Icon Component
  const Icon = ({ name, size = 24, color = colors.gray }) => {
    const icons = {
      home: '🏠', radio: '📡', play: '▶️', star: '⭐', grid: '⚏',
      newspaper: '📰', person: '👤', heart: '❤️', megaphone: '📢',
      arrow: '→', back: '←', live: '🔴', tv: '📺', video: '🎥',
      news: '📰', menu: '☰', close: '✕', logout: '🚪', settings: '⚙️',
      info: 'ℹ️', help: '❓', notification: '🔔', fire: '🔥', africa: '🌍'
    };
    
    return (
      <Text style={{ fontSize: size, color }}>{icons[name] || '•'}</Text>
    );
  };

  // Ultra Modern Welcome Page
  const WelcomePage = () => (
    <View style={styles.welcomeContainer}>
      <StatusBar barStyle="light-content" backgroundColor={colors.primary} />
      
      <View style={styles.welcomeBackground}>
        <View style={styles.gradientOverlay} />
        
        {/* Hero Section */}
        <ScrollView contentContainerStyle={styles.welcomeContent}>
          <View style={styles.heroSection}>
            <View style={styles.logoHero}>
              <Text style={styles.logoHeroText}>LCA</Text>
              <View style={styles.logoHeroCircle}>
                <Text style={styles.logoHeroSubText}>TV</Text>
              </View>
            </View>
            
            <Text style={styles.welcomeTitle}>Bienvenue sur LCA TV</Text>
            <Text style={styles.welcomeSubtitle}>La Chaîne Africaine de télévision</Text>
            <Text style={styles.welcomeDescription}>
              Découvrez l'actualité, le divertissement et la culture du Burkina Faso 
              en direct et en replay avec une qualité exceptionnelle 📺✨
            </Text>
          </View>

          {/* Enhanced Features Preview */}
          <View style={styles.featuresGrid}>
            <View style={styles.featureCard}>
              <View style={styles.featureIcon}>
                <Icon name="live" size={32} color={colors.red} />
              </View>
              <Text style={styles.featureTitle}>Direct 24/7</Text>
              <Text style={styles.featureDescription}>Suivez nos programmes en temps réel</Text>
            </View>

            <View style={styles.featureCard}>
              <View style={styles.featureIcon}>
                <Icon name="play" size={32} color={colors.blue} />
              </View>
              <Text style={styles.featureTitle}>Replays HD</Text>
              <Text style={styles.featureDescription}>Rattrapage de toutes vos émissions</Text>
            </View>

            <View style={styles.featureCard}>
              <View style={styles.featureIcon}>
                <Icon name="newspaper" size={32} color={colors.orange} />
              </View>
              <Text style={styles.featureTitle}>Actualités</Text>
              <Text style={styles.featureDescription}>Info nationale et internationale</Text>
            </View>

            <View style={styles.featureCard}>
              <View style={styles.featureIcon}>
                <Icon name="africa" size={32} color={colors.emerald} />
              </View>
              <Text style={styles.featureTitle}>Culture</Text>
              <Text style={styles.featureDescription}>Patrimoine burkinabè authentique</Text>
            </View>
          </View>

          {/* Action Buttons */}
          <View style={styles.welcomeActions}>
            <TouchableOpacity 
              style={styles.primaryActionButton}
              onPress={() => setCurrentPage('login')}
            >
              <Text style={styles.primaryActionText}>Se connecter</Text>
              <Icon name="arrow" size={20} color={colors.white} />
            </TouchableOpacity>
            
            <TouchableOpacity 
              style={styles.secondaryActionButton}
              onPress={() => setCurrentPage('register')}
            >
              <Text style={styles.secondaryActionText}>Créer un compte</Text>
            </TouchableOpacity>
            
            <TouchableOpacity 
              style={styles.ghostActionButton}
              onPress={() => setCurrentPage('home')}
            >
              <Text style={styles.ghostActionText}>Continuer sans compte</Text>
            </TouchableOpacity>
          </View>

          {/* Stats Section */}
          <View style={styles.statsSection}>
            <View style={styles.statCard}>
              <Icon name="fire" size={28} color={colors.accent} />
              <Text style={styles.statNumber}>500K+</Text>
              <Text style={styles.statLabel}>Téléspectateurs</Text>
            </View>
            <View style={styles.statCard}>
              <Icon name="live" size={28} color={colors.red} />
              <Text style={styles.statNumber}>24/7</Text>
              <Text style={styles.statLabel}>Diffusion</Text>
            </View>
            <View style={styles.statCard}>
              <Icon name="africa" size={28} color={colors.emerald} />
              <Text style={styles.statNumber}>100%</Text>
              <Text style={styles.statLabel}>Burkinabè</Text>
            </View>
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
          <View style={styles.sidebarHeader}>
            {user ? (
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
                    <Icon name="star" size={14} color={colors.accent} />
                    <Text style={styles.sidebarUserPoints}>{user.points || 0} points</Text>
                  </View>
                </View>
              </View>
            ) : (
              <View style={styles.sidebarGuestInfo}>
                <View style={styles.sidebarGuestAvatar}>
                  <Icon name="person" size={32} color={colors.white} />
                </View>
                <Text style={styles.sidebarGuestText}>Invité</Text>
                <TouchableOpacity 
                  style={styles.sidebarLoginBtn}
                  onPress={() => navigateTo('login')}
                >
                  <Text style={styles.sidebarLoginText}>Se connecter</Text>
                </TouchableOpacity>
              </View>
            )}
          </View>

          <ScrollView style={styles.sidebarMenu}>
            <TouchableOpacity style={styles.menuItem} onPress={() => navigateTo('home')}>
              <Icon name="home" size={24} color={colors.primaryLight} />
              <Text style={styles.menuItemText}>Accueil</Text>
            </TouchableOpacity>
            
            <TouchableOpacity style={styles.menuItem} onPress={() => navigateTo('live')}>
              <Icon name="radio" size={24} color={colors.red} />
              <Text style={styles.menuItemText}>Direct</Text>
              <View style={styles.liveBadge}>
                <Text style={styles.liveBadgeText}>LIVE</Text>
              </View>
            </TouchableOpacity>
            
            <TouchableOpacity style={styles.menuItem} onPress={() => Alert.alert('Replays', 'Accédez aux replays')}>
              <Icon name="play" size={24} color={colors.blue} />
              <Text style={styles.menuItemText}>Replays</Text>
            </TouchableOpacity>
            
            <TouchableOpacity style={styles.menuItem} onPress={() => Alert.alert('Actualités', 'Toute l\'info')}>
              <Icon name="news" size={24} color={colors.orange} />
              <Text style={styles.menuItemText}>Actualités</Text>
            </TouchableOpacity>
            
            <TouchableOpacity style={styles.menuItem} onPress={() => navigateTo('profile')}>
              <Icon name="person" size={24} color={colors.purple} />
              <Text style={styles.menuItemText}>Profil</Text>
            </TouchableOpacity>
            
            <View style={styles.menuDivider} />
            
            <TouchableOpacity style={styles.menuItem} onPress={() => Alert.alert('Favoris', 'Vos vidéos favorites')}>
              <Icon name="heart" size={24} color={colors.red} />
              <Text style={styles.menuItemText}>Mes Favoris</Text>
            </TouchableOpacity>
            
            <TouchableOpacity style={styles.menuItem} onPress={() => Alert.alert('Programme Publicitaire', 'Boostez votre visibilité avec LCA TV')}>
              <Icon name="megaphone" size={24} color={colors.darkBlue} />
              <Text style={styles.menuItemText}>Programme Pub</Text>
            </TouchableOpacity>
            
            {user && (
              <>
                <View style={styles.menuDivider} />
                <TouchableOpacity style={styles.menuItem} onPress={logout}>
                  <Icon name="logout" size={24} color={colors.red} />
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
        <Icon name="menu" size={24} color={colors.white} />
      </TouchableOpacity>
      
      <View style={styles.logoContainer}>
        <Text style={styles.logoText}>LCA</Text>
        <View style={styles.logoCircle}>
          <Text style={styles.logoSubText}>TV</Text>
        </View>
      </View>
      
      <TouchableOpacity style={styles.notificationButton}>
        <Icon name="notification" size={24} color={colors.white} />
        <View style={styles.notificationDot} />
      </TouchableOpacity>
    </View>
  );

  // Ultra Enhanced Home Page
  const HomePage = () => (
    <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
      {/* Hero Live Section */}
      <View style={styles.heroLiveSection}>
        <View style={styles.heroLiveOverlay}>
          <View style={styles.liveIndicator}>
            <Text style={styles.liveText}>🔴 EN DIRECT</Text>
          </View>
          <Text style={styles.heroLiveTitle}>LCA TV - Direct</Text>
          <Text style={styles.heroLiveSubtitle}>Journal du soir - Édition spéciale</Text>
          <TouchableOpacity style={styles.heroPlayButton} onPress={() => setCurrentPage('live')}>
            <Icon name="play" size={40} color={colors.white} />
          </TouchableOpacity>
          <Text style={styles.viewerCount}>🔴 1,247 spectateurs connectés</Text>
        </View>
      </View>

      {/* Quick Actions */}
      <View style={styles.quickActionsBar}>
        <TouchableOpacity style={styles.quickAction} onPress={() => setCurrentPage('live')}>
          <Icon name="live" size={24} color={colors.red} />
          <Text style={styles.quickActionText}>Direct</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.quickAction}>
          <Icon name="play" size={24} color={colors.blue} />
          <Text style={styles.quickActionText}>Replays</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.quickAction}>
          <Icon name="news" size={24} color={colors.orange} />
          <Text style={styles.quickActionText}>Actualités</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.quickAction}>
          <Icon name="tv" size={24} color={colors.purple} />
          <Text style={styles.quickActionText}>Programmes</Text>
        </TouchableOpacity>
      </View>

      {/* Featured Videos */}
      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Icon name="star" size={24} color={colors.accent} />
          <Text style={styles.sectionTitle}>Programmes populaires</Text>
          <TouchableOpacity>
            <Text style={styles.seeAllText}>Voir tout</Text>
          </TouchableOpacity>
        </View>
        
        <ScrollView horizontal showsHorizontalScrollIndicator={false}>
          {videos.slice(0, 6).map((video, index) => (
            <TouchableOpacity key={index} style={styles.modernVideoCard}>
              <Image source={{ uri: video.thumbnail }} style={styles.modernVideoThumbnail} />
              <View style={styles.videoPlayOverlay}>
                <Icon name="play" size={20} color={colors.white} />
              </View>
              <View style={styles.modernVideoInfo}>
                <Text style={styles.modernVideoTitle} numberOfLines={2}>{video.title}</Text>
                <View style={styles.videoMetaRow}>
                  <Text style={styles.videoStats}>{video.view_count} vues</Text>
                  <Text style={styles.videoDuration}>{video.duration}</Text>
                </View>
              </View>
            </TouchableOpacity>
          ))}
        </ScrollView>
      </View>

      {/* Categories Grid */}
      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Icon name="grid" size={24} color={colors.primaryLight} />
          <Text style={styles.sectionTitle}>Nos émissions</Text>
        </View>
        <View style={styles.categoriesGrid}>
          {categories.slice(0, 8).map((category, index) => (
            <TouchableOpacity key={index} style={styles.categoryCard}>
              <View style={styles.categoryIcon}>
                <Text style={styles.categoryEmoji}>{category.name.charAt(0)}</Text>
              </View>
              <Text style={styles.categoryName}>{category.name.substring(2)}</Text>
            </TouchableOpacity>
          ))}
        </View>
      </View>

      {/* News Section */}
      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Icon name="newspaper" size={24} color={colors.orange} />
          <Text style={styles.sectionTitle}>Actualités Flash</Text>
          <TouchableOpacity>
            <Text style={styles.seeAllText}>Voir tout</Text>
          </TouchableOpacity>
        </View>
        
        {news.slice(0, 3).map((article, index) => (
          <TouchableOpacity key={index} style={styles.newsCard}>
            <View style={styles.newsContent}>
              <View style={styles.newsHeader}>
                <Text style={styles.newsCategory}>{article.category?.toUpperCase()}</Text>
                <Text style={styles.newsTime}>Il y a 2h</Text>
              </View>
              <Text style={styles.newsTitle} numberOfLines={2}>{article.title}</Text>
              <Text style={styles.newsExcerpt} numberOfLines={2}>{article.excerpt}</Text>
            </View>
          </TouchableOpacity>
        ))}
      </View>

      {/* Enhanced Publicity Banner */}
      <View style={styles.section}>
        <TouchableOpacity style={styles.modernPublicityBanner}>
          <View style={styles.publicityContent}>
            <Icon name="megaphone" size={32} color={colors.white} />
            <View style={styles.publicityText}>
              <Text style={styles.publicityTitle}>Programme Publicitaire</Text>
              <Text style={styles.publicitySubtitle}>Développez votre business avec LCA TV</Text>
              <Text style={styles.publicityDescription}>Spots TV • Sponsoring • Digital</Text>
            </View>
            <Icon name="arrow" size={24} color={colors.white} />
          </View>
        </TouchableOpacity>
      </View>

      {/* Statistics Grid */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>LCA TV en chiffres</Text>
        <View style={styles.statsGrid}>
          <View style={styles.statItem}>
            <Icon name="fire" size={32} color={colors.red} />
            <Text style={styles.statValue}>500K+</Text>
            <Text style={styles.statLabel}>Téléspectateurs</Text>
          </View>
          <View style={styles.statItem}>
            <Icon name="tv" size={32} color={colors.blue} />
            <Text style={styles.statValue}>24/7</Text>
            <Text style={styles.statLabel}>Diffusion</Text>
          </View>
          <View style={styles.statItem}>
            <Icon name="play" size={32} color={colors.emerald} />
            <Text style={styles.statValue}>1000+</Text>
            <Text style={styles.statLabel}>Vidéos</Text>
          </View>
          <View style={styles.statItem}>
            <Icon name="star" size={32} color={colors.accent} />
            <Text style={styles.statValue}>4.8/5</Text>
            <Text style={styles.statLabel}>Satisfaction</Text>
          </View>
        </View>
      </View>
    </ScrollView>
  );

  // Auth pages remain the same but simplified
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
          
          <View style={styles.authHeader}>
            <Text style={styles.authTitle}>Connexion</Text>
            <Text style={styles.authSubtitle}>Connectez-vous pour accéder à vos favoris et points de fidélité</Text>
          </View>
          
          <View style={styles.inputContainer}>
            <TextInput
              style={styles.input}
              placeholder="Adresse email"
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
            {loading ? (
              <ActivityIndicator color={colors.white} />
            ) : (
              <>
                <Text style={styles.authButtonText}>Se connecter</Text>
                <Icon name="arrow" size={20} color={colors.white} />
              </>
            )}
          </TouchableOpacity>
          
          <TouchableOpacity onPress={() => setCurrentPage('register')}>
            <Text style={styles.linkText}>Pas encore de compte ? Créer un compte</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    );
  };

  const RegisterPage = () => {
    const [formData, setFormData] = useState({
      nom: '', prenom: '', email: '', telephone: '', password: '', confirm_password: '',
    });

    const updateFormData = (field, value) => {
      setFormData(prev => ({ ...prev, [field]: value }));
    };

    return (
      <ScrollView style={styles.content}>
        <View style={styles.authContainer}>
          <TouchableOpacity onPress={() => setCurrentPage('welcome')} style={styles.backButton}>
            <Icon name="back" size={24} color={colors.primary} />
            <Text style={styles.backText}>Retour</Text>
          </TouchableOpacity>
          
          <View style={styles.authHeader}>
            <Text style={styles.authTitle}>Inscription</Text>
            <Text style={styles.authSubtitle}>Créez votre compte LCA TV et bénéficiez de 100 points de bienvenue</Text>
          </View>
          
          <View style={styles.inputContainer}>
            <TextInput style={styles.input} placeholder="Nom de famille" value={formData.nom} onChangeText={(text) => updateFormData('nom', text)} />
          </View>
          <View style={styles.inputContainer}>
            <TextInput style={styles.input} placeholder="Prénom" value={formData.prenom} onChangeText={(text) => updateFormData('prenom', text)} />
          </View>
          <View style={styles.inputContainer}>
            <TextInput style={styles.input} placeholder="Adresse email" value={formData.email} onChangeText={(text) => updateFormData('email', text)} keyboardType="email-address" autoCapitalize="none" />
          </View>
          <View style={styles.inputContainer}>
            <TextInput style={styles.input} placeholder="Téléphone (+226XXXXXXXX)" value={formData.telephone} onChangeText={(text) => updateFormData('telephone', text)} keyboardType="phone-pad" />
          </View>
          <View style={styles.inputContainer}>
            <TextInput style={styles.input} placeholder="Mot de passe" value={formData.password} onChangeText={(text) => updateFormData('password', text)} secureTextEntry />
          </View>
          <View style={styles.inputContainer}>
            <TextInput style={styles.input} placeholder="Confirmer le mot de passe" value={formData.confirm_password} onChangeText={(text) => updateFormData('confirm_password', text)} secureTextEntry />
          </View>
          
          <TouchableOpacity 
            style={styles.authButton} 
            onPress={() => handleRegister({ ...formData, accept_cgu: true, newsletter: false })}
            disabled={loading}
          >
            {loading ? <ActivityIndicator color={colors.white} /> : (
              <>
                <Text style={styles.authButtonText}>Créer mon compte</Text>
                <Icon name="arrow" size={20} color={colors.white} />
              </>
            )}
          </TouchableOpacity>

          <TouchableOpacity onPress={() => setCurrentPage('login')}>
            <Text style={styles.linkText}>Déjà un compte ? Se connecter</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    );
  };

  // Enhanced Live Page
  const LivePage = () => (
    <ScrollView style={styles.content}>
      <View style={styles.livePageContainer}>
        <Text style={styles.pageTitle}>LCA TV - Direct</Text>
        
        <View style={styles.livePlayerContainer}>
          <View style={styles.livePlayerOverlay}>
            <TouchableOpacity style={styles.livePlayButton}>
              <Icon name="play" size={60} color={colors.white} />
            </TouchableOpacity>
            <Text style={styles.livePlayerText}>Regarder en direct</Text>
            <View style={styles.liveIndicatorLarge}>
              <Text style={styles.liveTextLarge}>🔴 EN DIRECT</Text>
            </View>
          </View>
        </View>
        
        <View style={styles.liveInfo}>
          <Text style={styles.liveInfoTitle}>Journal du soir - Édition spéciale</Text>
          <Text style={styles.liveInfoDescription}>
            Suivez en direct l'actualité du Burkina Faso et de l'Afrique de l'Ouest. 
            Au programme ce soir : politique, économie, sport et culture.
          </Text>
          <Text style={styles.viewerCount}>🔴 1,247 spectateurs connectés</Text>
        </View>
      </View>
    </ScrollView>
  );

  // Enhanced Profile Page
  const ProfilePage = () => (
    <ScrollView style={styles.content}>
      {user ? (
        <View style={styles.profileContainer}>
          <View style={styles.profileHeader}>
            <View style={styles.profileAvatar}>
              <Text style={styles.profileAvatarText}>{user.nom.charAt(0)}{user.prenom.charAt(0)}</Text>
            </View>
            <Text style={styles.profileName}>{user.prenom} {user.nom}</Text>
            <Text style={styles.profileEmail}>{user.email}</Text>
            <View style={styles.profilePointsBadge}>
              <Icon name="star" size={20} color={colors.accent} />
              <Text style={styles.profilePoints}>{user.points || 0} points</Text>
            </View>
          </View>
          
          <View style={styles.profileStats}>
            <View style={styles.profileStatItem}>
              <Icon name="heart" size={24} color={colors.red} />
              <Text style={styles.profileStatValue}>{user.favorites?.length || 0}</Text>
              <Text style={styles.profileStatLabel}>Favoris</Text>
            </View>
            <View style={styles.profileStatItem}>
              <Icon name="play" size={24} color={colors.blue} />
              <Text style={styles.profileStatValue}>23</Text>
              <Text style={styles.profileStatLabel}>Vidéos vues</Text>
            </View>
            <View style={styles.profileStatItem}>
              <Icon name="star" size={24} color={colors.accent} />
              <Text style={styles.profileStatValue}>{user.points || 0}</Text>
              <Text style={styles.profileStatLabel}>Points</Text>
            </View>
          </View>
        </View>
      ) : (
        <View style={styles.authPrompt}>
          <Icon name="person" size={80} color={colors.gray} />
          <Text style={styles.authPromptTitle}>Connectez-vous</Text>
          <Text style={styles.authPromptText}>
            Accédez à votre profil, vos favoris et vos points de fidélité
          </Text>
          <TouchableOpacity style={styles.authButton} onPress={() => setCurrentPage('login')}>
            <Text style={styles.authButtonText}>Se connecter</Text>
            <Icon name="arrow" size={20} color={colors.white} />
          </TouchableOpacity>
        </View>
      )}
    </ScrollView>
  );

  const renderCurrentPage = () => {
    switch (currentPage) {
      case 'welcome': return <WelcomePage />;
      case 'home': return <HomePage />;
      case 'login': return <LoginPage />;
      case 'register': return <RegisterPage />;
      case 'live': return <LivePage />;
      case 'profile': return <ProfilePage />;
      default: return <WelcomePage />;
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

// Ultra Modern Styles
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.white,
  },
  
  // Welcome Page Styles
  welcomeContainer: { flex: 1 },
  welcomeBackground: {
    flex: 1,
    backgroundColor: colors.primary,
    position: 'relative',
  },
  gradientOverlay: {
    position: 'absolute',
    top: 0, left: 0, right: 0, bottom: 0,
    backgroundColor: 'rgba(45,80,22,0.95)',
  },
  welcomeContent: {
    flexGrow: 1,
    justifyContent: 'center',
    paddingVertical: 40,
  },
  heroSection: {
    alignItems: 'center',
    paddingHorizontal: 30,
    marginBottom: 40,
  },
  logoHero: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 30,
  },
  logoHeroText: {
    fontSize: 60,
    fontWeight: 'bold',
    color: colors.white,
    marginRight: 15,
  },
  logoHeroCircle: {
    width: 50, height: 50, borderRadius: 25,
    backgroundColor: colors.blue,
    justifyContent: 'center', alignItems: 'center',
  },
  logoHeroSubText: {
    fontSize: 20,
    fontWeight: 'bold',
    color: colors.white,
  },
  welcomeTitle: {
    fontSize: 32, fontWeight: 'bold', color: colors.white,
    textAlign: 'center', marginBottom: 10,
  },
  welcomeSubtitle: {
    fontSize: 18, color: colors.white, opacity: 0.9,
    textAlign: 'center', marginBottom: 20,
  },
  welcomeDescription: {
    fontSize: 16, color: colors.white, opacity: 0.8,
    textAlign: 'center', lineHeight: 24, paddingHorizontal: 20,
  },

  // Features Grid
  featuresGrid: {
    flexDirection: 'row', flexWrap: 'wrap',
    justifyContent: 'space-between',
    paddingHorizontal: 30, marginBottom: 40,
  },
  featureCard: {
    width: (screenWidth - 80) / 2,
    backgroundColor: 'rgba(255,255,255,0.1)',
    borderRadius: 15, padding: 20, marginBottom: 15,
    alignItems: 'center',
  },
  featureIcon: {
    width: 60, height: 60, borderRadius: 30,
    backgroundColor: 'rgba(255,255,255,0.2)',
    justifyContent: 'center', alignItems: 'center',
    marginBottom: 10,
  },
  featureTitle: {
    fontSize: 16, fontWeight: 'bold', color: colors.white,
    textAlign: 'center', marginBottom: 5,
  },
  featureDescription: {
    fontSize: 12, color: colors.white, opacity: 0.9,
    textAlign: 'center',
  },

  // Action Buttons
  welcomeActions: {
    paddingHorizontal: 30, marginBottom: 40,
  },
  primaryActionButton: {
    backgroundColor: colors.primaryLight,
    borderRadius: 25, paddingVertical: 18, marginBottom: 15,
    flexDirection: 'row', alignItems: 'center', justifyContent: 'center',
    shadowColor: '#000', shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.3, shadowRadius: 12, elevation: 12,
  },
  primaryActionText: {
    color: colors.white, fontSize: 18, fontWeight: 'bold', marginRight: 10,
  },
  secondaryActionButton: {
    borderWidth: 2, borderColor: colors.white,
    borderRadius: 25, paddingVertical: 16, marginBottom: 15,
    alignItems: 'center',
  },
  secondaryActionText: {
    color: colors.white, fontSize: 16, fontWeight: 'bold',
  },
  ghostActionButton: {
    alignItems: 'center', paddingVertical: 12,
  },
  ghostActionText: {
    color: colors.white, fontSize: 16, opacity: 0.8,
    textDecorationLine: 'underline',
  },

  // Stats Section
  statsSection: {
    flexDirection: 'row', justifyContent: 'space-around',
    paddingHorizontal: 30, marginBottom: 40,
  },
  statCard: {
    alignItems: 'center',
    backgroundColor: 'rgba(255,255,255,0.1)',
    borderRadius: 15, padding: 20, minWidth: 90,
  },
  statNumber: {
    fontSize: 24, fontWeight: 'bold', color: colors.white, marginTop: 8,
  },
  statLabel: {
    fontSize: 12, color: colors.white, opacity: 0.8,
    marginTop: 4, textAlign: 'center',
  },

  // Sidebar Styles
  sidebarOverlay: { flex: 1, flexDirection: 'row' },
  sidebarBackdrop: { flex: 1, backgroundColor: 'rgba(0,0,0,0.5)' },
  sidebar: {
    width: screenWidth * 0.85, backgroundColor: colors.white,
    shadowColor: '#000', shadowOffset: { width: 4, height: 0 },
    shadowOpacity: 0.3, shadowRadius: 15, elevation: 15,
  },
  sidebarHeader: {
    backgroundColor: colors.primary,
    paddingTop: 50, paddingBottom: 25, paddingHorizontal: 25,
  },
  sidebarUserInfo: { flexDirection: 'row', alignItems: 'center' },
  sidebarAvatar: {
    width: 60, height: 60, borderRadius: 30,
    backgroundColor: colors.primaryLight,
    justifyContent: 'center', alignItems: 'center', marginRight: 15,
  },
  sidebarAvatarText: { fontSize: 20, fontWeight: 'bold', color: colors.white },
  sidebarUserDetails: { flex: 1 },
  sidebarUserName: {
    fontSize: 18, fontWeight: 'bold', color: colors.white, marginBottom: 4,
  },
  sidebarUserEmail: {
    fontSize: 14, color: colors.white, opacity: 0.8, marginBottom: 8,
  },
  pointsBadge: {
    flexDirection: 'row', alignItems: 'center',
    backgroundColor: 'rgba(255,255,255,0.2)',
    borderRadius: 12, paddingHorizontal: 8, paddingVertical: 4,
    alignSelf: 'flex-start',
  },
  sidebarUserPoints: {
    fontSize: 12, color: colors.accent, fontWeight: 'bold', marginLeft: 4,
  },
  sidebarGuestInfo: { alignItems: 'center' },
  sidebarGuestAvatar: {
    width: 70, height: 70, borderRadius: 35,
    backgroundColor: colors.primaryLight,
    justifyContent: 'center', alignItems: 'center', marginBottom: 15,
  },
  sidebarGuestText: { fontSize: 18, color: colors.white, marginBottom: 15 },
  sidebarLoginBtn: {
    backgroundColor: colors.primaryLight,
    paddingHorizontal: 25, paddingVertical: 10, borderRadius: 20,
  },
  sidebarLoginText: { color: colors.white, fontWeight: 'bold' },
  sidebarMenu: { flex: 1, paddingTop: 20 },
  menuItem: {
    flexDirection: 'row', alignItems: 'center',
    paddingHorizontal: 25, paddingVertical: 18,
    borderBottomWidth: 0.5, borderBottomColor: colors.lightGray,
  },
  menuItemText: {
    fontSize: 16, color: colors.black, marginLeft: 15,
    flex: 1, fontWeight: '500',
  },
  menuDivider: { height: 1, backgroundColor: colors.lightGray, marginVertical: 15 },
  liveBadge: {
    backgroundColor: colors.red,
    paddingHorizontal: 8, paddingVertical: 3, borderRadius: 10,
  },
  liveBadgeText: { color: colors.white, fontSize: 10, fontWeight: 'bold' },

  // Header Styles
  header: {
    backgroundColor: colors.primary, flexDirection: 'row',
    alignItems: 'center', paddingHorizontal: 20, paddingVertical: 15,
    justifyContent: 'space-between',
    shadowColor: '#000', shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2, shadowRadius: 4, elevation: 4,
  },
  menuButton: { padding: 8, borderRadius: 8 },
  logoContainer: { flexDirection: 'row', alignItems: 'center' },
  logoText: { fontSize: 24, fontWeight: 'bold', color: colors.white, marginRight: 8 },
  logoCircle: {
    width: 28, height: 28, borderRadius: 14,
    backgroundColor: colors.blue,
    justifyContent: 'center', alignItems: 'center',
  },
  logoSubText: { fontSize: 12, fontWeight: 'bold', color: colors.white },
  notificationButton: { padding: 8, position: 'relative' },
  notificationDot: {
    position: 'absolute', top: 4, right: 4,
    width: 8, height: 8, borderRadius: 4, backgroundColor: colors.red,
  },

  // Content Styles
  content: { flex: 1, backgroundColor: colors.white },
  pageContainer: { flex: 1 },

  // Home Page Styles
  heroLiveSection: {
    height: 200, backgroundColor: colors.primary,
    justifyContent: 'center', alignItems: 'center',
    marginBottom: 20, position: 'relative',
  },
  heroLiveOverlay: {
    justifyContent: 'center', alignItems: 'center', padding: 20,
  },
  liveIndicator: {
    position: 'absolute', top: 15, right: 15,
    backgroundColor: colors.red,
    paddingHorizontal: 8, paddingVertical: 4, borderRadius: 10,
  },
  liveText: { color: colors.white, fontSize: 10, fontWeight: 'bold' },
  heroLiveTitle: {
    fontSize: 24, fontWeight: 'bold', color: colors.white,
    textAlign: 'center', marginBottom: 8,
  },
  heroLiveSubtitle: {
    fontSize: 16, color: colors.white, opacity: 0.9,
    textAlign: 'center', marginBottom: 20,
  },
  heroPlayButton: {
    width: 70, height: 70, borderRadius: 35,
    backgroundColor: 'rgba(255,255,255,0.3)',
    justifyContent: 'center', alignItems: 'center', marginBottom: 10,
  },
  viewerCount: { fontSize: 14, color: colors.white, fontWeight: 'bold' },

  // Quick Actions
  quickActionsBar: {
    flexDirection: 'row', justifyContent: 'space-around',
    paddingHorizontal: 20, paddingVertical: 15,
    backgroundColor: colors.lightGray, marginBottom: 20,
  },
  quickAction: { alignItems: 'center', padding: 10 },
  quickActionText: {
    fontSize: 12, color: colors.darkGray,
    fontWeight: '600', marginTop: 5,
  },

  // Section Styles
  section: { marginVertical: 10, paddingHorizontal: 20 },
  sectionHeader: {
    flexDirection: 'row', alignItems: 'center', marginBottom: 15,
  },
  sectionTitle: {
    fontSize: 20, fontWeight: 'bold', color: colors.black,
    marginLeft: 12, flex: 1,
  },
  seeAllText: { color: colors.primaryLight, fontWeight: 'bold', fontSize: 14 },

  // Modern Video Cards
  modernVideoCard: {
    width: 200, marginRight: 15, backgroundColor: colors.white,
    borderRadius: 15, shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 }, shadowOpacity: 0.15,
    shadowRadius: 8, elevation: 6, overflow: 'hidden',
  },
  modernVideoThumbnail: { width: '100%', height: 120, resizeMode: 'cover' },
  videoPlayOverlay: {
    position: 'absolute', top: 40, left: 80,
    width: 40, height: 40, borderRadius: 20,
    backgroundColor: 'rgba(0,0,0,0.7)',
    justifyContent: 'center', alignItems: 'center',
  },
  modernVideoInfo: { padding: 12 },
  modernVideoTitle: {
    fontSize: 14, fontWeight: 'bold', color: colors.black,
    marginBottom: 8, lineHeight: 18,
  },
  videoMetaRow: {
    flexDirection: 'row', justifyContent: 'space-between',
    alignItems: 'center',
  },
  videoStats: { fontSize: 12, color: colors.gray },
  videoDuration: { fontSize: 12, color: colors.darkGray, fontWeight: '600' },

  // Categories Grid
  categoriesGrid: {
    flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'space-between',
  },
  categoryCard: {
    width: (screenWidth - 60) / 4, alignItems: 'center',
    backgroundColor: colors.lightGray, borderRadius: 15,
    padding: 15, marginBottom: 15,
  },
  categoryIcon: {
    width: 50, height: 50, borderRadius: 25,
    backgroundColor: colors.primaryLight,
    justifyContent: 'center', alignItems: 'center', marginBottom: 8,
  },
  categoryEmoji: { fontSize: 24 },
  categoryName: {
    fontSize: 11, color: colors.darkGray,
    fontWeight: '600', textAlign: 'center',
  },

  // News Cards
  newsCard: {
    backgroundColor: colors.white, borderRadius: 15, marginBottom: 15,
    shadowColor: '#000', shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1, shadowRadius: 6, elevation: 3,
    overflow: 'hidden', padding: 15,
  },
  newsContent: { flex: 1 },
  newsHeader: {
    flexDirection: 'row', justifyContent: 'space-between',
    alignItems: 'center', marginBottom: 8,
  },
  newsCategory: {
    fontSize: 10, color: colors.orange, fontWeight: 'bold',
    backgroundColor: colors.lightGray,
    paddingHorizontal: 8, paddingVertical: 2, borderRadius: 8,
  },
  newsTime: { fontSize: 10, color: colors.gray },
  newsTitle: {
    fontSize: 14, fontWeight: 'bold', color: colors.black,
    marginBottom: 5, lineHeight: 18,
  },
  newsExcerpt: { fontSize: 12, color: colors.gray, lineHeight: 16 },

  // Modern Publicity Banner
  modernPublicityBanner: {
    borderRadius: 20, backgroundColor: colors.blue,
    overflow: 'hidden', height: 120,
  },
  publicityContent: {
    flexDirection: 'row', alignItems: 'center',
    padding: 20, height: '100%',
  },
  publicityText: { flex: 1, marginLeft: 15 },
  publicityTitle: {
    fontSize: 18, fontWeight: 'bold', color: colors.white, marginBottom: 5,
  },
  publicitySubtitle: {
    fontSize: 14, color: colors.white, marginBottom: 5,
  },
  publicityDescription: { fontSize: 12, color: colors.white, opacity: 0.9 },

  // Statistics Grid
  statsGrid: {
    flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'space-between',
  },
  statItem: {
    width: (screenWidth - 60) / 2, alignItems: 'center',
    backgroundColor: colors.lightGray, borderRadius: 15,
    padding: 20, marginBottom: 15,
  },
  statValue: {
    fontSize: 24, fontWeight: 'bold', color: colors.primary, marginTop: 10,
  },
  statLabel: { fontSize: 12, color: colors.gray, marginTop: 4 },

  // Auth Styles
  authContainer: { padding: 25 },
  authHeader: { alignItems: 'center', marginBottom: 30 },
  backButton: {
    flexDirection: 'row', alignItems: 'center',
    alignSelf: 'flex-start', marginBottom: 20, padding: 5,
  },
  backText: {
    fontSize: 16, color: colors.primary, marginLeft: 8, fontWeight: '600',
  },
  authTitle: {
    fontSize: 32, fontWeight: 'bold', color: colors.black,
    textAlign: 'center', marginBottom: 10,
  },
  authSubtitle: {
    fontSize: 16, color: colors.gray, textAlign: 'center', lineHeight: 22,
  },
  inputContainer: { marginBottom: 20 },
  input: {
    backgroundColor: colors.lightGray, borderRadius: 15,
    paddingHorizontal: 20, paddingVertical: 18,
    fontSize: 16, color: colors.black,
    borderWidth: 1, borderColor: 'transparent',
  },
  authButton: {
    backgroundColor: colors.primary, borderRadius: 20, paddingVertical: 18,
    flexDirection: 'row', alignItems: 'center', justifyContent: 'center',
    marginTop: 20, marginBottom: 20,
    shadowColor: '#000', shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.2, shadowRadius: 8, elevation: 6,
  },
  authButtonText: {
    color: colors.white, fontSize: 18, fontWeight: 'bold', marginRight: 10,
  },
  linkText: {
    textAlign: 'center', color: colors.primaryLight,
    fontSize: 16, fontWeight: '600',
  },

  // Live Page Styles
  livePageContainer: { padding: 20 },
  pageTitle: {
    fontSize: 28, fontWeight: 'bold', color: colors.black,
    textAlign: 'center', marginBottom: 20,
  },
  livePlayerContainer: {
    height: 250, borderRadius: 20, backgroundColor: colors.primary,
    justifyContent: 'center', alignItems: 'center',
    marginBottom: 25, position: 'relative',
  },
  livePlayerOverlay: {
    justifyContent: 'center', alignItems: 'center',
    padding: 20,
  },
  livePlayButton: {
    width: 80, height: 80, borderRadius: 40,
    backgroundColor: 'rgba(255,255,255,0.3)',
    justifyContent: 'center', alignItems: 'center', marginBottom: 15,
  },
  livePlayerText: {
    color: colors.white, fontSize: 20, fontWeight: 'bold',
  },
  liveIndicatorLarge: {
    position: 'absolute', top: 20, right: 20,
    backgroundColor: colors.red,
    paddingHorizontal: 12, paddingVertical: 6, borderRadius: 15,
  },
  liveTextLarge: { color: colors.white, fontSize: 12, fontWeight: 'bold' },
  liveInfo: {
    backgroundColor: colors.lightGray, padding: 25, borderRadius: 20,
  },
  liveInfoTitle: {
    fontSize: 20, fontWeight: 'bold', color: colors.black, marginBottom: 12,
  },
  liveInfoDescription: {
    fontSize: 16, color: colors.gray, lineHeight: 24, marginBottom: 15,
  },

  // Profile Styles
  profileContainer: { padding: 25 },
  profileHeader: {
    alignItems: 'center', backgroundColor: colors.lightGray,
    borderRadius: 25, padding: 30, marginBottom: 25,
  },
  profileAvatar: {
    width: 100, height: 100, borderRadius: 50,
    backgroundColor: colors.primary,
    justifyContent: 'center', alignItems: 'center', marginBottom: 15,
  },
  profileAvatarText: { fontSize: 32, fontWeight: 'bold', color: colors.white },
  profileName: {
    fontSize: 24, fontWeight: 'bold', color: colors.black, marginBottom: 5,
  },
  profileEmail: { fontSize: 16, color: colors.gray, marginBottom: 15 },
  profilePointsBadge: {
    flexDirection: 'row', alignItems: 'center',
    backgroundColor: colors.primary, borderRadius: 20,
    paddingHorizontal: 15, paddingVertical: 8,
  },
  profilePoints: {
    fontSize: 16, color: colors.white, fontWeight: 'bold', marginLeft: 5,
  },
  profileStats: {
    flexDirection: 'row', justifyContent: 'space-around', marginBottom: 30,
  },
  profileStatItem: {
    alignItems: 'center', backgroundColor: colors.white,
    borderRadius: 15, padding: 20, minWidth: 90,
    shadowColor: '#000', shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1, shadowRadius: 4, elevation: 2,
  },
  profileStatValue: {
    fontSize: 24, fontWeight: 'bold', color: colors.primary, marginTop: 8,
  },
  profileStatLabel: { fontSize: 12, color: colors.gray, marginTop: 4 },

  // Auth Prompt
  authPrompt: {
    padding: 50, alignItems: 'center',
    backgroundColor: colors.lightGray, margin: 20, borderRadius: 25,
  },
  authPromptTitle: {
    fontSize: 24, fontWeight: 'bold', color: colors.black,
    marginTop: 20, marginBottom: 10,
  },
  authPromptText: {
    fontSize: 16, color: colors.gray, textAlign: 'center',
    marginBottom: 30, lineHeight: 22,
  },
});