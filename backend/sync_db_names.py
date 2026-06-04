import json
import os
from utils.database import execute_query, Database

def update_db_names():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, 'data', 'sample_restaurants.json')
    
    with open(json_path, 'r') as f:
        restaurants = json.load(f)
    
    # Mapping old names to new names based on what we found earlier
    # Capital Multicuisine -> Capital
    # The Nawaab -> Nawabs
    # Mehfil -> Mefil
    # Minerva Grand -> Minerva
    # Haldiram's -> Haldiram’s
    # Ohri's -> Ohri’s
    # Chicha's -> Chicha’s
    # Royalseema Ruchulu -> Royal Seema Ruchulu
    # Hotel Swagath -> Hotel Sawagth
    # Lucky Restaurant -> Lucky
    # Lé Vantage -> Lé Vantage Cafe and Bar
    # The Joint -> The Joint Cafe Bar

    mapping = {
        "Capital Multicuisine": "Capital",
        "The Nawaab": "Nawabs",
        "Mehfil": "Mefil",
        "Minerva Grand": "Minerva",
        "Haldiram's": "Haldiram’s",
        "Ohri's": "Ohri’s",
        "Chicha's": "Chicha’s",
        "Royalseema Ruchulu": "Royal Seema Ruchulu",
        "Hotel Swagath": "Hotel Sawagth",
        "Lucky Restaurant": "Lucky",
        "Lé Vantage": "Lé Vantage Cafe and Bar",
        "The Joint": "The Joint Cafe Bar"
    }

    print("Checking for name updates in DB...")
    
    # First, try to handle the specific mappings
    for old, new in mapping.items():
        try:
            # Check if old exists
            res = execute_query("SELECT id FROM restaurants WHERE name = %s", (old,))
            if res:
                id = res[0]['id']
                print(f"  Updating: '{old}' -> '{new}' (ID: {id})")
                execute_query("UPDATE restaurants SET name = %s WHERE id = %s", (new, id))
            else:
                # Check if it already has the new name
                res_new = execute_query("SELECT id FROM restaurants WHERE name = %s", (new,))
                if res_new:
                    print(f"  '{new}' already correctly named in DB.")
                else:
                    # Try fuzzy check if something is wrong
                    print(f"  Warning: Could not find '{old}' or '{new}' to update.")
        except Exception as e:
            print(f"  Error mapping {old}: {e}")

    # Now, ensure ALL 50 from the JSON are in the DB by name
    # If a name from JSON is not in DB, we should probably add it or check why
    existing_in_db = [r['name'] for r in execute_query("SELECT name FROM restaurants")]
    
    for r in restaurants:
        if r['name'] not in existing_in_db:
            print(f"  CRITICAL: '{r['name']}' is STILL MISSING from DB! Adding it...")
            # We would use Restaurant.create here, but to avoid circular imports or issues, 
            # let's just use raw SQL for this audit fix.
            sql = """INSERT INTO restaurants 
                     (name, cuisine_type, latitude, longitude, address, city, price_range, description, image_url, special_dish, best_seller, high_protein, popularity_score, authenticity_score)
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            params = (
                r['name'], r['cuisine_type'], r['latitude'], r['longitude'],
                r['address'], r['city'], r['price_range'], r.get('description'),
                r.get('image_url'), r.get('special_dish'), r.get('best_seller'),
                r.get('high_protein'), r.get('popularity_score', 0.5), r.get('authenticity_score', 0.5)
            )
            try:
                execute_query(sql, params)
                print(f"  [OK] Added {r['name']} to DB.")
            except Exception as e:
                print(f"  [X] Error adding {r['name']}: {e}")
        else:
            # Optionally update other fields to match JSON exactly
            # For now, names are the priority
            pass

    print("\nDatabase synchronization complete.")

if __name__ == "__main__":
    try:
        update_db_names()
    finally:
        Database.close_connections()
