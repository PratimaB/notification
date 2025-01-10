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

@api_router.get("/hello")
async def hello():
    try:
        return {"message": "Notification -1 sent successfully"}
    except Exception as e:
        return {"error": str(e)}    