"""
Models for Podcast Guest Opportunity Finder
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum


class ApplicationStatus(str, Enum):
    """Status of podcast application"""
    NOT_APPLIED = "not_applied"
    APPLIED = "applied"
    RESPONDED = "responded"
    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    REJECTED = "rejected"


class PodcastOpportunity(BaseModel):
    """Model for a podcast guest opportunity"""
    id: Optional[int] = None
    podcast_name: str = Field(..., description="Name of the podcast")
    host_name: Optional[str] = Field(None, description="Host name or contact person")
    host_contact: Optional[str] = Field(None, description="Contact email or social media")
    show_description: Optional[str] = Field(None, description="Description of the podcast show")
    typical_guest_profile: Optional[str] = Field(None, description="Description of typical guests")
    audience_size: Optional[int] = Field(None, description="Estimated audience size/downloads per episode")
    submission_link: Optional[str] = Field(None, description="Link to guest submission form or application")
    submission_process: Optional[str] = Field(None, description="Description of how to apply")
    source: Optional[str] = Field(None, description="Where this opportunity was found (Twitter, LinkedIn, PodMatch, etc.)")
    source_url: Optional[str] = Field(None, description="URL of the source post/listing")
    
    # Scoring fields
    relevance_score: float = Field(0.0, description="Relevance to AI/ML/PM (0-100)")
    audience_score: float = Field(0.0, description="Score based on audience size (0-100)")
    engagement_score: float = Field(0.0, description="Score based on engagement metrics (0-100)")
    total_score: float = Field(0.0, description="Combined total score (0-100)")
    
    # Metadata
    found_date: datetime = Field(default_factory=datetime.now, description="When this opportunity was found")
    deadline: Optional[datetime] = Field(None, description="Application deadline if specified")
    
    # Application tracking
    application_status: ApplicationStatus = Field(
        ApplicationStatus.NOT_APPLIED, 
        description="Current status of application"
    )
    applied_date: Optional[datetime] = Field(None, description="When application was submitted")
    notes: Optional[str] = Field(None, description="Additional notes about this opportunity")
    
    # Why it's a good fit
    fit_reason: Optional[str] = Field(None, description="Why this podcast is a good fit")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "podcast_name": "Product Thinking Podcast",
                "host_name": "Melissa Perri",
                "host_contact": "podcast@productthinking.com",
                "show_description": "Deep dives into product strategy and leadership",
                "typical_guest_profile": "Product leaders, PMs with 10+ years experience",
                "audience_size": 25000,
                "submission_link": "https://productthinking.com/guest",
                "source": "PodMatch",
                "relevance_score": 95.0,
                "audience_score": 85.0,
                "total_score": 90.0,
                "application_status": "not_applied",
                "fit_reason": "Strong alignment with product management expertise and AI/ML background"
            }
        }
    )


class PodcastSearchRequest(BaseModel):
    """Model for podcast search requests"""
    keywords: List[str] = Field(
        default_factory=lambda: ["product manager", "AI", "machine learning"],
        description="Keywords to search for"
    )
    min_audience_size: Optional[int] = Field(None, description="Minimum audience size")
    min_relevance_score: float = Field(0.0, description="Minimum relevance score (0-100)")
    sources: List[str] = Field(
        default_factory=lambda: ["twitter", "linkedin", "podmatch"],
        description="Sources to search (twitter, linkedin, podmatch, matchmaker, podcastguests)"
    )
    max_results: int = Field(50, description="Maximum number of results to return")
    days_back: int = Field(30, description="How many days back to search")


class PodcastSearchResult(BaseModel):
    """Model for search results"""
    opportunities: List[PodcastOpportunity] = Field(default_factory=list)
    total_found: int = 0
    search_date: datetime = Field(default_factory=datetime.now)
    sources_searched: List[str] = Field(default_factory=list)
