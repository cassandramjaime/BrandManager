"""
Tests for Journalist Opportunity Finder functionality
"""
import pytest
import os
import tempfile
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock

from brand_manager.journalist_models import (
    JournalistOpportunity,
    PublicationTier,
    Urgency,
    OpportunitySource,
    UserProfile,
    OpportunityFilter,
    PitchTemplate
)
from brand_manager.opportunity_database import OpportunityDatabase
from brand_manager.opportunity_finder import OpportunityFinder


@pytest.fixture
def temp_db():
    """Create a temporary database for testing"""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as f:
        db_path = f.name
    
    yield db_path
    
    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)


@pytest.fixture
def sample_opportunity():
    """Create a sample opportunity for testing"""
    return JournalistOpportunity(
        publication_name="TechCrunch",
        journalist_name="Jane Doe",
        topic="AI in Product Management",
        deadline=datetime.now() + timedelta(days=3),
        requirements="Looking for AI PM experts to discuss how AI is changing product management",
        contact_method="jane.doe@techcrunch.com",
        tier=PublicationTier.TIER_2,
        urgency=Urgency.MEDIUM,
        source=OpportunitySource.TWITTER,
        relevance_score=85.0,
        keywords=["AI", "product management", "artificial intelligence"]
    )


@pytest.fixture
def sample_user_profile():
    """Create a sample user profile for testing"""
    return UserProfile(
        name="John Smith",
        title="AI Product Manager",
        expertise_areas=["artificial intelligence", "product management", "machine learning"],
        experience_years=8,
        company="TechCorp",
        bio="AI PM with 8 years of experience building ML-powered products",
        achievements=["Led AI product launch", "Grew user base by 200%"],
        contact_info={"email": "john@example.com"}
    )


class TestJournalistModels:
    """Test journalist opportunity models"""
    
    def test_opportunity_creation(self, sample_opportunity):
        """Test creating a journalist opportunity"""
        assert sample_opportunity.publication_name == "TechCrunch"
        assert sample_opportunity.tier == PublicationTier.TIER_2
        assert sample_opportunity.urgency == Urgency.MEDIUM
        assert sample_opportunity.relevance_score == 85.0
        assert len(sample_opportunity.keywords) == 3
    
    def test_opportunity_defaults(self):
        """Test opportunity with minimal data"""
        opp = JournalistOpportunity(
            publication_name="Test Publication",
            topic="Test Topic",
            requirements="Test requirements",
            contact_method="test@example.com",
            tier=PublicationTier.TIER_3,
            urgency=Urgency.LOW,
            source=OpportunitySource.OTHER
        )
        assert opp.pitch_sent is False
        assert opp.response_received is False
        assert opp.relevance_score == 0.0
        assert opp.keywords == []
    
    def test_user_profile_creation(self, sample_user_profile):
        """Test creating a user profile"""
        assert sample_user_profile.name == "John Smith"
        assert sample_user_profile.experience_years == 8
        assert len(sample_user_profile.expertise_areas) == 3
        assert len(sample_user_profile.achievements) == 2
    
    def test_opportunity_filter_creation(self):
        """Test creating opportunity filter"""
        filter_params = OpportunityFilter(
            min_relevance_score=70.0,
            tiers=[PublicationTier.TIER_1, PublicationTier.TIER_2],
            urgency_levels=[Urgency.HIGH],
            only_not_pitched=True
        )
        assert filter_params.min_relevance_score == 70.0
        assert len(filter_params.tiers) == 2
        assert filter_params.only_not_pitched is True


