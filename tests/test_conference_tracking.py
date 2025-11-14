"""
Tests for conference tracking functionality
"""
import pytest
import os
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

from brand_manager.conference_models import (
    Conference, ConferenceSearchFilters, LocationType, TopicFocus,
    ConferenceSummaryReport
)
from brand_manager.conference_db import ConferenceDatabase
from brand_manager.conference_scrapers import (
    ConferenceScraper, ManualConferenceScraper, ConferenceAggregator
)
from brand_manager.conference_scorer import ConferenceScorer
from brand_manager.conference_exporter import ConferenceExporter
from brand_manager.conference_scheduler import ConferenceScheduler


class TestConferenceModels:
    """Test conference data models"""
    
    def test_conference_creation(self):
        """Test creating a conference"""
        conf = Conference(
            name="Test Conference",
            start_date=datetime(2024, 12, 1, 9, 0),
            end_date=datetime(2024, 12, 1, 18, 0),
            location="Virtual",
            location_type=LocationType.VIRTUAL,
            url="https://test.com",
            source="Test"
        )
        assert conf.name == "Test Conference"
        assert conf.location_type == LocationType.VIRTUAL
        assert conf.overall_score == 0.0
    
    def test_conference_with_optional_fields(self):
        """Test conference with optional fields"""
        conf = Conference(
            name="Test Conference",
            start_date=datetime(2024, 12, 1, 9, 0),
            end_date=datetime(2024, 12, 1, 18, 0),
            location="San Francisco, CA",
            location_type=LocationType.IN_PERSON,
            ticket_price_min=299.0,
            ticket_price_max=799.0,
            notable_speakers=["Speaker 1", "Speaker 2"],
            agenda_topics=["AI", "Product Management"],
            url="https://test.com",
            source="Test",
            topic_focus=[TopicFocus.AI_ML, TopicFocus.GENERAL_PM]
        )
        assert len(conf.notable_speakers) == 2
        assert len(conf.topic_focus) == 2
        assert conf.ticket_price_min == 299.0
    
    def test_search_filters(self):
        """Test search filters creation"""
        filters = ConferenceSearchFilters(
            start_date_from=datetime(2024, 1, 1),
            location_type=LocationType.VIRTUAL,
            min_score=7.0
        )
        assert filters.location_type == LocationType.VIRTUAL
        assert filters.min_score == 7.0


class TestConferenceDatabase:
    """Test conference database operations"""
    
    @pytest.fixture
    def temp_db(self):
        """Create a temporary database"""
        fd, path = tempfile.mkstemp(suffix='.db')
        os.close(fd)
        yield path
        if os.path.exists(path):
            os.remove(path)
    
    @pytest.fixture
    def sample_conference(self):
        """Create a sample conference"""
        return Conference(
            name="Test Conference",
            start_date=datetime(2024, 12, 1, 9, 0),
            end_date=datetime(2024, 12, 1, 18, 0),
            location="Virtual",
            location_type=LocationType.VIRTUAL,
            ticket_price_min=0.0,
            ticket_price_max=99.0,
            notable_speakers=["Speaker 1"],
            agenda_topics=["AI", "Product Management"],
            url="https://test.com/conf1",
            source="Test",
            topic_focus=[TopicFocus.AI_ML],
            overall_score=8.5
        )
    
    def test_add_conference(self, temp_db, sample_conference):
        """Test adding a conference to database"""
        with ConferenceDatabase(temp_db) as db:
            conf_id = db.add_conference(sample_conference)
            assert conf_id > 0
    
    def test_get_conference_by_id(self, temp_db, sample_conference):
        """Test retrieving a conference by ID"""
        with ConferenceDatabase(temp_db) as db:
            conf_id = db.add_conference(sample_conference)
            retrieved = db.get_conference_by_id(conf_id)
            
            assert retrieved is not None
            assert retrieved.name == sample_conference.name
            assert retrieved.url == sample_conference.url
    
    def test_search_conferences(self, temp_db, sample_conference):
        """Test searching conferences with filters"""
        with ConferenceDatabase(temp_db) as db:
            db.add_conference(sample_conference)
            
            # Search by location type
            filters = ConferenceSearchFilters(location_type=LocationType.VIRTUAL)
            results = db.search_conferences(filters)
            assert len(results) == 1
            
            # Search by score
            filters = ConferenceSearchFilters(min_score=8.0)
            results = db.search_conferences(filters)
            assert len(results) == 1
            
            # Search with no matches
            filters = ConferenceSearchFilters(min_score=9.0)
            results = db.search_conferences(filters)
            assert len(results) == 0
    
    def test_update_conference_by_url(self, temp_db, sample_conference):
        """Test updating an existing conference"""
        with ConferenceDatabase(temp_db) as db:
            # Add conference
            conf_id = db.add_conference(sample_conference)
            
            # Update conference with same URL
            sample_conference.name = "Updated Conference Name"
            updated_id = db.add_conference(sample_conference)
            
            # Should return same ID
            assert updated_id == conf_id
            
            # Verify update
            retrieved = db.get_conference_by_id(conf_id)
            assert retrieved.name == "Updated Conference Name"


