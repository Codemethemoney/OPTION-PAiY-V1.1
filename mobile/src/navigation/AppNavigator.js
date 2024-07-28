import React, { useEffect } from 'react';
import { NavigationContainer, DefaultTheme, DarkTheme } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createDrawerNavigator } from '@react-navigation/drawer'; // 3. Drawer Navigator
import { Ionicons } from '@expo/vector-icons';
import * as Linking from 'expo-linking'; // 1. Deep Linking
import { useAuth } from '../contexts/AuthContext';
import { Colors, Typography, Spacing } from '../styles';
import AsyncStorage from '@react-native-async-storage/async-storage'; // 5. Navigation State Persistence
import { useNotifications } from '../contexts/NotificationContext'; // 10. Dynamic Tab Badges
import { useColorScheme } from 'react-native'; // For theme switching

// ... (import your screens here)
// Additional Screen for Drawer Navigator
import AboutScreen from '../screens/AboutScreen'; 

const Stack = createStackNavigator();
const Tab = createBottomTabNavigator();
const Drawer = createDrawerNavigator(); // 3. Create Drawer Navigator

// 2. Transition Animations (Example)
const screenOptions = {
  headerShown: false,
  cardStyleInterpolator: ({ current, layouts }) => {
    return {
      cardStyle: {
        transform: [
          {
            translateX: current.progress.interpolate({
              inputRange: [0, 1],
              outputRange: [layouts.screen.width, 0],
            }),
          },
        ],
      },
    };
  },
};

// 4. Header Customization (Example)
const defaultHeaderOptions = {
  headerStyle: {
    backgroundColor: Colors.primary,
  },
  headerTintColor: Colors.white,
  headerTitleStyle: Typography.header,
};

// 7. Modal Stack
const ModalStack = () => (
  <Stack.Navigator screenOptions={screenOptions}>
    {/* Add screens for the modal here */}
  </Stack.Navigator>
);

// Add AboutScreen to the Drawer Navigator
const DrawerContent = () => (
  <Drawer.Navigator>
    <Drawer.Screen name="HomeDrawer" component={TabNavigator} options={{ headerShown: false, title: 'Home' }}/>
    <Drawer.Screen name="About" component={AboutScreen} options={defaultHeaderOptions}/>
  </Drawer.Navigator>
);

// ... (AuthStack and HomeStack remain the same)

// Modify TabNavigator to include badge count for Notifications tab (10)
const TabNavigator = () => {
  const { unreadCount } = useNotifications();

  return (
    <Tab.Navigator
      // ... (tab bar options remain the same)
    >
      {/* ... other tabs ... */}
      <Tab.Screen 
        name="Notifications" 
        component={NotificationScreen} 
        options={{
          // ...
          tabBarBadge: unreadCount > 0 ? unreadCount : null,
        }} 
      />
      {/* ... other tabs ... */}
    </Tab.Navigator>
  );
};

// ... (AppNavigator)

// 1. Deep Linking Configuration (Example)
const linking = {
  prefixes: [Linking.createURL('/')],
  config: {
    screens: {
      Home: 'home',
      // ... other screens and their paths ...
    },
  },
};

// Main AppNavigator
const AppNavigator = () => {
  const { user } = useAuth();
  const scheme = useColorScheme();

  return (
    <NavigationContainer 
      linking={linking} 
      theme={scheme === 'dark' ? DarkTheme : DefaultTheme} // Theme switching
    >
      {user ? <DrawerContent /> : <AuthStack />}
      {/* 7. Modal Stack (you'll need to trigger this from your screens) */}
      <ModalStack /> 
    </NavigationContainer>
  );
};