class TestOpportunityDatabase:
    """Test opportunity database functionality"""
    
    def test_database_initialization(self, temp_db):
        """Test database initialization creates tables"""
        db = OpportunityDatabase(temp_db)
        # If no error, tables were created successfully
        assert os.path.exists(temp_db)
    
    def test_add_opportunity(self, temp_db, sample_opportunity):
        """Test adding an opportunity to database"""
        db = OpportunityDatabase(temp_db)
        opportunity_id = db.add_opportunity(sample_opportunity)
        
        assert opportunity_id is not None
        assert len(opportunity_id) > 0
    
    def test_get_opportunity(self, temp_db, sample_opportunity):
        """Test retrieving an opportunity from database"""
        db = OpportunityDatabase(temp_db)
        opportunity_id = db.add_opportunity(sample_opportunity)
        
        retrieved = db.get_opportunity(opportunity_id)
        
        assert retrieved is not None
        assert retrieved.publication_name == sample_opportunity.publication_name
        assert retrieved.topic == sample_opportunity.topic
        assert retrieved.relevance_score == sample_opportunity.relevance_score
    
    def test_list_opportunities(self, temp_db, sample_opportunity):
        """Test listing opportunities"""
        db = OpportunityDatabase(temp_db)
        
        # Add multiple opportunities
        db.add_opportunity(sample_opportunity)
        
        opp2 = JournalistOpportunity(
            publication_name="Forbes",
            topic="Machine Learning in Business",
            requirements="Looking for ML experts",
            contact_method="editor@forbes.com",
            tier=PublicationTier.TIER_1,
            urgency=Urgency.HIGH,
            source=OpportunitySource.HARO,
            relevance_score=95.0
        )
        db.add_opportunity(opp2)
        
        opportunities = db.list_opportunities()
        assert len(opportunities) == 2
    
    def test_filter_opportunities(self, temp_db, sample_opportunity):
        """Test filtering opportunities"""
        db = OpportunityDatabase(temp_db)
        db.add_opportunity(sample_opportunity)
        
        # Filter by minimum score
        filter_params = OpportunityFilter(min_relevance_score=90.0)
        filtered = db.list_opportunities(filter_params)
        assert len(filtered) == 0  # Sample opportunity has score of 85
        
        # Filter by tier
        filter_params = OpportunityFilter(tiers=[PublicationTier.TIER_2])
        filtered = db.list_opportunities(filter_params)
        assert len(filtered) == 1
    
    def test_mark_pitch_sent(self, temp_db, sample_opportunity):
        """Test marking opportunity as pitched"""
        db = OpportunityDatabase(temp_db)
        opportunity_id = db.add_opportunity(sample_opportunity)
        
        db.mark_pitch_sent(opportunity_id, "Test pitch text")
        
        retrieved = db.get_opportunity(opportunity_id)
        assert retrieved.pitch_sent is True
        assert retrieved.pitch_sent_at is not None
    
    def test_mark_response_received(self, temp_db, sample_opportunity):
        """Test marking response received"""
        db = OpportunityDatabase(temp_db)
        opportunity_id = db.add_opportunity(sample_opportunity)
        
        db.mark_response_received(opportunity_id, "Test response")
        
        retrieved = db.get_opportunity(opportunity_id)
        assert retrieved.response_received is True
        assert retrieved.response_received_at is not None
    
    def test_get_statistics(self, temp_db, sample_opportunity):
        """Test getting statistics"""
        db = OpportunityDatabase(temp_db)
        opportunity_id = db.add_opportunity(sample_opportunity)
        
        stats = db.get_statistics()
        
        assert stats['total_opportunities'] == 1
        assert stats['pitches_sent'] == 0
        assert stats['responses_received'] == 0
        
        # Mark as pitched
        db.mark_pitch_sent(opportunity_id, "Test pitch")
        stats = db.get_statistics()
        assert stats['pitches_sent'] == 1
    
    def test_save_and_get_user_profile(self, temp_db, sample_user_profile):
        """Test saving and retrieving user profile"""
        db = OpportunityDatabase(temp_db)
        
        db.save_user_profile(sample_user_profile)
        retrieved = db.get_user_profile()
        
        assert retrieved is not None
        assert retrieved.name == sample_user_profile.name
        assert retrieved.title == sample_user_profile.title
        assert retrieved.experience_years == sample_user_profile.experience_years


