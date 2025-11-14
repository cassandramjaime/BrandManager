"""
Data models for ML/AI Research Paper Monitoring
"""
from datetime import datetime
from typing import List, Optional, Dict
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


class PaperSource(str, Enum):
    """Source of research paper"""
    ARXIV = "arxiv"
    PAPERS_WITH_CODE = "papers_with_code"
    HUGGING_FACE = "hugging_face"
    GOOGLE_SCHOLAR = "google_scholar"


class TopicCategory(str, Enum):
    """ML/AI topic categories"""
    LLMS = "llms"
    COMPUTER_VISION = "computer_vision"
    REINFORCEMENT_LEARNING = "reinforcement_learning"
    AI_SAFETY = "ai_safety"
    NLP = "nlp"
    GENERATIVE_AI = "generative_ai"
    MULTIMODAL = "multimodal"
    OTHER = "other"


class ApplicationArea(str, Enum):
    """Application areas for research papers"""
    HEALTHCARE = "healthcare"
    FINANCE = "finance"
    EDUCATION = "education"
    ROBOTICS = "robotics"
    AUTONOMOUS_VEHICLES = "autonomous_vehicles"
    NATURAL_LANGUAGE = "natural_language"
    COMPUTER_VISION = "computer_vision"
    GENERAL = "general"


class TechnicalDifficulty(str, Enum):
    """Technical difficulty level"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class ProductionReadiness(str, Enum):
    """Production readiness assessment"""
    THEORETICAL = "theoretical"
    EXPERIMENTAL = "experimental"
    PROTOTYPE = "prototype"
    PRODUCTION_READY = "production_ready"


class PaperFilter(BaseModel):
    """Filter criteria for research papers"""
    days_back: int = Field(30, description="Number of days to look back (30, 60, or 90)")
    topics: List[TopicCategory] = Field(
        default_factory=list,
        description="Topic categories to filter by"
    )
    min_citations: int = Field(0, description="Minimum citation count")
    sources: List[PaperSource] = Field(
        default_factory=list,
        description="Sources to fetch from"
    )
    keywords: List[str] = Field(
        default_factory=list,
        description="Keywords to search for"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "days_back": 30,
                "topics": ["llms", "ai_safety"],
                "min_citations": 10,
                "sources": ["arxiv", "papers_with_code"]
            }
        }
    )


class Paper(BaseModel):
    """Research paper data model"""
    paper_id: str = Field(..., description="Unique identifier for the paper")
    title: str = Field(..., description="Paper title")
    authors: List[str] = Field(..., description="List of authors")
    abstract: str = Field(..., description="Paper abstract")
    publication_date: datetime = Field(..., description="Publication date")
    source: PaperSource = Field(..., description="Source of the paper")
    url: str = Field(..., description="URL to the paper")
    pdf_url: Optional[str] = Field(None, description="URL to PDF version")
    citation_count: int = Field(0, description="Number of citations")
    categories: List[str] = Field(default_factory=list, description="Paper categories/tags")
    
    # Optional fields that may be extracted
    key_findings: Optional[str] = Field(None, description="Key findings from the paper")
    methodology: Optional[str] = Field(None, description="Methodology used")
    practical_applications: Optional[str] = Field(None, description="Practical applications")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "paper_id": "2301.00001",
                "title": "Advances in Large Language Models",
                "authors": ["John Doe", "Jane Smith"],
                "abstract": "This paper presents...",
                "publication_date": "2023-01-01T00:00:00",
                "source": "arxiv",
                "url": "https://arxiv.org/abs/2301.00001",
                "citation_count": 150
            }
        }
    )


class PaperSummary(BaseModel):
    """AI-generated summary of a research paper"""
    paper_id: str = Field(..., description="Reference to the paper")
    concise_summary: str = Field(..., description="2-3 paragraph summary")
    main_contribution: str = Field(..., description="Main contribution of the paper")
    methodology_summary: str = Field(..., description="Summary of methodology")
    results_summary: str = Field(..., description="Summary of key results")
    relevance_to_product: str = Field(..., description="Relevance to product management")
    
    # Categorization
    application_area: ApplicationArea = Field(..., description="Primary application area")
    technical_difficulty: TechnicalDifficulty = Field(..., description="Technical difficulty level")
    production_readiness: ProductionReadiness = Field(..., description="Production readiness")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "paper_id": "2301.00001",
                "concise_summary": "This paper introduces...",
                "main_contribution": "Novel architecture for...",
                "methodology_summary": "The authors used...",
                "results_summary": "Results show...",
                "relevance_to_product": "This could be applied to...",
                "application_area": "natural_language",
                "technical_difficulty": "advanced",
                "production_readiness": "experimental"
            }
        }
    )


class WeeklyDigest(BaseModel):
    """Weekly digest of top papers"""
    week_start: datetime = Field(..., description="Start of the week")
    week_end: datetime = Field(..., description="End of the week")
    top_papers: List[Paper] = Field(..., description="Top 10 papers of the week")
    summaries: Dict[str, PaperSummary] = Field(..., description="Summaries keyed by paper_id")
    total_papers_reviewed: int = Field(..., description="Total papers reviewed this week")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "week_start": "2023-01-01T00:00:00",
                "week_end": "2023-01-07T23:59:59",
                "top_papers": [],
                "summaries": {},
                "total_papers_reviewed": 150
            }
        }
    )


class SearchQuery(BaseModel):
    """Search query for past papers"""
    query: str = Field(..., description="Search query text")
    filters: Optional[PaperFilter] = Field(None, description="Optional filters")
    limit: int = Field(10, description="Maximum number of results")
    offset: int = Field(0, description="Offset for pagination")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "query": "transformer architecture",
                "limit": 10,
                "offset": 0
            }
        }
    )
