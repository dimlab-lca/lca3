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
  success: '#10b981',
};

export default function RegisterScreen() {
  const [formData, setFormData] = useState({
    nom: '',
    prenom: '',
    email: '',
    telephone: '',
    password: '',
    confirmPassword: '',
  });
  const [acceptCGU, setAcceptCGU] = useState(false);
  const [newsletter, setNewsletter] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [validation, setValidation] = useState({
    nom: true,
    prenom: true,
    email: true,
    telephone: true,
    password: true,
    confirmPassword: true,
  });
  
  const router = useRouter();

  const updateFormData = (field: string, value: string) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    // Real-time validation
    validateField(field, value);
  };

  const validateField = (field: string, value: string) => {
    let isValid = true;
    
    switch (field) {
      case 'nom':
      case 'prenom':
        isValid = value.trim().length >= 2;
        break;
      case 'email':
        isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
        break;
      case 'telephone':
        isValid = /^(\+226)?[0-9]{8}$/.test(value.replace(/\s+/g, ''));
        break;
      case 'password':
        isValid = value.length >= 6;
        break;
      case 'confirmPassword':
        isValid = value === formData.password;
        break;
    }
    
    setValidation(prev => ({ ...prev, [field]: isValid }));
    return isValid;
  };

  const validateAllFields = () => {
    const fields = ['nom', 'prenom', 'email', 'telephone', 'password', 'confirmPassword'];
    let allValid = true;
    
    fields.forEach(field => {
      const isValid = validateField(field, formData[field]);
      if (!isValid) allValid = false;
    });
    
    return allValid;
  };

  const handleRegister = async () => {
    if (!validateAllFields()) {
      Alert.alert('Erreur', 'Veuillez corriger les champs en erreur');
      return;
    }

    if (!acceptCGU) {
      Alert.alert('Erreur', 'Vous devez accepter les conditions générales d\'utilisation');
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      Alert.alert('Erreur', 'Les mots de passe ne correspondent pas');
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${process.env.EXPO_PUBLIC_BACKEND_URL}/api/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          nom: formData.nom.trim(),
          prenom: formData.prenom.trim(),
          email: formData.email.toLowerCase().trim(),
          telephone: formData.telephone.replace(/\s+/g, ''),
          password: formData.password,
          confirm_password: formData.confirmPassword,
          accept_cgu: acceptCGU,
          newsletter: newsletter,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        // Store user data and token
        await AsyncStorage.setItem('user', JSON.stringify(data.user));
        await AsyncStorage.setItem('access_token', data.access_token);
        
        Alert.alert(
          'Inscription réussie !', 
          `Bienvenue ${data.user.prenom} ! Vous avez reçu 100 points de bienvenue.`,
          [{ text: 'OK', onPress: () => router.replace('/') }]
        );
      } else {
        Alert.alert('Erreur d\'inscription', data.detail || 'Une erreur est survenue');
      }
    } catch (error) {
      console.error('Register error:', error);
      Alert.alert('Erreur', 'Problème de connexion. Veuillez réessayer.');
    } finally {
      setLoading(false);
    }
  };

  const navigateToLogin = () => {
    router.push('/login');
  };

  const formatPhoneNumber = (text: string) => {
    // Remove all non-digits
    const cleaned = text.replace(/\D/g, '');
    
    // Format as XX XX XX XX
    if (cleaned.length <= 2) return cleaned;
    if (cleaned.length <= 4) return cleaned.replace(/(\d{2})/, '$1 ');
    if (cleaned.length <= 6) return cleaned.replace(/(\d{2})(\d{2})/, '$1 $2 ');
    return cleaned.replace(/(\d{2})(\d{2})(\d{2})(\d{2})/, '$1 $2 $3 $4');
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
            <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
              <Ionicons name="arrow-back" size={24} color={colors.white} />
            </TouchableOpacity>
            
            <View style={styles.logoContainer}>
              <Text style={styles.logoText}>LCA</Text>
              <View style={styles.logoCircle}>
                <Text style={styles.logoSubText}>TV</Text>
              </View>
            </View>
            <Text style={styles.tagline}>La Chaîne Africaine de télévision</Text>
            <Text style={styles.welcomeText}>Créer votre compte</Text>
          </View>

          {/* Registration Form */}
          <View style={styles.formContainer}>
            {/* Nom */}
            <View style={[styles.inputContainer, !validation.nom && styles.inputError]}>
              <Ionicons name="person" size={20} color={colors.gray} style={styles.inputIcon} />
              <TextInput
                style={styles.input}
                placeholder="Nom"
                placeholderTextColor={colors.gray}
                value={formData.nom}
                onChangeText={(text) => updateFormData('nom', text)}
                autoCapitalize="words"
              />
              {validation.nom && formData.nom.length > 0 && (
                <Ionicons name="checkmark-circle" size={20} color={colors.success} />
              )}
            </View>

            {/* Prenom */}
            <View style={[styles.inputContainer, !validation.prenom && styles.inputError]}>
              <Ionicons name="person" size={20} color={colors.gray} style={styles.inputIcon} />
              <TextInput
                style={styles.input}
                placeholder="Prénom"
                placeholderTextColor={colors.gray}
                value={formData.prenom}
                onChangeText={(text) => updateFormData('prenom', text)}
                autoCapitalize="words"
              />
              {validation.prenom && formData.prenom.length > 0 && (
                <Ionicons name="checkmark-circle" size={20} color={colors.success} />
              )}
            </View>

            {/* Email */}
            <View style={[styles.inputContainer, !validation.email && styles.inputError]}>
              <Ionicons name="mail" size={20} color={colors.gray} style={styles.inputIcon} />
              <TextInput
                style={styles.input}
                placeholder="Email"
                placeholderTextColor={colors.gray}
                value={formData.email}
                onChangeText={(text) => updateFormData('email', text)}
                keyboardType="email-address"
                autoCapitalize="none"
                autoComplete="email"
              />
              {validation.email && formData.email.length > 0 && (
                <Ionicons name="checkmark-circle" size={20} color={colors.success} />
              )}
            </View>

            {/* Telephone */}
            <View style={[styles.inputContainer, !validation.telephone && styles.inputError]}>
              <Ionicons name="call" size={20} color={colors.gray} style={styles.inputIcon} />
              <Text style={styles.countryCode}>+226</Text>
              <TextInput
                style={styles.input}
                placeholder="XX XX XX XX"
                placeholderTextColor={colors.gray}
                value={formData.telephone}
                onChangeText={(text) => updateFormData('telephone', formatPhoneNumber(text))}
                keyboardType="phone-pad"
                maxLength={11}
              />
              {validation.telephone && formData.telephone.replace(/\s+/g, '').length === 8 && (
                <Ionicons name="checkmark-circle" size={20} color={colors.success} />
              )}
            </View>

            {/* Password */}
            <View style={[styles.inputContainer, !validation.password && styles.inputError]}>
              <Ionicons name="lock-closed" size={20} color={colors.gray} style={styles.inputIcon} />
              <TextInput
                style={[styles.input, { flex: 1 }]}
                placeholder="Mot de passe (min. 6 caractères)"
                placeholderTextColor={colors.gray}
                value={formData.password}
                onChangeText={(text) => updateFormData('password', text)}
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

            {/* Confirm Password */}
            <View style={[styles.inputContainer, !validation.confirmPassword && styles.inputError]}>
              <Ionicons name="lock-closed" size={20} color={colors.gray} style={styles.inputIcon} />
              <TextInput
                style={[styles.input, { flex: 1 }]}
                placeholder="Confirmer le mot de passe"
                placeholderTextColor={colors.gray}
                value={formData.confirmPassword}
                onChangeText={(text) => updateFormData('confirmPassword', text)}
                secureTextEntry={!showConfirmPassword}
              />
              <TouchableOpacity 
                onPress={() => setShowConfirmPassword(!showConfirmPassword)}
                style={styles.eyeIcon}
              >
                <Ionicons 
                  name={showConfirmPassword ? "eye" : "eye-off"} 
                  size={20} 
                  color={colors.gray} 
                />
              </TouchableOpacity>
            </View>

            {/* Checkboxes */}
            <View style={styles.checkboxSection}>
              <TouchableOpacity 
                style={styles.checkboxContainer}
                onPress={() => setAcceptCGU(!acceptCGU)}
              >
                <View style={[styles.checkbox, acceptCGU && styles.checkboxChecked]}>
                  {acceptCGU && <Ionicons name="checkmark" size={14} color={colors.white} />}
                </View>
                <Text style={styles.checkboxText}>
                  J'accepte les{' '}
                  <Text style={styles.linkText}>conditions générales d'utilisation</Text>
                </Text>
              </TouchableOpacity>

              <TouchableOpacity 
                style={styles.checkboxContainer}
                onPress={() => setNewsletter(!newsletter)}
              >
                <View style={[styles.checkbox, newsletter && styles.checkboxChecked]}>
                  {newsletter && <Ionicons name="checkmark" size={14} color={colors.white} />}
                </View>
                <Text style={styles.checkboxText}>
                  Je souhaite recevoir la newsletter LCA TV
                </Text>
              </TouchableOpacity>
            </View>

            {/* Register Button */}
            <TouchableOpacity 
              style={styles.registerButtonContainer}
              onPress={handleRegister}
              disabled={loading}
            >
              <LinearGradient
                colors={[colors.primary, colors.primaryLight]}
                style={styles.registerButton}
              >
                {loading ? (
                  <ActivityIndicator size="small" color={colors.white} />
                ) : (
                  <Text style={styles.registerButtonText}>Créer mon compte</Text>
                )}
              </LinearGradient>
            </TouchableOpacity>

            {/* Login Link */}
            <View style={styles.loginContainer}>
              <Text style={styles.loginPrompt}>Vous avez déjà un compte ?</Text>
              <TouchableOpacity onPress={navigateToLogin}>
                <Text style={styles.loginLink}>Se connecter</Text>
              </TouchableOpacity>
            </View>
          </View>

          {/* Benefits */}
          <View style={styles.benefitsContainer}>
            <Text style={styles.benefitsTitle}>En créant votre compte :</Text>
            <View style={styles.benefitItem}>
              <Ionicons name="gift" size={16} color={colors.primaryLight} />
              <Text style={styles.benefitText}>100 points de bienvenue offerts</Text>
            </View>
            <View style={styles.benefitItem}>
              <Ionicons name="star" size={16} color={colors.primaryLight} />
              <Text style={styles.benefitText}>Accès aux contenus exclusifs</Text>
            </View>
            <View style={styles.benefitItem}>
              <Ionicons name="heart" size={16} color={colors.primaryLight} />
              <Text style={styles.benefitText}>Sauvegarde de vos favoris</Text>
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
    paddingVertical: 30,
    borderBottomLeftRadius: 30,
    borderBottomRightRadius: 30,
    alignItems: 'center',
    position: 'relative',
  },
  backButton: {
    position: 'absolute',
    left: 20,
    top: 30,
    padding: 10,
  },
  logoContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  logoText: {
    fontSize: 36,
    fontWeight: 'bold',
    color: colors.white,
    marginRight: 12,
  },
  logoCircle: {
    width: 32,
    height: 32,
    borderRadius: 16,
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
    marginBottom: 10,
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
    paddingTop: 30,
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
  inputError: {
    borderWidth: 1,
    borderColor: colors.error,
  },
  inputIcon: {
    marginRight: 10,
  },
  countryCode: {
    fontSize: 16,
    color: colors.black,
    fontWeight: '600',
    marginRight: 5,
  },
  input: {
    flex: 1,
    fontSize: 16,
    color: colors.black,
  },
  eyeIcon: {
    padding: 5,
  },
  checkboxSection: {
    marginVertical: 20,
  },
  checkboxContainer: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginBottom: 15,
  },
  checkbox: {
    width: 20,
    height: 20,
    borderRadius: 4,
    borderWidth: 2,
    borderColor: colors.gray,
    marginRight: 12,
    marginTop: 2,
    justifyContent: 'center',
    alignItems: 'center',
  },
  checkboxChecked: {
    backgroundColor: colors.primaryLight,
    borderColor: colors.primaryLight,
  },
  checkboxText: {
    fontSize: 14,
    color: colors.black,
    flex: 1,
    lineHeight: 20,
  },
  linkText: {
    color: colors.primaryLight,
    fontWeight: '600',
  },
  registerButtonContainer: {
    borderRadius: 15,
    overflow: 'hidden',
    marginTop: 10,
    marginBottom: 30,
  },
  registerButton: {
    paddingVertical: 18,
    alignItems: 'center',
    justifyContent: 'center',
  },
  registerButtonText: {
    color: colors.white,
    fontSize: 18,
    fontWeight: 'bold',
  },
  loginContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 30,
  },
  loginPrompt: {
    fontSize: 16,
    color: colors.gray,
    marginRight: 5,
  },
  loginLink: {
    fontSize: 16,
    color: colors.primaryLight,
    fontWeight: 'bold',
  },
  benefitsContainer: {
    paddingHorizontal: 30,
    paddingVertical: 20,
  },
  benefitsTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: colors.black,
    marginBottom: 15,
    textAlign: 'center',
  },
  benefitItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  benefitText: {
    fontSize: 14,
    color: colors.gray,
    marginLeft: 10,
  },
});