import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  Image,
  TouchableOpacity,
  Dimensions,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { StatusBar } from 'expo-status-bar';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';

const { width: screenWidth } = Dimensions.get('window');

// Theme colors LCA TV
const colors = {
  primary: '#2d5016',
  primaryLight: '#22c55e',
  secondary: '#16a34a',
  blue: '#3b82f6',
  white: '#ffffff',
  gray: '#6b7280',
  lightGray: '#f3f4f6',
  black: '#111827',
};

export default function App() {
  const [currentPage, setCurrentPage] = useState('home');

  const navigateTo = (page: string) => {
    setCurrentPage(page);
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

  const HomePage = () => (
    <ScrollView style={styles.content} showsVerticalScrollIndicator={false}>
      {/* Live Section */}
      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Ionicons name="radio" size={24} color={colors.primaryLight} />
          <Text style={styles.sectionTitle}>Direct</Text>
          <View style={styles.liveIndicator}>
            <Text style={styles.liveText}>LIVE</Text>
          </View>
        </View>
        
        <TouchableOpacity onPress={() => navigateTo('live')} style={styles.liveContainer}>
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
          <TouchableOpacity onPress={() => navigateTo('replay')}>
            <Text style={styles.seeAllText}>Voir tout</Text>
          </TouchableOpacity>
        </View>
        
        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.horizontalScroll}>
          <TouchableOpacity style={styles.videoCard}>
            <Image 
              source={{ uri: 'https://i.ytimg.com/vi/eSApphrRKWg/hqdefault.jpg' }} 
              style={styles.videoThumbnail} 
            />
            <View style={styles.videoInfo}>
              <Text style={styles.videoTitle} numberOfLines={2}>Journal LCA TV - Édition du Soir</Text>
              <Text style={styles.videoStats}>15.4k vues • 234 likes</Text>
            </View>
          </TouchableOpacity>
          
          <TouchableOpacity style={styles.videoCard}>
            <Image 
              source={{ uri: 'https://i.ytimg.com/vi/xJatmbxIaIM/hqdefault.jpg' }} 
              style={styles.videoThumbnail} 
            />
            <View style={styles.videoInfo}>
              <Text style={styles.videoTitle} numberOfLines={2}>Franc-Parler - Débat Économie</Text>
              <Text style={styles.videoStats}>8.7k vues • 156 likes</Text>
            </View>
          </TouchableOpacity>
          
          <TouchableOpacity style={styles.videoCard}>
            <Image 
              source={{ uri: 'https://i.ytimg.com/vi/8aIAKRe4Spo/hqdefault.jpg' }} 
              style={styles.videoThumbnail} 
            />
            <View style={styles.videoInfo}>
              <Text style={styles.videoTitle} numberOfLines={2}>Festival des Masques - Culture</Text>
              <Text style={styles.videoStats}>12.3k vues • 298 likes</Text>
            </View>
          </TouchableOpacity>
        </ScrollView>
      </View>

      {/* Our Programs Grid */}
      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Ionicons name="grid" size={24} color={colors.primaryLight} />
          <Text style={styles.sectionTitle}>Nos émissions</Text>
        </View>
        
        <View style={styles.emissionsGrid}>
          <EmissionCard icon="newspaper" title="Journal LCA TV" onPress={() => Alert.alert('Journal LCA TV', 'Actualités du Burkina Faso')} />
          <EmissionCard icon="chatbubbles" title="Franc-Parler" onPress={() => Alert.alert('Franc-Parler', 'Débats politiques et économiques')} />
          <EmissionCard icon="woman" title="Questions de Femmes" onPress={() => Alert.alert('Questions de Femmes', 'Émission dédiée aux femmes')} />
          <EmissionCard icon="sunny" title="Soleil d'Afrique" onPress={() => Alert.alert('Soleil d\'Afrique', 'Culture africaine')} />
          <EmissionCard icon="football" title="Sports & Étalons" onPress={() => Alert.alert('Sports', 'Actualités sportives')} />
          <EmissionCard icon="people" title="Jeunesse Avenir" onPress={() => Alert.alert('Jeunesse', 'Émission pour les jeunes')} />
          <EmissionCard icon="flag" title="Burkina Faso" onPress={() => Alert.alert('Burkina Faso', 'Actualités nationales')} />
          <EmissionCard icon="musical-notes" title="Danse des Masques" onPress={() => Alert.alert('Culture', 'Danse traditionnelle')} />
        </View>
      </View>

      {/* News Section */}
      <View style={styles.section}>
        <View style={styles.sectionHeader}>
          <Ionicons name="newspaper-outline" size={24} color={colors.primaryLight} />
          <Text style={styles.sectionTitle}>Actualités</Text>
          <TouchableOpacity onPress={() => navigateTo('news')}>
            <Text style={styles.seeAllText}>Voir tout</Text>
          </TouchableOpacity>
        </View>
        
        <TouchableOpacity style={styles.newsCard}>
          <Image 
            source={{ uri: 'https://via.placeholder.com/300x200/2d5016/ffffff?text=LCA+TV+NEWS' }}
            style={styles.newsImage}
          />
          <View style={styles.newsContent}>
            <Text style={styles.newsTitle}>Flash Info - Burkina Faso</Text>
            <Text style={styles.newsExcerpt}>Les dernières nouvelles du pays des hommes intègres...</Text>
            <Text style={styles.newsDate}>Il y a 2 heures</Text>
          </View>
        </TouchableOpacity>
      </View>

      {/* Publicity Section */}
      <View style={styles.section}>
        <TouchableOpacity style={styles.publicityBanner} onPress={() => navigateTo('publicity')}>
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
  );

  const LoginPage = () => (
    <ScrollView style={styles.content}>
      <View style={styles.loginContainer}>
        <Text style={styles.pageTitle}>Connexion</Text>
        <Text style={styles.loginDescription}>
          Connectez-vous pour accéder à vos favoris et gagner des points de fidélité
        </Text>
        
        <View style={styles.featuresList}>
          <View style={styles.featureItem}>
            <Ionicons name="heart" size={20} color={colors.primaryLight} />
            <Text style={styles.featureText}>Sauvegardez vos vidéos favorites</Text>
          </View>
          <View style={styles.featureItem}>
            <Ionicons name="trophy" size={20} color={colors.primaryLight} />
            <Text style={styles.featureText}>Gagnez des points de fidélité</Text>
          </View>
          <View style={styles.featureItem}>
            <Ionicons name="notifications" size={20} color={colors.primaryLight} />
            <Text style={styles.featureText}>Notifications exclusives</Text>
          </View>
        </View>
        
        <TouchableOpacity style={styles.loginButtonLarge} onPress={() => Alert.alert('Connexion', 'Fonctionnalité en développement')}>
          <LinearGradient colors={[colors.primary, colors.primaryLight]} style={styles.loginGradient}>
            <Text style={styles.loginButtonTextLarge}>Se connecter</Text>
          </LinearGradient>
        </TouchableOpacity>
        
        <TouchableOpacity style={styles.registerButton} onPress={() => Alert.alert('Inscription', 'Créez votre compte LCA TV')}>
          <Text style={styles.registerButtonText}>Créer un compte</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );

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
            <Ionicons name="play-circle" size={80} color={colors.white} />
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
          <View style={styles.viewerInfo}>
            <Ionicons name="eye" size={16} color={colors.primaryLight} />
            <Text style={styles.viewerCount}>1,247 spectateurs connectés</Text>
          </View>
        </View>
      </View>
    </ScrollView>
  );

  // Bottom Navigation
  const BottomNav = () => (
    <View style={styles.bottomNav}>
      <TouchableOpacity 
        style={[styles.navItem, currentPage === 'home' && styles.navItemActive]} 
        onPress={() => navigateTo('home')}
      >
        <Ionicons name="home" size={24} color={currentPage === 'home' ? colors.primaryLight : colors.gray} />
        <Text style={[styles.navText, currentPage === 'home' && styles.navTextActive]}>Accueil</Text>
      </TouchableOpacity>
      
      <TouchableOpacity 
        style={[styles.navItem, currentPage === 'live' && styles.navItemActive]} 
        onPress={() => navigateTo('live')}
      >
        <Ionicons name="radio" size={24} color={currentPage === 'live' ? colors.primaryLight : colors.gray} />
        <Text style={[styles.navText, currentPage === 'live' && styles.navTextActive]}>Direct</Text>
      </TouchableOpacity>
      
      <TouchableOpacity 
        style={[styles.navItem, currentPage === 'replay' && styles.navItemActive]} 
        onPress={() => Alert.alert('Replay', 'Accédez aux replays de nos émissions')}
      >
        <Ionicons name="play-circle" size={24} color={currentPage === 'replay' ? colors.primaryLight : colors.gray} />
        <Text style={[styles.navText, currentPage === 'replay' && styles.navTextActive]}>Replay</Text>
      </TouchableOpacity>
      
      <TouchableOpacity 
        style={[styles.navItem, currentPage === 'login' && styles.navItemActive]} 
        onPress={() => navigateTo('login')}
      >
        <Ionicons name="person" size={24} color={currentPage === 'login' ? colors.primaryLight : colors.gray} />
        <Text style={[styles.navText, currentPage === 'login' && styles.navTextActive]}>Compte</Text>
      </TouchableOpacity>
    </View>
  );

  const renderCurrentPage = () => {
    switch (currentPage) {
      case 'home':
        return <HomePage />;
      case 'login':
        return <LoginPage />;
      case 'live':
        return <LivePage />;
      default:
        return <HomePage />;
    }
  };

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
      </View>

      {/* Content */}
      <View style={styles.pageContainer}>
        {renderCurrentPage()}
      </View>

      {/* Bottom Navigation */}
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
  pageTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: colors.black,
    textAlign: 'center',
    marginBottom: 20,
  },
  loginContainer: {
    padding: 20,
    alignItems: 'center',
  },
  loginDescription: {
    fontSize: 16,
    color: colors.gray,
    textAlign: 'center',
    marginBottom: 30,
    lineHeight: 22,
  },
  featuresList: {
    alignSelf: 'stretch',
    marginBottom: 40,
  },
  featureItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 15,
    padding: 15,
    backgroundColor: colors.lightGray,
    borderRadius: 12,
  },
  featureText: {
    fontSize: 16,
    color: colors.black,
    marginLeft: 15,
  },
  loginButtonLarge: {
    alignSelf: 'stretch',
    borderRadius: 15,
    overflow: 'hidden',
    marginBottom: 15,
  },
  loginGradient: {
    paddingVertical: 18,
    alignItems: 'center',
  },
  loginButtonTextLarge: {
    color: colors.white,
    fontSize: 18,
    fontWeight: 'bold',
  },
  registerButton: {
    alignSelf: 'stretch',
    paddingVertical: 15,
    alignItems: 'center',
    borderWidth: 2,
    borderColor: colors.primaryLight,
    borderRadius: 15,
  },
  registerButtonText: {
    color: colors.primaryLight,
    fontSize: 16,
    fontWeight: 'bold',
  },
  livePageContainer: {
    padding: 20,
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
    backgroundColor: '#ff4444',
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
  viewerInfo: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  viewerCount: {
    fontSize: 14,
    color: colors.primaryLight,
    fontWeight: 'bold',
    marginLeft: 8,
  },
});