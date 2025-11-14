"""
Data models for consumer product trends tracking
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class TrendSource(BaseModel):
    """Model for a data source"""
    name: str = Field(..., description="Name of the source")
    url: Optional[str] = Field(None, description="URL of the source")
    fetched_at: datetime = Field(default_factory=datetime.utcnow, description="When the data was fetched")
    

class ProductTrend(BaseModel):
    """Model for a product or trend"""
    title: str = Field(..., description="Name/title of the product or trend")
    description: str = Field(..., description="Description of the product/trend")
    category: str = Field(..., description="Category (social, fintech, health, productivity, etc.)")
    source: TrendSource = Field(..., description="Where this trend was found")
    key_features: List[str] = Field(default_factory=list, description="Key features or characteristics")
    target_audience: Optional[str] = Field(None, description="Target audience description")
    traction_metrics: Dict[str, Any] = Field(default_factory=dict, description="Metrics like upvotes, comments, funding")
    competitive_landscape: Optional[str] = Field(None, description="Competitive analysis")
    url: Optional[str] = Field(None, description="URL to the product/trend")
    discovered_at: datetime = Field(default_factory=datetime.utcnow, description="When we discovered this trend")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "AI-Powered Health Tracker",
                "description": "Mobile app using AI to track health metrics",
                "category": "health",
                "key_features": ["AI analysis", "Real-time tracking", "Personalized insights"],
                "target_audience": "Health-conscious individuals aged 25-45",
                "traction_metrics": {"upvotes": 250, "comments": 45}
            }
        }
    )


class StartupInfo(BaseModel):
    """Model for startup information"""
    name: str = Field(..., description="Startup name")
    description: str = Field(..., description="What the startup does")
    category: str = Field(..., description="Industry category")
    funding_amount: Optional[float] = Field(None, description="Funding amount if available")
    funding_stage: Optional[str] = Field(None, description="Funding stage (seed, series A, etc.)")
    founded_date: Optional[datetime] = Field(None, description="When the startup was founded")
    url: Optional[str] = Field(None, description="Startup URL")
    source: TrendSource = Field(..., description="Where we found this info")
    discovered_at: datetime = Field(default_factory=datetime.utcnow, description="When we discovered this")


class GoogleTrendData(BaseModel):
    """Model for Google Trends data"""
    keyword: str = Field(..., description="Search keyword")
    interest_over_time: List[Dict[str, Any]] = Field(default_factory=list, description="Interest data points")
    related_queries: List[str] = Field(default_factory=list, description="Related search queries")
    category: str = Field(..., description="Category this keyword belongs to")
    fetched_at: datetime = Field(default_factory=datetime.utcnow, description="When the data was fetched")


class TrendAnalysis(BaseModel):
    """Model for LLM-generated trend analysis"""
    common_patterns: List[str] = Field(default_factory=list, description="Common patterns identified")
    emerging_categories: List[str] = Field(default_factory=list, description="New categories emerging")
    opportunities: List[str] = Field(default_factory=list, description="Potential opportunities identified")
    technologies: List[str] = Field(default_factory=list, description="Technologies being adopted")
    summary: str = Field(..., description="Overall analysis summary")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="When analysis was generated")


class TrendItem(BaseModel):
    """Model for a single trend item in the weekly report"""
    rank: int = Field(..., description="Ranking in top trends")
    title: str = Field(..., description="Trend title")
    description: str = Field(..., description="Trend description")
    category: str = Field(..., description="Category")
    traction_score: float = Field(..., description="Combined traction score")
    why_trending: str = Field(..., description="Analysis of why it's trending")
    sources: List[str] = Field(default_factory=list, description="Where we saw this trend")


class WeeklyTrendReport(BaseModel):
    """Model for weekly trend report"""
    report_id: str = Field(..., description="Unique report identifier")
    week_start: datetime = Field(..., description="Start of the week")
    week_end: datetime = Field(..., description="End of the week")
    top_trends: List[TrendItem] = Field(default_factory=list, description="Top 10 trends")
    category_breakdown: Dict[str, int] = Field(default_factory=dict, description="Count by category")
    analysis: TrendAnalysis = Field(..., description="Overall trend analysis")
    total_items_analyzed: int = Field(0, description="Total items processed")
    categories_tracked: List[str] = Field(default_factory=list, description="Categories being tracked")
    generated_at: datetime = Field(default_factory=datetime.utcnow, description="When report was generated")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "report_id": "2025-W01",
                "week_start": "2025-01-01T00:00:00",
                "week_end": "2025-01-07T23:59:59",
                "top_trends": [],
                "category_breakdown": {"health": 15, "fintech": 10, "social": 8}
            }
        }
    )


class TrackedCategories(BaseModel):
    """Model for categories configuration"""
    categories: List[str] = Field(
        default_factory=lambda: ["social", "fintech", "health", "productivity", "education", "ecommerce"],
        description="List of categories to track"
    )
    custom_keywords: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Custom keywords for each category"
    )
