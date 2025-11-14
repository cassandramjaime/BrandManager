"""
Data models for journalist opportunity finder
"""
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


class PublicationTier(str, Enum):
    """Publication tier classification"""
    TIER_1 = "tier_1"  # WSJ, NYT, Forbes, etc.
    TIER_2 = "tier_2"  # TechCrunch, VentureBeat, Wired, etc.
    TIER_3 = "tier_3"  # Smaller blogs, niche publications


class Urgency(str, Enum):
    """Urgency level based on deadline"""
    HIGH = "high"      # Deadline within 24-48 hours
    MEDIUM = "medium"  # Deadline within 3-7 days
    LOW = "low"        # Deadline more than 7 days out


class OpportunitySource(str, Enum):
    """Source where opportunity was found"""
    HARO = "haro"
    TWITTER = "twitter"
    MEDIUM = "medium"
    SUBSTACK = "substack"
    LINKEDIN = "linkedin"
    TERKEL = "terkel"
    QWOTED = "qwoted"
    FEATURED = "featured"
    SOURCEBOTTLE = "sourcebottle"
    OTHER = "other"


class JournalistOpportunity(BaseModel):
    """Model for a journalist/publication opportunity"""
    id: Optional[str] = None
    publication_name: str = Field(..., description="Name of the publication")
    journalist_name: Optional[str] = Field(None, description="Name of journalist/editor")
    topic: str = Field(..., description="Topic/angle being sought")
    deadline: Optional[datetime] = Field(None, description="Submission deadline")
    requirements: str = Field(..., description="Submission requirements and details")
    contact_method: str = Field(..., description="How to submit/contact (email, form, etc.)")
    tier: PublicationTier = Field(..., description="Publication tier classification")
    urgency: Urgency = Field(..., description="Urgency level based on deadline")
    source: OpportunitySource = Field(..., description="Where the opportunity was found")
    relevance_score: float = Field(default=0.0, description="Relevance score (0-100)")
    
    # Keywords for filtering
    keywords: List[str] = Field(default_factory=list, description="Relevant keywords")
    
    # Tracking fields
    found_at: datetime = Field(default_factory=datetime.now, description="When opportunity was discovered")
    pitch_sent: bool = Field(default=False, description="Whether a pitch was sent")
    pitch_sent_at: Optional[datetime] = Field(None, description="When pitch was sent")
    response_received: bool = Field(default=False, description="Whether a response was received")
    response_received_at: Optional[datetime] = Field(None, description="When response was received")
    notes: str = Field(default="", description="Additional notes")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "publication_name": "TechCrunch",
                "journalist_name": "John Doe",
                "topic": "AI in Product Management",
                "deadline": "2025-11-20T23:59:59",
                "requirements": "Looking for AI PM experts to discuss how AI is changing product management",
                "contact_method": "john.doe@techcrunch.com",
                "tier": "tier_2",
                "urgency": "high",
                "source": "twitter",
                "relevance_score": 92.5
            }
        }
    )


class SearchQuery(BaseModel):
    """Model for search queries across platforms"""
    platform: OpportunitySource = Field(..., description="Platform to search")
    query: str = Field(..., description="Search query string")
    keywords: List[str] = Field(default_factory=list, description="Keywords to look for")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "platform": "twitter",
                "query": "#journorequest artificial intelligence",
                "keywords": ["AI", "product management", "artificial intelligence"]
            }
        }
    )


class OpportunityFilter(BaseModel):
    """Model for filtering opportunities"""
    min_relevance_score: float = Field(default=0.0, description="Minimum relevance score")
    tiers: List[PublicationTier] = Field(default_factory=list, description="Filter by tiers")
    urgency_levels: List[Urgency] = Field(default_factory=list, description="Filter by urgency")
    sources: List[OpportunitySource] = Field(default_factory=list, description="Filter by sources")
    keywords: List[str] = Field(default_factory=list, description="Keywords to filter by")
    only_not_pitched: bool = Field(default=False, description="Only show opportunities not yet pitched")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "min_relevance_score": 70.0,
                "tiers": ["tier_1", "tier_2"],
                "urgency_levels": ["high", "medium"],
                "only_not_pitched": True
            }
        }
    )


class PitchTemplate(BaseModel):
    """Model for personalized pitch templates"""
    opportunity_id: str = Field(..., description="ID of the opportunity")
    subject_line: str = Field(..., description="Email subject line")
    greeting: str = Field(..., description="Email greeting")
    body: str = Field(..., description="Main pitch body")
    closing: str = Field(..., description="Email closing")
    full_pitch: str = Field(..., description="Complete assembled pitch")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "opportunity_id": "opp_123",
                "subject_line": "AI PM Expert Available for TechCrunch Article",
                "greeting": "Hi John,",
                "body": "I saw your call for AI product management experts...",
                "closing": "Best regards,\nYour Name",
                "full_pitch": "Hi John,\n\nI saw your call for AI product management experts..."
            }
        }
    )


class DailyDigest(BaseModel):
    """Model for daily opportunity digest"""
    date: datetime = Field(default_factory=datetime.now, description="Digest date")
    total_opportunities: int = Field(..., description="Total opportunities found")
    high_priority: List[JournalistOpportunity] = Field(default_factory=list, description="High priority opportunities")
    medium_priority: List[JournalistOpportunity] = Field(default_factory=list, description="Medium priority opportunities")
    low_priority: List[JournalistOpportunity] = Field(default_factory=list, description="Low priority opportunities")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "date": "2025-11-14T00:00:00",
                "total_opportunities": 15,
                "high_priority": [],
                "medium_priority": [],
                "low_priority": []
            }
        }
    )


class UserProfile(BaseModel):
    """Model for user profile/background for pitch personalization"""
    name: str = Field(..., description="User's name")
    title: str = Field(..., description="Professional title")
    expertise_areas: List[str] = Field(default_factory=list, description="Areas of expertise")
    experience_years: int = Field(..., description="Years of experience")
    company: Optional[str] = Field(None, description="Current company")
    bio: str = Field(..., description="Professional bio")
    achievements: List[str] = Field(default_factory=list, description="Key achievements")
    contact_info: Dict[str, str] = Field(default_factory=dict, description="Contact information")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Jane Smith",
                "title": "AI Product Manager",
                "expertise_areas": ["artificial intelligence", "product management", "machine learning"],
                "experience_years": 8,
                "company": "TechCorp",
                "bio": "AI PM with 8 years of experience...",
                "achievements": ["Led AI product launch", "Grew user base by 200%"],
                "contact_info": {"email": "jane@example.com", "linkedin": "linkedin.com/in/janesmith"}
            }
        }
    )
