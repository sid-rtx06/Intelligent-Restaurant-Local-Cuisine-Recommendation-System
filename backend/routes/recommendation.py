from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ml.recommendation_engine import engine
from models.preference import Preference
from models.restaurant import Restaurant
from utils.helpers import success_response, error_response, handle_exceptions

recommendation_bp = Blueprint('recommendation', __name__)

@recommendation_bp.route('/', methods=['POST'])
@jwt_required()
@handle_exceptions
def get_recommendations():
    """
    Get personalized restaurant recommendations
    
    Request body:
    {
        "latitude": float,
        "longitude": float,
        "cuisine_preferences": ["Italian", "Chinese"],  // optional
        "mood_preferences": ["spicy", "healthy"],       // optional
        "budget_min": int,                              // optional
        "budget_max": int,                              // optional
        "max_distance_km": float,                       // optional
        "top_n": int                                    // optional, default 10
    }
    """
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    # Validate location
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    if latitude is None or longitude is None:
        return error_response("Location (latitude, longitude) is required", 400)
    
    try:
        latitude = float(latitude)
        longitude = float(longitude)
    except ValueError:
        return error_response("Invalid latitude or longitude format", 400)
    
    # Get user preferences if not provided
    user_prefs = Preference.find_by_user(user_id)
    
    cuisine_preferences = data.get('cuisine_preferences')
    if not cuisine_preferences and user_prefs:
        cuisine_preferences = user_prefs.get('cuisine_preferences', [])
    
    mood_preferences = data.get('mood_preferences')
    if not mood_preferences and user_prefs:
        mood_preferences = user_prefs.get('mood_preferences', [])
    
    budget_range = None
    if data.get('budget_min') is not None and data.get('budget_max') is not None:
        budget_range = (data['budget_min'], data['budget_max'])
    elif user_prefs:
        budget_range = (user_prefs.get('budget_min', 0), user_prefs.get('budget_max', 10000))
    
    max_distance_km = data.get('max_distance_km')
    if max_distance_km is None and user_prefs:
        max_distance_km = user_prefs.get('preferred_distance_km', 10)
    
    top_n = data.get('top_n', 50)
    
    # Get recommendations
    recommendations = engine.get_recommendations(
        user_id=user_id,
        user_location=(latitude, longitude),
        cuisine_preferences=cuisine_preferences,
        mood_preferences=mood_preferences,
        budget_range=budget_range,
        max_distance_km=max_distance_km,
        top_n=top_n
    )
    
    return success_response({
        'recommendations': recommendations,
        'count': len(recommendations),
        'filters_applied': {
            'location': {'latitude': latitude, 'longitude': longitude},
            'cuisine_preferences': cuisine_preferences,
            'mood_preferences': mood_preferences,
            'budget_range': budget_range,
            'max_distance_km': max_distance_km
        }
    })

@recommendation_bp.route('/nearby', methods=['POST'])
@handle_exceptions
def get_nearby_restaurants():
    """Get nearby restaurants without personalization (no auth required)"""
    data = request.get_json()
    
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    max_distance_km = data.get('max_distance_km', 10)
    
    if latitude is None or longitude is None:
        return error_response("Location (latitude, longitude) is required", 400)
    
    # Get all restaurants and filter by distance
    from utils.helpers import haversine_distance
    
    restaurants = Restaurant.find_all(limit=200)
    nearby = []
    
    for restaurant in restaurants:
        distance = haversine_distance(
            latitude, longitude,
            float(restaurant['latitude']), float(restaurant['longitude'])
        )
        
        if distance <= max_distance_km:
            restaurant['distance_km'] = round(distance, 2)
            nearby.append(restaurant)
    
    # Sort by distance
    nearby.sort(key=lambda x: x['distance_km'])
    
    return success_response({
        'restaurants': nearby[:100],
        'count': len(nearby)
    })
