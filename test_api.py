import urllib.request
import urllib.error
import json
import time

BASE_URL = "https://ai-smart-cuisine-finder.netlify.app/api"
# Or backend direct: BASE_URL = "https://intelligent-restaurant-local-cuisine.onrender.com/api"

def make_request(url, method="GET", data=None, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
        
    req_data = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=req_data, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            res_data = response.read().decode("utf-8")
            return json.loads(res_data), response.status
    except urllib.error.HTTPError as e:
        err_data = e.read().decode("utf-8")
        try:
            return json.loads(err_data), e.code
        except:
            return {"error": err_data}, e.code
    except Exception as e:
        return {"error": str(e)}, 500

def run_tests():
    print("1. Testing Health Endpoint...")
    health_res, status = make_request(f"{BASE_URL}/health")
    print(f"Status: {status}, Response: {json.dumps(health_res, indent=2)}")
    
    # Generate unique email
    email = f"test_{int(time.time())}@example.com"
    signup_data = {
        "name": "Integration Test User",
        "email": email,
        "password": "TestPassword123!"
    }
    
    print("\n2. Testing User Signup...")
    signup_res, status = make_request(f"{BASE_URL}/auth/signup", method="POST", data=signup_data)
    print(f"Status: {status}, Response: {json.dumps(signup_res, indent=2)}")
    
    if status != 201:
        print("Signup failed. Stopping tests.")
        return
        
    token = signup_res.get("data", {}).get("access_token")
    if not token:
        print("Token not found in signup response. Stopping tests.")
        return
        
    print("\n3. Testing Recommendations API (No trailing slash in URL)...")
    rec_data = {
        "latitude": 17.3850,
        "longitude": 78.4867,
        "cuisine_preferences": ["Indian"],
        "max_distance_km": 15
    }
    # Test path WITHOUT trailing slash: /recommendations
    rec_res, status = make_request(f"{BASE_URL}/recommendations", method="POST", data=rec_data, token=token)
    print(f"Status: {status}, Response (truncated): {json.dumps(rec_res, indent=2)[:400]}...")
    
    print("\n4. Testing Review Submission (Creating a review for restaurant ID 1)...")
    review_data = {
        "restaurant_id": 1,
        "text": "The food here was really delicious and the ambience was lovely. Highly recommended!",
        "rating": 5
    }
    # Test path WITHOUT trailing slash: /reviews
    review_res, status = make_request(f"{BASE_URL}/reviews", method="POST", data=review_data, token=token)
    print(f"Status: {status}, Response: {json.dumps(review_res, indent=2)}")

if __name__ == "__main__":
    run_tests()
