import React, { useState, useEffect, useCallback } from 'react';
import { View, Text, StyleSheet, ScrollView, Switch, ActivityIndicator, Alert, Appearance, Platform } from 'react-native';
import { ListItem, Button, Icon, Avatar } from 'react-native-elements';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useFocusEffect } from '@react-navigation/native'; 
import { useAuth } from '../contexts/AuthContext';
import { useTheme } from '../contexts/ThemeContext';
import { Colors, Typography, Spacing } from '../styles';
import * as LocalAuthentication from 'expo-local-authentication'; // 20. Biometrics
import { trackEvent } from '../utils/analytics';
import { fetchUserProfile, updateUserSettings } from '../services/api';

const SettingsScreen = () => {
  const { user, logout } = useAuth(); 
  const { theme, setTheme } = useTheme(); // 10. Dark Mode 
  const [userProfile, setUserProfile] = useState(null);
  const [settings, setSettings] = useState({
    pushNotifications: true,
    emailNotifications: true,
    darkMode: Appearance.getColorScheme() === 'dark', // 10. Initialize from system pref
    biometricLogin: false,
  });
  const [isLoading, setIsLoading] = useState(true);
  const [isUpdating, setIsUpdating] = useState(false); // 2. Loading indicator for updating

  useFocusEffect(
    useCallback(() => {
        loadUserProfile();
        loadSettings();
    }, [])
  ); // Load when screen is focused

  const loadUserProfile = async () => {
    try {
      const profile = await fetchUserProfile();
      setUserProfile(profile);
    } catch (error) {
      console.error('Error fetching user profile:', error);
      Alert.alert('Error', 'Failed to load user profile. Please try again.'); // 1. Error Handling
    } finally {
        setIsLoading(false); 
    }
  };

  // ... (loadSettings remains the same)

  const updateSetting = async (key, value) => {
    try {
      setIsUpdating(true); // 2. Show loading indicator
      const newSettings = { ...settings, [key]: value };
      setSettings(newSettings);
      await AsyncStorage.setItem('userSettings', JSON.stringify(newSettings));
      await updateUserSettings(newSettings);
      // 5. Analytics (Example)
      trackEvent('Setting_Changed', { setting: key, newValue: value });
    } catch (error) {
      console.error('Error updating setting:', error);
      Alert.alert('Error', 'Failed to update setting. Please try again.');
    } finally {
      setIsUpdating(false); // 2. Hide loading indicator
    }
  };

  // 14. Logout Implementation
  const handleLogout = async () => {
    try {
      await logout(); // Call logout from AuthContext
      // Optionally, navigate to the login screen
    } catch (error) {
      Alert.alert('Error', 'Failed to logout. Please try again.');
    }
  };

  // 12. Change Password (Placeholder - you'd need a form and API call here)
  const handleChangePassword = () => {
    Alert.alert('Not Implemented', 'Change password feature is not yet implemented.');
  };

  // 20. Check Biometrics Availability
  useEffect(() => {
    (async () => {
      const compatible = await LocalAuthentication.hasHardwareAsync();
      if (!compatible && settings.biometricLogin) {
        updateSetting('biometricLogin', false);
        Alert.alert('Biometrics Not Available', 'Your device does not support biometric authentication.');
      }
    })();
  }, []);

  // ... rest of the code is the same as before ... 
}

export default SettingsScreen;
