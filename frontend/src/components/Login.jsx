import React from "react";
import axios from "axios";
import { useState } from "react";   

const Login = (props) => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const token = props.clienttoken;


    const handleSubmit = async (e) => { 
        e.preventDefault();

        fetch('http://localhost:8000/api/login', {
            method: 'POST',
            body: JSON.stringify({
            email: email,
            password: password,
            fcm_token: token
            //email:"aaa@gmail.com" ,
            //password:"abc",
            //fcm_token:"fW3EtSplMQPtLsmVEgg2Ga:APA91bHf2JjFyrjGvCe3RfUQ1-CeKxXHddtI0Uj76DnfdrBIe0YjWpseDwLG-eAEUhhFNpdDHLbw34lqGIjgm1NtnYXtmHLt-JDzh7vUkAva5p0mKBrnFFM"

            }),
            headers: {
               'Content-type': 'application/json; charset=UTF-8',
            },
         })
            .then((response) => response.json())
            .then((json) => {
               console.log(json);
            })
            .catch((err) => {
               console.log(err.message);
            });
      };

    return (
        <div style={{ maxWidth: "400px", margin: "auto", padding: "20px" }}>
            <h3>Login</h3>
            <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: "15px" }}>
                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    style={{ width: "100%", padding: "8px", marginTop: "5px" }}
                />
            </div>
            <div style={{ marginBottom: "15px" }}>
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    style={{ width: "100%", padding: "8px", marginTop: "5px" }}
                />
            </div> 
                <button type="submit"  
                style={{ padding: "10px 15px" }}>Login</button>
            </form>
        </div>
    );
};

export default Login;