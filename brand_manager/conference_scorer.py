"""
Conference scoring and ranking system
"""
from typing import List
from .conference_models import Conference, TopicFocus


class ConferenceScorer:
    """Scores and ranks conferences based on various criteria"""
    
    def __init__(self):
        # Weight factors for overall score
        self.weights = {
            'relevance': 0.4,
            'speaker_quality': 0.3,
            'networking': 0.3
        }
        
        # Keywords indicating high relevance to AI/ML
        self.ai_keywords = [
            'ai', 'artificial intelligence', 'machine learning', 'ml',
            'deep learning', 'neural', 'generative ai', 'llm', 'gpt',
            'chatgpt', 'openai', 'ai-powered', 'ai-first'
        ]
        
        # Keywords indicating quality speakers
        self.quality_speaker_keywords = [
            'vp', 'cpo', 'chief product', 'director', 'head of product',
            'google', 'meta', 'amazon', 'microsoft', 'apple', 'netflix',
            'airbnb', 'uber', 'stripe', 'openai'
        ]
    
    def score_conference(self, conference: Conference) -> Conference:
        """
        Score a conference on multiple dimensions
        
        Args:
            conference: Conference to score
            
        Returns:
            Conference with updated scores
        """
        # Score AI/ML relevance
        conference.relevance_score = self._score_ai_relevance(conference)
        
        # Score speaker quality
        conference.speaker_quality_score = self._score_speaker_quality(conference)
        
        # Score networking opportunities
        conference.networking_score = self._score_networking(conference)
        
        # Calculate overall score
        conference.overall_score = (
            self.weights['relevance'] * conference.relevance_score +
            self.weights['speaker_quality'] * conference.speaker_quality_score +
            self.weights['networking'] * conference.networking_score
        )
        
        # Round scores to 1 decimal place
        conference.relevance_score = round(conference.relevance_score, 1)
        conference.speaker_quality_score = round(conference.speaker_quality_score, 1)
        conference.networking_score = round(conference.networking_score, 1)
        conference.overall_score = round(conference.overall_score, 1)
        
        return conference
    
    def _score_ai_relevance(self, conference: Conference) -> float:
        """
        Score conference relevance to AI product management (0-10)
        
        Factors:
        - Topic focus includes AI/ML
        - Conference name mentions AI
        - Agenda topics mention AI/ML
        - Description mentions AI
        """
        score = 0.0
        
        # Check topic focus (max 4 points)
        if TopicFocus.AI_ML in conference.topic_focus:
            score += 4.0
        elif TopicFocus.DATA in conference.topic_focus:
            score += 2.0
        
        # Check conference name (max 2 points)
        name_lower = conference.name.lower()
        ai_mentions = sum(1 for keyword in self.ai_keywords if keyword in name_lower)
        score += min(2.0, ai_mentions * 0.5)
        
        # Check agenda topics (max 3 points)
        agenda_text = ' '.join(conference.agenda_topics).lower()
        ai_topic_mentions = sum(1 for keyword in self.ai_keywords if keyword in agenda_text)
        score += min(3.0, ai_topic_mentions * 0.5)
        
        # Check description (max 1 point)
        if conference.description:
            desc_lower = conference.description.lower()
            if any(keyword in desc_lower for keyword in self.ai_keywords):
                score += 1.0
        
        return min(10.0, score)
    
    def _score_speaker_quality(self, conference: Conference) -> float:
        """
        Score speaker quality (0-10)
        
        Factors:
        - Number of notable speakers
        - Speaker titles and companies
        """
        score = 0.0
        
        if not conference.notable_speakers:
            return 3.0  # Base score for conferences without speaker info
        
        # Number of speakers (max 3 points)
        num_speakers = len(conference.notable_speakers)
        score += min(3.0, num_speakers * 0.5)
        
        # Quality indicators (max 7 points)
        speakers_text = ' '.join(conference.notable_speakers).lower()
        quality_mentions = sum(1 for keyword in self.quality_speaker_keywords if keyword in speakers_text)
        score += min(7.0, quality_mentions * 1.0)
        
        return min(10.0, score)
    
    def _score_networking(self, conference: Conference) -> float:
        """
        Score networking opportunities (0-10)
        
        Factors:
        - In-person vs virtual (in-person better for networking)
        - Conference duration (longer = more networking)
        - Conference size (inferred from price and speaker count)
        - Conference reputation (inferred from source and speaker quality)
        """
        score = 0.0
        
        # Location type (max 4 points)
        if conference.location_type.value == 'in-person':
            score += 4.0
        elif conference.location_type.value == 'hybrid':
            score += 3.0
        else:  # virtual
            score += 1.5
        
        # Duration (max 3 points)
        duration_days = (conference.end_date - conference.start_date).days + 1
        score += min(3.0, duration_days * 1.0)
        
        # Conference size/prestige based on price (max 2 points)
        if conference.ticket_price_max:
            if conference.ticket_price_max >= 800:
                score += 2.0  # High-end conferences tend to have better networking
            elif conference.ticket_price_max >= 400:
                score += 1.5
            elif conference.ticket_price_max >= 100:
                score += 1.0
            else:
                score += 0.5
        elif conference.ticket_price_min == 0:
            score += 0.5  # Free events may have less curated networking
        
        # Speaker count as proxy for conference size (max 1 point)
        if len(conference.notable_speakers) >= 10:
            score += 1.0
        elif len(conference.notable_speakers) >= 5:
            score += 0.7
        elif len(conference.notable_speakers) >= 2:
            score += 0.4
        
        return min(10.0, score)
    
    def rank_conferences(self, conferences: List[Conference]) -> List[Conference]:
        """
        Score and rank conferences
        
        Args:
            conferences: List of conferences to rank
            
        Returns:
            Sorted list of scored conferences (highest score first)
        """
        # Score all conferences
        scored_conferences = [self.score_conference(conf) for conf in conferences]
        
        # Sort by overall score (descending)
        scored_conferences.sort(key=lambda x: x.overall_score, reverse=True)
        
        return scored_conferences
