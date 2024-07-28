// index.js (or index.tsx)

import { AppRegistry, Platform, LogBox, YellowBox } from 'react-native'; // Import LogBox, YellowBox
import App from './App';
import { name as appName } from '../app.json';
import { init as initSentry } from '@sentry/react-native'; // 1. Error Boundary
import { configure } from 'mobx'; // 4. Global State Management (MobX)
import codePush from 'react-native-code-push'; // 16. App Updates
import SplashScreen from 'expo-splash-screen';
import * as Font from 'expo-font'; // 17. Custom Fonts
import { 
    initializeLocalization, 
    configureLocalization, 
    setI18nConfig 
} from './utils/i18n'; // 11. Internationalization
import { 
    logEvent, 
    setAnalyticsCollectionEnabled, 
    setUserProperties 
} from './utils/analytics'; // 14. Analytics Tracking
import './utils/errorHandler'; // Keep existing error handler
import { registerForPushNotificationsAsync } from './utils/notifications';

// 1. Error Boundary & Crash Reporting
initSentry({
  dsn: 'YOUR_SENTRY_DSN', // Replace with your actual Sentry DSN
  enableInExpoDevelopment: true,
  debug: __DEV__,
});

// 2. Environment Configuration (Example - using .env files)
if (__DEV__) {
  require("dotenv").config({ path: ".env.development" });
} else {
  require("dotenv").config({ path: ".env.production" });
}

// 3. Type Checking (TypeScript)
// This file would be index.tsx if using TypeScript. You would define types for all
// your components and functions throughout the project.

// 4. Global State Management (MobX - Example configuration)
configure({ enforceActions: "never" }); // Disable strict mode for easier development

// 5. Code Splitting & Lazy Loading 
// (Done at the component level using React.lazy and Suspense)
// e.g., const LazyComponent = React.lazy(() => import('./components/HeavyComponent'));

// 6. Web Platform Support
// If building a cross-platform app, you'd use react-native-web and configure it here.

// 7. Logging & Monitoring
// Assuming you have a logging utility already set up in your project.
logger.info('App initialization started');

// 8. Offline Persistence & Synchronization
// This would typically involve using AsyncStorage, WatermelonDB, or a similar library
// to store data offline and sync when online.

// 9. Deep Linking
// Handled in your NavigationContainer (e.g., App.js) using the linking prop.

// 10. Push Notifications
registerForPushNotificationsAsync().catch(console.error); // Register on startup

// 11. Security Configurations (Example - SSL Pinning)
// (Implementation would vary depending on your networking library)
// if (!__DEV__) {
//   axios.defaults.httpsAgent = new Agent({
//       rejectUnauthorized: true, // Require valid SSL certificates
//       // ... (add your SSL pinning configuration here)
//   });
// }

// 12. App Permissions
// Use libraries like expo-permissions to request permissions on app launch if needed.

// 13. A/B Testing
// You would typically integrate an A/B testing framework (e.g., Firebase A/B Testing)
// here or in your top-level component.

// 14. Analytics Tracking (Example)
logEvent('App_Launched', { platform: Platform.OS });
setAnalyticsCollectionEnabled(!__DEV__); // Enable analytics in production only

// 15. Accessibility Configurations
// Ensure your components have proper accessibilityLabels and roles.

// 16. App Updates (CodePush)
let codePushOptions = { checkFrequency: codePush.CheckFrequency.ON_APP_RESUME };
App = codePush(codePushOptions)(App); 

// 17. Custom Fonts and Assets
SplashScreen.preventAutoHideAsync(); // Prevent auto-hide until fonts are loaded
(async () => {
    await Font.loadAsync({
        'your-font-name': require('./assets/fonts/YourFont.ttf'),
        // ... load other fonts 
    });
    await SplashScreen.hideAsync(); // Hide splash screen after assets are loaded
})();

// 18. Debugging Tools
// In development mode, you might want to enable tools like Reactotron or Flipper.

// 19. Device-Specific Configurations (Example)
// You can access device information using libraries like expo-device.
// if (Platform.OS === 'android' && Device.manufacturer === 'Samsung') {
//   // Apply Samsung-specific configuration
// }

// 20. Performance Tracking & Optimization
// Use tools like the React DevTools Profiler or the Hermes Profiler
// to identify and address performance bottlenecks.

// Hide warnings in development mode (Not recommended for production)
if (__DEV__) {
    LogBox.ignoreLogs(['Warning: ...']);
    YellowBox.ignoreWarnings(['Warning: ...']);
}
 
// Configure i18n
initializeLocalization();
setI18nConfig();

AppRegistry.registerComponent(appName, () => App);
