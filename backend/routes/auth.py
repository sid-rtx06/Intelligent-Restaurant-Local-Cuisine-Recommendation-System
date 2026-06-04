from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.user import User
from models.preference import Preference
from utils.helpers import success_response, error_response, validate_email, handle_exceptions

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
@handle_exceptions
def signup():
    """User registration endpoint"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'email', 'password']
    for field in required_fields:
        if not data.get(field):
            return error_response(f"Missing required field: {field}", 400)
    
    name = data['name']
    email = data['email']
    password = data['password']
    phone = data.get('phone')
    
    # Validate email format
    if not validate_email(email):
        return error_response("Invalid email format", 400)
    
    # Check if user already exists
    existing_user = User.find_by_email(email)
    if existing_user:
        return error_response("Email already registered", 409)
    
    # Create user
    try:
        user_id = User.create(name, email, password, phone)
        
        # Create default preferences
        Preference.create_or_update(user_id)
        
        # Generate JWT token
        access_token = create_access_token(identity=str(user_id))
        
        return success_response({
            'user_id': user_id,
            'name': name,
            'email': email,
            'access_token': access_token
        }, "User registered successfully", 201)
    
    except Exception as e:
        return error_response(f"Registration failed: {str(e)}", 500)

@auth_bp.route('/login', methods=['POST'])
@handle_exceptions
def login():
    """User login endpoint"""
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return error_response("Email and password are required", 400)
    
    # Find user
    user = User.find_by_email(email)
    if not user:
        return error_response("Invalid email or password", 401)
    
    # Verify password
    if not User.verify_password(password, user['password_hash']):
        return error_response("Invalid email or password", 401)
    
    # Generate JWT token
    access_token = create_access_token(identity=str(user['id']))
    
    return success_response({
        'user_id': user['id'],
        'name': user['name'],
        'email': user['email'],
        'phone': user.get('phone'),
        'access_token': access_token
    }, "Login successful")

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
@handle_exceptions
def get_profile():
    """Get user profile (protected route)"""
    user_id = get_jwt_identity()
    
    user = User.find_by_id(user_id)
    if not user:
        return error_response("User not found", 404)
    
    # Get user preferences
    preferences = Preference.find_by_user(user_id)
    
    return success_response({
        'user': user,
        'preferences': preferences
    })

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
@handle_exceptions
def update_profile():
    """Update user profile (protected route)"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    # Update user info
    name = data.get('name')
    phone = data.get('phone')
    
    if name or phone:
        User.update_profile(user_id, name, phone)
    
    # Update preferences
    cuisine_preferences = data.get('cuisine_preferences')
    mood_preferences = data.get('mood_preferences')
    budget_min = data.get('budget_min')
    budget_max = data.get('budget_max')
    preferred_distance_km = data.get('preferred_distance_km')
    
    if any([cuisine_preferences, mood_preferences, budget_min, budget_max, preferred_distance_km]):
        Preference.create_or_update(
            user_id,
            cuisine_preferences=cuisine_preferences,
            mood_preferences=mood_preferences,
            budget_min=budget_min or 0,
            budget_max=budget_max or 10000,
            preferred_distance_km=preferred_distance_km or 10
        )
    
    return success_response(message="Profile updated successfully")
