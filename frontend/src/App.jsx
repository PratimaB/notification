import React from "react";
import { Routes, Route } from "react-router-dom";
import { useState, useEffect } from "react";
import Navigationbar from "./components/Navigationbar";   
import Register from "./components/Register";
import About from "./components/About";
import Login from "./components/Login.jsx"; 

import { requestForToken, onMessageListener } from "../firebaseConfig.js";


const App = () => {
    // Request for token on app load
    const [token,setToken] = useState("");


  useEffect(() => {
    requestForToken().then((token) => setToken(token)); 
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
  return (
    <div>
      <Navigationbar />
      <Routes>
        <Route path="/" element={<Login clienttoken={ token }/>} />
        <Route path="/register" element={<Register />} />
        <Route path="/about" element={<About />} />
        </Routes>
    </div>
  );
};

export default App;
