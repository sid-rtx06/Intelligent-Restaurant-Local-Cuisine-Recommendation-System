import json
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.restaurant import Restaurant
from models.review import Review
from ml.sentiment_analyzer import analyzer
from ml.fake_review_detector import detector, generate_synthetic_training_data
from utils.database import Database

def setup_sample_data():
    """Load sample restaurants and reviews into the database"""
    
    print("=" * 60)
    print("Setting up sample data...")
    print("=" * 60)
    
    # Load sample restaurants
    base_dir = os.path.dirname(os.path.abspath(__file__))
    restaurants_path = os.path.join(base_dir, 'data', 'sample_restaurants.json')
    
    with open(restaurants_path, 'r') as f:
        restaurants = json.load(f)
    
    print(f"\n[INFO] Loading {len(restaurants)} sample restaurants...")
    
    for restaurant in restaurants:
        try:
            restaurant_id = Restaurant.create(
                name=restaurant['name'],
                cuisine_type=restaurant['cuisine_type'],
                latitude=restaurant['latitude'],
                longitude=restaurant['longitude'],
                address=restaurant['address'],
                city=restaurant['city'],
                price_range=restaurant['price_range'],
                description=restaurant.get('description'),
                image_url=restaurant.get('image_url'),
                special_dish=restaurant.get('special_dish'),
                best_seller=restaurant.get('best_seller'),
                high_protein=restaurant.get('high_protein')
            )
            
            # Update scores
            Restaurant.update_scores(
                restaurant_id,
                authenticity_score=restaurant.get('authenticity_score', 0.5),
                popularity_score=restaurant.get('popularity_score', 0.5)
            )
            
            print(f"  [OK] Created: {restaurant['name']}")
        except Exception as e:
            print(f"  [ERROR] Error creating {restaurant['name']}: {e}")
    
    # Load sample reviews
    reviews_path = os.path.join(base_dir, 'data', 'sample_reviews.json')
    
    with open(reviews_path, 'r') as f:
        reviews = json.load(f)
    
    print(f"\n[INFO] Loading {len(reviews)} sample reviews...")
    
    for review in reviews:
        try:
            # Analyze sentiment
            sentiment = analyzer.analyze_sentiment(review['text'])
            
            # Detect fake reviews
            authenticity_score = detector.predict_authenticity(review['text'])
            is_authentic = authenticity_score > 0.5
            
            # Create review
            Review.create(
                restaurant_id=review['restaurant_id'],
                user_id=review['user_id'],
                text=review['text'],
                rating=review['rating'],
                sentiment=sentiment,
                authenticity_score=authenticity_score,
                is_authentic=is_authentic
            )
            
            print(f"  [OK] Created review for restaurant {review['restaurant_id']}")
        except Exception as e:
            print(f"  [ERROR] Error creating review: {e}")
    
    print("\n" + "=" * 60)
    print(" [OK] Sample data setup complete!")
    print("=" * 60)

def train_ml_models():
    """Train ML models with synthetic data"""
    
    print("\n" + "=" * 60)
    print("Training ML models...")
    print("=" * 60)
    
    # Generate synthetic training data
    print("\n[AI] Generating synthetic training data...")
    training_data = generate_synthetic_training_data()
    print(f"  Generated {len(training_data)} training samples")
    
    # Train fake review detector
    print("\n[AI] Training fake review detector...")
    accuracy = detector.train(training_data)
    
    # Save model
    detector.save_model()
    
    print("\n" + "=" * 60)
    print("[OK] ML models trained and saved!")
    print("=" * 60)

if __name__ == '__main__':
    try:
        # Train ML models first
        train_ml_models()
        
        # Setup sample data
        setup_sample_data()
        
        print("\n[DONE] Setup complete! You can now run the application.")
        print("   Run: python app.py")
        
    except Exception as e:
        print(f"\n[ERROR] Error during setup: {e}")
        import traceback
        traceback.print_exc()
    finally:
        Database.close_connections()
