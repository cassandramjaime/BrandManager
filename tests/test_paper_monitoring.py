"""
Tests for ML/AI Research Paper Monitoring functionality
"""
import pytest
import tempfile
import os
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock

from brand_manager.paper_models import (
    Paper, PaperSummary, PaperFilter, SearchQuery,
    PaperSource, TopicCategory, ApplicationArea,
    TechnicalDifficulty, ProductionReadiness
)
from brand_manager.paper_database import PaperDatabase
from brand_manager.paper_summarizer import PaperSummarizer
from brand_manager.digest_generator import DigestGenerator


@pytest.fixture
def temp_db():
    """Create a temporary database for testing"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name
    
    yield db_path
    
    # Cleanup
    if os.path.exists(db_path):
        os.unlink(db_path)


@pytest.fixture
def sample_paper():
    """Create a sample paper for testing"""
    return Paper(
        paper_id="test_001",
        title="Test Paper on LLMs",
        authors=["John Doe", "Jane Smith"],
        abstract="This is a test abstract about large language models.",
        publication_date=datetime.now(),
        source=PaperSource.ARXIV,
        url="https://example.com/paper/001",
        pdf_url="https://example.com/paper/001.pdf",
        citation_count=10,
        categories=["cs.CL", "cs.AI"]
    )


@pytest.fixture
def sample_summary():
    """Create a sample paper summary for testing"""
    return PaperSummary(
        paper_id="test_001",
        concise_summary="This paper presents a novel approach to LLM training.",
        main_contribution="Novel architecture for efficient training.",
        methodology_summary="Uses transformer-based approach with modifications.",
        results_summary="Achieved state-of-the-art results on multiple benchmarks.",
        relevance_to_product="Could reduce training costs significantly.",
        application_area=ApplicationArea.NATURAL_LANGUAGE,
        technical_difficulty=TechnicalDifficulty.ADVANCED,
        production_readiness=ProductionReadiness.EXPERIMENTAL
    )


class TestPaperModels:
    """Test paper data models"""
    
    def test_paper_creation(self, sample_paper):
        """Test creating a paper object"""
        assert sample_paper.paper_id == "test_001"
        assert sample_paper.title == "Test Paper on LLMs"
        assert len(sample_paper.authors) == 2
        assert sample_paper.source == PaperSource.ARXIV
    
    def test_paper_serialization(self, sample_paper):
        """Test paper can be serialized to dict"""
        paper_dict = sample_paper.model_dump()
        assert paper_dict['paper_id'] == "test_001"
        assert paper_dict['title'] == "Test Paper on LLMs"
        assert isinstance(paper_dict, dict)
    
    def test_paper_filter_creation(self):
        """Test creating a paper filter"""
        filter = PaperFilter(
            days_back=30,
            topics=[TopicCategory.LLMS],
            min_citations=10
        )
        assert filter.days_back == 30
        assert TopicCategory.LLMS in filter.topics
        assert filter.min_citations == 10
    
    def test_search_query_creation(self):
        """Test creating a search query"""
        query = SearchQuery(
            query="transformer architecture",
            limit=10,
            offset=0
        )
        assert query.query == "transformer architecture"
        assert query.limit == 10
    
    def test_paper_summary_creation(self, sample_summary):
        """Test creating a paper summary"""
        assert sample_summary.paper_id == "test_001"
        assert sample_summary.application_area == ApplicationArea.NATURAL_LANGUAGE
        assert sample_summary.technical_difficulty == TechnicalDifficulty.ADVANCED


class TestPaperDatabase:
    """Test paper database functionality"""
    
    def test_database_initialization(self, temp_db):
        """Test database initialization creates tables"""
        db = PaperDatabase(temp_db)
        assert os.path.exists(temp_db)
    
    def test_save_paper(self, temp_db, sample_paper):
        """Test saving a paper to database"""
        db = PaperDatabase(temp_db)
        result = db.save_paper(sample_paper)
        assert result is True
        
        # Verify paper was saved
        retrieved = db.get_paper(sample_paper.paper_id)
        assert retrieved is not None
        assert retrieved.paper_id == sample_paper.paper_id
        assert retrieved.title == sample_paper.title
    
    def test_save_duplicate_paper(self, temp_db, sample_paper):
        """Test saving duplicate paper replaces existing"""
        db = PaperDatabase(temp_db)
        db.save_paper(sample_paper)
        
        # Modify and save again
        sample_paper.citation_count = 20
        result = db.save_paper(sample_paper)
        
        # Should still succeed (replace)
        assert result is True
        
        # Verify updated citation count
        retrieved = db.get_paper(sample_paper.paper_id)
        assert retrieved.citation_count == 20
    
    def test_save_summary(self, temp_db, sample_paper, sample_summary):
        """Test saving a paper summary"""
        db = PaperDatabase(temp_db)
        
        # Save paper first
        db.save_paper(sample_paper)
        
        # Save summary
        result = db.save_summary(sample_summary)
        assert result is True
        
        # Retrieve summary
        retrieved = db.get_summary(sample_paper.paper_id)
        assert retrieved is not None
        assert retrieved.paper_id == sample_summary.paper_id
        assert retrieved.concise_summary == sample_summary.concise_summary
    
    def test_get_paper_not_found(self, temp_db):
        """Test getting a non-existent paper"""
        db = PaperDatabase(temp_db)
        paper = db.get_paper("nonexistent")
        assert paper is None
    
    def test_get_recent_papers(self, temp_db):
        """Test getting recent papers"""
        db = PaperDatabase(temp_db)
        
        # Add some papers
        for i in range(5):
            paper = Paper(
                paper_id=f"test_{i:03d}",
                title=f"Test Paper {i}",
                authors=["Test Author"],
                abstract="Test abstract",
                publication_date=datetime.now() - timedelta(days=i),
                source=PaperSource.ARXIV,
                url=f"https://example.com/{i}",
                citation_count=i
            )
            db.save_paper(paper)
        
        # Get recent papers
        recent = db.get_recent_papers(days=7, limit=10)
        assert len(recent) == 5
        
        # Should be ordered by date (newest first)
        assert recent[0].paper_id == "test_000"
    
    def test_get_top_papers(self, temp_db):
        """Test getting top papers by citations"""
        db = PaperDatabase(temp_db)
        
        # Add papers with different citation counts
        for i in range(5):
            paper = Paper(
                paper_id=f"test_{i:03d}",
                title=f"Test Paper {i}",
                authors=["Test Author"],
                abstract="Test abstract",
                publication_date=datetime.now() - timedelta(days=1),
                source=PaperSource.ARXIV,
                url=f"https://example.com/{i}",
                citation_count=i * 10
            )
            db.save_paper(paper)
        
        # Get top papers
        top = db.get_top_papers(days=7, limit=3)
        assert len(top) == 3
        
        # Should be ordered by citations (highest first)
        assert top[0].citation_count == 40
        assert top[1].citation_count == 30
        assert top[2].citation_count == 20
    
    def test_search_papers(self, temp_db):
        """Test full-text search functionality"""
        db = PaperDatabase(temp_db)
        
        # Add papers with different content
        papers_data = [
            ("001", "Transformer Architecture", "Paper about transformers"),
            ("002", "CNN for Vision", "Paper about convolutional networks"),
            ("003", "Transformer for NLP", "Another transformer paper"),
        ]
        
        for paper_id, title, abstract in papers_data:
            paper = Paper(
                paper_id=paper_id,
                title=title,
                authors=["Test Author"],
                abstract=abstract,
                publication_date=datetime.now(),
                source=PaperSource.ARXIV,
                url=f"https://example.com/{paper_id}",
                citation_count=0
            )
            db.save_paper(paper)
        
        # Search for "transformer"
        query = SearchQuery(query="transformer", limit=10)
        results = db.search_papers(query)
        
        # Should find papers with "transformer" in title or abstract
        assert len(results) >= 2
    
    def test_get_stats(self, temp_db, sample_paper):
        """Test getting database statistics"""
        db = PaperDatabase(temp_db)
        
        # Add some papers
        db.save_paper(sample_paper)
        
        stats = db.get_stats()
        assert stats['total_papers'] >= 1
        assert 'papers_by_source' in stats
        assert PaperSource.ARXIV.value in stats['papers_by_source']


class TestPaperSummarizer:
    """Test paper summarization"""
    
    @pytest.fixture
    def mock_openai_client(self):
        """Create a mock OpenAI client"""
        with patch('brand_manager.paper_summarizer.OpenAI') as mock_openai:
            mock_client = MagicMock()
            mock_openai.return_value = mock_client
            
            # Mock the chat completion response
            mock_response = MagicMock()
            mock_choice = MagicMock()
            mock_message = MagicMock()
            
            mock_message.content = """CONCISE SUMMARY:
