"""
Data models for conference tracking
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from enum import Enum


class LocationType(str, Enum):
    """Conference location types"""
    VIRTUAL = "virtual"
    IN_PERSON = "in-person"
    HYBRID = "hybrid"


class TopicFocus(str, Enum):
    """Conference topic focus areas"""
    AI_ML = "AI/ML"
    CONSUMER_PRODUCTS = "consumer products"
    GENERAL_PM = "general PM"
    ENTERPRISE = "enterprise"
    B2B = "B2B"
    B2C = "B2C"
    MOBILE = "mobile"
    WEB = "web"
    DATA = "data"
    DESIGN = "design"


class Conference(BaseModel):
    """Model for a conference"""
    id: Optional[int] = None
    name: str = Field(..., description="Conference name")
    start_date: datetime = Field(..., description="Conference start date")
    end_date: datetime = Field(..., description="Conference end date")
    location: str = Field(..., description="Conference location (city/country or 'Virtual')")
    location_type: LocationType = Field(..., description="Type of conference (virtual/in-person/hybrid)")
    ticket_price_min: Optional[float] = Field(None, description="Minimum ticket price in USD")
    ticket_price_max: Optional[float] = Field(None, description="Maximum ticket price in USD")
    notable_speakers: List[str] = Field(default_factory=list, description="List of notable speakers")
    agenda_topics: List[str] = Field(default_factory=list, description="Main agenda topics")
    registration_deadline: Optional[datetime] = Field(None, description="Registration deadline")
    url: str = Field(..., description="Conference website URL")
    source: str = Field(..., description="Data source (e.g., 'Eventbrite', 'Luma', 'ProductCon')")
    description: Optional[str] = Field(None, description="Conference description")
    topic_focus: List[TopicFocus] = Field(default_factory=list, description="Primary topic focus areas")
    
    # Scoring fields
    relevance_score: float = Field(0.0, description="AI product management relevance score (0-10)")
    speaker_quality_score: float = Field(0.0, description="Speaker quality score (0-10)")
    networking_score: float = Field(0.0, description="Networking opportunities score (0-10)")
    overall_score: float = Field(0.0, description="Overall score (0-10)")
    
    # Metadata
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "ProductCon 2024",
                "start_date": "2024-12-15T09:00:00",
                "end_date": "2024-12-16T18:00:00",
                "location": "San Francisco, CA",
                "location_type": "in-person",
                "ticket_price_min": 299.0,
                "ticket_price_max": 599.0,
                "notable_speakers": ["Jane Smith - VP Product at Google", "John Doe - CPO at Meta"],
                "agenda_topics": ["AI in Product Management", "Product Strategy", "User Research"],
                "registration_deadline": "2024-12-01T23:59:59",
                "url": "https://productcon.com/2024",
                "source": "ProductCon",
                "topic_focus": ["AI/ML", "general PM"]
            }
        }
    )


class ConferenceSearchFilters(BaseModel):
    """Search filters for conferences"""
    start_date_from: Optional[datetime] = Field(None, description="Filter conferences starting from this date")
    start_date_to: Optional[datetime] = Field(None, description="Filter conferences starting before this date")
    location_type: Optional[LocationType] = Field(None, description="Filter by location type")
    topic_focus: List[TopicFocus] = Field(default_factory=list, description="Filter by topic focus")
    min_score: Optional[float] = Field(None, description="Minimum overall score")
    max_price: Optional[float] = Field(None, description="Maximum ticket price")
    location_keywords: List[str] = Field(default_factory=list, description="Location keywords (e.g., 'San Francisco', 'Europe')")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "start_date_from": "2024-01-01T00:00:00",
                "start_date_to": "2024-12-31T23:59:59",
                "location_type": "virtual",
                "topic_focus": ["AI/ML"],
                "min_score": 7.0,
                "max_price": 500.0
            }
        }
    )


class ConferenceSummaryReport(BaseModel):
    """Summary report for conferences"""
    total_conferences: int = Field(..., description="Total number of conferences found")
    date_range: str = Field(..., description="Date range of conferences")
    top_conferences: List[Conference] = Field(..., description="Top rated conferences")
    recommendations: List[str] = Field(..., description="Recommendations based on search criteria")
    statistics: Dict[str, Any] = Field(default_factory=dict, description="Statistics about conferences")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_conferences": 25,
                "date_range": "Jan 2024 - Dec 2024",
                "top_conferences": [],
                "recommendations": [
                    "ProductCon 2024 is highly recommended for AI product management focus",
                    "Mind the Product offers excellent networking opportunities"
                ],
                "statistics": {
                    "avg_price": 450.0,
                    "virtual_count": 10,
                    "in_person_count": 15
                }
            }
        }
    )


class ScheduleConfig(BaseModel):
    """Configuration for scheduled searches"""
    frequency: str = Field(..., description="Frequency: 'weekly' or 'monthly'")
    filters: ConferenceSearchFilters = Field(..., description="Search filters to apply")
    email_recipients: List[str] = Field(default_factory=list, description="Email recipients for reports")
    enabled: bool = Field(True, description="Whether the schedule is enabled")
    last_run: Optional[datetime] = Field(None, description="Last time the search was run")
    next_run: Optional[datetime] = Field(None, description="Next scheduled run time")