class TestConferenceScrapers:
    """Test conference scrapers"""
    
    def test_manual_scraper(self):
        """Test manual conference scraper"""
        scraper = ManualConferenceScraper()
        conferences = scraper.scrape_conferences()
        
        assert len(conferences) > 0
        assert all(isinstance(conf, Conference) for conf in conferences)
        assert all(conf.url for conf in conferences)
    
    def test_conference_aggregator(self):
        """Test conference aggregator"""
        aggregator = ConferenceAggregator()
        conferences = aggregator.aggregate_conferences()
        
        assert len(conferences) > 0
        assert all(isinstance(conf, Conference) for conf in conferences)


class TestConferenceScorer:
    """Test conference scoring"""
    
    @pytest.fixture
    def scorer(self):
        """Create a scorer instance"""
        return ConferenceScorer()
    
    @pytest.fixture
    def ai_conference(self):
        """Create an AI-focused conference"""
        return Conference(
            name="AI Product Summit",
            start_date=datetime(2024, 12, 1, 9, 0),
            end_date=datetime(2024, 12, 2, 18, 0),
            location="New York, NY",
            location_type=LocationType.IN_PERSON,
            ticket_price_min=499.0,
            ticket_price_max=999.0,
            notable_speakers=[
                "VP of Product at Google",
                "Chief Product Officer at OpenAI",
                "Director of AI at Meta"
            ],
            agenda_topics=[
                "AI Product Management",
                "Machine Learning Integration",
                "Generative AI Applications"
            ],
            url="https://aiproduct.com",
            source="Test",
            topic_focus=[TopicFocus.AI_ML],
            description="Conference focused on AI and ML product management"
        )
    
    def test_score_conference(self, scorer, ai_conference):
        """Test scoring a conference"""
        scored = scorer.score_conference(ai_conference)
        
        assert scored.overall_score > 0
        assert scored.relevance_score > 0
        assert scored.speaker_quality_score > 0
        assert scored.networking_score > 0
        assert 0 <= scored.overall_score <= 10
    
    def test_ai_relevance_scoring(self, scorer, ai_conference):
        """Test AI relevance scoring"""
        scored = scorer.score_conference(ai_conference)
        
        # AI-focused conference should have high relevance score
        assert scored.relevance_score >= 7.0
    
    def test_speaker_quality_scoring(self, scorer, ai_conference):
        """Test speaker quality scoring"""
        scored = scorer.score_conference(ai_conference)
        
        # Conference with quality speakers should have good score
        assert scored.speaker_quality_score > 5.0
    
    def test_networking_scoring(self, scorer, ai_conference):
        """Test networking score"""
        scored = scorer.score_conference(ai_conference)
        
        # In-person multi-day conference should have good networking score
        assert scored.networking_score > 5.0
    
    def test_rank_conferences(self, scorer):
        """Test ranking multiple conferences"""
        conferences = ManualConferenceScraper().scrape_conferences()
        ranked = scorer.rank_conferences(conferences)
        
        # Check that conferences are sorted by score
        for i in range(len(ranked) - 1):
            assert ranked[i].overall_score >= ranked[i + 1].overall_score


