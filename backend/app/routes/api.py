from typing import Any
from fastapi import APIRouter, HTTPException
from mysql.connector.abstracts import MySQLConnectionAbstract, MySQLCursorAbstract

from mysql.connector.pooling import PooledMySQLConnection
from pydantic import BaseModel, EmailStr
from app.db.connection import create_connection
from app.routes.firebase_service import send_push_notification

api_router = APIRouter()

class User(BaseModel):
    name: str
    email: EmailStr
    password: str

class NotificationRequest(BaseModel):
    token: str
    title: str
    body: str

class LoginRequest(BaseModel):
    email: str
    password: str
    fcm_token: str

@api_router.post("/register")
async def register_user(user: User):
    connection: PooledMySQLConnection | MySQLConnectionAbstract | None = create_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:

        cursor: MySQLCursorAbstract | Any = connection.cursor()
        query = """
            INSERT INTO users (username, email, password)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (user.name, user.email, user.password))
        connection.commit()
        # Step 2: Insert notification for admin
        query = """
            INSERT INTO notifications (title, body, type, source)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query,(
            "New User Registration",f"User {user.name} has registered.","foreground","SRX App",)
        )
        connection.commit()

        return {"message": "User registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        connection.close()

@api_router.post("/send-notification/")
async def send_notification(payload: NotificationRequest):
    try:
        token = payload.token
        title = payload.title
        body = payload.body
        send_push_notification(token, title, body)
        return {"message": "Notification sent successfully"}
    except Exception as e:
        return {"error": str(e)}

@api_router.get("/notifications")
async def get_notifications():
    """
    Fetch notifications for the admin user.
    """
    connection: PooledMySQLConnection | MySQLConnectionAbstract | None = create_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")


    try:
        cursor=connection.cursor()
        # Query to fetch all notifications
        query = """
            SELECT id, title, body, type, source, received_at
            FROM notifications
            ORDER BY received_at DESC
        """
        cursor.execute(query)
        notifications = cursor.fetchall()

        return {"success": True, "notifications": notifications}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    
    finally:
        cursor.close()
        connection.close()

# Login payload for user
@api_router.post("/login")
async def login_user(data: LoginRequest):
    email = data.email
    password = data.password    
    fcm_token = data.fcm_token

    connection = create_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    cursor: MySQLCursorAbstract | Any = connection.cursor(dictionary=True)

    try:
        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
  
        if user:

            cursor.execute("SELECT id FROM usersToken WHERE email = %s", (email,))
            userLink = cursor.fetchone()
            if  userLink :
                # Update FCM token
                cursor.execute(
                    "UPDATE usersToken SET fcm_token = %s, last_login = NOW() WHERE email = %s",
                    (fcm_token, email)
                )
                connection.commit()
            else:
                # Register the user with FCM token
                cursor.execute(
                    "INSERT INTO usersToken (email, fcm_token) VALUES (%s, %s)",
                    (email, fcm_token)
                )
                connection.commit()

         # Notify other users
        cursor.execute("SELECT email, fcm_token FROM usersToken WHERE email != %s", (email,))
        other_users = cursor.fetchall()

        for email, usertoken in other_users:
            if email:
                send_push_notification(
                    str(usertoken),
                    title="User Login Alert",
                    body=f"{email} has logged into the application."
                ) 

        return {"message": "Login successful and notifications sent."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        connection.close()
    

@api_router.get("/hello")
async def hello():
    try:
        return {"message": "Hello GET from the server. "}
    except Exception as e:
        return {"error": str(e)}    
    
@api_router.post("/show")
async def show():
    connection: PooledMySQLConnection | MySQLConnectionAbstract | None = create_connection()
    if not connection:
        raise HTTPException(status_code=500, detail="Database connection failed")
    else:
        print(connection)
    try:
        return {"message": "Hello POST from the server. "}
    except Exception as e:
        return {"error": str(e)}      