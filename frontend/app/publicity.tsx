import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  TextInput,
  Alert,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { StatusBar } from 'expo-status-bar';
import { LinearGradient } from 'expo-linear-gradient';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';

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
  silver: '#6b7280',
  bronze: '#92400e',
};

interface Package {
  id: string;
  name: string;
  price: number;
  color: string;
  features: string[];
  popular?: boolean;
}

const packages: Package[] = [
  {
    id: 'basic',
    name: 'Package Basic',
    price: 50000,
    color: colors.bronze,
    features: [
      'Affichage sidebar uniquement',
      '1 annonce active',
      'Durée : 1 mois',
      'Support email',
      'Statistiques basiques'
    ]
  },
  {
    id: 'standard',
    name: 'Package Standard',
    price: 120000,
    color: colors.silver,
    features: [
      'Affichage sidebar et header',
      '3 annonces actives',
      'Durée : 3 mois',
      'Analytics basiques',
      'Support téléphone',
      'Ciblage géographique'
    ],
    popular: true
  },
  {
    id: 'premium',
    name: 'Package Premium',
    price: 250000,
    color: colors.gold,
    features: [
      'Toutes positions disponibles',
      'Annonces illimitées',
      'Durée : 6 mois',
      'Analytics avancées',
      'Support prioritaire',
      'Campagnes personnalisées',
      'Mentions à l\'antenne'
    ]
  },
  {
    id: 'sponsor',
    name: 'Package Sponsor',
    price: 500000,
    color: colors.primaryLight,
    features: [
      'Sponsoring complet de programmes',
      'Mentions à l\'antenne',
      'Logo permanent',
      'Analytics complètes',
      'Durée : 12 mois',
      'Campagnes sur-mesure',
      'Partenariat exclusif',
      'Événements dédiés'
    ]
  }
];

