from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.restaurant import Restaurant
from models.review import Review
from utils.helpers import success_response, error_response, handle_exceptions, deduplicate_by_name

restaurant_bp = Blueprint('restaurant', __name__)

@restaurant_bp.route('/', methods=['GET'])
@handle_exceptions
def get_restaurants():
    """Get all restaurants with filtering and search"""
    search = request.args.get('search')
    cuisine = request.args.get('cuisine')
    city = request.args.get('city')
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    
    # Model methods now return unique restaurants by name
    if search:
        restaurants = Restaurant.search(search, limit)
    elif cuisine:
        restaurants = Restaurant.find_by_cuisine(cuisine, limit)
    elif city:
        restaurants = Restaurant.find_by_city(city, limit)
    else:
        restaurants = Restaurant.find_all(limit, offset)
    
    return success_response({
        'restaurants': restaurants,
        'count': len(restaurants)
    })

@restaurant_bp.route('/<int:restaurant_id>', methods=['GET'])
@handle_exceptions
def get_restaurant(restaurant_id):
    """Get restaurant details by ID"""
    restaurant = Restaurant.find_by_id(restaurant_id)
    
    if not restaurant:
        return error_response("Restaurant not found", 404)
    
    # Get review statistics
    stats = Review.get_restaurant_stats(restaurant_id)
    restaurant['review_stats'] = stats
    
    return success_response({'restaurant': restaurant})

@restaurant_bp.route('/<int:restaurant_id>/reviews', methods=['GET'])
@handle_exceptions
def get_restaurant_reviews(restaurant_id):
    """Get reviews for a restaurant"""
    # Check if restaurant exists
    restaurant = Restaurant.find_by_id(restaurant_id)
    if not restaurant:
        return error_response("Restaurant not found", 404)
    
    # Get query parameters
    authentic_only = request.args.get('authentic_only', 'true').lower() == 'true'
    limit = int(request.args.get('limit', 50))
    
    # Get reviews
    reviews = Review.find_by_restaurant(restaurant_id, authentic_only, limit)
    
    return success_response({
        'reviews': reviews,
        'count': len(reviews)
    })

@restaurant_bp.route('/popular', methods=['GET'])
@handle_exceptions
def get_popular_restaurants():
    """Get popular restaurants"""
    limit = int(request.args.get('limit', 10))
    
    # Get more to allow for deduplication
    restaurants = Restaurant.get_popular_restaurants(limit * 2)
    
    # Deduplicate by name
    restaurants = deduplicate_by_name(restaurants)[:limit]
    
    # Add review stats
    for restaurant in restaurants:
        stats = Review.get_restaurant_stats(restaurant['id'])
        restaurant['review_stats'] = stats
    
    return success_response({
        'restaurants': restaurants,
        'count': len(restaurants)
    })

@restaurant_bp.route('/cuisines', methods=['GET'])
@handle_exceptions
def get_cuisines():
    """Get all available cuisine types"""
    from utils.database import execute_query
    
    cuisines = execute_query("SELECT * FROM cuisine_types ORDER BY name")
    
    return success_response({
        'cuisines': cuisines,
        'count': len(cuisines)
    })
