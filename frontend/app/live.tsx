import React, { useState, useRef, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Alert,
  Dimensions,
  ActivityIndicator,
  Image,
} from 'react-native';
import { LinearGradient } from 'expo-linear-gradient';
import { SafeAreaView } from 'react-native-safe-area-context';
import { StatusBar } from 'expo-status-bar';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
// import YoutubePlayer from 'react-native-youtube-iframe';

const { width: screenWidth, height: screenHeight } = Dimensions.get('window');

// LCA TV Theme colors
const colors = {
  primary: '#2d5016',
  primaryLight: '#22c55e',
  secondary: '#16a34a',
  blue: '#3b82f6',
  white: '#ffffff',
  gray: '#6b7280',
  black: '#111827',
  error: '#ef4444',
  transparent: 'transparent',
};

const LIVE_VIDEO_ID = 'ixQEmhTbvTI'; // Default LCA TV live stream

export default function LiveScreen() {
  const [playing, setPlaying] = useState(false);
  const [fullscreen, setFullscreen] = useState(false);
  const [loading, setLoading] = useState(true);
  const [viewerCount, setViewerCount] = useState(1250);
  const [isLive, setIsLive] = useState(true);
  const playerRef = useRef(null);
  const router = useRouter();

  useEffect(() => {
    // Simulate viewer count updates
    const interval = setInterval(() => {
      setViewerCount(prev => prev + Math.floor(Math.random() * 10) - 5);
    }, 30000); // Update every 30 seconds

    return () => clearInterval(interval);
  }, []);

  const onStateChange = (state: string) => {
    if (state === 'ended') {
      setPlaying(false);
    }
  };

  const onReady = () => {
    setLoading(false);
  };

  const onError = (error: string) => {
    console.error('YouTube Player Error:', error);
    setLoading(false);
    Alert.alert(
      'Erreur de lecture',
      'Impossible de charger le stream en direct. Vérifiez votre connexion internet.',
      [
        { text: 'Réessayer', onPress: () => setLoading(true) },
        { text: 'Retour', onPress: () => router.back() }
      ]
    );
  };

  const toggleFullscreen = () => {
    setFullscreen(!fullscreen);
  };

  const shareStream = () => {
    Alert.alert(
      'Partager le direct',
      'Partagez le direct de LCA TV avec vos amis !',
      [
        { text: 'WhatsApp', onPress: () => console.log('Share WhatsApp') },
        { text: 'Facebook', onPress: () => console.log('Share Facebook') },
        { text: 'Twitter', onPress: () => console.log('Share Twitter') },
        { text: 'Annuler', style: 'cancel' }
      ]
    );
  };

  const togglePlay = () => {
    setPlaying(!playing);
  };

  if (fullscreen) {
    return (
      <View style={styles.fullscreenContainer}>
        <StatusBar style="light" hidden />
        <YoutubePlayer
          ref={playerRef}
          height={screenHeight}
          width={screenWidth}
          play={playing}
          videoId={LIVE_VIDEO_ID}
          onChangeState={onStateChange}
          onReady={onReady}
          onError={onError}
          webViewStyle={styles.webView}
          initialPlayerParams={{
            loop: false,
            controls: true,
            modestbranding: true,
            rel: false,
            showinfo: false,
          }}
        />
        <TouchableOpacity 
          style={styles.exitFullscreenButton}
          onPress={toggleFullscreen}
        >
          <Ionicons name="contract" size={24} color={colors.white} />
        </TouchableOpacity>
      </View>
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
          <Text style={styles.headerTitle}>LCA TV - Direct</Text>
          {isLive && (
            <View style={styles.liveIndicator}>
              <View style={styles.liveDot} />
              <Text style={styles.liveText}>EN DIRECT</Text>
            </View>
          )}
        </View>
        
        <TouchableOpacity onPress={shareStream} style={styles.shareButton}>
          <Ionicons name="share-social" size={24} color={colors.white} />
        </TouchableOpacity>
      </View>

      {/* Video Player Placeholder */}
      <View style={styles.playerContainer}>
        <View style={styles.videoPlaceholder}>
          <Image
            source={{ uri: 'https://i.ytimg.com/vi/ixQEmhTbvTI/maxresdefault.jpg' }}
            style={styles.placeholderImage}
            resizeMode="cover"
          />
          <LinearGradient
            colors={['transparent', 'rgba(0,0,0,0.7)']}
            style={styles.videoOverlay}
          >
            <TouchableOpacity onPress={togglePlay} style={styles.playButton}>
              <Ionicons 
                name={playing ? "pause" : "play"} 
                size={48} 
                color={colors.white} 
              />
            </TouchableOpacity>
            <Text style={styles.liveLabel}>EN DIRECT</Text>
          </LinearGradient>
        </View>
        
        <View style={styles.playerControls}>
          <TouchableOpacity onPress={toggleFullscreen} style={styles.fullscreenBtn}>
            <Ionicons name="expand" size={24} color={colors.white} />
          </TouchableOpacity>
        </View>
      </View>

      {/* Stream Info */}
      <View style={styles.streamInfo}>
        <View style={styles.streamHeader}>
          <View style={styles.logoContainer}>
            <Text style={styles.logoText}>LCA</Text>
            <View style={styles.logoCircle}>
              <Text style={styles.logoSubText}>TV</Text>
            </View>
          </View>
          
          <View style={styles.streamDetails}>
            <Text style={styles.streamTitle}>Diffusion en direct de LCA TV</Text>
            <Text style={styles.streamDescription}>
              Votre chaîne de référence au Burkina Faso
            </Text>
            <View style={styles.viewerInfo}>
              <Ionicons name="eye" size={16} color={colors.primaryLight} />
              <Text style={styles.viewerCount}>{viewerCount.toLocaleString()} spectateurs</Text>
            </View>
          </View>
        </View>
      </View>

      {/* Program Schedule */}
      <View style={styles.scheduleContainer}>
        <Text style={styles.scheduleTitle}>Programme du jour</Text>
        
        <View style={styles.scheduleItem}>
          <Text style={styles.scheduleTime}>19:00</Text>
          <View style={styles.scheduleContent}>
            <Text style={styles.scheduleProgram}>Journal LCA TV</Text>
            <Text style={styles.scheduleDuration}>30 min</Text>
          </View>
          <View style={[styles.scheduleStatus, { backgroundColor: colors.primaryLight }]}>
            <Text style={styles.scheduleStatusText}>EN COURS</Text>
          </View>
        </View>
        
        <View style={styles.scheduleItem}>
          <Text style={styles.scheduleTime}>19:30</Text>
          <View style={styles.scheduleContent}>
            <Text style={styles.scheduleProgram}>Franc-Parler</Text>
            <Text style={styles.scheduleDuration}>45 min</Text>
          </View>
          <View style={[styles.scheduleStatus, { backgroundColor: colors.gray }]}>
            <Text style={styles.scheduleStatusText}>À SUIVRE</Text>
          </View>
        </View>
        
        <View style={styles.scheduleItem}>
          <Text style={styles.scheduleTime}>20:15</Text>
          <View style={styles.scheduleContent}>
            <Text style={styles.scheduleProgram}>Questions de Femmes</Text>
            <Text style={styles.scheduleDuration}>30 min</Text>
          </View>
          <View style={[styles.scheduleStatus, { backgroundColor: colors.gray }]}>
            <Text style={styles.scheduleStatusText}>À SUIVRE</Text>
          </View>
        </View>
      </View>

      {/* Action Buttons */}
      <View style={styles.actionButtons}>
        <TouchableOpacity 
          style={styles.actionButton}
          onPress={() => router.push('/replay')}
        >
          <Ionicons name="play-circle" size={24} color={colors.primaryLight} />
          <Text style={styles.actionButtonText}>Voir les replays</Text>
        </TouchableOpacity>
        
        <TouchableOpacity 
          style={styles.actionButton}
          onPress={() => router.push('/news')}
        >
          <Ionicons name="newspaper" size={24} color={colors.primaryLight} />
          <Text style={styles.actionButtonText}>Actualités</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.white,
  },
  fullscreenContainer: {
    flex: 1,
    backgroundColor: colors.black,
    justifyContent: 'center',
    alignItems: 'center',
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
    fontSize: 18,
    fontWeight: 'bold',
    color: colors.white,
    marginBottom: 5,
  },
  liveIndicator: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  liveDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: '#ff4444',
    marginRight: 5,
  },
  liveText: {
    fontSize: 12,
    color: colors.white,
    fontWeight: 'bold',
  },
  shareButton: {
    padding: 5,
  },
  playerContainer: {
    position: 'relative',
    backgroundColor: colors.black,
  },
  webView: {
    backgroundColor: colors.black,
  },
  loadingOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: colors.black,
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 1,
  },
  loadingText: {
    color: colors.white,
    marginTop: 10,
    fontSize: 16,
  },
  playerControls: {
    position: 'absolute',
    bottom: 20,
    left: 20,
    right: 20,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  playButton: {
    backgroundColor: 'rgba(0,0,0,0.7)',
    borderRadius: 25,
    padding: 10,
  },
  fullscreenBtn: {
    backgroundColor: 'rgba(0,0,0,0.7)',
    borderRadius: 20,
    padding: 8,
  },
  exitFullscreenButton: {
    position: 'absolute',
    top: 50,
    right: 20,
    backgroundColor: 'rgba(0,0,0,0.7)',
    borderRadius: 20,
    padding: 10,
  },
  videoPlaceholder: {
    height: 250,
    width: '100%',
    position: 'relative',
    backgroundColor: colors.black,
  },
  placeholderImage: {
    width: '100%',
    height: '100%',
  },
  videoOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    justifyContent: 'center',
    alignItems: 'center',
  },
  liveLabel: {
    position: 'absolute',
    top: 20,
    right: 20,
    backgroundColor: '#ff4444',
    color: colors.white,
    fontSize: 12,
    fontWeight: 'bold',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
  },
  streamInfo: {
    backgroundColor: colors.white,
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: colors.lightGray,
  },
  streamHeader: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  logoContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginRight: 15,
  },
  logoText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: colors.primary,
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
  streamDetails: {
    flex: 1,
  },
  streamTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: colors.black,
    marginBottom: 5,
  },
  streamDescription: {
    fontSize: 14,
    color: colors.gray,
    marginBottom: 8,
  },
  viewerInfo: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  viewerCount: {
    fontSize: 14,
    color: colors.primaryLight,
    fontWeight: '600',
    marginLeft: 5,
  },
  scheduleContainer: {
    backgroundColor: colors.white,
    padding: 20,
  },
  scheduleTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: colors.black,
    marginBottom: 15,
  },
  scheduleItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: colors.lightGray,
  },
  scheduleTime: {
    fontSize: 16,
    fontWeight: 'bold',
    color: colors.primary,
    width: 60,
  },
  scheduleContent: {
    flex: 1,
    marginLeft: 15,
  },
  scheduleProgram: {
    fontSize: 16,
    fontWeight: '600',
    color: colors.black,
    marginBottom: 2,
  },
  scheduleDuration: {
    fontSize: 14,
    color: colors.gray,
  },
  scheduleStatus: {
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 8,
  },
  scheduleStatusText: {
    fontSize: 10,
    fontWeight: 'bold',
    color: colors.white,
  },
  actionButtons: {
    flexDirection: 'row',
    padding: 20,
    justifyContent: 'space-around',
  },
  actionButton: {
    alignItems: 'center',
    padding: 15,
  },
  actionButtonText: {
    fontSize: 14,
    color: colors.primaryLight,
    fontWeight: '600',
    marginTop: 5,
  },
});