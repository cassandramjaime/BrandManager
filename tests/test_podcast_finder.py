"""
Tests for Podcast Guest Opportunity Finder
"""
import pytest
import tempfile
import os
from datetime import datetime
from pathlib import Path

from brand_manager.podcast_models import (
    PodcastOpportunity, 
    ApplicationStatus, 
    PodcastSearchRequest
)
from brand_manager.podcast_database import PodcastDatabase
from brand_manager.podcast_scorer import PodcastScorer
from brand_manager.podcast_searcher import PodcastSearcher
from brand_manager.podcast_exporter import PodcastExporter


class TestPodcastModels:
    """Test podcast models"""
    
    def test_podcast_opportunity_creation(self):
        """Test creating a podcast opportunity"""
        opp = PodcastOpportunity(
            podcast_name="Test Podcast",
            host_name="Test Host",
            audience_size=10000,
            relevance_score=85.0,
            total_score=80.0
        )
        
        assert opp.podcast_name == "Test Podcast"
        assert opp.host_name == "Test Host"
        assert opp.audience_size == 10000
        assert opp.application_status == ApplicationStatus.NOT_APPLIED
    
    def test_application_status_enum(self):
        """Test application status enum values"""
        assert ApplicationStatus.NOT_APPLIED.value == "not_applied"
        assert ApplicationStatus.APPLIED.value == "applied"
        assert ApplicationStatus.SCHEDULED.value == "scheduled"
    
    def test_search_request_defaults(self):
        """Test search request with defaults"""
        request = PodcastSearchRequest()
        
        assert "product manager" in request.keywords
        assert "AI" in request.keywords
        assert request.max_results == 50
        assert request.days_back == 30


class TestPodcastScorer:
    """Test podcast scoring functionality"""
    
    def setup_method(self):
        """Setup for each test"""
        self.scorer = PodcastScorer()
    
    def test_relevance_score_high(self):
        """Test high relevance score for AI/PM podcast"""
        score = self.scorer.calculate_relevance_score(
            "AI Product Management Podcast",
            "Discussion about product management and artificial intelligence",
            "Product managers working in AI/ML"
        )
        
        assert score >= 70.0
        assert score <= 100.0
    
    def test_relevance_score_low(self):
        """Test low relevance score for unrelated podcast"""
        score = self.scorer.calculate_relevance_score(
            "Cooking Show",
            "Recipes and cooking tips",
            "Chefs and food enthusiasts"
        )
        
        assert score < 30.0
    
    def test_audience_score_large(self):
        """Test audience score for large podcast"""
        score = self.scorer.calculate_audience_score(100000)
        assert score == 100.0
    
    def test_audience_score_medium(self):
        """Test audience score for medium podcast"""
        score = self.scorer.calculate_audience_score(10000)
        assert score == 70.0
    
    def test_audience_score_unknown(self):
        """Test audience score for unknown size"""
        score = self.scorer.calculate_audience_score(None)
        assert score == 10.0
    
    def test_engagement_score(self):
        """Test engagement score calculation"""
        score = self.scorer.calculate_engagement_score(
            has_submission_form=True,
            has_contact=True,
            has_description=True,
            source_credibility="podmatch"
        )
        
        assert score >= 80.0
    
    def test_total_score_calculation(self):
        """Test total score calculation"""
        total = self.scorer.calculate_total_score(
            relevance_score=80.0,
            audience_score=70.0,
            engagement_score=60.0
        )
        
        # Default weights: 50% relevance, 30% audience, 20% engagement
        expected = 80.0 * 0.5 + 70.0 * 0.3 + 60.0 * 0.2
        assert total == pytest.approx(expected, 0.01)
    
    def test_fit_reason_generation(self):
        """Test fit reason generation"""
        reason = self.scorer.generate_fit_reason(
            podcast_name="AI PM Podcast",
            relevance_score=85.0,
            audience_score=80.0,
            description="Product management in AI"
        )
        
        assert len(reason) > 0
        assert isinstance(reason, str)


