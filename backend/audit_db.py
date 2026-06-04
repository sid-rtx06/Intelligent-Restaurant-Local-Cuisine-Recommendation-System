from utils.database import execute_query
from collections import Counter
import json

def audit_db():
    results = execute_query("SELECT id, name, city FROM restaurants")
    
    names = [r['name'] for r in results]
    counts = Counter(names)
    dupes = {k: v for k, v in counts.items() if v > 1}
    
    report = {
        "total_records": len(results),
        "identical_names": dupes,
        "fuzzy_matches": []
    }
    
    unique_names = sorted(list(set(names)))
    for i in range(len(unique_names)):
        for j in range(i + 1, len(unique_names)):
            n1, n2 = unique_names[i], unique_names[j]
            # Simple fuzzy check: one is a substring of the other
            if n1.lower() in n2.lower() or n2.lower() in n1.lower():
                report["fuzzy_matches"].append((n1, n2))
                
    with open("audit_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print("Report written to audit_report.json")

if __name__ == "__main__":
    audit_db()
