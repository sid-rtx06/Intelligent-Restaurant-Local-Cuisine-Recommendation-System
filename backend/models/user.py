import bcrypt
from utils.database import execute_query
from datetime import datetime

class User:
    """User model for authentication and profile management"""
    
    @staticmethod
    def create(name, email, password, phone=None):
        """Create a new user"""
        # Hash password
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Insert user
        query = """
            INSERT INTO users (name, email, password_hash, phone)
            VALUES (%s, %s, %s, %s)
        """
        user_id = execute_query(query, (name, email, password_hash, phone), fetch_all=False)
        
        return user_id
    
    @staticmethod
    def find_by_email(email):
        """Find user by email"""
        query = "SELECT * FROM users WHERE email = %s"
        return execute_query(query, (email,), fetch_one=True)
    
    @staticmethod
    def find_by_id(user_id):
        """Find user by ID"""
        query = "SELECT id, name, email, phone, created_at FROM users WHERE id = %s"
        return execute_query(query, (user_id,), fetch_one=True)
    
    @staticmethod
    def verify_password(password, password_hash):
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    
    @staticmethod
    def update_profile(user_id, name=None, phone=None):
        """Update user profile"""
        updates = []
        params = []
        
        if name:
            updates.append("name = %s")
            params.append(name)
        if phone:
            updates.append("phone = %s")
            params.append(phone)
        
        if not updates:
            return False
        
        params.append(user_id)
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s"
        execute_query(query, tuple(params), fetch_all=False)
        return True
    
    @staticmethod
    def get_all_users(limit=100, offset=0):
        """Get all users with pagination"""
        query = "SELECT id, name, email, phone, created_at FROM users LIMIT %s OFFSET %s"
        return execute_query(query, (limit, offset))
