
import pymysql
import sys

try:
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        cursorclass=pymysql.cursors.DictCursor
    )
    print("[OK] Connected successfully")
    conn.close()
except Exception as e:
    print(f"[X] Connection error: {e}")
