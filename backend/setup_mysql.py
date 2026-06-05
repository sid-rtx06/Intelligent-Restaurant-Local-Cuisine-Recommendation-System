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
        # Fallback for container deployment where only the backend directory is present
        schema_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mysql_schema.sql')
        
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

    mysql_host = os.environ.get('MYSQL_HOST') or 'localhost'
    mysql_user = os.environ.get('MYSQL_USER') or 'root'
    mysql_password = os.environ.get('MYSQL_PASSWORD') or 'root'
    mysql_db = os.environ.get('MYSQL_DB') or 'restaurant_recommendation'
    mysql_port = int(os.environ.get('MYSQL_PORT') or 3306)

    conn = None
    connected_to_db = False

    try:
        # First try to connect to the target database directly (for environments like Aiven where database is pre-created)
        conn = pymysql.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            port=mysql_port,
            database=mysql_db,
            cursorclass=pymysql.cursors.DictCursor
        )
        print(f"[OK] Connected directly to database: {mysql_db}")
        connected_to_db = True
    except Exception as e:
        print(f"[INFO] Could not connect directly to database '{mysql_db}': {e}. Trying connection to root...")
        try:
            conn = pymysql.connect(
                host=mysql_host,
                user=mysql_user,
                password=mysql_password,
                port=mysql_port,
                cursorclass=pymysql.cursors.DictCursor
            )
            print(f"[OK] Connected to MySQL server root at {mysql_host}:{mysql_port}")
        except Exception as e2:
            print(f"[ERROR] Failed to connect to MySQL: {e2}")
            return False

    try:
        cursor = conn.cursor()
        
        # Split commands by semicolon and execute
        commands = schema_content.split(';')
        
        for command in commands:
            command = command.strip()
            if command:
                # Skip CREATE DATABASE and USE commands if we are already connected directly to the database
                # (prevents privilege errors on managed databases like Aiven)
                if connected_to_db and (command.upper().startswith("CREATE DATABASE") or command.upper().startswith("USE ")):
                    print(f"  Skipping database selection command: {command[:50]}...")
                    continue
                try:
                    cursor.execute(command)
                    print(f"  Executed: {command[:50]}...")
                except Exception as e:
                    print(f"  Warning executing command: {e}")
        
        conn.commit()
        print("\n[OK] MySQL database initialized successfully!")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] Error executing schema: {e}")
        return False
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    success = setup_mysql()
    if not success:
        sys.exit(1)
