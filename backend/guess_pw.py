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
    passwords = ['sujal', '', 'sruja', 'root', 'password', 'admin', '12345678']
    for p in passwords:
        if test_connection(p):
            print(f"FOUND: '{p}'")
            sys.exit(0)
    sys.exit(1)
