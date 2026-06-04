-- Create database
CREATE DATABASE IF NOT EXISTS restaurant_recommendation;
USE restaurant_recommendation;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email)
);

-- Restaurants table
CREATE TABLE IF NOT EXISTS restaurants (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(200) NOT NULL,
    cuisine_type VARCHAR(100),
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    address TEXT,
    city VARCHAR(100),
    price_range ENUM('$', '$$', '$$$', '$$$$') DEFAULT '$$',
    popularity_score FLOAT DEFAULT 0,
    authenticity_score FLOAT DEFAULT 0.5,
    image_url VARCHAR(500),
    description TEXT,
    special_dish VARCHAR(200),
    best_seller VARCHAR(200),
    high_protein VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_cuisine (cuisine_type),
    INDEX idx_location (latitude, longitude),
    INDEX idx_city (city)
);

-- User preferences table
CREATE TABLE IF NOT EXISTS user_preferences (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT UNIQUE,
    cuisine_preferences JSON,
    mood_preferences JSON,
    budget_min INT DEFAULT 0,
    budget_max INT DEFAULT 10000,
    preferred_distance_km INT DEFAULT 10,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- User interactions (for collaborative filtering)
CREATE TABLE IF NOT EXISTS user_interactions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    restaurant_id INT,
    interaction_type ENUM('view', 'favorite', 'order', 'review') NOT NULL,
    rating INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id) ON DELETE CASCADE,
    INDEX idx_user_restaurant (user_id, restaurant_id),
    INDEX idx_interaction_type (interaction_type)
);

-- Cuisine types reference table
CREATE TABLE IF NOT EXISTS cuisine_types (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    region VARCHAR(100)
);

-- Insert common cuisine types
INSERT INTO cuisine_types (name, description, region) VALUES
('Italian', 'Italian cuisine with pasta, pizza, and Mediterranean flavors', 'Europe'),
('Chinese', 'Traditional Chinese dishes with diverse regional styles', 'Asia'),
('Indian', 'Rich and spicy Indian cuisine with curries and tandoor', 'Asia'),
('Mexican', 'Mexican food with tacos, burritos, and bold flavors', 'Americas'),
('Japanese', 'Japanese cuisine including sushi, ramen, and tempura', 'Asia'),
('Thai', 'Thai food with aromatic herbs and spicy flavors', 'Asia'),
('American', 'Classic American comfort food and fast food', 'Americas'),
('Mediterranean', 'Healthy Mediterranean diet with olive oil and fresh ingredients', 'Europe'),
('Korean', 'Korean cuisine with kimchi, BBQ, and fermented foods', 'Asia'),
('French', 'Elegant French cuisine with fine dining traditions', 'Europe'),
('Vietnamese', 'Light and fresh Vietnamese dishes with herbs', 'Asia'),
('Middle Eastern', 'Middle Eastern food with kebabs, hummus, and flatbreads', 'Middle East'),
('Street Food', 'Local street food and quick bites', 'Various'),
('Fusion', 'Creative fusion combining multiple cuisines', 'Various')
ON DUPLICATE KEY UPDATE name=name;
-- Menu Items table
CREATE TABLE IF NOT EXISTS menu_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    restaurant_id INT,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    image_url VARCHAR(500),
    category VARCHAR(50),
    is_best_seller BOOLEAN DEFAULT FALSE,
    is_high_protein BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id) ON DELETE CASCADE,
    INDEX idx_restaurant (restaurant_id)
);
