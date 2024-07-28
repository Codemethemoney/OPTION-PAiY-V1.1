import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { 
    View, Text, StyleSheet, ScrollView, RefreshControl, ActivityIndicator, 
    TouchableOpacity, Linking, Alert 
} from 'react-native';
import { Card, Button } from 'react-native-elements';
import { useNavigation, useFocusEffect } from '@react-navigation/native';
import { fetchDashboardData } from '../services/api';
import { formatCurrency, formatPercentage } from '../utils/formatters';
import { Colors, Typography, Spacing } from '../styles';
import { useTheme } from '@react-navigation/native'; // 10. Dark Mode
import SkeletonContent from 'react-native-skeleton-content-nonexpo'; // 2. Skeleton Loading
import PropTypes from 'prop-types'; // 3. Type Checking
import { trackEvent } from '../utils/analytics'; // 5. Analytics
import Animated, { FadeIn } from 'react-native-reanimated'; // 7. Animations
import { useAuth } from '../contexts/AuthContext'; // 15. User Personalization

// Import components
import BalanceDisplay from '../components/BalanceDisplay';
import RecentTransactions from '../components/RecentTransactions';
import BillReminder from '../components/BillReminder';
import FinancialSummary from '../components/FinancialSummary';

const HomeScreen = () => {
    const { user } = useAuth();
    const [dashboardData, setDashboardData] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [refreshing, setRefreshing] = useState(false);
    const navigation = useNavigation();
    const { colors, dark } = useTheme(); // Get color scheme

    useFocusEffect(
        useCallback(() => {
            loadDashboardData();
        }, [])
    ); // 11. Pull-to-refresh

    const loadDashboardData = async () => {
        try {
            const data = await fetchDashboardData();
            setDashboardData(data);
        } catch (error) {
            console.error('Error fetching dashboard data:', error);
            Alert.alert('Error', 'Unable to fetch data. Please try again later.'); // 1. Error Handling
        } finally {
            setIsLoading(false);
        }
    };

    // 8. Deep Linking (Example)
    const handleDeepLink = ({ url }) => {
        if (url.includes('transactions')) {
            navigation.navigate('Transactions');
        } 
    };
    useEffect(() => {
        Linking.addEventListener('url', handleDeepLink);
        return () => Linking.removeEventListener('url', handleDeepLink);
    }, []);

    // 5. Analytics (Example)
    useEffect(() => {
        trackEvent('HomeScreen_Viewed', { user_id: user.id }); // Track screen view
    }, [user.id]); 

    // 6. Memoization (Example for one component)
    const memoizedRecentTransactions = useMemo(() => (
        <RecentTransactions transactions={dashboardData?.recentTransactions} />
    ), [dashboardData?.recentTransactions]); 

    // 2. Skeleton Loading
    const skeletonLayout = [
        { width: '90%', height: 150, marginBottom: 20 },
        { width: '90%', height: 80, marginBottom: 20 },
        { width: '90%', height: 120 },
    ];

    if (isLoading) {
        return (
            <SkeletonContent
                containerStyle={styles.skeletonContainer}
                isLoading={isLoading}
                layout={skeletonLayout}
            />
        );
    }

    return (
        <ScrollView
            style={[styles.container, { backgroundColor: colors.background }]} // 10. Dark mode
            refreshControl={
                <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
            }
        >
            {/* 15. Personalized Greeting */}
            <Animated.View entering={FadeIn}>  
                <Text style={[styles.greeting, { color: colors.text }]}>
                    {user ? `Welcome back, ${user.firstName}!` : 'Welcome to your finances!'}
                </Text>
            </Animated.View>
            
            <BalanceDisplay balance={dashboardData.balance} />

            <Card containerStyle={[styles.card, { backgroundColor: colors.cardBackground }]}> 
                <Card.Title style={[styles.cardTitle, { color: colors.text }]}>Quick Actions</Card.Title>
                {/* 13. Navigation to transaction screens */}
                <Button title="Send Money" onPress={() => navigation.navigate('SendMoney')} buttonStyle={styles.actionButton} />
                <Button title="Request Money" onPress={() => navigation.navigate('RequestMoney')} buttonStyle={styles.actionButton} />
            </Card>

            {/* 6. Memoization */}
            {memoizedRecentTransactions}  

            {/* ... other components ... */}
        </ScrollView>
    );
};


HomeScreen.propTypes = {
    // 3. Type Checking
    dashboardData: PropTypes.shape({
        balance: PropTypes.number.isRequired,
        recentTransactions: PropTypes.arrayOf(PropTypes.object).isRequired,
        upcomingBills: PropTypes.arrayOf(PropTypes.object).isRequired,
        financialSummary: PropTypes.object.isRequired,
    }),
};

// ... (styles, with additional styles for personalization, skeleton loading, error handling) 

export default HomeScreen;
