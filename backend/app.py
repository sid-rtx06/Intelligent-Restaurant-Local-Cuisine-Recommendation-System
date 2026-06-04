from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
import sys
import os

# Add backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_app():
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Initialize extensions
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    jwt = JWTManager(app)
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.restaurant import restaurant_bp
    from routes.recommendation import recommendation_bp
    from routes.review import review_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(restaurant_bp, url_prefix='/api/restaurants')
    app.register_blueprint(recommendation_bp, url_prefix='/api/recommendations')
    app.register_blueprint(review_bp, url_prefix='/api/reviews')
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        from utils.database import Database
        
        status = {
            'status': 'healthy',
            'database': {
                'mysql': 'unknown',
                'mongodb': 'unknown'
            }
        }
        
        try:
            Database.get_mysql_connection()
            status['database']['mysql'] = 'connected'
        except:
            status['database']['mysql'] = 'disconnected'
            status['status'] = 'degraded'
            
        try:
            Database.get_mongo_db()
            status['database']['mongodb'] = 'connected'
        except:
            status['database']['mongodb'] = 'disconnected'
            status['status'] = 'degraded'
            
        return jsonify(status)
    
    # Root endpoint
    @app.route('/', methods=['GET'])
    def root():
        return jsonify({
            'message': 'Intelligent Restaurant Recommendation System API',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/auth',
                'restaurants': '/api/restaurants',
                'recommendations': '/api/recommendations',
                'reviews': '/api/reviews'
            }
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'message': 'Endpoint not found'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500
    
    return app

if __name__ == '__main__':
    # Auto-initialize database if MySQL is reachable but DB/Tables are missing
    try:
        from utils.database import Database
        from setup_mysql import setup_mysql
        
        print("[CHECK] Checking database status...")
        try:
            # Check if we can connect and if tables exist
            from utils.database import execute_query
            execute_query("SELECT 1 FROM restaurants LIMIT 1")
            print("[OK] Database and tables verified.")
        except Exception as e:
            print(f"[WARNING] Database not ready ({e}). Attempting auto-initialization...")
            if setup_mysql():
                print("[OK] Database initialized successfully.")
                # Also load sample data if restaurants still empty
                try:
                    from setup_data import setup_sample_data
                    setup_sample_data()
                except Exception as e_data:
                    print(f"[WARNING] Could not load sample data: {e_data}")
            else:
                print("[ERROR] Auto-initialization failed. Please check MySQL service.")
    except Exception as e:
        print(f"[WARNING] Error during auto-init check: {e}")

    app = create_app()
    print("=" * 60)
    print("[API] Restaurant Recommendation System API")
    print("=" * 60)
    print("Server starting on http://localhost:5000")
    print("API Documentation:")
    print("  - Auth:            /api/auth")
    print("  - Restaurants:     /api/restaurants")
    print("  - Recommendations: /api/recommendations")
    print("  - Reviews:         /api/reviews")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
