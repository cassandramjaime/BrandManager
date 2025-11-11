"""
Brand Identity and Configuration Models
"""
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class BrandIdentity(BaseModel):
    """Model representing a brand's identity"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "TechFlow",
                "tagline": "Empowering Innovation",
                "description": "A cutting-edge technology consultancy",
                "values": ["Innovation", "Integrity", "Excellence"],
                "target_audience": "Tech startups and SMBs",
                "voice": "Professional yet approachable",
                "industry": "Technology Consulting",
                "unique_selling_points": ["AI-first approach", "24/7 support"]
            }
        }
    )
    
    name: str = Field(..., description="Brand name")
    tagline: Optional[str] = Field(None, description="Brand tagline or slogan")
    description: Optional[str] = Field(None, description="Brand description")
    values: List[str] = Field(default_factory=list, description="Core brand values")
    target_audience: Optional[str] = Field(None, description="Target audience description")
    voice: Optional[str] = Field(None, description="Brand voice/tone (e.g., professional, casual, friendly)")
    industry: Optional[str] = Field(None, description="Industry or sector")
    unique_selling_points: List[str] = Field(default_factory=list, description="Key differentiators")


class ContentRequest(BaseModel):
    """Model for content generation requests"""
    content_type: str = Field(..., description="Type of content (social_post, blog_title, slogan, etc.)")
    topic: Optional[str] = Field(None, description="Topic or theme for the content")
    platform: Optional[str] = Field(None, description="Platform (twitter, linkedin, instagram, etc.)")
    length: Optional[str] = Field("medium", description="Desired length (short, medium, long)")
    tone: Optional[str] = Field(None, description="Override brand voice for this content")
