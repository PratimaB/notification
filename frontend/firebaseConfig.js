import { initializeApp } from "firebase/app";
import { getMessaging, getToken, onMessage } from "firebase/messaging";
import { firebaseConfig } from './src/firebase-config_const.js';
import { vapidKey } from './src/firebase-config_const.js';

const app = initializeApp(firebaseConfig);
const messaging = getMessaging(app);

 export const requestForToken = async () => {
  try {
      const registration = await navigator.serviceWorker.register('/firebase-messaging-sw.js',{ type: 'module' });
      console.log('Service Worker registered successfully:', registration);

      const token = await getToken(messaging, { vapidKey: vapidKey, serviceWorkerRegistration: registration });
      console.log('FCM Token:', token);
      // Send this token to your backend for further use
      return token;
  } catch (error) {
      console.error('An error occurred while retrieving token:', error);
  }
}; 

export const onMessageListener = () =>
  new Promise((resolve) => {
    onMessage(messaging, (payload) => {
      console.log("Foreground Notification Received:", payload);
      resolve(payload);
    });
  });
