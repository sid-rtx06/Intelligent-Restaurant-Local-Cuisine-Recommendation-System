import json
import random

def generate_data():
    restaurants = [
        {
            "name": "Paradise",
            "cuisine_type": "Hyderabadi",
            "latitude": 17.4447, "longitude": 78.4983,
            "address": "Secunderabad", "city": "Hyderabad",
            "price_range": "$$",
            "description": "World-famous Hyderabadi Dum Biryani and authentic kebabs.",
            "image_url": "https://images.unsplash.com/photo-1589302168068-964664d93dc9?w=800",
            "special_dish": "Hyderabadi Dum Biryani",
            "best_seller": "Chicken Dum Biryani",
            "high_protein": "Mutton Biryani / mutton kebabs",
            "popularity_score": 0.98, "authenticity_score": 0.99
        },
        {
            "name": "Bawarchi",
            "cuisine_type": "Hyderabadi",
            "latitude": 17.4042, "longitude": 78.4897,
            "address": "RTC X Roads", "city": "Hyderabad",
            "price_range": "$$",
            "description": "Legendary Biryani destination known for its authentic spice blends.",
            "image_url": "https://images.unsplash.com/photo-1563379091339-014f772ba6d9?w=800",
            "special_dish": "Bawarchi-style Hyderabadi Biryani",
            "best_seller": "Chicken / Mutton Biryani",
            "high_protein": "Mutton biryani / kebabs",
            "popularity_score": 0.95, "authenticity_score": 0.97
        },
        {
            "name": "Capital",
            "cuisine_type": "Mughlai",
            "latitude": 17.3850, "longitude": 78.4867,
            "address": "Hyderabad Neighborhoods", "city": "Hyderabad",
            "price_range": "$$",
            "description": "Famous for Zafrani Biryani and grilled delicacies.",
            "image_url": "https://images.unsplash.com/photo-1514326640560-7d063ef2aed5?w=800",
            "special_dish": "Zafrani / Dum Biryani and grills",
            "best_seller": "Mutton biryani / mandi / kebab platters",
            "high_protein": "Mutton grills / mandi",
            "popularity_score": 0.88, "authenticity_score": 0.90
        },
        {
            "name": "Nawabs",
            "cuisine_type": "Mughlai",
            "latitude": 17.4483, "longitude": 78.3915,
            "address": "Madhapur", "city": "Hyderabad",
            "price_range": "$$$",
            "description": "Royal dining experience with signature kebab platters.",
            "image_url": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=800",
            "special_dish": "Nawaabi Biryani / kebab platters",
            "best_seller": "Biryani and kebabs",
            "high_protein": "Kebab platters / mutton dishes",
            "popularity_score": 0.85, "authenticity_score": 0.88
        },
        {
            "name": "Cafe Niloufer",
            "cuisine_type": "Irani",
            "latitude": 17.4000, "longitude": 78.4600,
            "address": "Red Hills/Lakdikapul", "city": "Hyderabad",
            "price_range": "$",
            "description": "Iconic cafe known for Irani Chai and Osmania Biscuits.",
            "image_url": "https://images.unsplash.com/photo-1544787210-213961136f1c?w=800",
            "special_dish": "Keema Osmania (keema bun / kheema dishes)",
            "best_seller": "Keema bun / Osmania biscuits & tea combo",
            "high_protein": "Keema dishes / kebabs",
            "popularity_score": 0.99, "authenticity_score": 0.95
        },
        {
            "name": "Mefil",
            "cuisine_type": "North Indian",
            "latitude": 17.3900, "longitude": 78.4900,
            "address": "Narayanguda", "city": "Hyderabad",
            "price_range": "$$",
            "description": "Popular for Mughlai kebabs and biryani combos.",
            "image_url": "https://images.unsplash.com/photo-1628294895950-9805252327bc?w=800",
            "special_dish": "Mughlai kebabs / biryani",
            "best_seller": "Kebabs and biryani combos",
            "high_protein": "Mutton or chicken kebab platters",
            "popularity_score": 0.89, "authenticity_score": 0.85
        },
        {
            "name": "Blue Fox",
            "cuisine_type": "Multi-cuisine",
            "latitude": 17.4200, "longitude": 78.4500,
            "address": "Himayatnagar", "city": "Hyderabad",
            "price_range": "$$$",
            "description": "Upscale lounge offering North Indian grills and sizzlers.",
            "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800",
            "special_dish": "North Indian grills / sizzlers",
            "best_seller": "Tandoori/grilled mains and combo platters",
            "high_protein": "Tandoori/Grilled chicken or fish",
            "popularity_score": 0.82, "authenticity_score": 0.80
        },
        {
            "name": "Hotel Nayab",
            "cuisine_type": "Hyderabadi",
            "latitude": 17.3600, "longitude": 78.4700,
            "address": "Old City", "city": "Hyderabad",
            "price_range": "$$",
            "description": "Traditionally famous for Mutton Biryani and authentic flavors.",
            "image_url": "https://images.unsplash.com/photo-1589302168068-964664d93dc9?w=800",
            "special_dish": "Mutton Biryani",
            "best_seller": "Mutton biryani and curries",
            "high_protein": "Mutton biryani / mutton curry",
            "popularity_score": 0.91, "authenticity_score": 0.94
        },
        {
            "name": "Chutneys",
            "cuisine_type": "South Indian",
            "latitude": 17.4204, "longitude": 78.4529,
            "address": "Banjara Hills", "city": "Hyderabad",
            "price_range": "$$",
            "description": "Legendary for its variety of chutneys and South Indian breakfast.",
            "image_url": "https://images.unsplash.com/photo-1589301760014-d92b43979185?w=800",
            "special_dish": "Signature chutneys and breakfast combos",
            "best_seller": "Masala dosa, idli-sambar combos, South Indian thali",
            "high_protein": "Sambar (dal/lentil) in thali; paneer/dosa",
            "popularity_score": 0.96, "authenticity_score": 0.97
        },
        {
            "name": "Minerva",
            "cuisine_type": "Andhra",
            "latitude": 17.4300, "longitude": 78.4800,
            "address": "Himayatnagar", "city": "Hyderabad",
            "price_range": "$$$",
            "description": "Famous for Andhra and Hyderabadi non-veg biryani and tandoori mains.",
            "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800",
            "special_dish": "Andhra / Hyderabadi non-veg biryani",
            "best_seller": "Mutton biryani / tandoori items",
            "high_protein": "Mutton dishes / meat platters",
            "popularity_score": 0.86, "authenticity_score": 0.88
        },
        {
            "name": "Antera",
            "cuisine_type": "Telugu",
            "latitude": 17.4500, "longitude": 78.4000,
            "address": "Jubilee Hills", "city": "Hyderabad",
            "price_range": "$$$",
            "description": "Upscale regional restaurant focusing on authentic Telugu flavors.",
            "image_url": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800",
            "special_dish": "Kebab platters / Mughlai rich mains",
            "best_seller": "Kebabs & biryani",
            "high_protein": "Meat platter / kebabs",
            "popularity_score": 0.84, "authenticity_score": 0.86
        },
        {
            "name": "Telangana Spicy Kitchen",
            "cuisine_type": "Telangana",
            "latitude": 17.4100, "longitude": 78.4400,
            "address": "Jubilee Hills", "city": "Hyderabad",
            "price_range": "$$$",
            "description": "Authentic regional Telangana mutton and chicken curries.",
            "image_url": "https://images.unsplash.com/photo-1626777552726-4a6b54c97eb4?w=800",
            "special_dish": "Spicy regional Telangana mutton/chicken curries",
            "best_seller": "Mutton curry with rice/rotis",
            "high_protein": "Mutton curry",
            "popularity_score": 0.87, "authenticity_score": 0.92
        },
        {
            "name": "Platform 65",
            "cuisine_type": "Multi-cuisine",
            "latitude": 17.4400, "longitude": 78.3800,
            "address": "Kukatpally", "city": "Hyderabad",
            "price_range": "$$",
            "description": "Train-themed restaurant serving Continental mains and steaks.",
            "image_url": "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800",
            "special_dish": "Continental mains / steaks / grills",
            "best_seller": "Burgers, grilled mains",
            "high_protein": "Steak / grilled chicken / fish",
            "popularity_score": 0.90, "authenticity_score": 0.82
        },
        {
            "name": "Kritunga",
            "cuisine_type": "Rayalaseema",
            "latitude": 17.4300, "longitude": 78.3900,
            "address": "Somajiguda", "city": "Hyderabad",
            "price_range": "$$",
            "description": "Renowned for spicy Rayalaseema cuisine and Mutton Pulao.",
            "image_url": "https://images.unsplash.com/photo-1627308595229-7830a5c91f9f?w=800",
            "special_dish": "Rayalaseema-style Biryani / Mutton Pulao",
            "best_seller": "Mutton curry / biryani / Andhra thali",
            "high_protein": "Mutton curries / grilled prawns",
            "popularity_score": 0.92, "authenticity_score": 0.96
        },
        {
            "name": "Spice 6",
            "cuisine_type": "North Indian",
            "latitude": 17.4200, "longitude": 78.4100,
            "address": "Banjara Hills", "city": "Hyderabad",
            "price_range": "$$$",
            "description": "Multi-cuisine restaurant known for North Indian and Indo-Chinese drills.",
            "image_url": "https://images.unsplash.com/photo-1544124499-17367cd20a5e?w=800",
            "special_dish": "North Indian / Indo-Chinese grilled mains",
            "best_seller": "Tandoori combos / biryani",
            "high_protein": "Tandoori chicken / kebab platters",
            "popularity_score": 0.80, "authenticity_score": 0.83
        },
        {
            "name": "Shah Ghouse",
            "cuisine_type": "Hyderabadi",
            "latitude": 17.3900, "longitude": 78.4300,
            "address": "Gachibowli", "city": "Hyderabad",
            "price_range": "$$",
            "description": "Local favorite for authentic Hyderabadi Dum Biryani and Haleem.",
            "image_url": "https://images.unsplash.com/photo-1563379091339-014f772ba6d9?w=800",
            "special_dish": "Hyderabadi Biryani (Shah Ghouse Dum Biryani)",
            "best_seller": "Mutton and chicken biryani",
            "high_protein": "Mutton biryani / kebabs",
            "popularity_score": 0.94, "authenticity_score": 0.96
        },
        {
            "name": "Pista House",
            "cuisine_type": "Hyderabadi",
            "latitude": 17.3600, "longitude": 78.4700,
            "address": "Old City", "city": "Hyderabad",
            "price_range": "$$",
            "description": "Global brand famous for its Haleem and traditional Hyderabadi sweets.",
            "image_url": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800",
            "special_dish": "Haleem (seasonal), Hyderabadi sweets",
            "best_seller": "Haleem (during Ramadan), sweets, kebabs",
            "high_protein": "Haleem (meat + lentils); kebabs",
            "popularity_score": 0.98, "authenticity_score": 0.98
        },
        {
            "name": "Shadab",
            "cuisine_type": "Hyderabadi",
            "latitude": 17.3600, "longitude": 78.4740,
            "address": "Charminar", "city": "Hyderabad",
            "price_range": "$$",
            "description": "Iconic eatery near Charminar famous for its Mutton Biryani and paya.",
            "image_url": "https://images.unsplash.com/photo-1563379091339-014f772ba6d9?w=800",
            "special_dish": "Mutton Biryani / Pathar ka gosht",
            "best_seller": "Mutton biryani and haleem",
            "high_protein": "Pathar ka gosht / mutton biryani",
            "popularity_score": 0.96, "authenticity_score": 0.98
        },
        {
            "name": "Maya Bazar",
            "cuisine_type": "Telugu",
            "latitude": 17.4300, "longitude": 78.4500,
            "address": "Hyderabad", "city": "Hyderabad",
            "price_range": "$$",
            "description": "Traditional dining with a focus on local Telugu delicacies and sweets.",
            "image_url": "https://images.unsplash.com/photo-1606787366850-de6330128bfc?w=800",
            "special_dish": "Traditional Hyderabadi dishes and sweets",
            "best_seller": "Biryani / traditional mains",
            "high_protein": "Mutton dishes / kebabs",
            "popularity_score": 0.85, "authenticity_score": 0.87
        },
        {
            "name": "Exotica",
            "cuisine_type": "Multi-cuisine",
            "latitude": 17.4100, "longitude": 78.4400,
            "address": "Banjara Hills", "city": "Hyderabad",
            "price_range": "$$$",
            "description": "Rooftop dining with a wide range of Continental and North Indian options.",
            "image_url": "https://images.unsplash.com/photo-1549488344-1f9b8d2bd1f3?w=800",
            "special_dish": "Multi-cuisine mains",
            "best_seller": "Continental / Chinese / North Indian mains",
            "high_protein": "Grilled fish/steak or tandoori chicken",
            "popularity_score": 0.88, "authenticity_score": 0.84
        },
        {
            "name": "Hotel Kinera",
            "cuisine_type": "Andhra",
            "latitude": 17.3800, "longitude": 78.4800,
            "address": "Hyderabad", "city": "Hyderabad",
            "price_range": "$$",
            "description": "Local favorite for homestyle non-veg curries and biryani.",
            "image_url": "https://images.unsplash.com/photo-1610057099443-fde8c4d50f91?w=800",
            "special_dish": "Mutton/chicken biryani and curries",
            "best_seller": "Biryani",
            "high_protein": "Mutton biryani",
            "popularity_score": 0.81, "authenticity_score": 0.85
        },
        {
            "name": "Haldiram’s",
            "cuisine_type": "Vegetarian",
            "latitude": 17.4200, "longitude": 78.4800,
            "address": "Malls across Hyderabad", "city": "Hyderabad",
            "price_range": "$$",
            "description": "Nationwide chain famous for its Indian sweets, chaat, and vegetarian thalis.",
            "image_url": "https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=800",
            "special_dish": "Sweets/chaat and thali items",
            "best_seller": "Samosa, chaat, sweets, thali",
            "high_protein": "Paneer dishes (paneer tikka), dal in thali",
            "popularity_score": 0.93, "authenticity_score": 0.90
        },
        {
            "name": "Ohri’s",
            "cuisine_type": "Multi-cuisine",
            "latitude": 17.4000, "longitude": 78.4800,
            "address": "Various locations", "city": "Hyderabad",
            "price_range": "$$$",
            "description": "Premium multi-concept dining destinations across the city.",
            "image_url": "https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=800",
            "special_dish": "Themed mains / continental fusion",
            "best_seller": "Buffet / themed mains; kebabs",
            "high_protein": "Meat platters / grilled fish or chicken mains",
            "popularity_score": 0.89, "authenticity_score": 0.87
        },
        {
            "name": "Lucky",
            "cuisine_type": "Hyderabadi",
            "latitude": 17.3700, "longitude": 78.4800,
            "address": "Old City", "city": "Hyderabad",
            "price_range": "$$",
            "description": "Known for its robust non-veg offerings and local biryani.",
            "image_url": "https://images.unsplash.com/photo-1594212699903-ec8a3ecc50f1?w=800",
            "special_dish": "Biryani / grills",
            "best_seller": "Biryani and kebabs",
            "high_protein": "Mutton dishes / kebabs",
            "popularity_score": 0.82, "authenticity_score": 0.85
        },
        {
            "name": "Amaravathi",
            "cuisine_type": "Andhra",
            "latitude": 17.4200, "longitude": 78.4700,
            "address": "Ameerpet", "city": "Hyderabad",
            "price_range": "$$",
            "description": "Authentic spicy Andhra meals and regional specialties.",
            "image_url": "https://images.unsplash.com/photo-1589301760014-d92b43979185?w=800",
            "special_dish": "Andhra specialities (spicy curries, rice dishes)",
            "best_seller": "Andhra thali / spicy mutton/chicken curries",
            "high_protein": "Mutton curry / fish items",
            "popularity_score": 0.84, "authenticity_score": 0.89
        },
        {
            "name": "Taj Mahal",
            "cuisine_type": "Mughlai",
            "latitude": 17.3800, "longitude": 78.4700,
            "address": "Abids", "city": "Hyderabad",
            "price_range": "$$",
            "description": "Classic Mughlai restaurant famous for its heritage biryani.",
            "image_url": "https://images.unsplash.com/photo-1514326640560-7d063ef2aed5?w=800",
            "special_dish": "Mughlai biryani / kebabs",
            "best_seller": "Biryani / kebab platters",
            "high_protein": "Mutton kebabs / biryani",
            "popularity_score": 0.87, "authenticity_score": 0.90
        },
        {
            "name": "Meridian",
            "cuisine_type": "Multi-cuisine",
            "latitude": 17.4100, "longitude": 78.4500,
            "address": "Panjagutta", "city": "Hyderabad",
            "price_range": "$$$",
            "description": "Modern multi-cuisine restaurant with a focus on steaks and grills.",
            "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=800",
            "special_dish": "Continental / multi-cuisine mains",
            "best_seller": "Buffet / mains; steaks/grills",
            "high_protein": "Steak / tandoori chicken / fish",
            "popularity_score": 0.85, "authenticity_score": 0.83
        },
        {
            "name": "Cafe Bahar",
            "cuisine_type": "Hyderabadi",
            "latitude": 17.3900, "longitude": 78.4700,
            "address": "Hyderguda", "city": "Hyderabad",
            "price_range": "$$",
            "description": "Legendary institution famous for its Biryani and local vibes.",
            "image_url": "https://images.unsplash.com/photo-1589302168068-964664d93dc9?w=800",
            "special_dish": "Hyderabadi Biryani (Cafe Bahar Biryani)",
            "best_seller": "Chicken/Mutton Biryani",
            "high_protein": "Mutton biryani / kebabs",
            "popularity_score": 0.95, "authenticity_score": 0.99
        },
        {
            "name": "Chicha’s",
            "cuisine_type": "Fusion",
            "latitude": 17.4300, "longitude": 78.4400,
            "address": "Banjara Hills", "city": "Hyderabad",
            "price_range": "$$",
            "description": "Modern cafe offering street-food inspired fusion and burgers.",
            "image_url": "https://images.unsplash.com/photo-1594212699903-ec8a3ecc50f1?w=800",
            "special_dish": "Street food-inspired mains and continental fusion",
            "best_seller": "Burgers, wraps, kebabs",
            "high_protein": "Grilled chicken/steak burger or kebab wraps",
            "popularity_score": 0.91, "authenticity_score": 0.88
        },
        {
            "name": "Royal Seema Ruchulu",
            "cuisine_type": "Rayalaseema",
            "latitude": 17.4200, "longitude": 78.4300,
            "address": "Jubilee Hills", "city": "Hyderabad",
            "price_range": "$$$",
            "description": "The destination for spicy Rayalaseema meals and gongura dishes.",
            "image_url": "https://images.unsplash.com/photo-1627308595229-7830a5c91f9f?w=800",
            "special_dish": "Rayalaseema-style meals - spicy mutton",
            "best_seller": "Andhra thali, mutton pepper fry",
            "high_protein": "Mutton pepper fry / meat curries",
            "popularity_score": 0.89, "authenticity_score": 0.95
        },
        {
            "name": "Shaji Ka Dhaba",
            "cuisine_type": "North Indian",
            "latitude": 17.4000, "longitude": 78.4500,
            "address": "Hyderabad", "city": "Hyderabad",
            "price_range": "$$",
            "description": "Rustic North Indian dhaba experience with rich gravies.",
            "image_url": "https://images.unsplash.com/photo-1544124499-17367cd20a5e?w=800",
            "special_dish": "North Indian dhaba mains - kebabs",
            "best_seller": "Butter chicken, kebabs, rotis",
            "high_protein": "Tandoori kebabs / chicken dishes",
            "popularity_score": 0.80, "authenticity_score": 0.84
        },
        {
            "name": "Peshawri",
            "cuisine_type": "Mughlai",
            "latitude": 17.4300, "longitude": 78.4500,
            "address": "ITC Kohenur", "city": "Hyderabad",
            "price_range": "$$$$",
            "description": "Award-winning fine dining serving Dal Bukhara and NW Frontier grills.",
            "image_url": "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=800",
            "special_dish": "North-West Frontier / Peshawari kebabs",
            "best_seller": "Dal Bukhara, tandoori meats, kebabs",
            "high_protein": "Tandoori meats / kebab platters",
            "popularity_score": 0.97, "authenticity_score": 0.99
        },
        {
            "name": "Lé Vantage Cafe and Bar",
            "cuisine_type": "Continental",
            "latitude": 17.4200, "longitude": 78.4100,
            "address": "Jubilee Hills", "city": "Hyderabad",
            "price_range": "$$$",
            "description": "Upscale cafe and bar with premium steaks and fusion starters.",
            "image_url": "https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=800",
            "special_dish": "Continental mains, cocktails, fusion starters",
            "best_seller": "Burgers, steaks, bar grills",
            "high_protein": "Steak / grilled chicken",
            "popularity_score": 0.87, "authenticity_score": 0.86
        },
        {
            "name": "Haiku",
            "cuisine_type": "Japanese",
            "latitude": 17.4200, "longitude": 78.4300,
            "address": "Jubilee Hills", "city": "Hyderabad",
            "price_range": "$$$$",
            "description": "Premium Japanese and Asian dining offering exquisite sushi.",
            "image_url": "https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=800",
            "special_dish": "Sushi/sashimi style rolls",
            "best_seller": "Sushi rolls, ramen, teriyaki mains",
            "high_protein": "Sashimi / grilled fish / teriyaki chicken",
            "popularity_score": 0.90, "authenticity_score": 0.97
        },
        {
            "name": "Seven Sisters",
            "cuisine_type": "North Eastern",
            "latitude": 17.4400, "longitude": 78.3800,
            "address": "Banjara Hills", "city": "Hyderabad",
            "price_range": "$$$",
            "description": "Unique experience with a focus on North-Eastern flavors.",
            "image_url": "https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800",
            "special_dish": "Multi-cuisine mains; North Eastern specialties",
            "best_seller": "Local specialties / biryanis / grills",
            "high_protein": "Meat mains / grilled fish",
            "popularity_score": 0.84, "authenticity_score": 0.91
        },
        {
            "name": "Krishnapatnam",
            "cuisine_type": "Coastal",
            "latitude": 17.4500, "longitude": 78.4000,
            "address": "Jubilee Hills", "city": "Hyderabad",
            "price_range": "$$$",
            "description": "Vibrant coastal restaurant famous for its seafood and prawn curries.",
            "image_url": "https://images.unsplash.com/photo-1514326640560-7d063ef2aed5?w=800",
            "special_dish": "Seafood specialties (lobster, prawns, fish)",
            "best_seller": "Prawn fry, fish curry",
            "high_protein": "Grilled fish / prawns",
            "popularity_score": 0.88, "authenticity_score": 0.93
        },
        {
            "name": "Pakka Local",
            "cuisine_type": "Telugu",
            "latitude": 17.4200, "longitude": 78.3900,
            "address": "Madhapur", "city": "Hyderabad",
            "price_range": "$$",
            "description": "Celebration of regional Telugu flavors in a modern setting.",
            "image_url": "https://images.unsplash.com/photo-1626777552726-4a6b54c97eb4?w=800",
            "special_dish": "Regional Andhra/Telangana local specialties",
            "best_seller": "Thali / biryani / local curries",
            "high_protein": "Meat curries / fish plates",
            "popularity_score": 0.86, "authenticity_score": 0.90
        },
        {
            "name": "Gabru Di Chaop",
            "cuisine_type": "Punjabi",
            "latitude": 17.4400, "longitude": 78.3700,
            "address": "Gachibowli", "city": "Hyderabad",
            "price_range": "$",
            "description": "Trendy North Indian concept focusing on chaap and street food.",
            "image_url": "https://images.unsplash.com/photo-1544124499-17367cd20a5e?w=800",
            "special_dish": "Chole bhature / Punjabi chaap",
            "best_seller": "Chaap dishes, tandoori platters",
            "high_protein": "Chaap (soya/meat) or tandoori kebabs",
            "popularity_score": 0.83, "authenticity_score": 0.81
        },
        {
            "name": "Mini Panjab",
            "cuisine_type": "Punjabi",
            "latitude": 17.4300, "longitude": 78.3900,
            "address": "Kondapur", "city": "Hyderabad",
            "price_range": "$$",
            "description": "Traditional Punjabi kitchen known for butter chicken and kebabs.",
            "image_url": "https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=800",
            "special_dish": "Punjabi curries, butter chicken",
            "best_seller": "Butter chicken / tandoori kebabs",
            "high_protein": "Tandoori kebabs / butter chicken",
            "popularity_score": 0.81, "authenticity_score": 0.86
        },
        {
            "name": "The Terrakota Kitchen",
            "cuisine_type": "Fusion",
            "latitude": 17.4500, "longitude": 78.3700,
            "address": "Financial District", "city": "Hyderabad",
            "price_range": "$$$",
            "description": "Unique boutique restaurant specializing in clay-pot slow cooking.",
            "image_url": "https://images.unsplash.com/photo-1606787366850-de6330128bfc?w=800",
            "special_dish": "Clay-pot (terracotta) slow cooked mains",
            "best_seller": "Clay pot mains, biryani",
            "high_protein": "Clay pot mutton/chicken mains",
            "popularity_score": 0.89, "authenticity_score": 0.92
        },
        {
            "name": "Arabian Mandi",
            "cuisine_type": "Arabic",
            "latitude": 17.3800, "longitude": 78.4300,
            "address": "Tolichowki", "city": "Hyderabad",
            "price_range": "$$",
            "description": "Authentic Arabic dining experience focusing on slow-cooked Mandi.",
            "image_url": "https://images.unsplash.com/photo-1594212699903-ec8a3ecc50f1?w=800",
            "special_dish": "Mandi (slow-cooked spiced rice with lamb)",
            "best_seller": "Lamb Mandi / chicken mandi",
            "high_protein": "Lamb mandi (lamb meat)",
            "popularity_score": 0.91, "authenticity_score": 0.94
        },
        {
            "name": "Girlfriend Mandi",
            "cuisine_type": "Arabic",
            "latitude": 17.4300, "longitude": 78.4100,
            "address": "Jubilee Hills", "city": "Hyderabad",
            "price_range": "$$",
            "description": "Quirky and modern Mandi concept with a trendy atmosphere.",
            "image_url": "https://images.unsplash.com/photo-1563379091339-014f772ba6d9?w=800",
            "special_dish": "Mandi rice with slow-cooked meats",
            "best_seller": "Chicken / Lamb mandi",
            "high_protein": "Lamb mandi",
            "popularity_score": 0.86, "authenticity_score": 0.82
        },
        {
            "name": "Balaji Family Dabha",
            "cuisine_type": "North Indian",
            "latitude": 17.4100, "longitude": 78.5000,
            "address": "Hyderabad Outskirts", "city": "Hyderabad",
            "price_range": "$",
            "description": "Homestyle North Indian meals and dhaba classics.",
            "image_url": "https://images.unsplash.com/photo-1628294895950-9805252327bc?w=800",
            "special_dish": "Homestyle North Indian dhabha mains",
            "best_seller": "Dal, butter chicken, kebabs",
            "high_protein": "Tandoori kebabs / meat curries",
            "popularity_score": 0.79, "authenticity_score": 0.88
        },
        {
            "name": "Salt & Pepper",
            "cuisine_type": "Seafood",
            "latitude": 17.4400, "longitude": 78.3600,
            "address": "Hitech City", "city": "Hyderabad",
            "price_range": "$$$",
            "description": "Modern multi-cuisine restaurant focusing on seafood and grills.",
            "image_url": "https://images.unsplash.com/photo-1544025162-d76694265947?w=800",
            "special_dish": "Seafood plates and grills",
            "best_seller": "Grilled fish, prawn starters",
            "high_protein": "Grilled fish / prawns",
            "popularity_score": 0.85, "authenticity_score": 0.84
        },
        {
            "name": "Vivaha Bhojanambu",
            "cuisine_type": "Telugu",
            "latitude": 17.4300, "longitude": 78.4300,
            "address": "Jubilee Hills", "city": "Hyderabad",
            "price_range": "$$$",
            "description": "Celebrated for traditional Andhra wedding-style thalis.",
            "image_url": "https://images.unsplash.com/photo-1589301988918-2410a4a9196b?w=800",
            "special_dish": "Traditional Telugu wedding thali",
            "best_seller": "Full traditional thali",
            "high_protein": "Meat curries / chicken/mutton items",
            "popularity_score": 0.92, "authenticity_score": 0.98
        },
        {
            "name": "Hotel Sawagth",
            "cuisine_type": "South Indian",
            "latitude": 17.4000, "longitude": 78.4800,
            "address": "Hyderabad", "city": "Hyderabad",
            "price_range": "$$",
            "description": "Local favorite for traditional non-veg curries and meals.",
            "image_url": "https://images.unsplash.com/photo-1610057099443-fde8c4d50f91?w=800",
            "special_dish": "Local biryani / non-veg mains",
            "best_seller": "Biryani / kebabs",
            "high_protein": "Mutton dishes",
            "popularity_score": 0.81, "authenticity_score": 0.85
        },
        {
            "name": "Golden Dragon",
            "cuisine_type": "Chinese",
            "latitude": 17.4100, "longitude": 78.4400,
            "address": "Banjara Hills", "city": "Hyderabad",
            "price_range": "$$$$",
            "description": "Premium fine-dining Chinese experience with signature flavors.",
            "image_url": "https://images.unsplash.com/photo-1526318896980-cf78c088247c?w=800",
            "special_dish": "Chinese mains (schezwan, manchurian)",
            "best_seller": "Manchurian, Hakka noodles, fried rice",
            "high_protein": "Chicken Manchurian / stir-fried prawns",
            "popularity_score": 0.90, "authenticity_score": 0.92
        },
        {
            "name": "Parmpara",
            "cuisine_type": "Rajasthani",
            "latitude": 17.4100, "longitude": 78.4500,
            "address": "Panjagutta", "city": "Hyderabad",
            "price_range": "$$$",
            "description": "Traditional North Indian and Rajasthani kitchen.",
            "image_url": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800",
            "special_dish": "Traditional North Indian / Rajasthani mains",
            "best_seller": "Thalis and non-veg mains",
            "high_protein": "Meat curries / paneer tikka",
            "popularity_score": 0.84, "authenticity_score": 0.88
        },
        {
            "name": "7 Seasons",
            "cuisine_type": "Multi-cuisine",
            "latitude": 17.4400, "longitude": 78.4700,
            "address": "Secunderabad", "city": "Hyderabad",
            "price_range": "$$",
            "description": "Vibrant multi-cuisine restaurant known for its expansive buffets.",
            "image_url": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800",
            "special_dish": "Multi-cuisine mains / buffet",
            "best_seller": "Buffet/continental mains; grilled meats",
            "high_protein": "Grilled fish / steak / kebabs",
            "popularity_score": 0.82, "authenticity_score": 0.84
        },
        {
            "name": "The Joint Cafe Bar",
            "cuisine_type": "Continental",
            "latitude": 17.4300, "longitude": 78.4100,
            "address": "Jubilee Hills", "city": "Hyderabad",
            "price_range": "$$$",
            "description": "Trendy cafe-bar known for bar grills and tapas.",
            "image_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800",
            "special_dish": "Bar grills, tapas, continental mains",
            "best_seller": "Burgers, cocktails, platters",
            "high_protein": "Steak / grilled chicken/fish platters",
            "popularity_score": 0.86, "authenticity_score": 0.81
        }
    ]

    # Add numeric IDs and Review Stats
    for i, r in enumerate(restaurants):
        r['id'] = i + 1
        r['review_stats'] = {
            "avg_rating": round(random.uniform(3.8, 4.9), 1),
            "total_reviews": random.randint(50, 5000)
        }
        # Add rich menus
        r['menu'] = [
            {"name": f"Signature {r['cuisine_type']} Dish", "price": random.randint(250, 800), "image": "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=400", "is_high_protein": True},
            {"name": r.get('best_seller', 'Popular Choice'), "price": random.randint(200, 600), "image": "https://images.unsplash.com/photo-1563379091339-014f772ba6d9?w=400", "is_high_protein": True},
            {"name": "Traditional Dessert", "price": random.randint(100, 300), "image": "https://images.unsplash.com/photo-1589113702131-0d33e7f6f743?w=400"},
            {"name": "Chef's Special Salad", "price": random.randint(150, 400), "image": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=400", "is_high_protein": False},
            {"name": "Local Favorite Drink", "price": random.randint(80, 200), "image": "https://images.unsplash.com/photo-1544787210-213961136f1c?w=400"}
        ]

    import os
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    restaurants_path = os.path.join(base_dir, 'data', 'sample_restaurants.json')
    js_path = os.path.join(base_dir, '..', 'frontend', 'js', 'sample_data.js')
    reviews_path = os.path.join(base_dir, 'data', 'sample_reviews.json')

    with open(restaurants_path, 'w') as f:
        json.dump(restaurants, f, indent=4)
    
    # Also update the JS file for offline mode
    js_content = f"// Automatically generated from backend/data/sample_restaurants.json\nconst RESTAURANTS_DATA = {json.dumps(restaurants, indent=4)};"
    with open(js_path, 'w') as f:
        f.write(js_content)
    
    print(f"Successfully generated {len(restaurants)} premium restaurants in JSON and JS files.")

    # Generate Reviews
    reviews = []
    review_texts = [
        "Absolutely amazing Biryani! The spices were perfect.",
        "The service was a bit slow, but the food made up for it.",
        "Authentic Hyderabadi flavors. Highly recommended!",
        "Poor quality food. Not worth the price.",
        "Best place for family dinner. The kebabs are juicy.",
        "I've had better. Paradise is overrated.",
        "Bawarchi is the true king of biryani.",
        "Loved the ambiance and the spicy mutton curry.",
        "The best South Indian breakfast in the city.",
        "Worst experience ever. Found a hair in my food.",
        "Great value for money and large portions.",
        "The Irani chai here is legendary.",
        "Must try the Zafrani Biryani!",
        "A bit too spicy for my taste, but very flavorful.",
        "The tandoori chicken was perfectly cooked."
    ]

    for r in restaurants:
        # Generate 5-10 reviews per restaurant
        num_reviews = random.randint(5, 10)
        for _ in range(num_reviews):
            reviews.append({
                "restaurant_id": r['id'],
                "user_id": random.randint(1, 100),
                "text": random.choice(review_texts),
                "rating": random.randint(3, 5),
                "is_authentic": random.choice([True, True, True, False]) # 75% authentic
            })

    with open(reviews_path, 'w') as f:
        json.dump(reviews, f, indent=4)
    
    print(f"Successfully generated {len(reviews)} sample reviews in backend/data/sample_reviews.json")

if __name__ == '__main__':
    generate_data()
