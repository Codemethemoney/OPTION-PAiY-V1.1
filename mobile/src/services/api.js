import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Alert } from 'react-native'; // 1. Error Handling
import * as yup from 'yup';  // 2. Schema Validation (Yup)
import NetInfo from "@react-native-community/netinfo";  // 11. Network Connectivity
import { AuthSession } from 'expo'; //15. Rate Limiting and Retry Logic

const BASE_URL = 'https://api.yourfinancialapp.com/v1';
const API_VERSION = 'v1'; // 13. API Versioning (Basic)

// Create an axios instance
const api = axios.create({
    baseURL: `${BASE_URL}/${API_VERSION}`,
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Error Handling and Logging (1)
const handleError = (error) => {
    if (axios.isCancel(error)) {
        logger.warn('Request canceled:', error.message);
    } else {
        const { message, status } = handleApiError(error);
        logger.error(`API Error: ${status} - ${message}`);
        // Show user-friendly error message
        Alert.alert('Error', message);
    }
};

// Request Interceptor (Authentication and Logging)
api.interceptors.request.use(
    async (config) => {
        const token = await AsyncStorage.getItem('userToken');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    handleError
);

// Response Interceptor (Refresh Token and Error Handling)
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;
        if (error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            try {
                const refreshToken = await AsyncStorage.getItem('refreshToken');
                const rs = await AuthSession.startAsync({
                    authUrl:
                        'https://your_auth_server.com/auth/refresh?refresh_token=' + refreshToken
                });
            } catch (_error) {
                await AsyncStorage.removeItem('userToken');
                await AsyncStorage.removeItem('refreshToken');
            }
        }
        return Promise.reject(error);
    }
);

// ... (API call functions)

// 2. Schema Validation (Yup)
const loginSchema = yup.object({
    email: yup.string().email().required(),
    password: yup.string().required(),
});

// Example usage
export const login = async (email, password) => {
    try {
        await loginSchema.validate({ email, password }); // Validate input
        return api.post('/auth/login', { email, password });
    } catch (error) {
        handleError(error);
    }
};

// ... (other API functions)

export default api;
