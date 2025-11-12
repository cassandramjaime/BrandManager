"""
Content Topic Research Models
"""
from typing import List, Optional, Dict
from pydantic import BaseModel, Field, ConfigDict


class TopicResearchRequest(BaseModel):
    """Model for topic research requests"""
    topic: str = Field(..., description="Topic to research")
    depth: str = Field("standard", description="Research depth: quick, standard, or deep")
    focus_areas: List[str] = Field(
        default_factory=list,
        description="Specific areas to focus on (trends, statistics, key_points, audience_interests, etc.)"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "topic": "AI in healthcare",
                "depth": "standard",
                "focus_areas": ["trends", "statistics", "key_points"]
            }
        }
    )


class TopicResearchResult(BaseModel):
    """Model for topic research results"""
    topic: str = Field(..., description="The researched topic")
    summary: str = Field(..., description="Brief summary of the topic")
    key_points: List[str] = Field(default_factory=list, description="Key points and insights")
    trends: List[str] = Field(default_factory=list, description="Current trends related to the topic")
    statistics: List[str] = Field(default_factory=list, description="Relevant statistics and data points")
    audience_interests: List[str] = Field(default_factory=list, description="What audiences care about regarding this topic")
    content_angles: List[str] = Field(default_factory=list, description="Suggested angles for content creation")
    competitor_insights: List[str] = Field(default_factory=list, description="Analysis of how competitors approach this topic")
    keywords: List[str] = Field(default_factory=list, description="Important keywords and phrases")
