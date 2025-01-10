
import { firebaseConfig } from '../src/firebase-config_const.js';
import 'https://www.gstatic.com/firebasejs/8.10.0/firebase-app.js';
import 'https://www.gstatic.com/firebasejs/8.10.0/firebase-messaging.js';

// Initialize Firebase in Service Worker
firebase.initializeApp(firebaseConfig);

 // Initialize Firebase Messaging
const messaging = firebase.messaging();

// Handle background messages
messaging.onBackgroundMessage((payload) => {
    console.log('[firebase-messaging-sw.js] Received background message', payload);

    const notificationTitle = payload.notification.title;
    const notificationOptions = {
        body: payload.notification.body,
        icon: payload.notification.icon, // Add an icon if available
    };

    // Show notification
    self.registration.showNotification(notificationTitle, notificationOptions);
}); 
