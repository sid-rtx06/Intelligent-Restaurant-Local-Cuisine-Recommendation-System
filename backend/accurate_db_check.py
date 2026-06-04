from utils.database import execute_query

user_list = [
    "Paradise", "Bawarchi", "Capital", "Nawabs", "Cafe Niloufer", 
    "Mefil", "Blue Fox", "Hotel Nayab", "Chutneys", "Minerva", 
    "Antera", "Telangana Spicy Kitchen", "Platform 65", "Kritunga", "Spice 6", 
    "Shah Ghouse", "Pista House", "Shadab", "Maya Bazar", "Exotica", 
    "Hotel Kinera", "Haldiram’s", "Ohri’s", "Lucky", "Amaravathi", 
    "Taj Mahal", "Meridian", "Cafe Bahar", "Chicha’s", "Royal Seema Ruchulu", 
    "Shaji Ka Dhaba", "Peshawri", "Lé Vantage Cafe and Bar", "Haiku", "Seven Sisters", 
    "Krishnapatnam", "Pakka Local", "Gabru Di Chaop", "Mini Panjab", "The Terrakota Kitchen", 
    "Arabian Mandi", "Girlfriend Mandi", "Balaji Family Dabha", "Salt & Pepper", "Vivaha Bhojanambu", 
    "Hotel Sawagth", "Golden Dragon", "Parmpara", "7 Seasons", "The Joint Cafe Bar"
]

def check_list():
    existing = [r['name'] for r in execute_query("SELECT name FROM restaurants")]
    
    missing = []
    matches = []
    
    for name in user_list:
        found = False
        for ex in existing:
            if name.lower() in ex.lower() or ex.lower() in name.lower():
                matches.append((name, ex))
                found = True
                break
        if not found:
            missing.append(name)
            
    print(f"Total in user list: {len(user_list)}")
    print(f"Matches found: {len(matches)}")
    print(f"Missing: {len(missing)}")
    if missing:
        print("Missing details:", missing)
    
    print("\nExisting in DB (Raw):")
    for name in existing:
        print(f"- {name}")

if __name__ == "__main__":
    check_list()
