import React, { useState, useEffect, useCallback } from 'react';
import { View, Text, StyleSheet, FlatList, TouchableOpacity, Alert, RefreshControl, Platform } from 'react-native';
import { useNavigation, useFocusEffect } from '@react-navigation/native';
import messaging from '@react-native-firebase/messaging';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Colors, Typography, Spacing } from '../styles';
import { requestNotificationPermission } from '../utils/permissions';
import { groupBy } from 'lodash';  // for notification grouping (1)
import dayjs from 'dayjs';  // For formatting timestamps (3)
import { useNotifications } from '../context/NotificationContext'; // 5. Context for read/unread status

const NotificationHandler = () => {
    const { notifications, setNotifications, markNotificationAsRead } = useNotifications();
    const [isLoading, setIsLoading] = useState(true);
    const [isRefreshing, setIsRefreshing] = useState(false); 
    const navigation = useNavigation();

    useEffect(() => {
        setupNotifications();

        // ... (Clean up listeners remains the same)
    }, []);

    // ... (setupNotifications, registerForRemoteMessages, setupNotificationListeners remain the same)

    // Modified handleNewNotification to update context and use grouping
    const handleNewNotification = async (remoteMessage) => {
        const newNotification = {
            // ... (notification data)
            isRead: false,  // 5. Set initial status as unread
        };

        setNotifications(prevNotifications => [newNotification, ...prevNotifications]);
        await saveNotifications(notifications);
    };

    // ... (handleNotificationOpen, loadSavedNotifications, saveNotifications remain the same)

    const clearAllNotifications = async () => {
        // ... (Clear notifications remains the same)
        markNotificationAsRead(null, true); // Mark all as read when clearing
    };

    // Group notifications by date (1)
    const groupedNotifications = groupBy(notifications, notification => dayjs(notification.timestamp).format('YYYY-MM-DD'));

    const renderNotificationGroupHeader = ({ section: { title } }) => (
        <Text style={styles.groupHeader}>{dayjs(title).format('MMMM D, YYYY')}</Text>
    );

    const renderNotificationItem = ({ item }) => (
        <TouchableOpacity
            style={[styles.notificationItem, item.isRead && styles.readNotification]}
            onPress={() => {
                handleNotificationOpen(item);
                markNotificationAsRead(item.id); // 5. Mark as read when opened
            }}
        >
            {/* ... (notification content) */}
        </TouchableOpacity>
    );

    return (
        <View style={styles.container}>
            {/* ... (title remains the same) */}
            {notifications.length > 0 ? (
                <>
                    <FlatList
                        data={Object.entries(groupedNotifications)}  // Render grouped data
                        renderItem={({ item: [date, notifications] }) => (
                            <View>
                                {renderNotificationGroupHeader({ section: { title: date } })}
                                <FlatList
                                    data={notifications}
                                    renderItem={renderNotificationItem}
                                    keyExtractor={item => item.id}
                                />
                            </View>
                        )}
                        keyExtractor={(item) => item[0]} // Use date as key
                        refreshControl={
                            <RefreshControl refreshing={isRefreshing} onRefresh={onRefresh} /> // 6. Pull-to-refresh
                        }
                        style={styles.notificationList}
                    />
                    {/* ... (clear button remains the same) */}
                </>
            ) : (
                <Text style={styles.emptyText}>No notifications</Text>
            )}
        </View>
    );
};

// ... (styles, with additional styles for group headers and read notifications)

export default NotificationHandler;
