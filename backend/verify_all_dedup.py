import requests
import json

def test_all_dedup():
    print("1. Testing Popular Restaurants Deduplication...")
    url_pop = "http://localhost:5000/api/restaurants/popular?limit=20"
    try:
        res = requests.get(url_pop)
        if res.status_code == 200:
            data = res.json().get('data', {}).get('restaurants', [])
            names = [r['name'] for r in data]
            unique_names = set(names)
            print(f"  Popular - Total: {len(names)}, Unique: {len(unique_names)}")
            if len(names) == len(unique_names):
                print("  [OK] Popular Deduplication OK")
            else:
                print(f"  [ERROR] Popular DUPES: {[n for n in unique_names if names.count(n) > 1]}")
    except Exception as e:
        print(f"  Error testing popular: {e}")

    print("\n2. Testing Search/General Listing Deduplication...")
    url_all = "http://localhost:5000/api/restaurants/?limit=20"
    try:
        res = requests.get(url_all)
        if res.status_code == 200:
            data = res.json().get('data', {}).get('restaurants', [])
            names = [r['name'] for r in data]
            unique_names = set(names)
            print(f"  All - Total: {len(names)}, Unique: {len(unique_names)}")
            if len(names) == len(unique_names):
                print("  [OK] All Deduplication OK")
            else:
                print(f"  [ERROR] All DUPES: {[n for n in unique_names if names.count(n) > 1]}")
    except Exception as e:
        print(f"  Error testing all: {e}")

if __name__ == "__main__":
    test_all_dedup()