class TestPodcastDatabase:
    """Test database functionality"""
    
    def setup_method(self):
        """Setup for each test"""
        # Create temporary database for testing
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db = PodcastDatabase(self.temp_db.name)
    
    def teardown_method(self):
        """Cleanup after each test"""
        # Remove temporary database
        if os.path.exists(self.temp_db.name):
            os.unlink(self.temp_db.name)
    
    def test_add_opportunity(self):
        """Test adding an opportunity to database"""
        opp = PodcastOpportunity(
            podcast_name="Test Podcast",
            host_name="Test Host",
            audience_size=5000,
            relevance_score=75.0,
            total_score=70.0
        )
        
        opp_id = self.db.add_opportunity(opp)
        assert opp_id > 0
    
    def test_get_opportunity(self):
        """Test retrieving an opportunity from database"""
        opp = PodcastOpportunity(
            podcast_name="Test Podcast",
            host_name="Test Host",
            audience_size=5000
        )
        
        opp_id = self.db.add_opportunity(opp)
        retrieved = self.db.get_opportunity(opp_id)
        
        assert retrieved is not None
        assert retrieved.podcast_name == "Test Podcast"
        assert retrieved.host_name == "Test Host"
    
    def test_get_all_opportunities(self):
        """Test retrieving all opportunities"""
        # Add multiple opportunities
        for i in range(3):
            opp = PodcastOpportunity(
                podcast_name=f"Podcast {i}",
                total_score=50.0 + i * 10
            )
            self.db.add_opportunity(opp)
        
        all_opps = self.db.get_all_opportunities()
        assert len(all_opps) == 3
        # Should be sorted by total_score descending
        assert all_opps[0].total_score >= all_opps[1].total_score
    
    def test_update_status(self):
        """Test updating opportunity status"""
        opp = PodcastOpportunity(
            podcast_name="Test Podcast",
            application_status=ApplicationStatus.NOT_APPLIED
        )
        
        opp_id = self.db.add_opportunity(opp)
        self.db.update_status(opp_id, ApplicationStatus.APPLIED, "Sent email")
        
        updated = self.db.get_opportunity(opp_id)
        assert updated.application_status == ApplicationStatus.APPLIED
        assert updated.notes == "Sent email"
    
    def test_filter_by_status(self):
        """Test filtering opportunities by status"""
        # Add opportunities with different statuses
        opp1 = PodcastOpportunity(
            podcast_name="Podcast 1",
            application_status=ApplicationStatus.NOT_APPLIED
        )
        opp2 = PodcastOpportunity(
            podcast_name="Podcast 2",
            application_status=ApplicationStatus.APPLIED
        )
        
        self.db.add_opportunity(opp1)
        self.db.add_opportunity(opp2)
        
        not_applied = self.db.get_all_opportunities(status=ApplicationStatus.NOT_APPLIED)
        assert len(not_applied) == 1
        assert not_applied[0].podcast_name == "Podcast 1"
    
    def test_search_opportunities(self):
        """Test searching opportunities"""
        opp1 = PodcastOpportunity(podcast_name="AI Product Podcast")
        opp2 = PodcastOpportunity(podcast_name="Marketing Show")
        
        self.db.add_opportunity(opp1)
        self.db.add_opportunity(opp2)
        
        results = self.db.search_opportunities("Product")
        assert len(results) == 1
        assert results[0].podcast_name == "AI Product Podcast"
    
    def test_get_statistics(self):
        """Test getting database statistics"""
        # Add some opportunities
        for i in range(5):
            opp = PodcastOpportunity(
                podcast_name=f"Podcast {i}",
                relevance_score=70.0,
                total_score=65.0
            )
            self.db.add_opportunity(opp)
        
        stats = self.db.get_statistics()
        assert stats['total'] == 5
        assert stats['avg_total_score'] > 0


class TestPodcastSearcher:
    """Test podcast searcher functionality"""
    
    def setup_method(self):
        """Setup for each test"""
        self.searcher = PodcastSearcher()
    
    def test_manual_opportunity_creation(self):
        """Test manually creating an opportunity"""
        opp = self.searcher.add_manual_opportunity(
            podcast_name="Product Management Podcast",
            host_name="PM Expert",
            show_description="Product management and AI discussions",
            audience_size=15000
        )
        
        assert opp.podcast_name == "Product Management Podcast"
        assert opp.total_score > 0
        assert opp.relevance_score > 0
        assert opp.fit_reason is not None
    
    def test_search_returns_result(self):
        """Test that search returns a result object"""
        request = PodcastSearchRequest(
            keywords=["AI", "product"],
            sources=["twitter"]
        )
        
        result = self.searcher.search(request)
        
        assert result is not None
        assert hasattr(result, 'opportunities')
        assert hasattr(result, 'total_found')


class TestPodcastExporter:
    """Test export functionality"""
    
    def setup_method(self):
        """Setup for each test"""
        self.exporter = PodcastExporter()
        self.temp_dir = tempfile.mkdtemp()
    
    def teardown_method(self):
        """Cleanup after each test"""
        # Clean up temp directory
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_export_to_csv(self):
        """Test exporting to CSV"""
        opportunities = [
            PodcastOpportunity(
                podcast_name="Test Podcast 1",
                host_name="Host 1",
                audience_size=10000,
                total_score=85.0
            ),
            PodcastOpportunity(
                podcast_name="Test Podcast 2",
                host_name="Host 2",
                audience_size=5000,
                total_score=75.0
            )
        ]
        
        csv_path = os.path.join(self.temp_dir, "test.csv")
        self.exporter.export_to_csv(opportunities, csv_path)
        
        assert os.path.exists(csv_path)
        
        # Verify CSV content
        with open(csv_path, 'r') as f:
            content = f.read()
            assert "Test Podcast 1" in content
            assert "Host 1" in content
    
    def test_export_to_markdown(self):
        """Test exporting to Markdown"""
        opportunities = [
            PodcastOpportunity(
                podcast_name="Test Podcast",
                host_name="Host",
                total_score=80.0
            )
        ]
        
        md_path = os.path.join(self.temp_dir, "test.md")
        self.exporter.export_to_markdown(opportunities, md_path)
        
        assert os.path.exists(md_path)
        
        # Verify Markdown content
        with open(md_path, 'r') as f:
            content = f.read()
            assert "Test Podcast" in content
            assert "# Podcast Guest Opportunities" in content
    
    def test_create_quick_summary(self):
        """Test creating a quick summary"""
        opportunities = [
            PodcastOpportunity(
                podcast_name="Podcast 1",
                total_score=90.0,
                fit_reason="Great fit"
            ),
            PodcastOpportunity(
                podcast_name="Podcast 2",
                total_score=80.0
            )
        ]
        
        summary = self.exporter.create_quick_summary(opportunities, top_n=2)
        
        assert "Podcast 1" in summary
        assert "90.0" in summary
        assert len(summary) > 0
    
    def test_export_empty_list_raises_error(self):
        """Test that exporting empty list raises error"""
        with pytest.raises(ValueError):
            self.exporter.export_to_csv([], "test.csv")
