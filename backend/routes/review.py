from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.review import Review
from models.restaurant import Restaurant
from ml.sentiment_analyzer import analyzer
from ml.fake_review_detector import detector
from utils.helpers import success_response, error_response, handle_exceptions

review_bp = Blueprint('review', __name__)

@review_bp.route('/', methods=['POST'])
@review_bp.route('', methods=['POST'])
@jwt_required()
@handle_exceptions
def create_review():
    """
    Create a new review with automatic sentiment analysis and fake detection
    
    Request body:
    {
        "restaurant_id": int,
        "text": string,
        "rating": int (1-5)
    }
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Validate required fields
    restaurant_id = data.get('restaurant_id')
    text = data.get('text')
    rating = data.get('rating')
    
    if not all([restaurant_id, text, rating]):
        return error_response("restaurant_id, text, and rating are required", 400)
    
    # Validate rating
    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            return error_response("Rating must be between 1 and 5", 400)
    except ValueError:
        return error_response("Invalid rating format", 400)
    
    # Check if restaurant exists
    restaurant = Restaurant.find_by_id(restaurant_id)
    if not restaurant:
        return error_response("Restaurant not found", 404)
    
    # Perform sentiment analysis
    sentiment = analyzer.analyze_sentiment(text)
    
    # Perform fake review detection
    authenticity_score = detector.predict_authenticity(text)
    is_authentic = authenticity_score > 0.5  # Threshold for authenticity
    
    # Create review
    review_id = Review.create(
        restaurant_id=restaurant_id,
        user_id=user_id,
        text=text,
        rating=rating,
        sentiment=sentiment,
        authenticity_score=authenticity_score,
        is_authentic=is_authentic
    )
    
    # Update restaurant authenticity score
    stats = Review.get_restaurant_stats(restaurant_id)
    if stats['total_reviews'] > 0:
        Restaurant.update_scores(
            restaurant_id,
            authenticity_score=stats['avg_authenticity']
        )
    
    return success_response({
        'review_id': review_id,
        'sentiment': sentiment,
        'authenticity_score': round(authenticity_score, 3),
        'is_authentic': is_authentic
    }, "Review submitted successfully", 201)

@review_bp.route('/user', methods=['GET'])
@jwt_required()
@handle_exceptions
def get_user_reviews():
    """Get reviews by the current user"""
    user_id = get_jwt_identity()
    limit = int(request.args.get('limit', 50))
    
    reviews = Review.find_by_user(user_id, limit)
    
    return success_response({
        'reviews': reviews,
        'count': len(reviews)
    })

@review_bp.route('/<review_id>', methods=['GET'])
@handle_exceptions
def get_review(review_id):
    """Get a specific review by ID"""
    review = Review.find_by_id(review_id)
    
    if not review:
        return error_response("Review not found", 404)
    
    return success_response({'review': review})

@review_bp.route('/<review_id>/analyze', methods=['POST'])
@jwt_required()
@handle_exceptions
def analyze_review(review_id):
    """Re-analyze a review's sentiment and authenticity"""
    review = Review.find_by_id(review_id)
    
    if not review:
        return error_response("Review not found", 404)
    
    # Re-analyze sentiment
    sentiment = analyzer.analyze_sentiment(review['text'])
    Review.update_sentiment(review_id, sentiment)
    
    # Re-analyze authenticity
    authenticity_score = detector.predict_authenticity(review['text'])
    is_authentic = authenticity_score > 0.5
    Review.update_authenticity(review_id, authenticity_score, is_authentic)
    
    return success_response({
        'sentiment': sentiment,
        'authenticity_score': round(authenticity_score, 3),
        'is_authentic': is_authentic
    }, "Review re-analyzed successfully")

@review_bp.route('/', methods=['GET'])
@review_bp.route('', methods=['GET'])
@handle_exceptions
def get_all_reviews():
    """Get all reviews for admin moderation"""
    limit = int(request.args.get('limit', 100))
    status = request.args.get('status')
    
    reviews = Review.find_all(limit=limit, status=status)
    
    for r in reviews:
        if r.get('restaurant_id'):
            try:
                restaurant = Restaurant.find_by_id(r['restaurant_id'])
                r['restaurant_name'] = restaurant['name'] if restaurant else 'Unknown'
            except:
                r['restaurant_name'] = 'Unknown'
        
        if r.get('user_id'):
            try:
                from models.user import User
                user = User.find_by_id(r['user_id'])
                r['user_name'] = user['name'] if user else 'Anonymous'
            except:
                r['user_name'] = 'Anonymous'
                
    return success_response({
        'reviews': reviews,
        'count': len(reviews)
    })

@review_bp.route('/<review_id>', methods=['PUT'])
@jwt_required()
@handle_exceptions
def update_review_status(review_id):
    """Update review authenticity status (admin action)"""
    data = request.get_json()
    is_authentic = data.get('is_authentic')
    
    if is_authentic is None:
        return error_response("is_authentic is required", 400)
        
    success = Review.update_status(review_id, is_authentic)
    if not success:
        return error_response("Failed to update review status", 500)
        
    return success_response(message="Review status updated successfully")

@review_bp.route('/<review_id>', methods=['DELETE'])
@jwt_required()
@handle_exceptions
def delete_review(review_id):
    """Delete a review (admin action)"""
    success = Review.delete(review_id)
    if not success:
        return error_response("Failed to delete review", 500)
        
    return success_response(message="Review deleted successfully")
