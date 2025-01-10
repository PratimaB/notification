import React from "react";
import Register from "./components/Register";
import { useEffect } from "react";
import { requestForToken, onMessageListener } from "../firebaseConfig.js";


const App = () => {
  useEffect(() => {
  // Request for token on app load
    requestForToken();
    // Listen for foreground notifications
    onMessageListener()
      .then((payload) => {
        console.log("Notification in foreground:", payload);
        if (Notification.permission === "granted") {
          const { notification } = payload;
          new Notification(notification.title, {
            body: notification.body,
            icon: notification.icon,
          });
        }
      })
      .catch((err) => console.log("Failed to receive foreground notification:", err));
  }, []);
  return <Register />;
};

/*
 function App() {
  return (
    <div>
      <Register />
    </div>
  );
} 
*/
export default App;
