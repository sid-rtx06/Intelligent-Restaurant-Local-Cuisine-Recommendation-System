import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
from config import Config

class FakeReviewDetector:
    """
    Fake Review Detection using TF-IDF and Random Forest
    Analyzes review text patterns to identify potentially fake reviews
    """
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 3),
            min_df=2,
            max_df=0.8,
            stop_words='english'
        )
        self.classifier = RandomForestClassifier(
            n_estimators=100,
            max_depth=20,
            random_state=42,
            class_weight='balanced'
        )
        self.is_trained = False
        
    def train(self, reviews_df):
        """
        Train the fake review detection model
        
        Args:
            reviews_df: DataFrame with columns ['text', 'is_fake']
                       where is_fake is 1 for fake, 0 for authentic
        """
        if 'text' not in reviews_df.columns or 'is_fake' not in reviews_df.columns:
            raise ValueError("DataFrame must contain 'text' and 'is_fake' columns")
        
        # Prepare data
        X = reviews_df['text'].values
        y = reviews_df['is_fake'].values
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Vectorize text
        X_train_vec = self.vectorizer.fit_transform(X_train)
        X_test_vec = self.vectorizer.transform(X_test)
        
        # Train classifier
        self.classifier.fit(X_train_vec, y_train)
        
        # Evaluate
        y_pred = self.classifier.predict(X_test_vec)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Fake Review Detection Model Trained!")
        print(f"Accuracy: {accuracy:.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['Authentic', 'Fake']))
        
        self.is_trained = True
        return accuracy
    
    def predict_authenticity(self, review_text):
        """
        Predict authenticity score for a single review
        
        Args:
            review_text: String containing the review text
            
        Returns:
            float: Authenticity score (0-1), where higher means more authentic
        """
        if not self.is_trained:
            # If model not trained, return neutral score
            return 0.5
        
        # Vectorize the review
        review_vec = self.vectorizer.transform([review_text])
        
        # Get probability of being authentic (class 0)
        proba = self.classifier.predict_proba(review_vec)[0]
        authenticity_score = proba[0]  # Probability of being authentic
        
        return float(authenticity_score)
    
    def predict_batch(self, review_texts):
        """
        Predict authenticity scores for multiple reviews
        
        Args:
            review_texts: List of review text strings
            
        Returns:
            numpy array: Authenticity scores (0-1)
        """
        if not self.is_trained:
            return np.full(len(review_texts), 0.5)
        
        reviews_vec = self.vectorizer.transform(review_texts)
        probas = self.classifier.predict_proba(reviews_vec)
        return probas[:, 0]  # Return authentic probabilities
    
    def save_model(self, path=None):
        """Save the trained model and vectorizer"""
        if path is None:
            path = Config.MODEL_PATH
        
        os.makedirs(path, exist_ok=True)
        
        joblib.dump(self.vectorizer, os.path.join(path, 'vectorizer.pkl'))
        joblib.dump(self.classifier, os.path.join(path, 'fake_review_model.pkl'))
        print(f"Model saved to {path}")
    
    def load_model(self, path=None):
        """Load a pre-trained model and vectorizer. Auto-trains if missing."""
        if path is None:
            path = Config.MODEL_PATH
        
        vectorizer_path = os.path.join(path, 'vectorizer.pkl')
        model_path = os.path.join(path, 'fake_review_model.pkl')
        
        if os.path.exists(vectorizer_path) and os.path.exists(model_path):
            try:
                self.vectorizer = joblib.load(vectorizer_path)
                self.classifier = joblib.load(model_path)
                self.is_trained = True
                print("[OK] Fake review model loaded successfully")
                return True
            except Exception as e:
                print(f"[WARN] Error loading model: {e}")
        
        # Self-initialization: Train with synthetic data if missing
        print("[AI] Model files not found or corrupted. Triggering automatic training...")
        try:
            from .fake_review_detector import generate_synthetic_training_data
            data = generate_synthetic_training_data()
            self.train(data)
            self.save_model()
            return True
        except Exception as e:
            print(f"[ERROR] Auto-training failed: {e}")
            return False

def generate_synthetic_training_data():
    """
    Generate synthetic training data for fake review detection
    This is a placeholder - in production, use real labeled data
    """
    # Authentic review patterns
    authentic_reviews = [
        "The food was absolutely delicious! I especially loved the pasta carbonara.",
        "Great atmosphere and friendly staff. The pizza was a bit cold though.",
        "Decent place for a quick lunch. Nothing extraordinary but good value.",
        "I've been coming here for years. Consistent quality and service.",
        "The portions were generous and the flavors were authentic.",
        "Service was slow but the food made up for it. Will come back.",
        "Nice ambiance for a date night. A bit pricey but worth it.",
        "The menu has good variety. I tried the chicken tikka and it was flavorful.",
        "Clean restaurant with attentive waiters. Food arrived hot and fresh.",
        "My family enjoyed our meal here. Kids loved the desserts.",
    ] * 50  # Repeat to create more samples
    
    # Fake review patterns (overly generic, repetitive, extreme)
    fake_reviews = [
        "Best restaurant ever! Amazing! Perfect! Excellent! Must visit!",
        "This is the best place in the world. Everything is perfect. 5 stars!",
        "Awesome awesome awesome! So good! Best food ever! Go now!",
        "Perfect service perfect food perfect everything. Highly recommend!",
        "Amazing experience! Best ever! Will definitely come back! Perfect!",
        "This restaurant is the best. Food is amazing. Service is perfect.",
        "Excellent excellent excellent! Everything was perfect! Best place!",
        "Great great great! So amazing! Perfect food! Best service ever!",
        "This is the most amazing restaurant. Everything is perfect. Must try!",
        "Best food in the city! Perfect service! Amazing atmosphere! 5 stars!",
    ] * 50
    
    # Create DataFrame
    df = pd.DataFrame({
        'text': authentic_reviews + fake_reviews,
        'is_fake': [0] * len(authentic_reviews) + [1] * len(fake_reviews)
    })
    
    return df

# Initialize global detector instance
detector = FakeReviewDetector()

# Try to load pre-trained model, otherwise use untrained model
detector.load_model()
