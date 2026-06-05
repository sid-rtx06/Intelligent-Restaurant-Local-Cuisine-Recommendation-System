import time
import pymysql
from pymongo import MongoClient
from config import Config

def wait_for_mysql():
    print("Waiting for MySQL to be ready...")
    start_time = time.time()
    while True:
        try:
            conn = pymysql.connect(
                host=Config.MYSQL_HOST,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                port=Config.MYSQL_PORT,
                connect_timeout=2
            )
            conn.close()
            print("MySQL is ready!")
            return True
        except Exception as e:
            if time.time() - start_time > 60:
                print(f"Timeout waiting for MySQL: {e}")
                return False
            time.sleep(2)

def wait_for_mongodb():
    print("Waiting for MongoDB to be ready...")
    start_time = time.time()
    while True:
        try:
            client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=2000)
            client.server_info()
            client.close()
            print("MongoDB is ready!")
            return True
        except Exception as e:
            if time.time() - start_time > 60:
                print(f"Timeout waiting for MongoDB: {e}")
                return False
            time.sleep(2)

if __name__ == '__main__':
    mysql_ready = wait_for_mysql()
    mongo_ready = wait_for_mongodb()
    if not (mysql_ready and mongo_ready):
        print("Required databases not available. Exiting.")
        exit(1)
    print("All databases are ready! Proceeding.")
