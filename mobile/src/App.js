import React, { useState, useEffect } from 'react';
import { StatusBar, Platform } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as Linking from 'expo-linking'; // 5. Deep Linking
import * as Notifications from 'expo-notifications';
import * as SplashScreen from 'expo-splash-screen'; // 2. Theme Provider
import { 
    Provider as PaperProvider,
    DefaultTheme as PaperDefaultTheme,
    DarkTheme as PaperDarkTheme 
} from 'react-native-paper'; // 2. Theme Provider
import { 
    AuthContext, 
    AuthProvider 
} from './contexts/AuthContext'; // 1. Global State
import { ThemeProvider } from './contexts/ThemeContext'; // 2. Theme Provider

// ... (import your screens and other components here)

const Stack = createStackNavigator();

const App = () => {
    const [isLoading, setIsLoading] = useState(true);
    const [userToken, setUserToken] = useState(null);
    const [themeMode, setThemeMode] = useState(Appearance.getColorScheme()); // 2. Theme Provider

    useEffect(() => {
        // Check for stored authentication token
        const bootstrapAsync = async () => {
            try {
                const token = await AsyncStorage.getItem('userToken');
                if (token) {
                    // Validate token by fetching user profile (you might need to adjust this)
                    await fetchUserProfile();
                    setUserToken(token);
                }
            } catch (error) {
                console.error('Error during app initialization:', error); // 7. Error Tracking
                // Handle token invalidation or expiration (e.g., logout user)
            } finally {
                setIsLoading(false);
                await SplashScreen.hideAsync(); // Hide splash screen after loading
            }
        };

        bootstrapAsync();

        // 6. Push Notifications (Request permissions on app start)
        registerForPushNotificationsAsync();
    }, []);

    const registerForPushNotificationsAsync = async () => {
        // ... (your notification registration logic here)
    };

    // 2. Theme Provider
    const theme = themeMode === 'dark' ? PaperDarkTheme : PaperDefaultTheme;

    // 5. Deep Linking Configuration
    const linking = {
        prefixes: [Linking.createURL('/')],
        config: {
            // ... your deep linking configuration here
        },
    };
    
    // ... (error handling for authentication remains the same)

    return (
        <ErrorBoundary>
            <AuthProvider>  {/* 1. Global State Management */}
                <ThemeProvider>  {/* 2. Theme Provider */}
                    <SafeAreaProvider>
                        <PaperProvider theme={theme}> {/* 2. Theme Provider */}
                            <NavigationContainer linking={linking} theme={theme}> {/* 5. Deep Linking & 2. Theme Provider */}
                                <Stack.Navigator>
                                    {/* ... your stack navigator logic remains the same ... */}
                                </Stack.Navigator>
                            </NavigationContainer>
                        </PaperProvider>
                    </SafeAreaProvider>
                </ThemeProvider>
            </AuthProvider>
        </ErrorBoundary>
    );
};

export default App;
