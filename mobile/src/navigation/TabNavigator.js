import React, { useEffect, useRef, useState } from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Ionicons } from '@expo/vector-icons';
import { View, Text, StyleSheet, TouchableOpacity, Animated } from 'react-native';
import * as Linking from 'expo-linking';  // 7. Deep Linking
import { Colors, Typography, Spacing } from '../styles';
import { useNotifications } from '../contexts/NotificationContext'; // 2. Badge Functionality
import { ErrorBoundary } from 'react-error-boundary'; // 8. Error Boundaries
import { useNavigation } from '@react-navigation/native'; 
import { useAuth } from '../contexts/AuthContext'; // 5. Conditional Rendering

// ... (import your screens here)

const Tab = createBottomTabNavigator();

const FallbackComponent = ({ error }) => ( 
  <View style={styles.errorContainer}>
    <Text style={styles.errorText}>Something went wrong:</Text>
    <Text style={styles.errorText}>{error.message}</Text>
  </View>
);

// Custom Tab Bar Item Component (4)
const CustomTabBarItem = ({ children, onPress, accessibilityLabel, badgeCount }) => {
  const scale = useRef(new Animated.Value(1)).current;

  const handlePressIn = () => {
    Animated.spring(scale, {
      toValue: 0.9,
      useNativeDriver: true,
    }).start();
  };

  const handlePressOut = () => {
    Animated.spring(scale, {
      toValue: 1,
      useNativeDriver: true,
    }).start();
    onPress();
  };

  return (
    <TouchableOpacity
      activeOpacity={1}
      accessibilityLabel={accessibilityLabel} 
      onPressIn={handlePressIn}
      onPressOut={handlePressOut}
      style={styles.tabBarItem}
    >
      <Animated.View style={{ transform: [{ scale }] }}>
        {children}
      </Animated.View>
      {badgeCount > 0 && (
        <View style={styles.badge}>
          <Text style={styles.badgeText}>{badgeCount}</Text>
        </View>
      )}
    </TouchableOpacity>
  );
};

const TabNavigator = () => {
  const { user } = useAuth();
  const navigation = useNavigation();
  const { unreadCount } = useNotifications();

  // 7. Deep Linking
  useEffect(() => {
    const handleDeepLink = (event) => {
      const path = Linking.parse(event.url).path;
      if (path === '/transactions') {
        navigation.navigate('Transactions');
      } 
      // ... handle other paths
    };

    Linking.addEventListener('url', handleDeepLink);
    return () => {
      Linking.removeEventListener('url', handleDeepLink);
    };
  }, []);

  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          // ... (icon logic remains the same)
        },
        // 1. Custom Styles
        tabBarActiveTintColor: Colors.primary,
        tabBarInactiveTintColor: Colors.secondary,
        tabBarStyle: styles.tabBar,
        tabBarItemStyle: styles.tabBarItem,
        tabBarLabelStyle: Typography.tabLabel,
        // 4. Custom Tab Bar Item
        tabBarButton: (props) => (
          <CustomTabBarItem
            {...props}
            accessibilityLabel={`${route.name} Tab`} // 3. Accessibility Labels
            badgeCount={route.name === 'Notifications' ? unreadCount : 0} // 2. Badge
          />
        ),
      })}
    >
      { user ? (
        <>
          <Tab.Screen 
            name="Home" 
            component={HomeScreen} 
            options={{ title: 'Dashboard' }}
          />
          <Tab.Screen 
            name="Transactions" 
            component={TransactionScreen} 
            options={{ title: 'Transactions' }}
          />
        </>
        ) : null // 5. Conditional Rendering of Tabs
      }
      {/* 8. Error Boundaries for Screens */}
      <Tab.Screen 
        name="Settings" 
        component={SettingsScreen} 
        options={{ title: 'Settings' }}
      />
    </Tab.Navigator>
  );
};

// Styles (1)
const styles = StyleSheet.create({
  // ... other styles
  tabBar: {
    backgroundColor: Colors.background,
    borderTopWidth: 1,
    borderTopColor: Colors.border,
  },
  tabBarItem: {
    padding: Spacing.small, 
  },
  badge: {
    position: 'absolute',
    top: 5,
    right: 5,
    backgroundColor: Colors.error,
    borderRadius: 10,
    minWidth: 18,
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: 4,
  },
  badgeText: {
    color: Colors.white,
    fontSize: 10,
    fontWeight: 'bold',
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: Spacing.medium,
  },
  errorText: {
    ...Typography.body,
    textAlign: 'center',
    marginBottom: Spacing.small,
  },
});

export default TabNavigator;