class TestOpportunityFinder:
    """Test opportunity finder functionality"""
    
    @pytest.fixture
    def mock_openai_client(self):
        """Create a mock OpenAI client"""
        with patch('brand_manager.opportunity_finder.OpenAI') as mock_openai:
            mock_client = MagicMock()
            mock_openai.return_value = mock_client
            yield mock_client
    
    def test_finder_initialization_with_key(self, mock_openai_client, temp_db):
        """Test finder initialization with API key"""
        finder = OpportunityFinder(api_key="test-key", db_path=temp_db)
        assert finder.api_key == "test-key"
    
    def test_finder_initialization_without_key(self, temp_db):
        """Test finder initialization without API key raises error"""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="OpenAI API key is required"):
                OpportunityFinder(db_path=temp_db)
    
    def test_classify_publication_tier(self, mock_openai_client, temp_db):
        """Test publication tier classification"""
        finder = OpportunityFinder(api_key="test-key", db_path=temp_db)
        
        assert finder.classify_publication_tier("TechCrunch") == PublicationTier.TIER_2
        assert finder.classify_publication_tier("Wall Street Journal") == PublicationTier.TIER_1
        assert finder.classify_publication_tier("Forbes") == PublicationTier.TIER_1
        assert finder.classify_publication_tier("Unknown Blog") == PublicationTier.TIER_3
    
    def test_calculate_urgency(self, mock_openai_client, temp_db):
        """Test urgency calculation"""
        finder = OpportunityFinder(api_key="test-key", db_path=temp_db)
        
        # High urgency - deadline in 1 day
        deadline_high = datetime.now() + timedelta(days=1)
        assert finder.calculate_urgency(deadline_high) == Urgency.HIGH
        
        # Medium urgency - deadline in 5 days
        deadline_medium = datetime.now() + timedelta(days=5)
        assert finder.calculate_urgency(deadline_medium) == Urgency.MEDIUM
        
        # Low urgency - deadline in 10 days
        deadline_low = datetime.now() + timedelta(days=10)
        assert finder.calculate_urgency(deadline_low) == Urgency.LOW
        
        # No deadline
        assert finder.calculate_urgency(None) == Urgency.LOW
    
    def test_calculate_relevance_score_without_profile(self, mock_openai_client, temp_db):
        """Test relevance scoring without user profile"""
        finder = OpportunityFinder(api_key="test-key", db_path=temp_db)
        
        # Opportunity with AI and PM keywords
        opp_dict = {
            "topic": "AI in product management",
            "requirements": "Looking for AI product managers"
        }
        score = finder.calculate_relevance_score(opp_dict)
        assert score == 85.0  # Both AI and PM match
        
        # Opportunity with only AI
        opp_dict = {
            "topic": "Artificial intelligence trends",
            "requirements": "Looking for AI experts"
        }
        score = finder.calculate_relevance_score(opp_dict)
        assert score == 60.0  # Only AI match
    
    def test_parse_opportunity_with_ai(self, mock_openai_client, temp_db):
        """Test parsing opportunity with AI"""
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        
        mock_message.content = '''{
            "publication_name": "TechCrunch",
            "journalist_name": "John Doe",
            "topic": "AI Product Management",
            "deadline": null,
            "requirements": "Looking for AI PM experts",
            "contact_method": "john@techcrunch.com",
            "keywords": ["AI", "product management"]
        }'''
        
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_openai_client.chat.completions.create.return_value = mock_response
        
        finder = OpportunityFinder(api_key="test-key", db_path=temp_db)
        
        opportunity = finder.parse_opportunity_with_ai(
            "TechCrunch looking for AI PM experts. Contact john@techcrunch.com",
            OpportunitySource.TWITTER
        )
        
        assert opportunity is not None
        assert opportunity.publication_name == "TechCrunch"
        assert opportunity.topic == "AI Product Management"
        assert opportunity.source == OpportunitySource.TWITTER
    
    def test_generate_pitch(self, mock_openai_client, temp_db, sample_opportunity, sample_user_profile):
        """Test pitch generation"""
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        
        mock_message.content = """SUBJECT: AI PM Expert Available for TechCrunch Article

GREETING: Hi Jane,

BODY:
I saw your call for AI product management experts and wanted to reach out. As an AI Product Manager with 8 years of experience, I have extensive knowledge in this area.

I have led several AI product launches and grown user bases significantly through ML-powered features.

CLOSING:
Best regards,
John Smith"""
        
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_openai_client.chat.completions.create.return_value = mock_response
        
        finder = OpportunityFinder(api_key="test-key", db_path=temp_db)
        finder.db.save_user_profile(sample_user_profile)
        
        pitch = finder.generate_pitch(sample_opportunity, sample_user_profile)
        
        assert isinstance(pitch, PitchTemplate)
        assert len(pitch.subject_line) > 0
        assert "Jane" in pitch.greeting or "Hi" in pitch.greeting
        assert len(pitch.body) > 0
        assert len(pitch.full_pitch) > 0
    
    def test_generate_daily_digest(self, mock_openai_client, temp_db, sample_opportunity):
        """Test daily digest generation"""
        finder = OpportunityFinder(api_key="test-key", db_path=temp_db)
        
        # Add some opportunities
        finder.db.add_opportunity(sample_opportunity)
        
        digest = finder.generate_daily_digest()
        
        assert digest is not None
        assert digest.total_opportunities >= 0
        assert isinstance(digest.high_priority, list)
        assert isinstance(digest.medium_priority, list)
        assert isinstance(digest.low_priority, list)
