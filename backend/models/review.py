from utils.database import get_reviews_collection
from datetime import datetime
from bson import ObjectId

class Review:
    """Review model for MongoDB review storage"""
    
    @staticmethod
    def create(restaurant_id, user_id, text, rating, sentiment=None, 
               authenticity_score=0.5, is_authentic=True):
        """Create a new review"""
        collection = get_reviews_collection()
        
        review_doc = {
            'restaurant_id': restaurant_id,
            'user_id': user_id,
            'text': text,
            'rating': rating,
            'sentiment': sentiment or {},
            'authenticity_score': authenticity_score,
            'is_authentic': is_authentic,
            'created_at': datetime.utcnow()
        }
        
        result = collection.insert_one(review_doc)
        return str(result.inserted_id)
    
    @staticmethod
    def find_by_restaurant(restaurant_id, authentic_only=True, limit=50):
        """Find reviews for a restaurant"""
        collection = get_reviews_collection()
        
        query = {'restaurant_id': restaurant_id}
        if authentic_only:
            query['is_authentic'] = True
        
        reviews = list(collection.find(query).sort('created_at', -1).limit(limit))
        
        # Convert ObjectId to string
        for review in reviews:
            review['_id'] = str(review['_id'])
        
        return reviews
    
    @staticmethod
    def find_by_user(user_id, limit=50):
        """Find reviews by a user"""
        collection = get_reviews_collection()
        
        reviews = list(collection.find({'user_id': user_id}).sort('created_at', -1).limit(limit))
        
        for review in reviews:
            review['_id'] = str(review['_id'])
        
        return reviews
    
    @staticmethod
    def find_by_id(review_id):
        """Find review by ID"""
        collection = get_reviews_collection()
        
        try:
            review = collection.find_one({'_id': ObjectId(review_id)})
            if review:
                review['_id'] = str(review['_id'])
            return review
        except:
            return None
    
    @staticmethod
    def update_sentiment(review_id, sentiment):
        """Update review sentiment"""
        collection = get_reviews_collection()
        
        try:
            collection.update_one(
                {'_id': ObjectId(review_id)},
                {'$set': {'sentiment': sentiment}}
            )
            return True
        except:
            return False
    
    @staticmethod
    def update_authenticity(review_id, authenticity_score, is_authentic):
        """Update review authenticity score"""
        collection = get_reviews_collection()
        
        try:
            collection.update_one(
                {'_id': ObjectId(review_id)},
                {'$set': {
                    'authenticity_score': authenticity_score,
                    'is_authentic': is_authentic
                }}
            )
            return True
        except:
            return False
    
    @staticmethod
    def get_restaurant_stats(restaurant_id):
        """Get restaurant review statistics"""
        from utils.database import Database

        db = Database.get_mongo_db()
        reviews = list(db.reviews.find({"restaurant_id": restaurant_id}))

        total_reviews = len(reviews)

        if total_reviews == 0:
            return {
                "total_reviews": 0,
                "average_rating": 0,
                "avg_rating": 0,
                "avg_authenticity": 0.5,
                "sentiment_counts": {}
            }

        # Calculate average rating
        avg_rating = sum(r.get("rating", 0) for r in reviews) / total_reviews
        
        # Calculate average authenticity score
        avg_authenticity = sum(r.get("authenticity_score", 0.5) for r in reviews) / total_reviews

        # Handle sentiment safely
        sentiments = []
        for r in reviews:
            sentiment = r.get("sentiment", "neutral")

            if isinstance(sentiment, dict):
                sentiments.append(sentiment.get("label", "neutral"))
            else:
                sentiments.append(sentiment)

        sentiment_counts = {}
        for s in sentiments:
            sentiment_counts[s] = sentiment_counts.get(s, 0) + 1

        return {
            "total_reviews": total_reviews,
            "average_rating": round(avg_rating, 2),
            "avg_rating": round(avg_rating, 2),
            "avg_authenticity": round(avg_authenticity, 4),
            "sentiment_counts": sentiment_counts
        }