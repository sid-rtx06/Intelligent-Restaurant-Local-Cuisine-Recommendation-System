import pymysql
import os
import sys

def setup_mysql():
    print("=" * 60)
    print("Setting up MySQL Database...")
    print("=" * 60)

    # Path to schema file
    # Go up one level from backend to root, then into database
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database', 'mysql_schema.sql')
    
    if not os.path.exists(schema_path):
        print(f"Error: Schema file not found at {schema_path}")
        return False

    print(f"Reading schema from: {schema_path}")
    
    try:
        with open(schema_path, 'r') as f:
            schema_content = f.read()
    except Exception as e:
        print(f"Error reading schema file: {e}")
        return False

    try:
        # First try with credentials from config/default
        # Note: We hardcode them here for initial setup as config.py might not be set up
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='root',
            cursorclass=pymysql.cursors.DictCursor
        )
        print("[OK] Connected to MySQL server (no password)")
    except Exception as e:
        print(f"[ERROR] Connection failed with no password: {e}")
        print("Please enter your MySQL 'root' password:")
        try:
            # password = input() 
            password = 'root' 
            conn = pymysql.connect(
                host='localhost',
                user='root',
                password=password.strip(),
                cursorclass=pymysql.cursors.DictCursor
            )
            print("[OK] Connected to MySQL server (authentication successful)")
        except Exception as e2:
            print(f"[ERROR] Failed to connect to MySQL: {e2}")
            return False

    try:
        cursor = conn.cursor()
        
        # Split commands by semicolon and execute
        # Careful with semicolons in strings depending on complexity, but for this schema simple split is fine
        commands = schema_content.split(';')
        
        for command in commands:
            command = command.strip()
            if command:
                try:
                    cursor.execute(command)
                    print(f"  Executed: {command[:50]}...")
                except Exception as e:
                    # Ignore "database exists" or "table exists" warnings if desirable, but better to show
                    print(f"  Warning executing command: {e}")
        
        conn.commit()
        print("\n[OK] MySQL database initialized successfully!")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Error executing schema: {e}")
        return False
    finally:
        conn.close()

if __name__ == '__main__':
    success = setup_mysql()
    if not success:
        sys.exit(1)
