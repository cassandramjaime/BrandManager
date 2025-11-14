"""
Journalist opportunity finder using AI and multiple sources
"""
import os
from typing import List, Optional, Dict
from datetime import datetime, timedelta
from openai import OpenAI
from .journalist_models import (
    JournalistOpportunity,
    PublicationTier,
    Urgency,
    OpportunitySource,
    SearchQuery,
    UserProfile,
    PitchTemplate,
    DailyDigest
)
from .opportunity_database import OpportunityDatabase


class OpportunityFinder:
    """AI-powered journalist opportunity finder"""
    
    # Publication tier mappings
    TIER_1_PUBLICATIONS = [
        "wall street journal", "wsj", "new york times", "nyt", "forbes",
        "bloomberg", "financial times", "the economist", "reuters", "associated press",
        "washington post", "usa today", "time magazine"
    ]
    
    TIER_2_PUBLICATIONS = [
        "techcrunch", "venturebeat", "wired", "the verge", "ars technica",
        "mashable", "engadget", "gizmodo", "fast company", "inc", "entrepreneur",
        "business insider", "cnet", "zdnet", "readwrite", "betakit"
    ]
    
    def __init__(self, api_key: Optional[str] = None, db_path: str = "opportunities.db"):
        """
        Initialize the opportunity finder
        
        Args:
            api_key: OpenAI API key. If not provided, uses OPENAI_API_KEY env var
            db_path: Path to SQLite database
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.db = OpportunityDatabase(db_path)
    
    def classify_publication_tier(self, publication_name: str) -> PublicationTier:
        """
        Classify publication tier based on publication name
        
        Args:
            publication_name: Name of the publication
            
        Returns:
            PublicationTier enum value
        """
        pub_lower = publication_name.lower()
        
        if any(tier1 in pub_lower for tier1 in self.TIER_1_PUBLICATIONS):
            return PublicationTier.TIER_1
        elif any(tier2 in pub_lower for tier2 in self.TIER_2_PUBLICATIONS):
            return PublicationTier.TIER_2
        else:
            return PublicationTier.TIER_3
    
    def calculate_urgency(self, deadline: Optional[datetime]) -> Urgency:
        """
        Calculate urgency based on deadline
        
        Args:
            deadline: Deadline datetime
            
        Returns:
            Urgency enum value
        """
        if not deadline:
            return Urgency.LOW
        
        days_until = (deadline - datetime.now()).days
        
        if days_until <= 2:
            return Urgency.HIGH
        elif days_until <= 7:
            return Urgency.MEDIUM
        else:
            return Urgency.LOW
    
    def calculate_relevance_score(
        self,
        opportunity: Dict,
        user_profile: Optional[UserProfile] = None
    ) -> float:
        """
        Calculate relevance score for an opportunity using AI
        
        Args:
            opportunity: Dictionary with opportunity details
            user_profile: Optional user profile for personalization
            
        Returns:
            Relevance score (0-100)
        """
        if not user_profile:
            user_profile = self.db.get_user_profile()
        
        if not user_profile:
            # Without user profile, use basic keyword matching
            ai_keywords = ["ai", "artificial intelligence", "machine learning", "ml"]
            pm_keywords = ["product management", "product manager", "pm"]
            
            topic_lower = opportunity.get("topic", "").lower()
            requirements_lower = opportunity.get("requirements", "").lower()
            
            text = f"{topic_lower} {requirements_lower}"
            
            ai_match = any(kw in text for kw in ai_keywords)
            pm_match = any(kw in text for kw in pm_keywords)
            
            if ai_match and pm_match:
                return 85.0
            elif ai_match or pm_match:
                return 60.0
            else:
                return 30.0
        
        # Use AI to calculate relevance
        prompt = f"""Analyze this journalist opportunity and rate its relevance for the following expert.

Expert Profile:
- Name: {user_profile.name}
- Title: {user_profile.title}
- Expertise: {', '.join(user_profile.expertise_areas)}
- Experience: {user_profile.experience_years} years
- Bio: {user_profile.bio[:200]}

Opportunity:
- Publication: {opportunity.get('publication_name', 'Unknown')}
- Topic: {opportunity.get('topic', 'Unknown')}
- Requirements: {opportunity.get('requirements', 'Unknown')}

Rate the relevance on a scale of 0-100 where:
- 90-100: Perfect match, expert is ideal for this opportunity
- 70-89: Strong match, expert is well-qualified
- 50-69: Good match, expert has relevant experience
- 30-49: Moderate match, some relevant experience
- 0-29: Poor match, limited relevance