This paper introduces a novel approach to training large language models more efficiently.
The research demonstrates significant improvements in training time while maintaining model quality.
This has important implications for making LLM development more accessible.

MAIN CONTRIBUTION:
The main contribution is a new optimization algorithm that reduces training time by 40% without sacrificing model performance.

METHODOLOGY:
The authors developed a modified attention mechanism combined with adaptive learning rates. They tested on multiple model sizes.

RESULTS:
The approach achieved 40% faster training on GPT-scale models while maintaining comparable performance on standard benchmarks.

PRODUCT RELEVANCE:
This could significantly reduce the cost of training custom LLMs, making it more feasible for companies to develop specialized models.

APPLICATION AREA: natural_language

TECHNICAL DIFFICULTY: advanced

PRODUCTION READINESS: experimental"""
            
            mock_choice.message = mock_message
            mock_response.choices = [mock_choice]
            
            mock_client.chat.completions.create.return_value = mock_response
            
            yield mock_client
    
    def test_summarizer_initialization_with_key(self, mock_openai_client):
        """Test summarizer initialization with API key"""
        summarizer = PaperSummarizer(api_key="test-key")
        assert summarizer.api_key == "test-key"
    
    def test_summarizer_initialization_without_key(self):
        """Test summarizer initialization without API key raises error"""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="OpenAI API key is required"):
                PaperSummarizer()
    
    def test_summarize_paper(self, mock_openai_client, sample_paper):
        """Test summarizing a paper"""
        summarizer = PaperSummarizer(api_key="test-key")
        
        summary = summarizer.summarize_paper(sample_paper)
        
        assert isinstance(summary, PaperSummary)
        assert summary.paper_id == sample_paper.paper_id
        assert len(summary.concise_summary) > 0
        assert summary.application_area == ApplicationArea.NATURAL_LANGUAGE
        assert summary.technical_difficulty == TechnicalDifficulty.ADVANCED
        assert summary.production_readiness == ProductionReadiness.EXPERIMENTAL
        assert mock_openai_client.chat.completions.create.called


class TestDigestGenerator:
    """Test weekly digest generation"""
    
    def test_generate_weekly_digest(self, temp_db, sample_paper, sample_summary):
        """Test generating a weekly digest"""
        db = PaperDatabase(temp_db)
        
        # Add paper and summary
        db.save_paper(sample_paper)
        db.save_summary(sample_summary)
        
        # Generate digest
        generator = DigestGenerator(db)
        digest = generator.generate_weekly_digest(top_n=10)
        
        assert digest is not None
        assert digest.total_papers_reviewed >= 0
        assert len(digest.top_papers) >= 0
    
    def test_export_to_json(self, temp_db, sample_paper, sample_summary):
        """Test exporting digest to JSON"""
        db = PaperDatabase(temp_db)
        db.save_paper(sample_paper)
        db.save_summary(sample_summary)
        
        generator = DigestGenerator(db)
        digest = generator.generate_weekly_digest(top_n=10)
        
        # Export to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            output_path = f.name
        
        try:
            generator.export_to_json(digest, output_path)
            assert os.path.exists(output_path)
            
            # Verify JSON is valid
            import json
            with open(output_path, 'r') as f:
                data = json.load(f)
                assert 'week_start' in data
                assert 'week_end' in data
                assert 'top_papers' in data
        finally:
            if os.path.exists(output_path):
                os.unlink(output_path)
    
    def test_generate_text_digest(self, temp_db, sample_paper, sample_summary):
        """Test generating text digest"""
        db = PaperDatabase(temp_db)
        db.save_paper(sample_paper)
        db.save_summary(sample_summary)
        
        generator = DigestGenerator(db)
        digest = generator.generate_weekly_digest(top_n=10)
        
        text = generator.generate_text_digest(digest)
        
        assert isinstance(text, str)
        assert len(text) > 0
        assert "WEEKLY ML/AI RESEARCH PAPER DIGEST" in text
    
    def test_generate_email_html(self, temp_db, sample_paper, sample_summary):
        """Test generating HTML email"""
        db = PaperDatabase(temp_db)
        db.save_paper(sample_paper)
        db.save_summary(sample_summary)
        
        generator = DigestGenerator(db)
        digest = generator.generate_weekly_digest(top_n=10)
        
        html = generator.generate_email_html(digest)
        
        assert isinstance(html, str)
        assert len(html) > 0
        assert "<!DOCTYPE html>" in html
        assert "Weekly ML/AI Research Paper Digest" in html
