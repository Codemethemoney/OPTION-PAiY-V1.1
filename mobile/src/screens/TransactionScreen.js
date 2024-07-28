import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { View, Text, StyleSheet, FlatList, ActivityIndicator, TouchableOpacity, Alert, ScrollView, RefreshControl } from 'react-native';
import { SearchBar, Button, ListItem, Icon, Overlay } from 'react-native-elements';
import { useNavigation, useFocusEffect } from '@react-navigation/native';
import { format, parseISO, differenceInDays } from 'date-fns';
import { enUS } from 'date-fns/locale';
import { PieChart } from "react-native-chart-kit";

import { fetchTransactions, filterTransactions } from '../services/api';
import { formatCurrency } from '../utils/formatters';
import { Colors, Typography, Spacing } from '../styles';
import { trackEvent } from '../utils/analytics';
import FilterModal from '../components/FilterModal'; // Custom filter modal component

const TransactionScreen = () => {
  const navigation = useNavigation();
  const [transactions, setTransactions] = useState([]);
  const [filteredTransactions, setFilteredTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [filter, setFilter] = useState('all'); // 'all', 'income', 'expense'
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);
  const [refreshing, setRefreshing] = useState(false);
  const [isFilterModalVisible, setFilterModalVisible] = useState(false);

  useFocusEffect(
    useCallback(() => {
      loadTransactions();
    }, [])
  ); // 17. Pull to refresh on focus

  useEffect(() => {
    applyFilters(); // 12. Apply filters on data change
  }, [search, filter, startDate, endDate, transactions]);


  // 5. Analytics (Example)
  useEffect(() => {
    trackEvent('TransactionScreen_Viewed');
  }, []);

  const loadTransactions = async () => {
    try {
      setLoading(true);
      const data = await fetchTransactions(); // 18. Assuming this function handles caching
      setTransactions(data);
    } catch (error) {
      console.error('Error fetching transactions:', error);
      Alert.alert('Error', 'Unable to fetch transactions. Please try again later.'); // 1. Error Handling
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  // 11. Sorting and Filtering
  const applyFilters = () => {
    let filtered = transactions;
    
    if (search) {
      filtered = filtered.filter(transaction =>
        transaction.description.toLowerCase().includes(search.toLowerCase()) ||
        transaction.amount.toString().includes(search)
      );
    }

    if (filter !== 'all') {
      filtered = filtered.filter(transaction => transaction.type === filter);
    }

    if (startDate && endDate) {
      filtered = filtered.filter(transaction => {
        const transactionDate = parseISO(transaction.date);
        return transactionDate >= startDate && transactionDate <= endDate;
      });
    }

    setFilteredTransactions(filtered); // 13. Data for pie chart can be derived from this
  };
  
  // 13. Data Visualization (Pie Chart Example)
  const chartData = useMemo(() => {
    const categoryTotals = {};
    filteredTransactions.forEach(transaction => {
      if (transaction.type === 'expense') { 
        categoryTotals[transaction.category] = (categoryTotals[transaction.category] || 0) + transaction.amount;
      }
    });
    return Object.entries(categoryTotals).map(([name, amount]) => ({
      name,
      amount,
      color: Colors.chartColors[Object.keys(categoryTotals).indexOf(name) % Colors.chartColors.length], 
      legendFontColor: '#7F7F7F',
      legendFontSize: 15,
    }));
  }, [filteredTransactions]);
  
  const renderPieChart = () => (
    <PieChart
      data={chartData}
      width={StyleSheet.absoluteFill.width}
      height={220}
      chartConfig={{
        backgroundColor: Colors.background,
        backgroundGradientFrom: Colors.background,
        backgroundGradientTo: Colors.background,
        color: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`, // Optional
        labelColor: (opacity = 1) => `rgba(255, 255, 255, ${opacity})`,
        style: {
          borderRadius: 16,
        },
      }}
      accessor="amount"
      backgroundColor="transparent"
      paddingLeft="15"
      absolute
    />
  );

  // ... (renderTransactionItem remains the same)

  const toggleFilterModal = () => {
    setFilterModalVisible(!isFilterModalVisible);
  };

  if (loading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <SearchBar 
        placeholder="Search transactions..."
        onChangeText={setSearch}
        value={search}
        platform="ios"
        containerStyle={styles.searchBar}
      />
      
      <View style={styles.filterContainer}>
        <Button title="Filter" type="outline" buttonStyle={styles.filterButton} onPress={toggleFilterModal} />
      </View>
      
      <FilterModal 
        isVisible={isFilterModalVisible} 
        onClose={toggleFilterModal}
        filter={filter}
        setFilter={setFilter}
        startDate={startDate}
        setStartDate={setStartDate}
        endDate={endDate}
        setEndDate={setEndDate}
      />
    
      {filteredTransactions.length > 0 && chartData.length > 0 && renderPieChart()} 
      
      <ScrollView 
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={handleRefresh} />}
      >
        <FlatList
          data={filteredTransactions}
          renderItem={renderTransactionItem}
          keyExtractor={(item) => item.id.toString()}
          ListEmptyComponent={
            <Text style={styles.emptyList}>No transactions found</Text>
          }
        />
      </ScrollView>

      <TouchableOpacity 
        style={styles.fab}
        onPress={() => navigation.navigate('AddTransaction')}
      >
        <Icon name="add" color="#FFFFFF" />
      </TouchableOpacity>
    </View>
  );
};
 

export default TransactionScreen;


