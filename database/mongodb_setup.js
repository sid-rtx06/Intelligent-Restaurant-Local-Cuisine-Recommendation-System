// MongoDB setup script for reviews collection
// Run with: mongosh < mongodb_setup.js

use restaurant_reviews;

// Create reviews collection with schema validation
db.createCollection("reviews", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["restaurant_id", "user_id", "text", "rating"],
            properties: {
                restaurant_id: {
                    bsonType: "int",
                    description: "Restaurant ID from MySQL"
                },
                user_id: {
                    bsonType: "int",
                    description: "User ID from MySQL"
                },
                text: {
                    bsonType: "string",
                    description: "Review text content"
                },
                rating: {
                    bsonType: "int",
                    minimum: 1,
                    maximum: 5,
                    description: "Rating from 1 to 5"
                },
                sentiment: {
                    bsonType: "object",
                    properties: {
                        polarity: { bsonType: "double" },
                        subjectivity: { bsonType: "double" },
                        label: { bsonType: "string" }
                    }
                },
                authenticity_score: {
                    bsonType: "double",
                    minimum: 0,
                    maximum: 1,
                    description: "Fake review detection score (0-1)"
                },
                is_authentic: {
                    bsonType: "bool",
                    description: "Whether review is classified as authentic"
                },
                created_at: {
                    bsonType: "date",
                    description: "Review creation timestamp"
                }
            }
        }
    }
});

// Create indexes for better query performance
db.reviews.createIndex({ "restaurant_id": 1 });
db.reviews.createIndex({ "user_id": 1 });
db.reviews.createIndex({ "authenticity_score": -1 });
db.reviews.createIndex({ "is_authentic": 1 });
db.reviews.createIndex({ "created_at": -1 });
db.reviews.createIndex({ "restaurant_id": 1, "is_authentic": 1 });

print("MongoDB setup completed successfully!");
print("Collection 'reviews' created with indexes");
