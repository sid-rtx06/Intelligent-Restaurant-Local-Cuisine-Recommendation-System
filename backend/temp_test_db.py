import pymysql
import sys

def test_connection(password):
    print(f"Testing connection with password: '{password}'")
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password=password,
            database='restaurant_recommendation'
        )
        print("[OK] Success!")
        conn.close()
        return True
    except Exception as e:
        print(f"[X] Failed: {e}")
        return False

if __name__ == "__main__":
    passwords = ['sujal', '']
    for p in passwords:
        if test_connection(p):
            print(f"\nFOUND WORKING PASSWORD: '{p}'")
            sys.exit(0)
    print("\nNo working password found among tested options.")
    sys.exit(1)
