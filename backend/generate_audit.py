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
    
    with open('audit_report.txt', 'w', encoding='utf-8') as f:
        f.write(f"Total in user list: {len(user_list)}\n")
        f.write(f"Total in DB: {len(existing)}\n\n")
        
        missing = []
        for name in user_list:
            found = False
            for ex in existing:
                if name.lower() == ex.lower():
                    found = True
                    break
                # Fuzzy check
                if name.lower() in ex.lower() or ex.lower() in name.lower():
                    found = True
                    break
            if not found:
                missing.append(name)
        
        f.write(f"Missing (not even fuzzy match): {len(missing)}\n")
        for m in missing:
            f.write(f"MISSING: {m}\n")
            
        f.write("\n--- Full Mapping Attempt ---\n")
        for name in user_list:
            best_match = None
            for ex in existing:
                if name.lower() == ex.lower():
                    best_match = ex
                    break
                if name.lower() in ex.lower() or ex.lower() in name.lower():
                    best_match = ex
            
            f.write(f"{name} -> {best_match if best_match else '!!! NOT FOUND !!!'}\n")

if __name__ == "__main__":
    check_list()
