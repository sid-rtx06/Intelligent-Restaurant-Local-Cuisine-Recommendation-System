from textblob import TextBlob
import nltk
from typing import Dict, List

class SentimentAnalyzer:
    """
    Sentiment Analysis for restaurant reviews
    Extracts polarity, subjectivity, and sentiment labels
    """
    
    def __init__(self):
        # Download required NLTK data (run once)
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)
    
    def analyze_sentiment(self, text: str) -> Dict:
        """
        Analyze sentiment of review text
        
        Args:
            text: Review text string
            
        Returns:
            dict: {
                'polarity': float (-1 to 1, negative to positive),
                'subjectivity': float (0 to 1, objective to subjective),
                'label': str ('positive', 'negative', 'neutral')
            }
        """
        # Create TextBlob object
        blob = TextBlob(text)
        
        # Get sentiment scores
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Determine label
        if polarity > 0.1:
            label = 'positive'
        elif polarity < -0.1:
            label = 'negative'
        else:
            label = 'neutral'
        
        return {
            'polarity': round(polarity, 4),
            'subjectivity': round(subjectivity, 4),
            'label': label
        }
    
    def analyze_batch(self, texts: List[str]) -> List[Dict]:
        """
        Analyze sentiment for multiple reviews
        
        Args:
            texts: List of review text strings
            
        Returns:
            list: List of sentiment dictionaries
        """
        return [self.analyze_sentiment(text) for text in texts]
    
    def get_overall_sentiment(self, texts: List[str]) -> Dict:
        """
        Get overall sentiment statistics for a collection of reviews
        
        Args:
            texts: List of review text strings
            
        Returns:
            dict: Overall sentiment statistics
        """
        sentiments = self.analyze_batch(texts)
        
        if not sentiments:
            return {
                'avg_polarity': 0,
                'avg_subjectivity': 0,
                'positive_count': 0,
                'negative_count': 0,
                'neutral_count': 0,
                'total_count': 0
            }
        
        polarities = [s['polarity'] for s in sentiments]
        subjectivities = [s['subjectivity'] for s in sentiments]
        labels = [s['label'] for s in sentiments]
        
        return {
            'avg_polarity': round(sum(polarities) / len(polarities), 4),
            'avg_subjectivity': round(sum(subjectivities) / len(subjectivities), 4),
            'positive_count': labels.count('positive'),
            'negative_count': labels.count('negative'),
            'neutral_count': labels.count('neutral'),
            'total_count': len(sentiments),
            'positive_percentage': round(labels.count('positive') / len(labels) * 100, 2),
            'negative_percentage': round(labels.count('negative') / len(labels) * 100, 2)
        }
    
    def extract_key_phrases(self, text: str, top_n: int = 5) -> List[str]:
        """
        Extract key noun phrases from review text
        
        Args:
            text: Review text string
            top_n: Number of top phrases to return
            
        Returns:
            list: Key noun phrases
        """
        blob = TextBlob(text)
        phrases = list(blob.noun_phrases)
        
        # Return unique phrases
        unique_phrases = []
        seen = set()
        for phrase in phrases:
            if phrase not in seen and len(phrase) > 3:
                unique_phrases.append(phrase)
                seen.add(phrase)
                if len(unique_phrases) >= top_n:
                    break
        
        return unique_phrases

# Initialize global analyzer instance
analyzer = SentimentAnalyzer()