export default function PublicityScreen() {
  const [selectedPackage, setSelectedPackage] = useState<string | null>(null);
  const [contactForm, setContactForm] = useState({
    company: '',
    name: '',
    email: '',
    phone: '',
    message: ''
  });
  const [showContactForm, setShowContactForm] = useState(false);
  const router = useRouter();

  const formatPrice = (price: number) => {
    return new Intl.NumberFormat('fr-FR').format(price) + ' FCFA';
  };

  const handlePackageSelect = (packageId: string) => {
    setSelectedPackage(packageId);
    setShowContactForm(true);
  };

  const handleSubmitContact = () => {
    if (!contactForm.company || !contactForm.name || !contactForm.email || !contactForm.phone) {
      Alert.alert('Erreur', 'Veuillez remplir tous les champs obligatoires');
      return;
    }

    Alert.alert(
      'Demande envoyée',
      'Votre demande a été envoyée avec succès. Notre équipe commerciale vous contactera dans les 24h.',
      [{ text: 'OK', onPress: () => setShowContactForm(false) }]
    );
    
    // Reset form
    setContactForm({
      company: '',
      name: '',
      email: '',
      phone: '',
      message: ''
    });
    setSelectedPackage(null);
  };

  const renderPackageCard = (pkg: Package) => (
    <View key={pkg.id} style={[styles.packageCard, pkg.popular && styles.popularPackage]}>
      {pkg.popular && (
        <View style={styles.popularBadge}>
          <Text style={styles.popularText}>PLUS POPULAIRE</Text>
        </View>
      )}
      
      <LinearGradient
        colors={[pkg.color, `${pkg.color}CC`]}
        style={styles.packageHeader}
      >
        <Text style={styles.packageName}>{pkg.name}</Text>
        <Text style={styles.packagePrice}>{formatPrice(pkg.price)}</Text>
        <Text style={styles.packagePriceSubtext}>par mois</Text>
      </LinearGradient>
      
      <View style={styles.packageContent}>
        {pkg.features.map((feature, index) => (
          <View key={index} style={styles.featureItem}>
            <Ionicons name="checkmark-circle" size={20} color={colors.primaryLight} />
            <Text style={styles.featureText}>{feature}</Text>
          </View>
        ))}
        
        <TouchableOpacity 
          style={[styles.selectButton, { backgroundColor: pkg.color }]}
          onPress={() => handlePackageSelect(pkg.id)}
        >
          <Text style={styles.selectButtonText}>Choisir ce package</Text>
        </TouchableOpacity>
      </View>
    </View>
  );

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar style="light" backgroundColor={colors.primary} />
      
      <KeyboardAvoidingView 
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.keyboardView}
      >
        <ScrollView style={styles.scrollView} showsVerticalScrollIndicator={false}>
          {/* Header */}
          <View style={styles.header}>
            <TouchableOpacity onPress={() => router.back()} style={styles.backButton}>
              <Ionicons name="arrow-back" size={24} color={colors.white} />
            </TouchableOpacity>
            
            <View style={styles.headerContent}>
              <Text style={styles.headerTitle}>Programme Publicitaire</Text>
              <Text style={styles.headerSubtitle}>Boostez votre visibilité avec LCA TV</Text>
            </View>
          </View>

          {/* Hero Section */}
          <View style={styles.heroSection}>
            <LinearGradient
              colors={[colors.primary, colors.primaryLight]}
              style={styles.heroGradient}
            >
              <Ionicons name="megaphone" size={48} color={colors.white} />
              <Text style={styles.heroTitle}>Maximisez votre impact</Text>
              <Text style={styles.heroDescription}>
                Touchez plus de 500,000 téléspectateurs quotidiens au Burkina Faso
                et dans la sous-région avec nos solutions publicitaires sur-mesure.
              </Text>
              
              <View style={styles.statsContainer}>
                <View style={styles.statItem}>
                  <Text style={styles.statNumber}>500K+</Text>
                  <Text style={styles.statLabel}>Téléspectateurs</Text>
                </View>
                <View style={styles.statItem}>
                  <Text style={styles.statNumber}>95%</Text>
                  <Text style={styles.statLabel}>Taux de mémorisation</Text>
                </View>
                <View style={styles.statItem}>
                  <Text style={styles.statNumber}>24/7</Text>
                  <Text style={styles.statLabel}>Diffusion</Text>
                </View>
              </View>
            </LinearGradient>
          </View>

          {/* Benefits Section */}
          <View style={styles.benefitsSection}>
            <Text style={styles.sectionTitle}>Pourquoi choisir LCA TV ?</Text>
            
            <View style={styles.benefitsList}>
              <View style={styles.benefitItem}>
                <Ionicons name="people" size={32} color={colors.primaryLight} />
                <View style={styles.benefitContent}>
                  <Text style={styles.benefitTitle}>Audience massive</Text>
                  <Text style={styles.benefitDescription}>
                    Plus de 500,000 téléspectateurs fidèles au Burkina Faso
                  </Text>
                </View>
              </View>
              
              <View style={styles.benefitItem}>
                <Ionicons name="trending-up" size={32} color={colors.primaryLight} />
                <View style={styles.benefitContent}>
                  <Text style={styles.benefitTitle}>ROI prouvé</Text>
                  <Text style={styles.benefitDescription}>
                    95% de nos clients renouvellent leur contrat publicitaire
                  </Text>
                </View>
              </View>
              
              <View style={styles.benefitItem}>
                <Ionicons name="analytics" size={32} color={colors.primaryLight} />
                <View style={styles.benefitContent}>
                  <Text style={styles.benefitTitle}>Analytics détaillées</Text>
                  <Text style={styles.benefitDescription}>
                    Suivez en temps réel les performances de vos campagnes
                  </Text>
                </View>
              </View>
              
              <View style={styles.benefitItem}>
                <Ionicons name="shield-checkmark" size={32} color={colors.primaryLight} />
                <View style={styles.benefitContent}>
                  <Text style={styles.benefitTitle}>Contenu premium</Text>
                  <Text style={styles.benefitDescription}>
                    Associez votre marque à des programmes de qualité
                  </Text>
                </View>
              </View>
            </View>
          </View>

          {/* Packages Section */}
          <View style={styles.packagesSection}>
            <Text style={styles.sectionTitle}>Nos Packages Publicitaires</Text>
            <Text style={styles.sectionSubtitle}>
              Choisissez la solution qui correspond à vos objectifs marketing
            </Text>
            
            <View style={styles.packagesContainer}>
              {packages.map(renderPackageCard)}
            </View>
          </View>

          {/* Contact Form */}
          {showContactForm && (
            <View style={styles.contactSection}>
              <Text style={styles.sectionTitle}>Demande de devis</Text>
              <Text style={styles.sectionSubtitle}>
                Package sélectionné: {packages.find(p => p.id === selectedPackage)?.name}
              </Text>
              
              <View style={styles.formContainer}>
                <View style={styles.inputContainer}>
                  <Ionicons name="business" size={20} color={colors.gray} />
                  <TextInput
                    style={styles.input}
                    placeholder="Nom de l'entreprise *"
                    placeholderTextColor={colors.gray}
                    value={contactForm.company}
                    onChangeText={(text) => setContactForm({...contactForm, company: text})}
                  />
                </View>
                
                <View style={styles.inputContainer}>
                  <Ionicons name="person" size={20} color={colors.gray} />
                  <TextInput
                    style={styles.input}
                    placeholder="Nom du contact *"
                    placeholderTextColor={colors.gray}
                    value={contactForm.name}
                    onChangeText={(text) => setContactForm({...contactForm, name: text})}
                  />
                </View>
                
                <View style={styles.inputContainer}>
                  <Ionicons name="mail" size={20} color={colors.gray} />
                  <TextInput
                    style={styles.input}
                    placeholder="Email *"
                    placeholderTextColor={colors.gray}
                    value={contactForm.email}
                    onChangeText={(text) => setContactForm({...contactForm, email: text})}
                    keyboardType="email-address"
                    autoCapitalize="none"
                  />
                </View>
                
                <View style={styles.inputContainer}>
                  <Ionicons name="call" size={20} color={colors.gray} />
                  <TextInput
                    style={styles.input}
                    placeholder="Téléphone *"
                    placeholderTextColor={colors.gray}
                    value={contactForm.phone}
                    onChangeText={(text) => setContactForm({...contactForm, phone: text})}
                    keyboardType="phone-pad"
                  />
                </View>
                
                <View style={[styles.inputContainer, styles.textAreaContainer]}>
                  <Ionicons name="chatbubble-ellipses" size={20} color={colors.gray} style={styles.textAreaIcon} />
                  <TextInput
                    style={[styles.input, styles.textArea]}
                    placeholder="Message (objectifs, période souhaitée, etc.)"
                    placeholderTextColor={colors.gray}
                    value={contactForm.message}
                    onChangeText={(text) => setContactForm({...contactForm, message: text})}
                    multiline
                    numberOfLines={4}
                  />
                </View>
                
                <TouchableOpacity style={styles.submitButtonContainer} onPress={handleSubmitContact}>
                  <LinearGradient
                    colors={[colors.primary, colors.primaryLight]}
                    style={styles.submitButton}
                  >
                    <Text style={styles.submitButtonText}>Envoyer la demande</Text>
                  </LinearGradient>
                </TouchableOpacity>
              </View>
            </View>
          )}

          {/* Success Stories */}
          <View style={styles.successSection}>
            <Text style={styles.sectionTitle}>Nos clients nous font confiance</Text>
            
            <View style={styles.clientsGrid}>
              {['Coris Bank', 'Orange Burkina', 'SONABEL', 'Faso Soap'].map((client, index) => (
                <View key={index} style={styles.clientCard}>
                  <View style={styles.clientLogo}>
                    <Text style={styles.clientInitial}>{client.charAt(0)}</Text>
                  </View>
                  <Text style={styles.clientName}>{client}</Text>
                </View>
              ))}
            </View>
          </View>

          {/* CTA Section */}
          <View style={styles.ctaSection}>
            <LinearGradient
              colors={[colors.blue, colors.primaryLight]}
              style={styles.ctaGradient}
            >
              <Text style={styles.ctaTitle}>Prêt à démarrer ?</Text>
              <Text style={styles.ctaDescription}>
                Contactez notre équipe commerciale pour un devis personnalisé
              </Text>
              
              <View style={styles.contactInfo}>
                <View style={styles.contactItem}>
                  <Ionicons name="call" size={20} color={colors.white} />
                  <Text style={styles.contactText}>+226 XX XX XX XX</Text>
                </View>
                <View style={styles.contactItem}>
                  <Ionicons name="mail" size={20} color={colors.white} />
                  <Text style={styles.contactText}>pub@lcatv.bf</Text>
                </View>
              </View>
            </LinearGradient>
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
  scrollView: {
    flex: 1,
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
  },
  headerSubtitle: {
    fontSize: 14,
    color: colors.white,
    opacity: 0.8,
  },
  heroSection: {
    margin: 20,
    borderRadius: 15,
    overflow: 'hidden',
  },
  heroGradient: {
    padding: 30,
    alignItems: 'center',
  },
  heroTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: colors.white,
    marginTop: 15,
    marginBottom: 10,
    textAlign: 'center',
  },
  heroDescription: {
    fontSize: 16,
    color: colors.white,
    textAlign: 'center',
    opacity: 0.9,
    lineHeight: 22,
    marginBottom: 20,
  },
  statsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    width: '100%',
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
    marginTop: 2,
  },
  benefitsSection: {
    padding: 20,
  },
  sectionTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: colors.black,
    marginBottom: 10,
    textAlign: 'center',
  },
  sectionSubtitle: {
    fontSize: 16,
    color: colors.gray,
    textAlign: 'center',
    marginBottom: 20,
  },
  benefitsList: {
    marginTop: 10,
  },
  benefitItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20,
    padding: 15,
    backgroundColor: colors.lightGray,
    borderRadius: 12,
  },
  benefitContent: {
    flex: 1,
    marginLeft: 15,
  },
  benefitTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: colors.black,
    marginBottom: 5,
  },
  benefitDescription: {
    fontSize: 14,
    color: colors.gray,
    lineHeight: 20,
  },
  packagesSection: {
    padding: 20,
    backgroundColor: colors.lightGray,
  },
  packagesContainer: {
    marginTop: 10,
  },
  packageCard: {
    backgroundColor: colors.white,
    borderRadius: 15,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 5,
    position: 'relative',
  },
  popularPackage: {
    borderWidth: 2,
    borderColor: colors.primaryLight,
    transform: [{ scale: 1.02 }],
  },
  popularBadge: {
    position: 'absolute',
    top: -10,
    left: 20,
    right: 20,
    backgroundColor: colors.primaryLight,
    borderRadius: 15,
    paddingVertical: 5,
    zIndex: 1,
  },
  popularText: {
    color: colors.white,
    fontSize: 12,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  packageHeader: {
    padding: 20,
    alignItems: 'center',
    borderTopLeftRadius: 15,
    borderTopRightRadius: 15,
  },
  packageName: {
    fontSize: 20,
    fontWeight: 'bold',
    color: colors.white,
    marginBottom: 5,
  },
  packagePrice: {
    fontSize: 28,
    fontWeight: 'bold',
    color: colors.white,
  },
  packagePriceSubtext: {
    fontSize: 14,
    color: colors.white,
    opacity: 0.8,
  },
  packageContent: {
    padding: 20,
  },
  featureItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  featureText: {
    fontSize: 14,
    color: colors.black,
    marginLeft: 10,
    flex: 1,
  },
  selectButton: {
    marginTop: 15,
    paddingVertical: 12,
    borderRadius: 8,
    alignItems: 'center',
  },
  selectButtonText: {
    color: colors.white,
    fontSize: 16,
    fontWeight: 'bold',
  },
  contactSection: {
    padding: 20,
  },
  formContainer: {
    marginTop: 20,
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.lightGray,
    borderRadius: 10,
    paddingHorizontal: 15,
    paddingVertical: 12,
    marginBottom: 15,
  },
  textAreaContainer: {
    alignItems: 'flex-start',
    paddingVertical: 15,
  },
  textAreaIcon: {
    marginTop: 5,
  },
  input: {
    flex: 1,
    fontSize: 16,
    color: colors.black,
    marginLeft: 10,
  },
  textArea: {
    minHeight: 80,
    textAlignVertical: 'top',
  },
  submitButtonContainer: {
    borderRadius: 10,
    overflow: 'hidden',
    marginTop: 10,
  },
  submitButton: {
    paddingVertical: 15,
    alignItems: 'center',
  },
  submitButtonText: {
    color: colors.white,
    fontSize: 16,
    fontWeight: 'bold',
  },
  successSection: {
    padding: 20,
  },
  clientsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
    marginTop: 20,
  },
  clientCard: {
    width: '45%',
    alignItems: 'center',
    marginBottom: 20,
    padding: 15,
    backgroundColor: colors.lightGray,
    borderRadius: 10,
  },
  clientLogo: {
    width: 50,
    height: 50,
    borderRadius: 25,
    backgroundColor: colors.primaryLight,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 10,
  },
  clientInitial: {
    fontSize: 20,
    fontWeight: 'bold',
    color: colors.white,
  },
  clientName: {
    fontSize: 14,
    fontWeight: '600',
    color: colors.black,
    textAlign: 'center',
  },
  ctaSection: {
    margin: 20,
    borderRadius: 15,
    overflow: 'hidden',
  },
  ctaGradient: {
    padding: 30,
    alignItems: 'center',
  },
  ctaTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: colors.white,
    marginBottom: 10,
  },
  ctaDescription: {
    fontSize: 16,
    color: colors.white,
    textAlign: 'center',
    marginBottom: 20,
    opacity: 0.9,
  },
  contactInfo: {
    alignItems: 'center',
  },
  contactItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 10,
  },
  contactText: {
    fontSize: 16,
    color: colors.white,
    marginLeft: 10,
    fontWeight: '600',
  },
});