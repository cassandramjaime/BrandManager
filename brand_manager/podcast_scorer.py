"""
Scoring system for podcast opportunities
"""
from typing import List, Optional
import re


class PodcastScorer:
    """Score podcast opportunities based on various criteria"""
    
    # Keywords for AI/ML/PM relevance
    AI_ML_KEYWORDS = [
        'ai', 'artificial intelligence', 'machine learning', 'ml', 'deep learning',
        'neural network', 'data science', 'nlp', 'computer vision', 'robotics',
        'automation', 'chatbot', 'llm', 'gpt', 'generative ai'
    ]
    
    PM_KEYWORDS = [
        'product manager', 'product management', 'product leader', 'product strategy',
        'pm', 'product', 'saas', 'software', 'tech', 'startup', 'roadmap',
        'product development', 'agile', 'scrum', 'innovation'
    ]
    
    def __init__(self):
        """Initialize the scorer"""
        pass
    
    def calculate_relevance_score(
        self,
        podcast_name: str,
        description: Optional[str] = None,
        guest_profile: Optional[str] = None
    ) -> float:
        """
        Calculate relevance score based on AI/ML/PM keywords
        Returns score from 0-100
        """
        text_to_analyze = f"{podcast_name} {description or ''} {guest_profile or ''}".lower()
        
        # Count keyword matches
        ai_ml_matches = sum(
            1 for keyword in self.AI_ML_KEYWORDS 
            if keyword in text_to_analyze
        )
        pm_matches = sum(
            1 for keyword in self.PM_KEYWORDS 
            if keyword in text_to_analyze
        )
        
        # Calculate base score (0-100)
        # Each AI/ML keyword match gives 10 points (max 60)
        # Each PM keyword match gives 8 points (max 40)
        ai_ml_score = min(ai_ml_matches * 10, 60)
        pm_score = min(pm_matches * 8, 40)
        
        total_score = ai_ml_score + pm_score
        
        # Bonus points for exact matches of important phrases
        if 'product manager' in text_to_analyze or 'product management' in text_to_analyze:
            total_score = min(total_score + 10, 100)
        
        if 'artificial intelligence' in text_to_analyze or 'machine learning' in text_to_analyze:
            total_score = min(total_score + 10, 100)
        
        return round(total_score, 2)
    
    def calculate_audience_score(self, audience_size: Optional[int]) -> float:
        """
        Calculate audience score based on size
        Returns score from 0-100
        
        Scoring tiers:
        - 100K+: 100 points
        - 50K-100K: 90 points
        - 25K-50K: 80 points
        - 10K-25K: 70 points
        - 5K-10K: 60 points
        - 2K-5K: 50 points
        - 1K-2K: 40 points
        - 500-1K: 30 points
        - Under 500: 20 points
        - Unknown: 10 points (give benefit of doubt for small but growing shows)
        """
        if audience_size is None:
            return 10.0
        
        if audience_size >= 100000:
            return 100.0
        elif audience_size >= 50000:
            return 90.0
        elif audience_size >= 25000:
            return 80.0
        elif audience_size >= 10000:
            return 70.0
        elif audience_size >= 5000:
            return 60.0
        elif audience_size >= 2000:
            return 50.0
        elif audience_size >= 1000:
            return 40.0
        elif audience_size >= 500:
            return 30.0
        else:
            return 20.0
    
    def calculate_engagement_score(
        self,
        has_submission_form: bool = False,
        has_contact: bool = False,
        has_description: bool = False,
        source_credibility: str = "unknown"
    ) -> float:
        """
        Calculate engagement score based on completeness of information
        Returns score from 0-100
        """
        score = 0.0
        
        # Points for having submission information
        if has_submission_form:
            score += 40.0
        
        # Points for contact information
        if has_contact:
            score += 20.0
        
        # Points for detailed description
        if has_description:
            score += 20.0
        
        # Points based on source credibility
        source_scores = {
            'podmatch': 20.0,
            'matchmaker': 20.0,
            'podcastguests': 20.0,
            'linkedin': 15.0,
            'twitter': 10.0,
            'website': 15.0,
            'unknown': 5.0
        }
        score += source_scores.get(source_credibility.lower(), 5.0)
        
        return min(score, 100.0)
    
    def calculate_total_score(
        self,
        relevance_score: float,
        audience_score: float,
        engagement_score: float,
        weights: Optional[dict] = None
    ) -> float:
        """
        Calculate total weighted score
        Default weights: relevance 50%, audience 30%, engagement 20%
        Returns score from 0-100
        """
        if weights is None:
            weights = {
                'relevance': 0.5,
                'audience': 0.3,
                'engagement': 0.2
            }
        
        total = (
            relevance_score * weights.get('relevance', 0.5) +
            audience_score * weights.get('audience', 0.3) +
            engagement_score * weights.get('engagement', 0.2)
        )
        
        return round(total, 2)
    
    def generate_fit_reason(
        self,
        podcast_name: str,
        relevance_score: float,
        audience_score: float,
        description: Optional[str] = None
    ) -> str:
        """Generate a human-readable explanation of why this is a good fit"""
        reasons = []
        
        if relevance_score >= 70:
            reasons.append("Strong topical alignment with AI/ML and product management")
        elif relevance_score >= 50:
            reasons.append("Good alignment with your expertise areas")
        elif relevance_score >= 30:
            reasons.append("Moderate relevance to your background")
        
        if audience_score >= 80:
            reasons.append(f"Large, established audience")
        elif audience_score >= 60:
            reasons.append(f"Growing audience with good reach")
        elif audience_score >= 40:
            reasons.append(f"Smaller but potentially engaged audience")
        
        # Add specific insights from description if available
        if description:
            description_lower = description.lower()
            if 'product' in description_lower and 'ai' in description_lower:
                reasons.append("Specifically focused on AI product topics")
            elif 'technical' in description_lower or 'engineering' in description_lower:
                reasons.append("Technical audience that appreciates PM/AI expertise")
        
        if not reasons:
            reasons.append("Potential opportunity worth exploring")
        
        return "; ".join(reasons)
