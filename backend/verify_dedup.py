import requests
import json

def test_deduplication():
    # Test Nearby (No Auth)
    print("Testing Nearby Recommendations (Deduplication)...")
    url = "http://localhost:5000/api/recommendations/nearby"
    data = {
        "latitude": 17.3850,
        "longitude": 78.4867,
        "max_distance_km": 50
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            results = response.json().get('data', {}).get('restaurants', [])
            names = [r['name'] for r in results]
            unique_names = set(names)
            print(f"  Total results: {len(names)}")
            print(f"  Unique names: {len(unique_names)}")
            
            if len(names) == len(unique_names):
                print("  [OK] Deduplication SUCCESS for Nearby")
            else:
                duplicates = [name for name in unique_names if names.count(name) > 1]
                print(f"  [ERROR] Deduplication FAILED. Duplicates found: {duplicates}")
        else:
            print(f"  [ERROR] Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"  [ERROR] Failed to connect: {e}")

if __name__ == "__main__":
    test_deduplication()
