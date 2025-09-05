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
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

const { width: screenWidth, height: screenHeight } = Dimensions.get('window');

// LCA TV Colors
const colors = {
  primary: '#2d5016',
  primaryLight: '#22c55e',
  secondary: '#16a34a',
  blue: '#3b82f6',
  white: '#ffffff',
  gray: '#6b7280',
  lightGray: '#f3f4f6',
  black: '#111827',
  red: '#ef4444',
};

export default function App() {
  const [currentPage, setCurrentPage] = useState('welcome');
  const [user, setUser] = useState(null);
  const [videos, setVideos] = useState([]);
  const [news, setNews] = useState([]);
  const [loading, setLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    try {
      // Check user session
      const userData = await AsyncStorage.getItem('user');
      if (userData) {
        setUser(JSON.parse(userData));
      }
      
      // Load videos and news
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
      // Fallback videos
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
      // Fallback news
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

  const logout = async () => {
    await AsyncStorage.removeItem('user');
    await AsyncStorage.removeItem('access_token');
    setUser(null);
    setCurrentPage('home');
  };

  // Icon Component (simple text-based icons)
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
    };
    
    return (
      <Text style={{ fontSize: size, color }}>{icons[name] || '•'}</Text>
    );
  };

  // Header Component
  const Header = () => (
    <View style={styles.header}>
      <View style={styles.logoContainer}>
        <Text style={styles.logoText}>LCA</Text>
        <View style={styles.logoCircle}>
          <Text style={styles.logoSubText}>TV</Text>
        </View>
      </View>
      <Text style={styles.tagline}>La Chaîne Africaine de télévision</Text>
      {!user && currentPage === 'home' && (
        <TouchableOpacity onPress={() => setCurrentPage('login')} style={styles.loginButton}>
          <Text style={styles.loginButtonText}>Se connecter</Text>
        </TouchableOpacity>
      )}
    </View>
  );

  // Home Page
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
          <TouchableOpacity onPress={() => setCurrentPage('replay')}>
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

      {/* Emissions Grid */}
      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Icon name="grid" size={24} color={colors.primaryLight} />
          <Text style={styles.sectionTitle}>Nos émissions</Text>
        </View>
        
        <View style={styles.emissionsGrid}>
          <EmissionCard icon="newspaper" title="Journal LCA TV" onPress={() => Alert.alert('Journal LCA TV', 'Actualités du Burkina Faso')} />
          <EmissionCard icon="heart" title="Franc-Parler" onPress={() => Alert.alert('Franc-Parler', 'Débats politiques')} />
          <EmissionCard icon="person" title="Questions de Femmes" onPress={() => Alert.alert('Questions de Femmes', 'Émission féminine')} />
          <EmissionCard icon="star" title="Soleil d'Afrique" onPress={() => Alert.alert('Soleil d\'Afrique', 'Culture africaine')} />
          <EmissionCard icon="play" title="Sports & Étalons" onPress={() => Alert.alert('Sports', 'Actualités sportives')} />
          <EmissionCard icon="tv" title="Jeunesse Avenir" onPress={() => Alert.alert('Jeunesse', 'Émission jeunesse')} />
          <EmissionCard icon="home" title="Burkina Faso" onPress={() => Alert.alert('Burkina Faso', 'Actualités nationales')} />
          <EmissionCard icon="video" title="Danse des Masques" onPress={() => Alert.alert('Culture', 'Danse traditionnelle')} />
        </View>
      </View>

      {/* News */}
      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Icon name="news" size={24} color={colors.primaryLight} />
          <Text style={styles.sectionTitle}>Actualités</Text>
          <TouchableOpacity onPress={() => setCurrentPage('news')}>
            <Text style={styles.seeAllText}>Voir tout</Text>
          </TouchableOpacity>
        </View>
        
        {news.slice(0, 1).map((article, index) => (
          <TouchableOpacity key={index} style={styles.newsCard}>
            <Image source={{ uri: article.image_url }} style={styles.newsImage} />
            <View style={styles.newsContent}>
              <Text style={styles.newsTitle}>{article.title}</Text>
              <Text style={styles.newsExcerpt}>{article.excerpt}</Text>
              <Text style={styles.newsDate}>Il y a 2 heures</Text>
            </View>
          </TouchableOpacity>
        ))}
      </View>

      {/* Publicity */}
      <View style={styles.section}>
        <TouchableOpacity style={styles.publicityBanner} onPress={() => setCurrentPage('publicity')}>
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

  // Emission Card Component
  const EmissionCard = ({ icon, title, onPress }) => (
    <TouchableOpacity style={styles.emissionCard} onPress={onPress}>
      <View style={styles.emissionContent}>
        <Icon name={icon} size={24} color={colors.white} />
        <Text style={styles.emissionText}>{title}</Text>
      </View>
    </TouchableOpacity>
  );

  // Login Page
  const LoginPage = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    return (
      <ScrollView style={styles.content}>
        <View style={styles.authContainer}>
          <TouchableOpacity onPress={() => setCurrentPage('home')} style={styles.backButton}>
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

    const handleSubmit = () => {
      if (!formData.nom || !formData.prenom || !formData.email || !formData.password) {
        Alert.alert('Erreur', 'Veuillez remplir tous les champs');
        return;
      }
      if (formData.password !== formData.confirm_password) {
        Alert.alert('Erreur', 'Les mots de passe ne correspondent pas');
        return;
      }
      handleRegister({ ...formData, accept_cgu: true, newsletter: false });
    };

    return (
      <ScrollView style={styles.content}>
        <View style={styles.authContainer}>
          <TouchableOpacity onPress={() => setCurrentPage('login')} style={styles.backButton}>
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
            onPress={handleSubmit}
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
      <TouchableOpacity onPress={() => setCurrentPage('home')} style={styles.backButton}>
        <Icon name="back" size={24} color={colors.primary} />
        <Text style={styles.backText}>Retour</Text>
      </TouchableOpacity>
      
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
    </ScrollView>
  );

  // Profile Page
  const ProfilePage = () => (
    <ScrollView style={styles.content}>
      <TouchableOpacity onPress={() => setCurrentPage('home')} style={styles.backButton}>
        <Icon name="back" size={24} color={colors.primary} />
        <Text style={styles.backText}>Retour</Text>
      </TouchableOpacity>
      
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
          
          <TouchableOpacity style={styles.logoutButton} onPress={logout}>
            <Text style={styles.logoutButtonText}>Se déconnecter</Text>
          </TouchableOpacity>
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

  // Bottom Navigation
  const BottomNav = () => (
    <View style={styles.bottomNav}>
      <TouchableOpacity 
        style={[styles.navItem, currentPage === 'home' && styles.navItemActive]} 
        onPress={() => setCurrentPage('home')}
      >
        <Icon name="home" size={24} color={currentPage === 'home' ? colors.primaryLight : colors.gray} />
        <Text style={[styles.navText, currentPage === 'home' && styles.navTextActive]}>Accueil</Text>
      </TouchableOpacity>
      
      <TouchableOpacity 
        style={[styles.navItem, currentPage === 'live' && styles.navItemActive]} 
        onPress={() => setCurrentPage('live')}
      >
        <Icon name="radio" size={24} color={currentPage === 'live' ? colors.primaryLight : colors.gray} />
        <Text style={[styles.navText, currentPage === 'live' && styles.navTextActive]}>Direct</Text>
      </TouchableOpacity>
      
      <TouchableOpacity 
        style={[styles.navItem, currentPage === 'replay' && styles.navItemActive]} 
        onPress={() => Alert.alert('Replay', 'Accédez aux replays de nos émissions')}
      >
        <Icon name="play" size={24} color={currentPage === 'replay' ? colors.primaryLight : colors.gray} />
        <Text style={[styles.navText, currentPage === 'replay' && styles.navTextActive]}>Replay</Text>
      </TouchableOpacity>
      
      <TouchableOpacity 
        style={[styles.navItem, currentPage === 'profile' && styles.navItemActive]} 
        onPress={() => setCurrentPage('profile')}
      >
        <Icon name="person" size={24} color={currentPage === 'profile' ? colors.primaryLight : colors.gray} />
        <Text style={[styles.navText, currentPage === 'profile' && styles.navTextActive]}>Profil</Text>
      </TouchableOpacity>
    </View>
  );

  const renderCurrentPage = () => {
    switch (currentPage) {
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
        return <HomePage />;
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor={colors.primary} />
      <Header />
      <View style={styles.pageContainer}>
        {renderCurrentPage()}
      </View>
      <BottomNav />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.white,
  },
  header: {
    backgroundColor: colors.primary,
    paddingHorizontal: 20,
    paddingVertical: 15,
    borderBottomLeftRadius: 20,
    borderBottomRightRadius: 20,
    alignItems: 'center',
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
    marginBottom: 8,
  },
  loginButton: {
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
  emissionsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  emissionCard: {
    width: (screenWidth - 60) / 2,
    marginBottom: 15,
    borderRadius: 12,
    backgroundColor: colors.primary,
    overflow: 'hidden',
  },
  emissionContent: {
    padding: 20,
    alignItems: 'center',
    minHeight: 100,
    justifyContent: 'center',
    backgroundColor: colors.primary,
  },
  emissionText: {
    color: colors.white,
    fontWeight: 'bold',
    fontSize: 14,
    textAlign: 'center',
    marginTop: 8,
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
  bottomNav: {
    flexDirection: 'row',
    backgroundColor: colors.white,
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderTopWidth: 1,
    borderTopColor: colors.lightGray,
  },
  navItem: {
    flex: 1,
    alignItems: 'center',
    paddingVertical: 5,
  },
  navItemActive: {
    backgroundColor: colors.lightGray,
    borderRadius: 10,
  },
  navText: {
    fontSize: 12,
    color: colors.gray,
    marginTop: 2,
  },
  navTextActive: {
    color: colors.primaryLight,
    fontWeight: 'bold',
  },
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
  pageTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: colors.black,
    textAlign: 'center',
    marginBottom: 20,
    marginTop: 20,
  },
  livePlayerContainer: {
    height: 250,
    borderRadius: 15,
    overflow: 'hidden',
    position: 'relative',
    marginHorizontal: 20,
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
    margin: 20,
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
  statItem: {
    alignItems: 'center',
    backgroundColor: colors.lightGray,
    padding: 20,
    borderRadius: 15,
    flex: 1,
    marginHorizontal: 10,
  },
  statValue: {
    fontSize: 28,
    fontWeight: 'bold',
    color: colors.primary,
  },
  statLabel: {
    fontSize: 14,
    color: colors.gray,
    marginTop: 5,
  },
  logoutButton: {
    backgroundColor: colors.red,
    borderRadius: 15,
    paddingVertical: 15,
    alignItems: 'center',
  },
  logoutButtonText: {
    color: colors.white,
    fontSize: 16,
    fontWeight: 'bold',
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