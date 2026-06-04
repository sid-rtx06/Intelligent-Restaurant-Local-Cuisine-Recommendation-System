from utils.database import execute_query
from typing import List, Dict, Optional

class Restaurant:
    """Restaurant model for managing restaurant data"""
    
    @staticmethod
    def create(name, cuisine_type, latitude, longitude, address, city, 
               price_range='$$', description=None, image_url=None,
               special_dish=None, best_seller=None, high_protein=None):
        """Create a new restaurant"""
        query = """
            INSERT INTO restaurants 
            (name, cuisine_type, latitude, longitude, address, city, price_range, description, image_url, special_dish, best_seller, high_protein)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        restaurant_id = execute_query(
            query, 
            (name, cuisine_type, latitude, longitude, address, city, price_range, description, image_url, special_dish, best_seller, high_protein),
            fetch_all=False
        )
        return restaurant_id
    
    @staticmethod
    def find_by_id(restaurant_id):
        """Find restaurant by ID"""
        query = "SELECT * FROM restaurants WHERE id = %s"
        return execute_query(query, (restaurant_id,), fetch_one=True)
    
    @staticmethod
    def find_all(limit=100, offset=0):
        """Get all restaurants with pagination"""
        # Get more to allow for name-based deduplication
        query = "SELECT * FROM restaurants"
        results = execute_query(query)
        from utils.helpers import deduplicate_by_name
        return deduplicate_by_name(results)[offset:offset+limit]
    
    @staticmethod
    def find_by_cuisine(cuisine_type, limit=50):
        """Find restaurants by cuisine type"""
        query = "SELECT * FROM restaurants WHERE cuisine_type LIKE %s"
        results = execute_query(query, (f"%{cuisine_type}%",))
        from utils.helpers import deduplicate_by_name
        return deduplicate_by_name(results)[:limit]
    
    @staticmethod
    def find_by_city(city, limit=50):
        """Find restaurants by city"""
        query = "SELECT * FROM restaurants WHERE city = %s"
        results = execute_query(query, (city,))
        from utils.helpers import deduplicate_by_name
        return deduplicate_by_name(results)[:limit]
    
    @staticmethod
    def update_scores(restaurant_id, authenticity_score=None, popularity_score=None):
        """Update restaurant authenticity and popularity scores"""
        updates = []
        params = []
        
        if authenticity_score is not None:
            updates.append("authenticity_score = %s")
            params.append(authenticity_score)
        if popularity_score is not None:
            updates.append("popularity_score = %s")
            params.append(popularity_score)
        
        if not updates:
            return False
        
        params.append(restaurant_id)
        query = f"UPDATE restaurants SET {', '.join(updates)} WHERE id = %s"
        execute_query(query, tuple(params), fetch_all=False)
        return True
    
    @staticmethod
    def search(query_text, limit=20):
        """Search restaurants by name or cuisine"""
        query = """
            SELECT * FROM restaurants 
            WHERE name LIKE %s OR cuisine_type LIKE %s OR description LIKE %s
        """
        search_term = f"%{query_text}%"
        results = execute_query(query, (search_term, search_term, search_term))
        from utils.helpers import deduplicate_by_name
        return deduplicate_by_name(results)[:limit]
    
    @staticmethod
    def get_popular_restaurants(limit=10):
        """Get most popular restaurants"""
        query = """
            SELECT * FROM restaurants 
            ORDER BY popularity_score DESC, authenticity_score DESC
        """
        results = execute_query(query)
        from utils.helpers import deduplicate_by_name
        return deduplicate_by_name(results)[:limit]
