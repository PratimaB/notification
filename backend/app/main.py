from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.api import api_router
import os

app = FastAPI()

frontend_url=os.getenv('FRONTEND_URL') or ''
# Allow CORS for React frontend
origins = [
    frontend_url,  # Adjust for your React development server
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api")
