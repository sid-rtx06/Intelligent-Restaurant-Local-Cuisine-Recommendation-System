import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import Config
from pymongo import MongoClient

def check_mongodb():
    print(f"Testing connection to MongoDB at: {Config.MONGO_URI}")
    try:
        # Use a short timeout of 3 seconds
        client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=3000)
        
        # Test connection by requesting server info
        info = client.server_info()
        print("[OK] Successfully connected to MongoDB!")
        print(f"   MongoDB Version: {info.get('version')}")
        
        # Check database
        db_name = Config.MONGO_DB
        print(f"\nChecking database: '{db_name}'")
        db = client[db_name]
        
        # List collections
        collections = db.list_collection_names()
        print(f"[OK] Database accessed successfully.")
        print(f"   Found {len(collections)} collections: {', '.join(collections) if collections else 'None'}")
        
        if 'reviews' in collections:
            count = db.reviews.count_documents({})
            print(f"   The 'reviews' collection has {count} documents.")
            
    except Exception as e:
        print(f"[ERROR] Connection error: {e}")

if __name__ == '__main__':
    check_mongodb()
