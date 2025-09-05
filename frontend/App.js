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
      const response = await fetch('https://replay-fidelity.preview.emergentagent.com/api/videos');
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
          like_count: '234'
        },
        {
          id: 'xJatmbxIaIM',
          title: 'Franc-Parler - Débat Économie',
          thumbnail: 'https://i.ytimg.com/vi/xJatmbxIaIM/hqdefault.jpg',
          view_count: '8750',
          like_count: '156'
        }
      ]);
    }
  };

  const loadNews = async () => {
    try {
      const response = await fetch('https://replay-fidelity.preview.emergentagent.com/api/news');
      const data = await response.json();
      setNews(data.news || []);
    } catch (error) {
      console.error('Error loading news:', error);
      setNews([
        {
          _id: '1',
          title: 'Flash Info - Burkina Faso',
          excerpt: 'Les dernières nouvelles du pays des hommes intègres...',
          image_url: 'https://via.placeholder.com/300x200/2d5016/ffffff?text=LCA+TV+NEWS',
          published_at: new Date().toISOString()
        }
      ]);
    }
  };

  const handleLogin = async (email, password) => {
    setLoading(true);
    try {
      const response = await fetch('https://replay-fidelity.preview.emergentagent.com/api/auth/login', {
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
      const response = await fetch('https://replay-fidelity.preview.emergentagent.com/api/auth/register', {
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
      home: '🏠',
      radio: '📡',
      play: '▶️',
      star: '⭐',
      grid: '⚏',
      newspaper: '📰',
      person: '👤',
      heart: '❤️',
      megaphone: '📢',
      arrow: '→',
      back: '←',
      live: '🔴',
      tv: '📺',
      video: '🎥',
      news: '📰',
      menu: '☰',
      close: '✕',
      logout: '🚪',
      settings: '⚙️',
      info: 'ℹ️',
      help: '❓',
      notification: '🔔',
    };
    
    return (
      <Text style={{ fontSize: size, color }}>{icons[name] || '•'}</Text>
    );
  };

  // Welcome Page - Ultra Modern
  const WelcomePage = () => (
    <View style={styles.welcomeContainer}>
      <StatusBar barStyle="light-content" backgroundColor={colors.primary} />
      
      {/* Background Gradient */}
      <View style={styles.welcomeBackground}>
        <View style={styles.gradientOverlay} />
        
        {/* Hero Section */}
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
            en direct et en replay
          </Text>
        </View>

        {/* Features Preview */}
        <View style={styles.featuresPreview}>
          <View style={styles.featurePreviewItem}>
            <Icon name="live" size={32} color={colors.red} />
            <Text style={styles.featurePreviewText}>Direct 24/7</Text>
          </View>
          <View style={styles.featurePreviewItem}>
            <Icon name="play" size={32} color={colors.blue} />
            <Text style={styles.featurePreviewText}>Replays</Text>
          </View>
          <View style={styles.featurePreviewItem}>
            <Icon name="news" size={32} color={colors.orange} />
            <Text style={styles.featurePreviewText}>Actualités</Text>
          </View>
        </View>

        {/* Action Buttons */}
        <View style={styles.welcomeActions}>
          <TouchableOpacity 
            style={styles.primaryActionButton}
            onPress={() => setCurrentPage('login')}
          >
            <View style={styles.primaryActionGradient}>
              <Text style={styles.primaryActionText}>Se connecter</Text>
            </View>
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
          <View style={styles.statItem}>
            <Text style={styles.statNumber}>500K+</Text>
            <Text style={styles.statLabel}>Téléspectateurs</Text>
          </View>
          <View style={styles.statItem}>
            <Text style={styles.statNumber}>24/7</Text>
            <Text style={styles.statLabel}>Diffusion</Text>
          </View>
          <View style={styles.statItem}>
            <Text style={styles.statNumber}>100%</Text>
            <Text style={styles.statLabel}>Burkinabè</Text>
          </View>
        </View>
      </View>
    </View>
  );

  // Sidebar Component
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
          {/* Sidebar Header */}
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
                  <Text style={styles.sidebarUserPoints}>{user.points || 0} points</Text>
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

          {/* Navigation Menu */}
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
            
            <TouchableOpacity style={styles.menuItem} onPress={() => Alert.alert('Replays', 'Accédez aux replays de nos émissions')}>
              <Icon name="play" size={24} color={colors.blue} />
              <Text style={styles.menuItemText}>Replays</Text>
            </TouchableOpacity>
            
            <TouchableOpacity style={styles.menuItem} onPress={() => Alert.alert('Actualités', 'Toute l\'info du Burkina Faso')}>
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
            
            <TouchableOpacity style={styles.menuItem} onPress={() => Alert.alert('Publicité', 'Programme publicitaire LCA TV')}>
              <Icon name="megaphone" size={24} color={colors.darkBlue} />
              <Text style={styles.menuItemText}>Programme Pub</Text>
            </TouchableOpacity>
            
            <TouchableOpacity style={styles.menuItem} onPress={() => Alert.alert('Notifications', 'Paramètres de notifications')}>
              <Icon name="notification" size={24} color={colors.gray} />
              <Text style={styles.menuItemText}>Notifications</Text>
            </TouchableOpacity>
            
            <TouchableOpacity style={styles.menuItem} onPress={() => Alert.alert('Paramètres', 'Paramètres de l\'application')}>
              <Icon name="settings" size={24} color={colors.gray} />
              <Text style={styles.menuItemText}>Paramètres</Text>
            </TouchableOpacity>
            
            <TouchableOpacity style={styles.menuItem} onPress={() => Alert.alert('À propos', 'LCA TV Mobile v1.0\nDéveloppé pour LCA TV')}>
              <Icon name="info" size={24} color={colors.gray} />
              <Text style={styles.menuItemText}>À propos</Text>
            </TouchableOpacity>
            
            <TouchableOpacity style={styles.menuItem} onPress={() => Alert.alert('Aide', 'Contactez-nous : support@lcatv.bf')}>
              <Icon name="help" size={24} color={colors.gray} />
              <Text style={styles.menuItemText}>Aide</Text>
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

  // Header Component with Sidebar Toggle
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

  // Home Page (unchanged but with new header)
  const HomePage = () => (
    <ScrollView style={styles.content}>
      {/* Live Section */}
      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Icon name="radio" size={24} color={colors.primaryLight} />
          <Text style={styles.sectionTitle}>Direct</Text>
          <View style={styles.liveIndicator}>
            <Text style={styles.liveText}>LIVE</Text>
          </View>
        </View>
        
        <TouchableOpacity onPress={() => setCurrentPage('live')} style={styles.liveContainer}>
          <Image
            source={{ uri: 'https://i.ytimg.com/vi/ixQEmhTbvTI/maxresdefault.jpg' }}
            style={styles.liveImage}
            resizeMode="cover"
          />
          <View style={styles.liveOverlay}>
            <Icon name="play" size={60} color={colors.white} />
            <Text style={styles.liveTitle}>Regarder en direct</Text>
          </View>
        </TouchableOpacity>
      </View>

      {/* Featured Videos */}
      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Icon name="star" size={24} color={colors.primaryLight} />
          <Text style={styles.sectionTitle}>Programmes populaires</Text>
          <TouchableOpacity onPress={() => Alert.alert('Replays', 'Accédez aux replays')}>
            <Text style={styles.seeAllText}>Voir tout</Text>
          </TouchableOpacity>
        </View>
        
        <ScrollView horizontal showsHorizontalScrollIndicator={false}>
          {videos.slice(0, 3).map((video, index) => (
            <TouchableOpacity key={index} style={styles.videoCard}>
              <Image source={{ uri: video.thumbnail }} style={styles.videoThumbnail} />
              <View style={styles.videoInfo}>
                <Text style={styles.videoTitle} numberOfLines={2}>{video.title}</Text>
                <Text style={styles.videoStats}>{video.view_count} vues • {video.like_count} likes</Text>
              </View>
            </TouchableOpacity>
          ))}
        </ScrollView>
      </View>

      {/* Rest of home page content... */}
      <View style={styles.section}>
        <TouchableOpacity style={styles.publicityBanner} onPress={() => Alert.alert('Programme Publicitaire', 'Boostez votre visibilité avec LCA TV')}>
          <View style={styles.publicityContent}>
            <Icon name="megaphone" size={32} color={colors.white} />
            <View style={styles.publicityText}>
              <Text style={styles.publicityTitle}>Programme Publicitaire</Text>
              <Text style={styles.publicitySubtitle}>Boostez votre visibilité avec LCA TV</Text>
            </View>
            <Icon name="arrow" size={24} color={colors.white} />
          </View>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );

  // Login Page
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
            {loading ? (
              <ActivityIndicator color={colors.white} />
            ) : (
              <Text style={styles.authButtonText}>Se connecter</Text>
            )}
          </TouchableOpacity>
          
          <TouchableOpacity onPress={() => setCurrentPage('register')}>
            <Text style={styles.linkText}>Créer un compte</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    );
  };

  // Register Page
  const RegisterPage = () => {
    const [formData, setFormData] = useState({
      nom: '',
      prenom: '',
      email: '',
      telephone: '',
      password: '',
      confirm_password: '',
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
          
          <Text style={styles.authTitle}>Inscription</Text>
          <Text style={styles.authSubtitle}>Créez votre compte LCA TV</Text>
          
          <View style={styles.inputContainer}>
            <TextInput
              style={styles.input}
              placeholder="Nom"
              value={formData.nom}
              onChangeText={(text) => updateFormData('nom', text)}
            />
          </View>
          
          <View style={styles.inputContainer}>
            <TextInput
              style={styles.input}
              placeholder="Prénom"
              value={formData.prenom}
              onChangeText={(text) => updateFormData('prenom', text)}
            />
          </View>
          
          <View style={styles.inputContainer}>
            <TextInput
              style={styles.input}
              placeholder="Email"
              value={formData.email}
              onChangeText={(text) => updateFormData('email', text)}
              keyboardType="email-address"
              autoCapitalize="none"
            />
          </View>
          
          <View style={styles.inputContainer}>
            <TextInput
              style={styles.input}
              placeholder="Téléphone (+226XXXXXXXX)"
              value={formData.telephone}
              onChangeText={(text) => updateFormData('telephone', text)}
              keyboardType="phone-pad"
            />
          </View>
          
          <View style={styles.inputContainer}>
            <TextInput
              style={styles.input}
              placeholder="Mot de passe"
              value={formData.password}
              onChangeText={(text) => updateFormData('password', text)}
              secureTextEntry
            />
          </View>
          
          <View style={styles.inputContainer}>
            <TextInput
              style={styles.input}
              placeholder="Confirmer le mot de passe"
              value={formData.confirm_password}
              onChangeText={(text) => updateFormData('confirm_password', text)}
              secureTextEntry
            />
          </View>
          
          <TouchableOpacity 
            style={styles.authButton} 
            onPress={() => handleRegister({ ...formData, accept_cgu: true, newsletter: false })}
            disabled={loading}
          >
            {loading ? (
              <ActivityIndicator color={colors.white} />
            ) : (
              <Text style={styles.authButtonText}>Créer mon compte</Text>
            )}
          </TouchableOpacity>
        </View>
      </ScrollView>
    );
  };

  // Live Page
  const LivePage = () => (
    <ScrollView style={styles.content}>
      <View style={styles.livePageContainer}>
        <Text style={styles.pageTitle}>LCA TV - Direct</Text>
        
        <View style={styles.livePlayerContainer}>
          <Image
            source={{ uri: 'https://i.ytimg.com/vi/ixQEmhTbvTI/maxresdefault.jpg' }}
            style={styles.livePlayerImage}
            resizeMode="cover"
          />
          <View style={styles.livePlayerOverlay}>
            <Icon name="play" size={80} color={colors.white} />
            <Text style={styles.livePlayerText}>Stream en direct</Text>
            <View style={styles.liveIndicatorLarge}>
              <Text style={styles.liveTextLarge}>🔴 EN DIRECT</Text>
            </View>
          </View>
        </View>
        
        <View style={styles.liveInfo}>
          <Text style={styles.liveInfoTitle}>LCA TV - La Chaîne Africaine de télévision</Text>
          <Text style={styles.liveInfoDescription}>
            Suivez en direct nos programmes : Journal, Franc-Parler, Questions de Femmes, et bien plus encore.
          </Text>
          <Text style={styles.viewerCount}>🔴 1,247 spectateurs connectés</Text>
        </View>
      </View>
    </ScrollView>
  );

  // Profile Page
  const ProfilePage = () => (
    <ScrollView style={styles.content}>
      {user ? (
        <View style={styles.profileContainer}>
          <Text style={styles.pageTitle}>Mon Profil</Text>
          
          <View style={styles.userInfo}>
            <View style={styles.avatar}>
              <Text style={styles.avatarText}>{user.nom.charAt(0)}{user.prenom.charAt(0)}</Text>
            </View>
            <Text style={styles.userName}>{user.prenom} {user.nom}</Text>
            <Text style={styles.userEmail}>{user.email}</Text>
          </View>
          
          <View style={styles.statsContainer}>
            <View style={styles.statItem}>
              <Text style={styles.statValue}>{user.points || 0}</Text>
              <Text style={styles.statLabel}>Points</Text>
            </View>
            <View style={styles.statItem}>
              <Text style={styles.statValue}>{user.favorites?.length || 0}</Text>
              <Text style={styles.statLabel}>Favoris</Text>
            </View>
          </View>
        </View>
      ) : (
        <View style={styles.authPrompt}>
          <Text style={styles.authPromptText}>Connectez-vous pour voir votre profil</Text>
          <TouchableOpacity style={styles.authButton} onPress={() => setCurrentPage('login')}>
            <Text style={styles.authButtonText}>Se connecter</Text>
          </TouchableOpacity>
        </View>
      )}
    </ScrollView>
  );

  const renderCurrentPage = () => {
    switch (currentPage) {
      case 'welcome':
        return <WelcomePage />;
      case 'home':
        return <HomePage />;
      case 'login':
        return <LoginPage />;
      case 'register':
        return <RegisterPage />;
      case 'live':
        return <LivePage />;
      case 'profile':
        return <ProfilePage />;
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
    backgroundColor: colors.white,
  },
  
  // Welcome Page Styles
  welcomeContainer: {
    flex: 1,
  },
  welcomeBackground: {
    flex: 1,
    backgroundColor: colors.primary,
    position: 'relative',
  },
  gradientOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(45,80,22,0.9)',
  },
  heroSection: {
    alignItems: 'center',
    paddingTop: 80,
    paddingHorizontal: 30,
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
    width: 50,
    height: 50,
    borderRadius: 25,
    backgroundColor: colors.blue,
    justifyContent: 'center',
    alignItems: 'center',
  },
  logoHeroSubText: {
    fontSize: 20,
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
    marginBottom: 20,
  },
  welcomeDescription: {
    fontSize: 16,
    color: colors.white,
    opacity: 0.8,
    textAlign: 'center',
    lineHeight: 24,
    paddingHorizontal: 20,
  },
  featuresPreview: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    paddingHorizontal: 40,
    marginTop: 40,
    marginBottom: 50,
  },
  featurePreviewItem: {
    alignItems: 'center',
  },
  featurePreviewText: {
    color: colors.white,
    fontSize: 14,
    fontWeight: 'bold',
    marginTop: 8,
  },
  welcomeActions: {
    paddingHorizontal: 30,
    marginBottom: 40,
  },
  primaryActionButton: {
    backgroundColor: colors.primaryLight,
    borderRadius: 25,
    paddingVertical: 18,
    marginBottom: 15,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 8,
  },
  primaryActionGradient: {
    alignItems: 'center',
  },
  primaryActionText: {
    color: colors.white,
    fontSize: 18,
    fontWeight: 'bold',
  },
  secondaryActionButton: {
    borderWidth: 2,
    borderColor: colors.white,
    borderRadius: 25,
    paddingVertical: 16,
    marginBottom: 15,
    alignItems: 'center',
  },
  secondaryActionText: {
    color: colors.white,
    fontSize: 16,
    fontWeight: 'bold',
  },
  ghostActionButton: {
    alignItems: 'center',
    paddingVertical: 12,
  },
  ghostActionText: {
    color: colors.white,
    fontSize: 16,
    opacity: 0.8,
    textDecorationLine: 'underline',
  },
  statsSection: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    paddingHorizontal: 40,
    marginTop: 20,
  },
  statItem: {
    alignItems: 'center',
  },
  statNumber: {
    fontSize: 24,
    fontWeight: 'bold',
    color: colors.white,
  },
  statLabel: {
    fontSize: 12,
    color: colors.white,
    opacity: 0.8,
    marginTop: 4,
  },

  // Sidebar Styles
  sidebarOverlay: {
    flex: 1,
    flexDirection: 'row',
  },
  sidebarBackdrop: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
  },
  sidebar: {
    width: screenWidth * 0.8,
    backgroundColor: colors.white,
    shadowColor: '#000',
    shadowOffset: { width: 2, height: 0 },
    shadowOpacity: 0.3,
    shadowRadius: 10,
    elevation: 10,
  },
  sidebarHeader: {
    backgroundColor: colors.primary,
    paddingTop: 40,
    paddingBottom: 20,
    paddingHorizontal: 20,
  },
  sidebarUserInfo: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  sidebarAvatar: {
    width: 50,
    height: 50,
    borderRadius: 25,
    backgroundColor: colors.primaryLight,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 15,
  },
  sidebarAvatarText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: colors.white,
  },
  sidebarUserDetails: {
    flex: 1,
  },
  sidebarUserName: {
    fontSize: 18,
    fontWeight: 'bold',
    color: colors.white,
    marginBottom: 2,
  },
  sidebarUserEmail: {
    fontSize: 14,
    color: colors.white,
    opacity: 0.8,
    marginBottom: 4,
  },
  sidebarUserPoints: {
    fontSize: 12,
    color: colors.primaryLight,
    fontWeight: 'bold',
  },
  sidebarGuestInfo: {
    alignItems: 'center',
  },
  sidebarGuestAvatar: {
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: colors.primaryLight,
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
    backgroundColor: colors.primaryLight,
    paddingHorizontal: 20,
    paddingVertical: 8,
    borderRadius: 15,
  },
  sidebarLoginText: {
    color: colors.white,
    fontWeight: 'bold',
  },
  sidebarMenu: {
    flex: 1,
    paddingTop: 20,
  },
  menuItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 15,
    borderBottomWidth: 0.5,
    borderBottomColor: colors.lightGray,
  },
  menuItemText: {
    fontSize: 16,
    color: colors.black,
    marginLeft: 15,
    flex: 1,
  },
  menuDivider: {
    height: 1,
    backgroundColor: colors.lightGray,
    marginVertical: 10,
  },
  liveBadge: {
    backgroundColor: colors.red,
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 8,
  },
  liveBadgeText: {
    color: colors.white,
    fontSize: 10,
    fontWeight: 'bold',
  },

  // Header Styles
  header: {
    backgroundColor: colors.primary,
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 15,
    justifyContent: 'space-between',
  },
  menuButton: {
    padding: 5,
  },
  logoContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  logoText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: colors.white,
    marginRight: 8,
  },
  logoCircle: {
    width: 24,
    height: 24,
    borderRadius: 12,
    backgroundColor: colors.blue,
    justifyContent: 'center',
    alignItems: 'center',
  },
  logoSubText: {
    fontSize: 10,
    fontWeight: 'bold',
    color: colors.white,
  },
  notificationButton: {
    padding: 5,
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

  // Common Styles
  pageContainer: {
    flex: 1,
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
    backgroundColor: 'rgba(0,0,0,0.3)',
  },
  liveTitle: {
    color: colors.white,
    fontSize: 18,
    fontWeight: 'bold',
    marginTop: 10,
  },
  liveIndicator: {
    backgroundColor: colors.red,
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
  publicityBanner: {
    borderRadius: 15,
    backgroundColor: colors.blue,
    overflow: 'hidden',
    marginTop: 10,
  },
  publicityContent: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 20,
  },
  publicityText: {
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

  // Auth Styles
  authContainer: {
    padding: 20,
  },
  backButton: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20,
  },
  backText: {
    fontSize: 16,
    color: colors.primary,
    marginLeft: 8,
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
    marginBottom: 15,
  },
  input: {
    backgroundColor: colors.lightGray,
    borderRadius: 12,
    paddingHorizontal: 15,
    paddingVertical: 15,
    fontSize: 16,
    color: colors.black,
  },
  authButton: {
    backgroundColor: colors.primary,
    borderRadius: 15,
    paddingVertical: 18,
    alignItems: 'center',
    marginTop: 20,
    marginBottom: 15,
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

  // Live Page Styles
  livePageContainer: {
    padding: 20,
  },
  pageTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: colors.black,
    textAlign: 'center',
    marginBottom: 20,
  },
  livePlayerContainer: {
    height: 250,
    borderRadius: 15,
    overflow: 'hidden',
    position: 'relative',
    marginBottom: 20,
  },
  livePlayerImage: {
    width: '100%',
    height: '100%',
  },
  livePlayerOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0,0,0,0.3)',
  },
  livePlayerText: {
    color: colors.white,
    fontSize: 20,
    fontWeight: 'bold',
    marginTop: 10,
  },
  liveIndicatorLarge: {
    position: 'absolute',
    top: 15,
    right: 15,
    backgroundColor: colors.red,
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 15,
  },
  liveTextLarge: {
    color: colors.white,
    fontSize: 14,
    fontWeight: 'bold',
  },
  liveInfo: {
    backgroundColor: colors.lightGray,
    padding: 20,
    borderRadius: 15,
  },
  liveInfoTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: colors.black,
    marginBottom: 10,
  },
  liveInfoDescription: {
    fontSize: 16,
    color: colors.gray,
    lineHeight: 22,
    marginBottom: 15,
  },
  viewerCount: {
    fontSize: 14,
    color: colors.primaryLight,
    fontWeight: 'bold',
  },

  // Profile Styles
  profileContainer: {
    padding: 20,
  },
  userInfo: {
    alignItems: 'center',
    marginBottom: 30,
  },
  avatar: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: colors.primary,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 15,
  },
  avatarText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: colors.white,
  },
  userName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: colors.black,
    marginBottom: 5,
  },
  userEmail: {
    fontSize: 16,
    color: colors.gray,
  },
  statsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginBottom: 30,
  },
  statValue: {
    fontSize: 28,
    fontWeight: 'bold',
    color: colors.primary,
  },
  authPrompt: {
    padding: 40,
    alignItems: 'center',
  },
  authPromptText: {
    fontSize: 18,
    color: colors.gray,
    textAlign: 'center',
    marginBottom: 30,
  },
});