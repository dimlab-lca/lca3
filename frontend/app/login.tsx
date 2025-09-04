import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  Alert,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
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
  darkGreen: '#22543d',
  white: '#ffffff',
  gray: '#6b7280',
  lightGray: '#f3f4f6',
  black: '#111827',
  error: '#ef4444',
};

export default function LoginScreen() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleLogin = async () => {
    if (!email || !password) {
      Alert.alert('Erreur', 'Veuillez remplir tous les champs');
      return;
    }

    if (!isValidEmail(email)) {
      Alert.alert('Erreur', 'Veuillez entrer un email valide');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${process.env.EXPO_PUBLIC_BACKEND_URL}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: email.toLowerCase().trim(),
          password,
          remember_me: rememberMe,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        // Store user data and token
        await AsyncStorage.setItem('user', JSON.stringify(data.user));
        await AsyncStorage.setItem('access_token', data.access_token);
        
        Alert.alert(
          'Connexion réussie', 
          `Bienvenue ${data.user.prenom} !`,
          [{ text: 'OK', onPress: () => router.replace('/') }]
        );
      } else {
        Alert.alert('Erreur de connexion', data.detail || 'Email ou mot de passe incorrect');
      }
    } catch (error) {
      console.error('Login error:', error);
      Alert.alert('Erreur', 'Problème de connexion. Veuillez réessayer.');
    } finally {
      setLoading(false);
    }
  };

  const navigateToRegister = () => {
    router.push('/register');
  };

  const handleForgotPassword = () => {
    Alert.alert(
      'Mot de passe oublié',
      'Contactez-nous à contact@lcatv.bf pour réinitialiser votre mot de passe.',
      [{ text: 'OK' }]
    );
  };

  const isValidEmail = (email: string) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar style="light" backgroundColor={colors.primary} />
      
      <KeyboardAvoidingView 
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.keyboardView}
      >
        <ScrollView contentContainerStyle={styles.scrollContent} showsVerticalScrollIndicator={false}>
          {/* Header with logo */}
          <View style={styles.header}>
            <View style={styles.logoContainer}>
              <Text style={styles.logoText}>LCA</Text>
              <View style={styles.logoCircle}>
                <Text style={styles.logoSubText}>TV</Text>
              </View>
            </View>
            <Text style={styles.tagline}>La Chaîne Africaine de télévision</Text>
            <Text style={styles.welcomeText}>Connectez-vous à votre compte</Text>
          </View>

          {/* Login Form */}
          <View style={styles.formContainer}>
            <View style={styles.inputContainer}>
              <Ionicons name="mail" size={20} color={colors.gray} style={styles.inputIcon} />
              <TextInput
                style={styles.input}
                placeholder="Email ou téléphone"
                placeholderTextColor={colors.gray}
                value={email}
                onChangeText={setEmail}
                keyboardType="email-address"
                autoCapitalize="none"
                autoComplete="email"
              />
            </View>

            <View style={styles.inputContainer}>
              <Ionicons name="lock-closed" size={20} color={colors.gray} style={styles.inputIcon} />
              <TextInput
                style={[styles.input, { flex: 1 }]}
                placeholder="Mot de passe"
                placeholderTextColor={colors.gray}
                value={password}
                onChangeText={setPassword}
                secureTextEntry={!showPassword}
              />
              <TouchableOpacity 
                onPress={() => setShowPassword(!showPassword)}
                style={styles.eyeIcon}
              >
                <Ionicons 
                  name={showPassword ? "eye" : "eye-off"} 
                  size={20} 
                  color={colors.gray} 
                />
              </TouchableOpacity>
            </View>

            {/* Remember me & Forgot password */}
            <View style={styles.optionsContainer}>
              <TouchableOpacity 
                style={styles.rememberContainer}
                onPress={() => setRememberMe(!rememberMe)}
              >
                <View style={[styles.checkbox, rememberMe && styles.checkboxChecked]}>
                  {rememberMe && <Ionicons name="checkmark" size={14} color={colors.white} />}
                </View>
                <Text style={styles.rememberText}>Rester connecté</Text>
              </TouchableOpacity>

              <TouchableOpacity onPress={handleForgotPassword}>
                <Text style={styles.forgotText}>Mot de passe oublié ?</Text>
              </TouchableOpacity>
            </View>

            {/* Login Button */}
            <TouchableOpacity 
              style={styles.loginButtonContainer}
              onPress={handleLogin}
              disabled={loading}
            >
              <LinearGradient
                colors={[colors.primary, colors.primaryLight]}
                style={styles.loginButton}
              >
                {loading ? (
                  <ActivityIndicator size="small" color={colors.white} />
                ) : (
                  <Text style={styles.loginButtonText}>Se connecter</Text>
                )}
              </LinearGradient>
            </TouchableOpacity>

            {/* Register Link */}
            <View style={styles.registerContainer}>
              <Text style={styles.registerPrompt}>Vous n'avez pas de compte ?</Text>
              <TouchableOpacity onPress={navigateToRegister}>
                <Text style={styles.registerLink}>Créer un compte</Text>
              </TouchableOpacity>
            </View>
          </View>

          {/* Features Section */}
          <View style={styles.featuresContainer}>
            <Text style={styles.featuresTitle}>Avec votre compte LCA TV :</Text>
            <View style={styles.featureItem}>
              <Ionicons name="heart" size={16} color={colors.primaryLight} />
              <Text style={styles.featureText}>Sauvegardez vos vidéos favorites</Text>
            </View>
            <View style={styles.featureItem}>
              <Ionicons name="trophy" size={16} color={colors.primaryLight} />
              <Text style={styles.featureText}>Gagnez des points de fidélité</Text>
            </View>
            <View style={styles.featureItem}>
              <Ionicons name="notifications" size={16} color={colors.primaryLight} />
              <Text style={styles.featureText}>Recevez les notifications exclusives</Text>
            </View>
            <View style={styles.featureItem}>
              <Ionicons name="download" size={16} color={colors.primaryLight} />
              <Text style={styles.featureText}>Téléchargez pour regarder hors ligne</Text>
            </View>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.white,
  },
  keyboardView: {
    flex: 1,
  },
  scrollContent: {
    flexGrow: 1,
  },
  header: {
    backgroundColor: colors.primary,
    paddingHorizontal: 30,
    paddingVertical: 40,
    borderBottomLeftRadius: 30,
    borderBottomRightRadius: 30,
    alignItems: 'center',
  },
  logoContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  logoText: {
    fontSize: 40,
    fontWeight: 'bold',
    color: colors.white,
    marginRight: 15,
  },
  logoCircle: {
    width: 35,
    height: 35,
    borderRadius: 17.5,
    backgroundColor: colors.blue,
    justifyContent: 'center',
    alignItems: 'center',
  },
  logoSubText: {
    fontSize: 14,
    fontWeight: 'bold',
    color: colors.white,
  },
  tagline: {
    fontSize: 16,
    color: colors.white,
    opacity: 0.9,
    marginBottom: 15,
    textAlign: 'center',
  },
  welcomeText: {
    fontSize: 18,
    color: colors.white,
    fontWeight: '600',
    textAlign: 'center',
  },
  formContainer: {
    paddingHorizontal: 30,
    paddingTop: 40,
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.lightGray,
    borderRadius: 15,
    paddingHorizontal: 15,
    paddingVertical: 15,
    marginBottom: 15,
  },
  inputIcon: {
    marginRight: 10,
  },
  input: {
    flex: 1,
    fontSize: 16,
    color: colors.black,
  },
  eyeIcon: {
    padding: 5,
  },
  optionsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 30,
  },
  rememberContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  checkbox: {
    width: 20,
    height: 20,
    borderRadius: 4,
    borderWidth: 2,
    borderColor: colors.gray,
    marginRight: 8,
    justifyContent: 'center',
    alignItems: 'center',
  },
  checkboxChecked: {
    backgroundColor: colors.primaryLight,
    borderColor: colors.primaryLight,
  },
  rememberText: {
    fontSize: 14,
    color: colors.black,
  },
  forgotText: {
    fontSize: 14,
    color: colors.primaryLight,
    fontWeight: '600',
  },
  loginButtonContainer: {
    borderRadius: 15,
    overflow: 'hidden',
    marginBottom: 30,
  },
  loginButton: {
    paddingVertical: 18,
    alignItems: 'center',
    justifyContent: 'center',
  },
  loginButtonText: {
    color: colors.white,
    fontSize: 18,
    fontWeight: 'bold',
  },
  registerContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 30,
  },
  registerPrompt: {
    fontSize: 16,
    color: colors.gray,
    marginRight: 5,
  },
  registerLink: {
    fontSize: 16,
    color: colors.primaryLight,
    fontWeight: 'bold',
  },
  featuresContainer: {
    paddingHorizontal: 30,
    paddingVertical: 20,
  },
  featuresTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: colors.black,
    marginBottom: 15,
    textAlign: 'center',
  },
  featureItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  featureText: {
    fontSize: 14,
    color: colors.gray,
    marginLeft: 10,
  },
});