import numpy as np
from typing import List, Dict, Tuple
from utils.helpers import haversine_distance, deduplicate_by_name
from models.restaurant import Restaurant
from utils.database import execute_query, get_reviews_collection
from config import Config

class RecommendationEngine:
    """
    Hybrid Recommendation Engine combining:
    1. Content-based filtering (preferences, cuisine, budget)
    2. Collaborative filtering (similar user behavior)
    3. Location-based filtering (distance, regional popularity)
    4. Authenticity and sentiment scores
    """
    
    def __init__(self):
        self.preference_weight = Config.PREFERENCE_WEIGHT
        self.authenticity_weight = Config.AUTHENTICITY_WEIGHT
        self.distance_weight = Config.DISTANCE_WEIGHT
        self.popularity_weight = Config.POPULARITY_WEIGHT
    
    def get_recommendations(
        self,
        user_id: int,
        user_location: Tuple[float, float],
        cuisine_preferences: List[str] = None,
        mood_preferences: List[str] = None,
        budget_range: Tuple[int, int] = None,
        max_distance_km: float = None,
        top_n: int = 50
    ) -> List[Dict]:
        """
        Get personalized restaurant recommendations
        
        Args:
            user_id: User ID
            user_location: (latitude, longitude) tuple
            cuisine_preferences: List of preferred cuisines
            mood_preferences: List of mood preferences (spicy, healthy, etc.)
            budget_range: (min, max) price range
            max_distance_km: Maximum distance in kilometers
            top_n: Number of recommendations to return
            
        Returns:
            List of restaurant dictionaries with scores and explanations
        """
        if max_distance_km is None:
            max_distance_km = Config.MAX_DISTANCE_KM
        
        # Get all restaurants (model handles deduplication)
        restaurants = Restaurant.find_all(limit=1000)
        
        if not restaurants:
            return []
        
        # Calculate scores for each restaurant
        scored_restaurants = []
        
        for restaurant in restaurants:
            # Calculate distance
            distance = haversine_distance(
                user_location[0], user_location[1],
                float(restaurant['latitude']), float(restaurant['longitude'])
            )
            
            # Skip if too far
            if distance > max_distance_km:
                continue
            
            # Calculate component scores
            preference_score = self._calculate_preference_score(
                restaurant, cuisine_preferences, mood_preferences
            )
            
            authenticity_score = float(restaurant.get('authenticity_score', 0.5))
            
            distance_score = self._calculate_distance_score(distance, max_distance_km)
            
            popularity_score = float(restaurant.get('popularity_score', 0))
            
            # Calculate weighted final score
            final_score = (
                preference_score * self.preference_weight +
                authenticity_score * self.authenticity_weight +
                distance_score * self.distance_weight +
                popularity_score * self.popularity_weight
            )
            
            # Generate explanation
            explanation = self._generate_explanation(
                restaurant, preference_score, authenticity_score,
                distance_score, popularity_score, distance,
                cuisine_preferences, mood_preferences
            )
            
            # Add to results
            scored_restaurants.append({
                **restaurant,
                'distance_km': round(distance, 2),
                'recommendation_score': round(final_score, 4),
                'score_breakdown': {
                    'preference': round(preference_score, 3),
                    'authenticity': round(authenticity_score, 3),
                    'distance': round(distance_score, 3),
                    'popularity': round(popularity_score, 3)
                },
                'explanation': explanation
            })
        
        # Sort by score and return top N
        scored_restaurants.sort(key=lambda x: x['recommendation_score'], reverse=True)
        
        # Apply collaborative filtering boost
        if user_id:
            scored_restaurants = self._apply_collaborative_boost(
                user_id, scored_restaurants
            )
        
        return scored_restaurants[:top_n]
    
    def _calculate_preference_score(
        self,
        restaurant: Dict,
        cuisine_preferences: List[str],
        mood_preferences: List[str]
    ) -> float:
        """Calculate content-based preference match score"""
        score = 0.0
        
        # Cuisine match (70% of preference score)
        if cuisine_preferences and restaurant.get('cuisine_type'):
            cuisine_type = restaurant['cuisine_type'].lower()
            for pref in cuisine_preferences:
                if pref.lower() in cuisine_type or cuisine_type in pref.lower():
                    score += 0.7
                    break
        
        # Mood match (30% of preference score)
        # This would require additional restaurant metadata
        # For now, use a simplified approach
        if mood_preferences:
            score += 0.3 * 0.5  # Placeholder
        
        return min(score, 1.0)
    
    def _calculate_distance_score(self, distance: float, max_distance: float) -> float:
        """Calculate distance-based score (closer is better)"""
        if distance >= max_distance:
            return 0.0
        
        # Exponential decay: closer restaurants get higher scores
        score = np.exp(-distance / (max_distance / 3))
        return min(score, 1.0)
    
    def _apply_collaborative_boost(
        self,
        user_id: int,
        restaurants: List[Dict]
    ) -> List[Dict]:
        """
        Apply collaborative filtering boost based on similar users
        """
        # Get user's interaction history
        user_interactions = execute_query(
            "SELECT restaurant_id, interaction_type FROM user_interactions WHERE user_id = %s",
            (user_id,)
        )
        
        if not user_interactions:
            return restaurants
        
        # Find similar users (users who interacted with same restaurants)
        interacted_restaurant_ids = [i['restaurant_id'] for i in user_interactions]
        
        if not interacted_restaurant_ids:
            return restaurants
        
        placeholders = ','.join(['%s'] * len(interacted_restaurant_ids))
        similar_users_query = f"""
            SELECT DISTINCT user_id 
            FROM user_interactions 
            WHERE restaurant_id IN ({placeholders})
            AND user_id != %s
            LIMIT 50
        """
        
        similar_users = execute_query(
            similar_users_query,
            (*interacted_restaurant_ids, user_id)
        )
        
        if not similar_users:
            return restaurants
        
        # Get restaurants liked by similar users
        similar_user_ids = [u['user_id'] for u in similar_users]
        placeholders = ','.join(['%s'] * len(similar_user_ids))
        
        collaborative_query = f"""
            SELECT restaurant_id, COUNT(*) as interaction_count
            FROM user_interactions
            WHERE user_id IN ({placeholders})
            AND interaction_type IN ('favorite', 'order')
            GROUP BY restaurant_id
        """
        
        collaborative_restaurants = execute_query(
            collaborative_query,
            tuple(similar_user_ids)
        )
        
        # Create boost map
        boost_map = {
            r['restaurant_id']: min(r['interaction_count'] / 10, 0.2)
            for r in collaborative_restaurants
        }
        
        # Apply boost
        for restaurant in restaurants:
            if restaurant['id'] in boost_map:
                restaurant['recommendation_score'] += boost_map[restaurant['id']]
        
        # Re-sort
        restaurants.sort(key=lambda x: x['recommendation_score'], reverse=True)
        
        return restaurants
    
    def _generate_explanation(
        self,
        restaurant: Dict,
        preference_score: float,
        authenticity_score: float,
        distance_score: float,
        popularity_score: float,
        distance: float,
        cuisine_preferences: List[str],
        mood_preferences: List[str]
    ) -> str:
        """Generate human-readable explanation for recommendation"""
        reasons = []
        
        # Preference match
        if preference_score > 0.5 and cuisine_preferences:
            reasons.append(f"Matches your preference for {', '.join(cuisine_preferences)} cuisine")
        
        # Authenticity
        if authenticity_score > 0.7:
            reasons.append("High authenticity score with verified genuine reviews")
        
        # Distance
        if distance < 2:
            reasons.append(f"Very close to you ({distance:.1f} km)")
        elif distance < 5:
            reasons.append(f"Nearby location ({distance:.1f} km)")
        
        # Popularity
        if popularity_score > 0.7:
            reasons.append("Highly popular among users")
        
        if not reasons:
            reasons.append("Good overall match for your preferences")
        
        return " • ".join(reasons)

# Initialize global engine instance
engine = RecommendationEngine()
