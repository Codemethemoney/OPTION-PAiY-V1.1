import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Alert } from 'react-native';
import * as Sentry from '@sentry/react-native';  // 17. Error Tracking (Sentry)

// Load credentials securely
const { TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER } = process.env;

const twilioApi = axios.create({
    baseURL: `https://api.twilio.com/2010-04-01/Accounts/${TWILIO_ACCOUNT_SID}`,
    auth: {
        username: TWILIO_ACCOUNT_SID,
        password: TWILIO_AUTH_TOKEN,
    },
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
    },
});

const smsService = {
    // 1. Error Handling and Logging
    sendSMS: async (to, body) => {
        try {
            const response = await twilioApi.post('/Messages.json', {
                To: to,
                From: TWILIO_PHONE_NUMBER,
                Body: body,
            });
            logger.info(`SMS sent to ${to}: ${body}`);
            return response.data;
        } catch (error) {
            logger.error(`Error sending SMS to ${to}: ${error.response?.data || error.message}`);
            Sentry.captureException(error); // 17. Report error to Sentry
            throw error; // Re-throw for higher-level handling
        }
    },

    // 2. Rate Limiting (using a simple in-memory store)
    rateLimitStore: {},

    sendSMSWithRateLimit: async (to, body, limit = 5, period = 60) => { // 5 msgs per minute
        const now = Date.now();
        const lastRequests = smsService.rateLimitStore[to] || [];
        const validRequests = lastRequests.filter(time => now - time < period * 1000);
        if (validRequests.length >= limit) {
            throw new Error("Rate limit exceeded");
        }

        const result = await smsService.sendSMS(to, body);
        smsService.rateLimitStore[to] = [...validRequests, now];
        return result;
    },


    // ... (other methods like sendVerificationCode, verifyCode remain the same)

    // 4. SMS Templates (Example)
    smsTemplates: {
        verificationCode: (code) => `Your verification code is: ${code}`,
        paymentConfirmation: (amount, recipient) => `Your payment of $${amount} to ${recipient} was successful.`,
        // ... other templates
    },
};

// 5. TypeScript (Example type definitions)
// interface SMSService {
//     sendSMS: (to: string, body: string) => Promise<any>;
//     // ... other method signatures
// }
 

// ... (Rest of the code remains the same)
