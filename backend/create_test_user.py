import sys
import os

# Add backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.user import User
from utils.database import Database

def create_test_user():
    print("Checking if test user exists...")
    existing_user = User.find_by_email("test@example.com")
    
    if existing_user:
        print("Test user already exists.")
    else:
        print("Creating test user: test@example.com / password123")
        try:
            User.create("Test User", "test@example.com", "password123", "+1234567890")
            print("[OK] Test user created successfully!")
        except Exception as e:
            print(f"[X] Error creating test user: {e}")

if __name__ == "__main__":
    try:
        create_test_user()
    finally:
        Database.close_connections()
