import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Image,
  Alert,
  ActivityIndicator,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { StatusBar } from 'expo-status-bar';
import { LinearGradient } from 'expo-linear-gradient';
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
  gold: '#f59e0b',
};

interface User {
  _id: string;
  nom: string;
  prenom: string;
  email: string;
  telephone: string;
  points: number;
  favorites: string[];
  created_at: string;
  last_login?: string;
}

export default function ProfileScreen() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState({
    videosWatched: 0,
    favoriteCount: 0,
    memberSince: '',
  });
  const router = useRouter();

  useEffect(() => {
    loadUserProfile();
  }, []);

  const loadUserProfile = async () => {
    try {
      setLoading(true);
      const userData = await AsyncStorage.getItem('user');
      
      if (!userData) {
        router.replace('/login');
        return;
      }

      const parsedUser = JSON.parse(userData);
      setUser(parsedUser);
      
      // Load updated profile from backend
      const token = await AsyncStorage.getItem('access_token');
      if (token) {
        const response = await fetch(`${process.env.EXPO_PUBLIC_BACKEND_URL}/api/user/profile`, {
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        });

        if (response.ok) {
          const profileData = await response.json();
          setUser(profileData);
          await AsyncStorage.setItem('user', JSON.stringify(profileData));
          
          // Calculate stats
          setStats({
            videosWatched: Math.floor(profileData.points / 2), // Assuming 2 points per video watched
            favoriteCount: profileData.favorites?.length || 0,
            memberSince: new Date(profileData.created_at).toLocaleDateString('fr-FR', {
              month: 'long',
              year: 'numeric'
            }),
          });
        }
      }
    } catch (error) {
      console.error('Error loading profile:', error);
      Alert.alert('Erreur', 'Impossible de charger le profil');
      router.replace('/login');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    Alert.alert(
      'Déconnexion',
      'Êtes-vous sûr de vouloir vous déconnecter ?',
      [
        { text: 'Annuler', style: 'cancel' },
        { 
          text: 'Déconnexion', 
          style: 'destructive',
          onPress: async () => {
            await AsyncStorage.multiRemove(['user', 'access_token']);
            router.replace('/');
          }
        }
      ]
    );
  };

  const navigateToFavorites = () => {
    router.push('/favorites');
  };

  const navigateToSettings = () => {
    Alert.alert('Bientôt disponible', 'Cette fonctionnalité sera disponible prochainement');
  };

  const getLoyaltyLevel = (points: number) => {
    if (points >= 1000) return { level: 'Or', color: colors.gold, icon: 'star' };
    if (points >= 500) return { level: 'Argent', color: colors.gray, icon: 'medal' };
    if (points >= 100) return { level: 'Bronze', color: '#92400e', icon: 'trophy' };
    return { level: 'Nouveau', color: colors.primaryLight, icon: 'leaf' };
  };

  const getNextLevelPoints = (points: number) => {
    if (points < 100) return 100 - points;
    if (points < 500) return 500 - points;
    if (points < 1000) return 1000 - points;
    return 0; // Max level reached
  };

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <StatusBar style="light" backgroundColor={colors.primary} />
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color={colors.primaryLight} />
          <Text style={styles.loadingText}>Chargement du profil...</Text>
        </View>
      </SafeAreaView>
    );
  }

  if (!user) {
    return (
      <SafeAreaView style={styles.container}>
        <StatusBar style="light" backgroundColor={colors.primary} />
        <View style={styles.errorContainer}>
          <Ionicons name="person-circle-outline" size={64} color={colors.gray} />
          <Text style={styles.errorText}>Profil non trouvé</Text>
          <TouchableOpacity onPress={() => router.push('/login')} style={styles.loginButton}>
            <Text style={styles.loginButtonText}>Se connecter</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  const loyaltyInfo = getLoyaltyLevel(user.points);
  const nextLevelPoints = getNextLevelPoints(user.points);

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar style="light" backgroundColor={colors.primary} />
      
      <ScrollView style={styles.scrollView} showsVerticalScrollIndicator={false}>
        {/* Header with Profile */}
        <View style={styles.headerContainer}>
          <LinearGradient
            colors={[colors.primary, colors.primaryLight]}
            style={styles.headerGradient}
          >
            <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
              <Ionicons name="arrow-back" size={24} color={colors.white} />
            </TouchableOpacity>
            
            <View style={styles.profileSection}>
              <View style={styles.avatarContainer}>
                <Text style={styles.avatarText}>
                  {user.nom.charAt(0)}{user.prenom.charAt(0)}
                </Text>
              </View>
              
              <Text style={styles.userName}>{user.prenom} {user.nom}</Text>
              <Text style={styles.userEmail}>{user.email}</Text>
              <Text style={styles.memberSince}>Membre depuis {stats.memberSince}</Text>
            </View>
          </LinearGradient>
        </View>

        {/* Loyalty Program */}
        <View style={styles.loyaltyContainer}>
          <View style={styles.loyaltyHeader}>
            <Ionicons name={loyaltyInfo.icon as any} size={24} color={loyaltyInfo.color} />
            <Text style={styles.loyaltyTitle}>Programme de Fidélité</Text>
          </View>
          
          <View style={styles.loyaltyContent}>
            <View style={styles.pointsSection}>
              <Text style={styles.pointsValue}>{user.points}</Text>
              <Text style={styles.pointsLabel}>Points LCA</Text>
            </View>
            
            <View style={styles.levelSection}>
              <View style={[styles.levelBadge, { backgroundColor: loyaltyInfo.color }]}>
                <Text style={styles.levelText}>{loyaltyInfo.level}</Text>
              </View>
              
              {nextLevelPoints > 0 && (
                <Text style={styles.nextLevelText}>
                  Plus que {nextLevelPoints} points pour le niveau suivant
                </Text>
              )}
            </View>
          </View>
          
          {/* Progress Bar */}
          {nextLevelPoints > 0 && (
            <View style={styles.progressContainer}>
              <View style={styles.progressBar}>
                <View 
                  style={[
                    styles.progressFill, 
                    { 
                      width: `${((user.points % 500) / 500) * 100}%`,
                      backgroundColor: loyaltyInfo.color 
                    }
                  ]} 
                />
              </View>
            </View>
          )}
        </View>

        {/* Stats */}
        <View style={styles.statsContainer}>
          <Text style={styles.sectionTitle}>Mes Statistiques</Text>
          
          <View style={styles.statsGrid}>
            <View style={styles.statCard}>
              <Ionicons name="play-circle" size={32} color={colors.primaryLight} />
              <Text style={styles.statValue}>{stats.videosWatched}</Text>
              <Text style={styles.statLabel}>Vidéos regardées</Text>
            </View>
            
            <View style={styles.statCard}>
              <Ionicons name="heart" size={32} color={colors.error} />
              <Text style={styles.statValue}>{stats.favoriteCount}</Text>
              <Text style={styles.statLabel}>Favoris</Text>
            </View>
            
            <View style={styles.statCard}>
              <Ionicons name="trophy" size={32} color={colors.gold} />
              <Text style={styles.statValue}>{user.points}</Text>
              <Text style={styles.statLabel}>Points totaux</Text>
            </View>
          </View>
        </View>

        {/* Quick Actions */}
        <View style={styles.actionsContainer}>
          <Text style={styles.sectionTitle}>Actions Rapides</Text>
          
          <TouchableOpacity style={styles.actionItem} onPress={navigateToFavorites}>
            <View style={styles.actionIcon}>
              <Ionicons name="heart" size={24} color={colors.primaryLight} />
            </View>
            <View style={styles.actionContent}>
              <Text style={styles.actionTitle}>Mes Favoris</Text>
              <Text style={styles.actionDescription}>
                {stats.favoriteCount} vidéos sauvegardées
              </Text>
            </View>
            <Ionicons name="chevron-forward" size={20} color={colors.gray} />
          </TouchableOpacity>
          
          <TouchableOpacity style={styles.actionItem} onPress={() => router.push('/news')}>
            <View style={styles.actionIcon}>
              <Ionicons name="newspaper" size={24} color={colors.blue} />
            </View>
            <View style={styles.actionContent}>
              <Text style={styles.actionTitle}>Actualités</Text>
              <Text style={styles.actionDescription}>Toute l'info du Burkina Faso</Text>
            </View>
            <Ionicons name="chevron-forward" size={20} color={colors.gray} />
          </TouchableOpacity>
          
          <TouchableOpacity style={styles.actionItem} onPress={() => router.push('/live')}>
            <View style={styles.actionIcon}>
              <Ionicons name="radio" size={24} color={colors.error} />
            </View>
            <View style={styles.actionContent}>
              <Text style={styles.actionTitle}>Direct</Text>
              <Text style={styles.actionDescription}>Regarder LCA TV en direct</Text>
            </View>
            <Ionicons name="chevron-forward" size={20} color={colors.gray} />
          </TouchableOpacity>
          
          <TouchableOpacity style={styles.actionItem} onPress={navigateToSettings}>
            <View style={styles.actionIcon}>
              <Ionicons name="settings" size={24} color={colors.gray} />
            </View>
            <View style={styles.actionContent}>
              <Text style={styles.actionTitle}>Paramètres</Text>
              <Text style={styles.actionDescription}>Gérer votre compte</Text>
            </View>
            <Ionicons name="chevron-forward" size={20} color={colors.gray} />
          </TouchableOpacity>
        </View>

        {/* How to Earn Points */}
        <View style={styles.pointsGuideContainer}>
          <Text style={styles.sectionTitle}>Comment gagner des points ?</Text>
          
          <View style={styles.pointsGuideList}>
            <View style={styles.pointsGuideItem}>
              <Ionicons name="play-circle" size={20} color={colors.primaryLight} />
              <Text style={styles.pointsGuideText}>+2 points par vidéo regardée</Text>
            </View>
            
            <View style={styles.pointsGuideItem}>
              <Ionicons name="heart-circle" size={20} color={colors.error} />
              <Text style={styles.pointsGuideText}>+5 points par favori ajouté</Text>
            </View>
            
            <View style={styles.pointsGuideItem}>
              <Ionicons name="person-add" size={20} color={colors.blue} />
              <Text style={styles.pointsGuideText}>+100 points à l'inscription</Text>
            </View>
          </View>
        </View>

        {/* Logout Button */}
        <View style={styles.logoutContainer}>
          <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
            <Ionicons name="log-out" size={20} color={colors.error} />
            <Text style={styles.logoutText}>Se déconnecter</Text>
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
  },
  loadingText: {
    fontSize: 16,
    color: colors.gray,
    marginTop: 10,
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  errorText: {
    fontSize: 18,
    color: colors.gray,
    marginTop: 15,
    marginBottom: 20,
  },
  loginButton: {
    backgroundColor: colors.primaryLight,
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 20,
  },
  loginButtonText: {
    color: colors.white,
    fontWeight: 'bold',
  },
  scrollView: {
    flex: 1,
  },
  headerContainer: {
    marginBottom: 20,
  },
  headerGradient: {
    paddingTop: 20,
    paddingBottom: 40,
    paddingHorizontal: 20,
    position: 'relative',
  },
  backButton: {
    position: 'absolute',
    top: 20,
    left: 20,
    padding: 5,
  },
  profileSection: {
    alignItems: 'center',
    marginTop: 40,
  },
  avatarContainer: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: colors.white,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 15,
  },
  avatarText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: colors.primary,
  },
  userName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: colors.white,
    marginBottom: 5,
  },
  userEmail: {
    fontSize: 16,
    color: colors.white,
    opacity: 0.9,
    marginBottom: 5,
  },
  memberSince: {
    fontSize: 14,
    color: colors.white,
    opacity: 0.7,
  },
  loyaltyContainer: {
    marginHorizontal: 20,
    backgroundColor: colors.white,
    borderRadius: 15,
    padding: 20,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  loyaltyHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 15,
  },
  loyaltyTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: colors.black,
    marginLeft: 10,
  },
  loyaltyContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
  },
  pointsSection: {
    alignItems: 'center',
  },
  pointsValue: {
    fontSize: 32,
    fontWeight: 'bold',
    color: colors.primaryLight,
  },
  pointsLabel: {
    fontSize: 14,
    color: colors.gray,
  },
  levelSection: {
    alignItems: 'center',
  },
  levelBadge: {
    paddingHorizontal: 15,
    paddingVertical: 8,
    borderRadius: 20,
    marginBottom: 5,
  },
  levelText: {
    color: colors.white,
    fontSize: 14,
    fontWeight: 'bold',
  },
  nextLevelText: {
    fontSize: 12,
    color: colors.gray,
    textAlign: 'center',
  },
  progressContainer: {
    marginTop: 10,
  },
  progressBar: {
    height: 8,
    backgroundColor: colors.lightGray,
    borderRadius: 4,
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    borderRadius: 4,
  },
  statsContainer: {
    paddingHorizontal: 20,
    marginBottom: 20,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: colors.black,
    marginBottom: 15,
  },
  statsGrid: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  statCard: {
    flex: 1,
    backgroundColor: colors.lightGray,
    borderRadius: 12,
    padding: 15,
    alignItems: 'center',
    marginHorizontal: 5,
  },
  statValue: {
    fontSize: 20,
    fontWeight: 'bold',
    color: colors.black,
    marginTop: 5,
  },
  statLabel: {
    fontSize: 12,
    color: colors.gray,
    textAlign: 'center',
    marginTop: 5,
  },
  actionsContainer: {
    paddingHorizontal: 20,
    marginBottom: 20,
  },
  actionItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.white,
    paddingVertical: 15,
    paddingHorizontal: 15,
    borderRadius: 12,
    marginBottom: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 2,
    elevation: 2,
  },
  actionIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: colors.lightGray,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 15,
  },
  actionContent: {
    flex: 1,
  },
  actionTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: colors.black,
    marginBottom: 2,
  },
  actionDescription: {
    fontSize: 14,
    color: colors.gray,
  },
  pointsGuideContainer: {
    paddingHorizontal: 20,
    marginBottom: 20,
  },
  pointsGuideList: {
    backgroundColor: colors.lightGray,
    borderRadius: 12,
    padding: 15,
  },
  pointsGuideItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  pointsGuideText: {
    fontSize: 14,
    color: colors.black,
    marginLeft: 10,
  },
  logoutContainer: {
    paddingHorizontal: 20,
    paddingBottom: 30,
  },
  logoutButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.white,
    paddingVertical: 15,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: colors.error,
  },
  logoutText: {
    fontSize: 16,
    color: colors.error,
    fontWeight: '600',
    marginLeft: 8,
  },
});