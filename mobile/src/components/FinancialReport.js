import React, { useState, useEffect, useCallback } from 'react';
import { 
    View, Text, StyleSheet, ScrollView, ActivityIndicator, TouchableOpacity, Alert 
} from 'react-native';
import { LineChart, PieChart } from 'react-native-chart-kit';
import { getFinancialReport } from '../services/financialService';
import { formatCurrency, formatPercentage } from '../utils/formatters';
import { Colors, Typography, Spacing } from '../styles';
import { useFocusEffect } from '@react-navigation/native'; // for focus handling
import AsyncStorage from '@react-native-async-storage/async-storage'; // for simple caching

const FinancialReport = () => {
    // ... (state variables and useEffect remain the same)

    // 1. Data Caching (Basic with AsyncStorage)
    const cacheKey = `financialReport_${selectedPeriod}`;
    useFocusEffect(
        useCallback(() => {
            const fetchAndCacheReport = async () => {
                try {
                    setIsLoading(true);
                    const data = await getFinancialReport(selectedPeriod);
                    setReport(data);
                    await AsyncStorage.setItem(cacheKey, JSON.stringify(data)); // Cache
                } catch (error) {
                    console.error('Error fetching report:', error);
                    const cachedData = await AsyncStorage.getItem(cacheKey);
                    if (cachedData) {
                        setReport(JSON.parse(cachedData)); // Load from cache if available
                        Alert.alert('Warning', 'Using cached data. Unable to fetch latest report.');
                    } else {
                        Alert.alert('Error', 'Unable to fetch financial report. Please check your connection.');
                    }
                } finally {
                    setIsLoading(false);
                }
            };
            fetchAndCacheReport();
        }, [selectedPeriod]) 
    );

    // 2. Error Handling (Incorporated within fetchAndCacheReport)

    // ... (renderSummary, renderIncomeVsExpensesChart, and renderExpenseCategoriesChart remain the same)

    // 3. Custom Tooltips (Example using react-native-interactive-chart)
    const chartTooltip = ({ datum }) => (
        <View style={styles.tooltip}>
            <Text style={styles.tooltipText}>{datum.xLabel}: {formatCurrency(datum.y)}</Text>
        </View>
    );

    // ... (renderPeriodSelector remains the same)

    // ... (loading state remains the same)

    return (
        <ScrollView style={styles.container}>
            {/* ... (rest of the content) */}
            <LineChart
                // ... (other chart props)
                renderDotContent={renderTooltip}  // Add tooltip
            />
            <PieChart
                // ... (other chart props)
                renderDotContent={renderTooltip}  // Add tooltip
            />
        </ScrollView>
    );
};

// ... (styles, with additional styles for tooltip)

export default FinancialReport;
