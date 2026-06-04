import requests
import json
from collections import Counter

BASE_URL = "http://localhost:5000/api"

def check_dupes(name, endpoint, method="GET", data=None):
    print(f"\n--- Checking {name} ({endpoint}) ---")
    try:
        if method == "GET":
            res = requests.get(f"{BASE_URL}{endpoint}")
        else:
            res = requests.post(f"{BASE_URL}{endpoint}", json=data)
        
        if res.status_code != 200:
            print(f"  Error: {res.status_code} - {res.text}")
            return
            
        res_json = res.json()
        items = []
        if 'recommendations' in res_json.get('data', {}):
            items = res_json['data']['recommendations']
        elif 'restaurants' in res_json.get('data', {}):
            items = res_json['data']['restaurants']
            
        names = [curr['name'] for curr in items]
        counts = Counter(names)
        dupes = {k: v for k, v in counts.items() if v > 1}
        
        print(f"  Total items: {len(names)}")
        print(f"  Unique items: {len(set(names))}")
        if dupes:
            print(f"  [ERROR] DUPES FOUND: {dupes}")
        else:
            print("  [OK] No duplicates found.")
            
    except Exception as e:
        print(f"  Connection error: {e}")

if __name__ == "__main__":
    # 1. Popular
    check_dupes("Popular", "/restaurants/popular?limit=20")
    
    # 2. Search
    check_dupes("Search (All)", "/restaurants/?limit=20")
    
    # 3. Nearby
    nearby_data = {
        "latitude": 17.3850,
        "longitude": 78.4867,
        "max_distance_km": 50
    }
    check_dupes("Nearby", "/recommendations/nearby", "POST", nearby_data)
    
    # 4. Personalized (Need Auth)
    # We'll skip for now or try without auth if allowed (it will likely fail 401)
    print("\nSkipping personalized due to auth requirement for now.")
