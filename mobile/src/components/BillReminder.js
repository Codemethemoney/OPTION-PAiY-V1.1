import React, { useState, useEffect, useCallback } from 'react';
import { 
    View, Text, StyleSheet, FlatList, TouchableOpacity, Alert, RefreshControl 
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { getBillReminders, markBillAsPaid } from '../services/financialService';
import { formatCurrency, formatDate } from '../utils/formatters';
import { Colors, Typography, Spacing } from '../styles';
import BillDetails from '../components/BillDetails';  // 3. Import BillDetails component

const BillReminder = () => {
    const [bills, setBills] = useState([]);
    const [isLoading, setIsLoading] = useState(true);
    const [isRefreshing, setIsRefreshing] = useState(false);  // 1. State for refresh
    const [sortBy, setSortBy] = useState('dueDate'); // 2. State for sorting
    const navigation = useNavigation();

    useEffect(() => {
        fetchBillReminders();
    }, []);

    // 1. Pull-to-Refresh Functionality
    const onRefresh = useCallback(async () => {
        setIsRefreshing(true);
        await fetchBillReminders();
        setIsRefreshing(false);
    }, []);

    const fetchBillReminders = async () => {
        try {
            const reminders = await getBillReminders();

            // 2. Sorting (Default by Due Date)
            const sortedReminders = reminders.sort((a, b) => {
                if (sortBy === 'dueDate') {
                    return new Date(a.dueDate) - new Date(b.dueDate);
                } else if (sortBy === 'amount') {
                    return a.amount - b.amount;
                }
            });

            setBills(sortedReminders);
        } catch (error) {
            // ... (error handling remains the same)
        } finally {
            setIsLoading(false);
        }
    };

    const handleMarkAsPaid = async (billId) => {
        // ... (bill marking as paid remains the same)
    };

    // 3. Bill Details Navigation
    const navigateToBillDetails = (bill) => {
        navigation.navigate('BillDetails', { bill }); 
    };

    const renderBillItem = ({ item }) => (
        <TouchableOpacity onPress={() => navigateToBillDetails(item)} style={styles.billItem}>
            {/* ... (bill item content remains the same) */}
        </TouchableOpacity>
    );

    // ... (loading and no bills state handling remains the same)

    return (
        <View style={styles.container}>
            {/* ... (title remains the same) */}
            <FlatList
                data={bills}
                renderItem={renderBillItem}
                keyExtractor={(item) => item.id.toString()}
                showsVerticalScrollIndicator={false}
                refreshControl={  // 1. Refresh control
                    <RefreshControl refreshing={isRefreshing} onRefresh={onRefresh} />
                }
            />

            {/* 2. Sorting Buttons (Example) */}
            {/*<View style={styles.sortingButtons}>
                <TouchableOpacity onPress={() => setSortBy('dueDate')}>
                    <Text style={[styles.sortButton, sortBy === 'dueDate' && styles.activeSortButton]}>Due Date</Text>
                </TouchableOpacity>
                <TouchableOpacity onPress={() => setSortBy('amount')}>
                    <Text style={[styles.sortButton, sortBy === 'amount' && styles.activeSortButton]}>Amount</Text>
                </TouchableOpacity>
            </View>*/} 
        </View>
    );
};

// ... (styles remain the same)

export default BillReminder;
