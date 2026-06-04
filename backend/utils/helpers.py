import math
from datetime import datetime
from functools import wraps
from flask import jsonify

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    Returns distance in kilometers
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
    
    return c * r

def validate_email(email):
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate phone number format"""
    import re
    # Remove spaces and dashes
    phone = phone.replace(' ', '').replace('-', '')
    pattern = r'^\+?1?\d{10,15}$'
    return re.match(pattern, phone) is not None

def success_response(data=None, message="Success", status=200):
    """Standard success response format"""
    response = {
        "success": True,
        "message": message
    }
    if data is not None:
        response["data"] = data
    return jsonify(response), status

def error_response(message="An error occurred", status=400, errors=None):
    """Standard error response format"""
    response = {
        "success": False,
        "message": message
    }
    if errors:
        response["errors"] = errors
    return jsonify(response), status

def handle_exceptions(f):
    """Decorator to handle exceptions in route handlers"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(f"Error in {f.__name__}: {str(e)}")
            return error_response(f"Internal server error: {str(e)}", 500)
    return decorated_function

def deduplicate_by_name(items):
    """Deduplicate a list of dictionaries by a normalized 'name' key"""
    import re
    
    seen_normalized = set()
    unique_items = []
    
    # Common words to remove for normalization
    noise_words = [
        'restaurant', 'hotel', 'cafe', 'bar', 'grill', 'multicuisine', 
        'bakery', 'sweets', 'junction', 'kitchen', 'point'
    ]
    noise_pattern = re.compile(r'\b(' + '|'.join(noise_words) + r')\b', re.IGNORECASE)

    for item in items:
        name = item.get('name', '')
        if not name:
            continue
            
        # 1. Basic normalization
        norm = name.lower().strip()
        
        # 2. Handle curly quotes and other characters
        norm = norm.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
        
        # 3. Handle specific known misspellings/aliases
        if 'sawagth' in norm:
            norm = norm.replace('sawagth', 'swagath')
        if 'mefil' in norm:
            norm = norm.replace('mefil', 'mehfil')
        
        # 4. Remove common suffixes/prefixes and non-alphanumeric noise
        # This helps match "Lucky" with "Lucky Restaurant"
        clean_name = noise_pattern.sub('', norm)
        clean_name = re.sub(r'[^a-z0-9]', '', clean_name)
        
        # 5. Use the safest key (if clean_name becomes empty, fallback to norm)
        key = clean_name if clean_name else norm
        
        if key not in seen_normalized:
            unique_items.append(item)
            seen_normalized.add(key)
            
    return unique_items

def format_datetime(dt):
    """Format datetime for JSON serialization"""
    if isinstance(dt, datetime):
        return dt.isoformat()
    return dt
