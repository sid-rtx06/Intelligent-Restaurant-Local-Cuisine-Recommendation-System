import pymysql
import sys

def test_connection(password):
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password=password,
            database='restaurant_recommendation'
        )
        conn.close()
        return True
    except Exception as e:
        return False

if __name__ == "__main__":
    passwords = ['Sujal', 'Srujal', 'Srujal@123', 'Sujal@123', 'root123']
    for p in passwords:
        if test_connection(p):
            print(f"FOUND: '{p}'")
            sys.exit(0)
    sys.exit(1)
