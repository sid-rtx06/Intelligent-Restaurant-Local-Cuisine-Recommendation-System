# Intelligent Restaurant & Local Cuisine Recommendation System

An AI-powered full-stack web application that provides personalized and trustworthy restaurant recommendations using Machine Learning, NLP, and fake review detection.

## 🌟 Features

- **🛡️ Fake Review Detection**: ML-powered authenticity scoring to filter out fake reviews
- **💭 Sentiment Analysis**: NLP-based sentiment extraction from reviews
- **🎯 Hybrid Recommendation Engine**: Combines content-based, collaborative, and location-based filtering
- **✨ Explainable AI**: Transparent recommendations with detailed explanations
- **📍 Location-Based Discovery**: Find restaurants near you with intelligent distance filtering
- **🎨 Modern UI**: Stunning dark mode design with glassmorphism and smooth animations

## 🏗️ Architecture

### Frontend
- **HTML5, CSS3, JavaScript** (Vanilla)
- Modern responsive design with dark mode
- Glassmorphism effects and gradient animations
- Google Fonts (Inter, Outfit)

### Backend
- **Python Flask** - RESTful API
- **JWT Authentication** - Secure user sessions
- **Modular Architecture** - Clean separation of concerns

### Databases
- **MySQL** - Structured data (users, restaurants, preferences)
- **MongoDB** - Unstructured review data with NLP metadata

### Machine Learning
- **Fake Review Detection** - TF-IDF + Random Forest
- **Sentiment Analysis** - TextBlob NLP
- **Recommendation Engine** - Hybrid filtering with weighted scoring

## 📋 Prerequisites

- Python 3.8+
- MySQL 5.7+
- MongoDB 4.0+
- Modern web browser

## 🚀 Installation

### 1. Clone the Repository

```bash
cd RTRP
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Database Setup

#### MySQL
```bash
# Login to MySQL
mysql -u root -p

# Run the schema script
source ../database/mysql_schema.sql
```

#### MongoDB
```bash
# Run MongoDB setup
mongosh < ../database/mongodb_setup.js
```

### 4. Configure Environment

Create a `.env` file in the `backend` directory (optional):

```env
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=restaurant_recommendation
MONGO_URI=mongodb://localhost:27017/
```

### 5. Setup Sample Data & Train ML Models

```bash
cd backend
python setup_data.py
```

This will:
- Train the fake review detection model
- Load sample restaurants into MySQL
- Load sample reviews into MongoDB
- Analyze sentiment and authenticity

### 1. Requirements
Ensure you have **MySQL** and **MongoDB** installed and running on their default ports (3306 and 27017).

### 2. One-Click Startup
The simplest way to run everything is using the unified runner script:

```bash
python run_all.py
```

This script will:
- Check for MySQL and MongoDB availability.
- Automatically set up the database and sample data if missing.
- Train the AI models for fake review detection and sentiment analysis.
- Start both the Flask API server (port 5000) and the Frontend web server (port 8000).
- Open the application in your default web browser.

### 3. Troubleshooting
If you encounter a "Connection Issue Detected" message:
- Check that your MySQL service is running.
- Ensure all Python dependencies are installed using `pip install -r backend/requirements.txt`.
- Re-run `python run_all.py`.

## 📚 API Documentation

### Authentication

#### POST `/api/auth/signup`
Register a new user
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123",
  "phone": "+1234567890"
}
```

#### POST `/api/auth/login`
Login user
```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

#### GET `/api/auth/profile`
Get user profile (requires JWT token)

### Restaurants

#### GET `/api/restaurants`
Get all restaurants with optional filters
- Query params: `cuisine`, `city`, `search`, `limit`, `offset`

#### GET `/api/restaurants/{id}`
Get restaurant details by ID

#### GET `/api/restaurants/{id}/reviews`
Get restaurant reviews
- Query params: `authentic_only` (default: true)

#### GET `/api/restaurants/popular`
Get popular restaurants

### Recommendations

#### POST `/api/recommendations`
Get personalized recommendations (requires JWT)
```json
{
  "latitude": 17.3850,
  "longitude": 78.4867,
  "cuisine_preferences": ["Italian", "Chinese"],
  "mood_preferences": ["Spicy", "Healthy"],
  "budget_min": 0,
  "budget_max": 5000,
  "max_distance_km": 10,
  "top_n": 10
}
```

#### POST `/api/recommendations/nearby`
Get nearby restaurants (no auth required)
```json
{
  "latitude": 17.3850,
  "longitude": 78.4867,
  "max_distance_km": 10
}
```

### Reviews

#### POST `/api/reviews`
Submit a review (requires JWT)
```json
{
  "restaurant_id": 1,
  "text": "Amazing food and great service!",
  "rating": 5
}
```

#### GET `/api/reviews/user`
Get current user's reviews (requires JWT)

## 🎯 How It Works

### 1. Fake Review Detection
- Uses TF-IDF vectorization to convert review text into numerical features
- Random Forest classifier trained on authentic vs fake review patterns
- Returns authenticity score (0-1) for each review

### 2. Sentiment Analysis
- TextBlob NLP library extracts polarity (-1 to 1) and subjectivity (0 to 1)
- Categorizes reviews as positive, negative, or neutral
- Stores sentiment metadata in MongoDB

### 3. Hybrid Recommendation Engine
Combines multiple filtering approaches:

**Content-Based Filtering (40%)**
- Matches user preferences (cuisine, mood, budget) with restaurant attributes

**Authenticity Score (30%)**
- Prioritizes restaurants with high authentic review scores

**Location-Based Filtering (20%)**
- Uses Haversine formula to calculate distance
- Exponential decay favors closer restaurants

**Popularity Score (10%)**
- Based on user interactions and review count

**Final Score** = Weighted sum of all components

### 4. Explainable AI
Each recommendation includes:
- Score breakdown by component
- Human-readable explanation
- Transparency in decision-making

## 🎨 Frontend Features

- **Landing Page**: Hero section with feature showcase
- **Authentication**: Login and signup with validation
- **Home Page**: Preference selection with interactive chips and sliders
- **Recommendations**: AI-powered suggestions with score breakdowns
- **Restaurant Details**: Full details with reviews and sentiment analysis
- **Review Submission**: Write reviews with star ratings

## 🔒 Security

- JWT-based authentication
- Password hashing with bcrypt
- CORS protection
- Input validation and sanitization

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| Frontend | HTML5, CSS3, JavaScript |
| Backend | Python, Flask |
| Databases | MySQL, MongoDB |
| ML/AI | scikit-learn, NLTK, TextBlob |
| Authentication | JWT, bcrypt |
| API | RESTful, JSON |

## 📊 Database Schema

### MySQL Tables
- `users` - User accounts
- `restaurants` - Restaurant information
- `user_preferences` - User food preferences
- `user_interactions` - Interaction history for collaborative filtering
- `cuisine_types` - Reference table for cuisines

### MongoDB Collections
- `reviews` - Review text with sentiment and authenticity metadata

## 🤝 Contributing

This is an academic project. Feel free to fork and enhance!

## 📝 License

MIT License

## 👨‍💻 Author

Built with ❤️ using AI and Machine Learning

## 🙏 Acknowledgments

- scikit-learn for ML algorithms
- TextBlob for NLP
- Flask for the backend framework
- Unsplash for sample images

---

**Note**: This is a demonstration project with sample data. For production use, integrate with real restaurant APIs (Google Places, Yelp, Zomato) and use actual labeled datasets for ML training.