class TestConferenceExporter:
    """Test conference export and reporting"""
    
    @pytest.fixture
    def exporter(self):
        """Create an exporter instance"""
        return ConferenceExporter()
    
    @pytest.fixture
    def sample_conferences(self):
        """Create sample conferences"""
        scorer = ConferenceScorer()
        conferences = ManualConferenceScraper().scrape_conferences()
        return [scorer.score_conference(conf) for conf in conferences[:3]]
    
    def test_export_to_csv(self, exporter, sample_conferences):
        """Test CSV export"""
        fd, csv_path = tempfile.mkstemp(suffix='.csv')
        os.close(fd)
        
        try:
            exporter.export_to_csv(sample_conferences, csv_path)
            
            # Verify file exists and has content
            assert os.path.exists(csv_path)
            with open(csv_path, 'r') as f:
                lines = f.readlines()
                assert len(lines) > 1  # Header + at least one conference
                assert 'Name' in lines[0]  # Check header
        finally:
            if os.path.exists(csv_path):
                os.remove(csv_path)
    
    def test_generate_summary_report(self, exporter, sample_conferences):
        """Test summary report generation"""
        report = exporter.generate_summary_report(sample_conferences)
        
        assert isinstance(report, ConferenceSummaryReport)
        assert report.total_conferences == len(sample_conferences)
        assert len(report.top_conferences) > 0
        assert len(report.recommendations) > 0
        assert 'total' in report.statistics
    
    def test_save_text_report(self, exporter, sample_conferences):
        """Test saving text report"""
        fd, report_path = tempfile.mkstemp(suffix='.txt')
        os.close(fd)
        
        try:
            report = exporter.generate_summary_report(sample_conferences)
            exporter.save_text_report(report, report_path)
            
            # Verify file exists and has content
            assert os.path.exists(report_path)
            with open(report_path, 'r') as f:
                content = f.read()
                assert 'CONFERENCE RESEARCH SUMMARY REPORT' in content
                assert 'RECOMMENDATIONS' in content
        finally:
            if os.path.exists(report_path):
                os.remove(report_path)


class TestConferenceScheduler:
    """Test conference scheduling"""
    
    @pytest.fixture
    def temp_config(self):
        """Create temporary config file"""
        fd, path = tempfile.mkstemp(suffix='.json')
        os.close(fd)
        yield path
        if os.path.exists(path):
            os.remove(path)
    
    def test_scheduler_initialization(self, temp_config):
        """Test scheduler initialization"""
        scheduler = ConferenceScheduler(temp_config)
        assert scheduler.config is not None
        assert scheduler.config.enabled == False
    
    def test_set_schedule(self, temp_config):
        """Test setting up a schedule"""
        scheduler = ConferenceScheduler(temp_config)
        
        filters = ConferenceSearchFilters(
            location_type=LocationType.VIRTUAL,
            min_score=7.0
        )
        
        scheduler.set_schedule('weekly', filters)
        
        assert scheduler.config.enabled == True
        assert scheduler.config.frequency == 'weekly'
        assert scheduler.config.next_run is not None
    
    def test_enable_disable_schedule(self, temp_config):
        """Test enabling and disabling schedule"""
        scheduler = ConferenceScheduler(temp_config)
        
        scheduler.set_schedule('weekly', ConferenceSearchFilters())
        assert scheduler.config.enabled == True
        
        scheduler.disable_schedule()
        assert scheduler.config.enabled == False
        
        scheduler.enable_schedule()
        assert scheduler.config.enabled == True
    
    def test_get_status(self, temp_config):
        """Test getting scheduler status"""
        scheduler = ConferenceScheduler(temp_config)
        scheduler.set_schedule('monthly', ConferenceSearchFilters())
        
        status = scheduler.get_status()
        
        assert status['enabled'] == True
        assert status['frequency'] == 'monthly'
        assert 'next_run' in status
        assert 'filters' in status
