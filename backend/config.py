import os
from datetime import timedelta

class Config:
    """Application configuration"""
    
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = True
    
    # JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # MySQL Database
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or 'root'
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'restaurant_recommendation'
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT') or 3306)
    
    # MongoDB
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/'
    MONGO_DB = os.environ.get('MONGO_DB', 'restaurant_reviews')
    
    # ML Models
    MODEL_PATH = os.path.join(os.path.dirname(__file__), 'ml', 'models')
    
    # Recommendation weights
    PREFERENCE_WEIGHT = 0.40
    AUTHENTICITY_WEIGHT = 0.30
    DISTANCE_WEIGHT = 0.20
    POPULARITY_WEIGHT = 0.10
    
    # Location settings
    MAX_DISTANCE_KM = 50  # Maximum distance for recommendations