Respond with ONLY a number between 0 and 100."""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at matching professionals with media opportunities. Provide only a numeric relevance score."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=10
            )
            
            score_text = response.choices[0].message.content.strip()
            score = float(score_text)
            return max(0.0, min(100.0, score))
            
        except Exception as e:
            print(f"Error calculating relevance score: {e}")
            return 50.0  # Default to moderate relevance
    
    def parse_opportunity_with_ai(
        self,
        text: str,
        source: OpportunitySource,
        user_profile: Optional[UserProfile] = None
    ) -> Optional[JournalistOpportunity]:
        """
        Parse opportunity text using AI to extract structured data
        
        Args:
            text: Raw opportunity text
            source: Source where opportunity was found
            user_profile: Optional user profile for relevance scoring
            
        Returns:
            JournalistOpportunity object or None if parsing fails
        """
        prompt = f"""Extract journalist opportunity information from the following text.

Text:
{text}

Extract and provide the following information in JSON format:
{{
    "publication_name": "Name of publication (or 'Unknown' if not found)",
    "journalist_name": "Name of journalist/editor (or null if not found)",
    "topic": "Topic or angle being sought",
    "deadline": "Deadline in ISO format YYYY-MM-DDTHH:MM:SS or null if not mentioned",
    "requirements": "What they're looking for/submission requirements",
    "contact_method": "How to submit or contact (email, form URL, etc.)",
    "keywords": ["keyword1", "keyword2", "keyword3"]
}}

Respond with ONLY valid JSON."""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at extracting structured information from journalist opportunity posts. Always respond with valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            import json
            data = json.loads(response.choices[0].message.content.strip())
            
            # Parse deadline if provided
            deadline = None
            if data.get('deadline'):
                try:
                    deadline = datetime.fromisoformat(data['deadline'])
                except:
                    pass
            
            # Create opportunity object
            tier = self.classify_publication_tier(data.get('publication_name', 'Unknown'))
            urgency = self.calculate_urgency(deadline)
            
            opportunity_dict = {
                'publication_name': data.get('publication_name', 'Unknown'),
                'topic': data.get('topic', 'Unknown'),
                'requirements': data.get('requirements', text[:200])
            }
            
            relevance_score = self.calculate_relevance_score(opportunity_dict, user_profile)
            
            opportunity = JournalistOpportunity(
                publication_name=data.get('publication_name', 'Unknown'),
                journalist_name=data.get('journalist_name'),
                topic=data.get('topic', 'Unknown'),
                deadline=deadline,
                requirements=data.get('requirements', text[:200]),
                contact_method=data.get('contact_method', 'See original post'),
                tier=tier,
                urgency=urgency,
                source=source,
                relevance_score=relevance_score,
                keywords=data.get('keywords', [])
            )
            
            return opportunity
            
        except Exception as e:
            print(f"Error parsing opportunity: {e}")
            return None
    
    def search_twitter_opportunities(self, max_results: int = 10) -> List[JournalistOpportunity]:
        """
        Simulate searching Twitter/X for journalist opportunities
        Note: In production, this would use Twitter API
        
        Args:
            max_results: Maximum number of results to return
            
        Returns:
            List of JournalistOpportunity objects
        """
        # This is a placeholder that demonstrates the structure
        # In production, you would integrate with Twitter API
        
        print("Note: Twitter/X search requires Twitter API credentials.")
        print("This is a demo showing the expected functionality.")
        
        # Example opportunities that might be found
        sample_opportunities = []
        
        return sample_opportunities
    
    def generate_pitch(
        self,
        opportunity: JournalistOpportunity,
        user_profile: Optional[UserProfile] = None
    ) -> PitchTemplate:
        """
        Generate a personalized pitch for an opportunity
        
        Args:
            opportunity: The opportunity to pitch for
            user_profile: User profile for personalization
            
        Returns:
            PitchTemplate with personalized pitch
        """
        if not user_profile:
            user_profile = self.db.get_user_profile()
        
        if not user_profile:
            raise ValueError("User profile is required to generate pitches. Please set up your profile first.")
        
        prompt = f"""Generate a professional pitch email for this journalist opportunity.

Opportunity:
- Publication: {opportunity.publication_name}
- Journalist: {opportunity.journalist_name or 'Editor'}
- Topic: {opportunity.topic}
- Requirements: {opportunity.requirements}

Expert Profile:
- Name: {user_profile.name}
- Title: {user_profile.title}
- Expertise: {', '.join(user_profile.expertise_areas)}
- Experience: {user_profile.experience_years} years
- Bio: {user_profile.bio}
- Key Achievements: {', '.join(user_profile.achievements[:3])}

