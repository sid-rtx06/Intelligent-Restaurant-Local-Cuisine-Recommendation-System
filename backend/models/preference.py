from utils.database import execute_query
import json

class Preference:
    """User preference model"""
    
    @staticmethod
    def create_or_update(user_id, cuisine_preferences=None, mood_preferences=None,
                        budget_min=0, budget_max=10000, preferred_distance_km=10):
        """Create or update user preferences"""
        # Check if preferences exist
        existing = Preference.find_by_user(user_id)
        
        # Convert lists to JSON strings
        cuisine_json = json.dumps(cuisine_preferences) if cuisine_preferences else None
        mood_json = json.dumps(mood_preferences) if mood_preferences else None
        
        if existing:
            # Update
            query = """
                UPDATE user_preferences 
                SET cuisine_preferences = %s, mood_preferences = %s,
                    budget_min = %s, budget_max = %s, preferred_distance_km = %s
                WHERE user_id = %s
            """
            execute_query(
                query,
                (cuisine_json, mood_json, budget_min, budget_max, preferred_distance_km, user_id),
                fetch_all=False
            )
        else:
            # Create
            query = """
                INSERT INTO user_preferences 
                (user_id, cuisine_preferences, mood_preferences, budget_min, budget_max, preferred_distance_km)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            execute_query(
                query,
                (user_id, cuisine_json, mood_json, budget_min, budget_max, preferred_distance_km),
                fetch_all=False
            )
        
        return True
    
    @staticmethod
    def find_by_user(user_id):
        """Find preferences by user ID"""
        query = "SELECT * FROM user_preferences WHERE user_id = %s"
        result = execute_query(query, (user_id,), fetch_one=True)
        
        if result:
            # Parse JSON fields
            if result.get('cuisine_preferences'):
                result['cuisine_preferences'] = json.loads(result['cuisine_preferences'])
            if result.get('mood_preferences'):
                result['mood_preferences'] = json.loads(result['mood_preferences'])
        
        return result
    
    @staticmethod
    def delete(user_id):
        """Delete user preferences"""
        query = "DELETE FROM user_preferences WHERE user_id = %s"
        execute_query(query, (user_id,), fetch_all=False)
        return True
