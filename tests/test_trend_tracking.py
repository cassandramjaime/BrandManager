"""
Tests for trend tracking functionality
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
import json

from brand_manager.trend_models import (
    ProductTrend, TrendSource, StartupInfo, GoogleTrendData,
    TrendAnalysis, TrendItem, WeeklyTrendReport, TrackedCategories
)
from brand_manager.data_sources import (
    ProductHuntCollector, TechNewsCollector, HackerNewsCollector,
    RedditCollector, TrendDataAggregator
)
from brand_manager.trend_analyzer import TrendAnalyzer
from brand_manager.storage import TrendStorage
from brand_manager.trend_tracker import TrendTracker


class TestTrendModels:
    """Test trend data models"""
    
    def test_product_trend_creation(self):
        """Test creating a ProductTrend"""
        source = TrendSource(name="Test Source", url="https://example.com")
        
        trend = ProductTrend(
            title="Test Product",
            description="A test product description",
            category="tech",
            source=source,
            key_features=["Feature 1", "Feature 2"],
            traction_metrics={"upvotes": 100}
        )
        
        assert trend.title == "Test Product"
        assert trend.category == "tech"
        assert len(trend.key_features) == 2
        assert trend.traction_metrics["upvotes"] == 100
    
    def test_weekly_report_creation(self):
        """Test creating a WeeklyTrendReport"""
        analysis = TrendAnalysis(
            common_patterns=["Pattern 1"],
            emerging_categories=["Category 1"],
            opportunities=["Opportunity 1"],
            technologies=["Tech 1"],
            summary="Test summary"
        )
        
        trend_item = TrendItem(
            rank=1,
            title="Test Trend",
            description="Description",
            category="tech",
            traction_score=95.5,
            why_trending="Because it's great",
            sources=["Source 1"]
        )
        
        report = WeeklyTrendReport(
            report_id="2025-W01",
            week_start=datetime(2025, 1, 1),
            week_end=datetime(2025, 1, 7),
            top_trends=[trend_item],
            category_breakdown={"tech": 10},
            analysis=analysis,
            total_items_analyzed=50
        )
        
        assert report.report_id == "2025-W01"
        assert len(report.top_trends) == 1
        assert report.total_items_analyzed == 50
    
    def test_tracked_categories(self):
        """Test TrackedCategories model"""
        config = TrackedCategories(
            categories=["tech", "health"],
            custom_keywords={"tech": ["ai", "ml"]}
        )
        
        assert "tech" in config.categories
        assert len(config.custom_keywords["tech"]) == 2


class TestDataCollectors:
    """Test data collection from various sources"""
    
    @patch('feedparser.parse')
    def test_product_hunt_collector(self, mock_parse):
        """Test Product Hunt data collection"""
        # Mock feedparser response
        mock_entry = Mock()
        mock_entry.title = "Test Product"
        mock_entry.summary = "A great product"
        mock_entry.get = Mock(side_effect=lambda key, default='': {
            'link': 'https://example.com',
            'summary': 'A great product'
        }.get(key, default))
        mock_entry.tags = []
        
        mock_feed = Mock()
        mock_feed.entries = [mock_entry]
        mock_parse.return_value = mock_feed
        
        collector = ProductHuntCollector()
        trends = collector.collect_trending(limit=1)
        
        assert len(trends) > 0
        assert trends[0].title == "Test Product"
    
    @patch('requests.Session.get')
    def test_hacker_news_collector(self, mock_get):
        """Test Hacker News data collection"""
        # Mock API responses
        mock_get.return_value.json.side_effect = [
            [12345],  # Top stories
            {  # Story details
                'type': 'story',
                'title': 'Test Story',
                'score': 100,
                'descendants': 50,
                'url': 'https://example.com'
            }
        ]
        
        collector = HackerNewsCollector()
        trends = collector.collect_top_stories(limit=1)
        
        assert len(trends) > 0
        assert trends[0].title == "Test Story"
        assert trends[0].traction_metrics['score'] == 100
    
    def test_reddit_categorization(self):
        """Test Reddit subreddit categorization"""
        collector = RedditCollector()
        
        assert collector._categorize_subreddit('technology') == 'tech'
        assert collector._categorize_subreddit('startups') == 'startups'
        assert collector._categorize_subreddit('unknown') == 'other'


class TestTrendAnalyzer:
    """Test trend analysis functionality"""
    
    @patch('brand_manager.trend_analyzer.OpenAI')
    def test_analyzer_initialization(self, mock_openai):
        """Test analyzer initialization"""
        analyzer = TrendAnalyzer(api_key="test-key")
        assert analyzer.api_key == "test-key"
    
    def test_traction_score_calculation(self):
        """Test traction score calculation"""
        with patch('brand_manager.trend_analyzer.OpenAI'):
            analyzer = TrendAnalyzer(api_key="test-key")
            
            source = TrendSource(name="Product Hunt", url="https://example.com")
            trend = ProductTrend(
                title="Test",
                description="Test",
                category="tech",
                source=source,
                traction_metrics={"score": 100, "upvotes": 50}
            )
            
            score = analyzer._calculate_traction_score(trend)
            assert score > 0
    
    @patch('brand_manager.trend_analyzer.OpenAI')
    def test_analyze_trends(self, mock_openai):
        """Test trend analysis with LLM"""
        # Mock OpenAI response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        
        mock_message.content = """COMMON PATTERNS:
- Pattern 1
- Pattern 2

EMERGING CATEGORIES:
- Category 1

OPPORTUNITIES:
- Opportunity 1

TECHNOLOGIES:
- Tech 1

SUMMARY:
This is a test summary."""
        
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client
        
        analyzer = TrendAnalyzer(api_key="test-key")
        
        source = TrendSource(name="Test", url="https://example.com")
        trends = [
            ProductTrend(
                title="Test 1",
                description="Description 1",
                category="tech",
                source=source
            )
        ]
        
        analysis = analyzer.analyze_trends(trends)
        
        assert isinstance(analysis, TrendAnalysis)
        assert len(analysis.common_patterns) > 0
        assert analysis.summary != ""


class TestTrendStorage:
    """Test trend data storage"""
    
    def test_storage_initialization(self, tmp_path):
        """Test storage directory creation"""
        storage = TrendStorage(storage_dir=str(tmp_path / "test_storage"))
        
        assert storage.trends_dir.exists()
        assert storage.reports_dir.exists()
    
    def test_save_and_load_trends(self, tmp_path):
        """Test saving and loading trends"""
        storage = TrendStorage(storage_dir=str(tmp_path / "test_storage"))
        
        source = TrendSource(name="Test", url="https://example.com")
        trends = [
            ProductTrend(
                title="Test Trend",
                description="Description",
                category="tech",
                source=source
            )
        ]
        
        # Save trends
        saved_path = storage.save_trends(trends)
        assert saved_path is not None
        
        # Load trends
        loaded_trends = storage.load_trends()
        assert len(loaded_trends) > 0
        assert loaded_trends[0].title == "Test Trend"
    
    def test_categories_config(self, tmp_path):
        """Test saving and loading categories config"""
        storage = TrendStorage(storage_dir=str(tmp_path / "test_storage"))
        
        config = TrackedCategories(
            categories=["tech", "health"],
            custom_keywords={"tech": ["ai"]}
        )
        
        # Save config
        saved_path = storage.save_categories_config(config)
        assert saved_path is not None
        
        # Load config
        loaded_config = storage.load_categories_config()
        assert "tech" in loaded_config.categories


class TestTrendTracker:
    """Test main trend tracker orchestrator"""
    
    @patch('brand_manager.trend_tracker.TrendDataAggregator')
    @patch('brand_manager.trend_tracker.TrendAnalyzer')
    def test_tracker_initialization(self, mock_analyzer, mock_aggregator):
        """Test tracker initialization"""
        tracker = TrendTracker(openai_api_key="test-key")
        
        assert tracker.aggregator is not None
        assert tracker.analyzer is not None
        assert tracker.storage is not None
    
    @patch('brand_manager.trend_tracker.TrendDataAggregator')
    @patch('brand_manager.trend_tracker.TrendAnalyzer')
    def test_collect_current_trends(self, mock_analyzer, mock_aggregator, tmp_path):
        """Test collecting current trends"""
        # Mock aggregator to return sample trends
        source = TrendSource(name="Test", url="https://example.com")
        mock_trends = [
            ProductTrend(
                title="Test",
                description="Desc",
                category="tech",
                source=source
            )
        ]
        
        mock_aggregator_instance = mock_aggregator.return_value
        mock_aggregator_instance.collect_all_trends.return_value = mock_trends
        
        tracker = TrendTracker(
            openai_api_key="test-key",
            storage_dir=str(tmp_path / "storage")
        )
        
        trends = tracker.collect_current_trends()
        
        assert len(trends) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