Generate a compelling pitch email with:
1. Subject line (compelling and professional)
2. Greeting
3. Opening paragraph (reference their call and show you understand it)
4. Value proposition (why you're qualified - 2-3 sentences)
5. Specific expertise/examples (1-2 relevant achievements)
6. Call to action
7. Professional closing

Keep it concise (250-300 words total). Be professional but personable.

Provide the response in this exact format:

SUBJECT: [subject line]

GREETING: [greeting]

BODY:
[main pitch body]

CLOSING:
[closing]"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at writing compelling, professional pitch emails to journalists. You understand how to quickly establish credibility and relevance."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=600
            )
            
            pitch_text = response.choices[0].message.content.strip()
            
            # Parse the structured response
            subject = ""
            greeting = ""
            body = ""
            closing = ""
            
            lines = pitch_text.split('\n')
            current_section = None
            
            for line in lines:
                if line.startswith('SUBJECT:'):
                    subject = line.replace('SUBJECT:', '').strip()
                    current_section = 'subject'
                elif line.startswith('GREETING:'):
                    greeting = line.replace('GREETING:', '').strip()
                    current_section = 'greeting'
                elif line.startswith('BODY:'):
                    current_section = 'body'
                elif line.startswith('CLOSING:'):
                    current_section = 'closing'
                elif current_section == 'body':
                    body += line + '\n'
                elif current_section == 'closing':
                    closing += line + '\n'
            
            body = body.strip()
            closing = closing.strip()
            
            # Assemble full pitch
            full_pitch = f"{greeting}\n\n{body}\n\n{closing}"
            
            return PitchTemplate(
                opportunity_id=opportunity.id or "unknown",
                subject_line=subject,
                greeting=greeting,
                body=body,
                closing=closing,
                full_pitch=full_pitch
            )
            
        except Exception as e:
            print(f"Error generating pitch: {e}")
            # Return a basic template on error
            return PitchTemplate(
                opportunity_id=opportunity.id or "unknown",
                subject_line=f"Expert Source for {opportunity.topic}",
                greeting=f"Hi {opportunity.journalist_name or 'there'},",
                body=f"I saw your call for experts on {opportunity.topic}. As a {user_profile.title} with {user_profile.experience_years} years of experience, I would be glad to contribute.",
                closing=f"Best regards,\n{user_profile.name}",
                full_pitch=f"Hi {opportunity.journalist_name or 'there'},\n\nI saw your call for experts on {opportunity.topic}. As a {user_profile.title} with {user_profile.experience_years} years of experience, I would be glad to contribute.\n\nBest regards,\n{user_profile.name}"
            )
    
    def generate_daily_digest(self, date: Optional[datetime] = None) -> DailyDigest:
        """
        Generate a daily digest of opportunities
        
        Args:
            date: Date for the digest (defaults to today)
            
        Returns:
            DailyDigest object
        """
        if not date:
            date = datetime.now()
        
        # Get all opportunities from the database
        from .journalist_models import OpportunityFilter
        
        all_opportunities = self.db.list_opportunities()
        
        # Filter to opportunities found in the last 24 hours
        cutoff = date - timedelta(days=1)
        recent_opportunities = [
            opp for opp in all_opportunities
            if opp.found_at >= cutoff
        ]
        
        # Categorize by priority based on relevance score and urgency
        high_priority = [
            opp for opp in recent_opportunities
            if opp.relevance_score >= 70 or (opp.urgency == Urgency.HIGH and opp.relevance_score >= 50)
        ]
        
        medium_priority = [
            opp for opp in recent_opportunities
            if 50 <= opp.relevance_score < 70 and opp.urgency != Urgency.HIGH
        ]
        
        low_priority = [
            opp for opp in recent_opportunities
            if opp.relevance_score < 50
        ]
        
        # Sort each category by relevance score
        high_priority.sort(key=lambda x: x.relevance_score, reverse=True)
        medium_priority.sort(key=lambda x: x.relevance_score, reverse=True)
        low_priority.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return DailyDigest(
            date=date,
            total_opportunities=len(recent_opportunities),
            high_priority=high_priority,
            medium_priority=medium_priority,
            low_priority=low_priority
        )
    
    def add_opportunity_from_text(
        self,
        text: str,
        source: OpportunitySource,
        user_profile: Optional[UserProfile] = None
    ) -> Optional[str]:
        """
        Parse and add an opportunity from raw text
        
        Args:
            text: Raw opportunity text
            source: Source platform
            user_profile: Optional user profile
            
        Returns:
            Opportunity ID if successful, None otherwise
        """
        opportunity = self.parse_opportunity_with_ai(text, source, user_profile)
        
        if opportunity:
            opportunity_id = self.db.add_opportunity(opportunity)
            return opportunity_id
        
        return None
