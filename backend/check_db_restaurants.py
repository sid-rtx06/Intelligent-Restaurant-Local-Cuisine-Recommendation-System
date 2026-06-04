from utils.database import execute_query
import json

def check_restaurants():
    try:
        results = execute_query("SELECT name FROM restaurants")
        names = [r['name'] for r in results]
        print(f"Total restaurants in DB: {len(names)}")
        print(json.dumps(names))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_restaurants()
