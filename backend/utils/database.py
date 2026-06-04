import pymysql
from pymongo import MongoClient
from config import Config

class Database:
    """Database connection manager for MySQL and MongoDB"""
    
    _mysql_connection = None
    _mongo_client = None
    _mongo_db = None
    
    @classmethod
    def get_mysql_connection(cls):
        """Get MySQL connection"""
        if cls._mysql_connection is None or not cls._mysql_connection.open:
            try:
                cls._mysql_connection = pymysql.connect(
                    host=Config.MYSQL_HOST,
                    user=Config.MYSQL_USER,
                    password=Config.MYSQL_PASSWORD,
                    database=Config.MYSQL_DB,
                    port=Config.MYSQL_PORT,
                    cursorclass=pymysql.cursors.DictCursor,
                    autocommit=True,
                    connect_timeout=5
                )
            except Exception as e:
                print(f"[ERROR] Critical Error: Could not connect to MySQL at {Config.MYSQL_HOST}:{Config.MYSQL_PORT}")
                print(f"   Reason: {e}")
                print("   Please ensure MySQL service is running and credentials in config.py are correct.")
                raise
        return cls._mysql_connection
    
    @classmethod
    def get_mongo_db(cls):
        """Get MongoDB database"""
        if cls._mongo_client is None:
            try:
                cls._mongo_client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=5000)
                # Force a connection check
                cls._mongo_client.server_info()
                cls._mongo_db = cls._mongo_client[Config.MONGO_DB]
            except Exception as e:
                print(f"[ERROR] Critical Error: Could not connect to MongoDB at {Config.MONGO_URI}")
                print(f"   Reason: {e}")
                print("   Please ensure MongoDB service is running.")
                raise
        return cls._mongo_db
    
    @classmethod
    def close_connections(cls):
        """Close all database connections"""
        if cls._mysql_connection and cls._mysql_connection.open:
            cls._mysql_connection.close()
        if cls._mongo_client:
            cls._mongo_client.close()

def execute_query(query, params=None, fetch_one=False, fetch_all=True):
    """Execute MySQL query and return results"""
    connection = Database.get_mysql_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, params or ())
            if fetch_one:
                return cursor.fetchone()
            elif fetch_all:
                return cursor.fetchall()
            else:
                return cursor.lastrowid
    except Exception as e:
        print(f"Database error: {e}")
        raise

def get_reviews_collection():
    """Get MongoDB reviews collection"""
    db = Database.get_mongo_db()
    return db.reviews
