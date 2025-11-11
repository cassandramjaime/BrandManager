"""
Tests for Brand Manager
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from brand_manager.models import BrandIdentity, ContentRequest
from brand_manager.ai_manager import AIBrandManager


@pytest.fixture
def sample_brand():
    """Create a sample brand identity for testing"""
    return BrandIdentity(
        name="TechFlow",
        tagline="Empowering Innovation",
        description="A cutting-edge technology consultancy",
        values=["Innovation", "Integrity", "Excellence"],
        target_audience="Tech startups and SMBs",
        voice="Professional yet approachable",
        industry="Technology Consulting",
        unique_selling_points=["AI-first approach", "24/7 support"]
    )


@pytest.fixture
def mock_openai_client():
    """Create a mock OpenAI client"""
    with patch('brand_manager.ai_manager.OpenAI') as mock_openai:
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        # Mock the chat completion response structure
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        mock_message.content = "Sample AI response"
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        
        mock_client.chat.completions.create.return_value = mock_response
        
        yield mock_client


class TestBrandIdentity:
    """Test BrandIdentity model"""
    
    def test_brand_identity_creation(self, sample_brand):
        """Test creating a brand identity"""
        assert sample_brand.name == "TechFlow"
        assert sample_brand.tagline == "Empowering Innovation"
        assert len(sample_brand.values) == 3
        assert "Innovation" in sample_brand.values
    
    def test_brand_identity_minimal(self):
        """Test creating a minimal brand identity with only required fields"""
        brand = BrandIdentity(name="MinimalBrand")
        assert brand.name == "MinimalBrand"
        assert brand.tagline is None
        assert brand.values == []
    
    def test_brand_identity_serialization(self, sample_brand):
        """Test brand identity can be serialized to dict"""
        brand_dict = sample_brand.model_dump()
        assert brand_dict['name'] == "TechFlow"
        assert isinstance(brand_dict, dict)


class TestContentRequest:
    """Test ContentRequest model"""
    
    def test_content_request_creation(self):
        """Test creating a content request"""
        request = ContentRequest(
            content_type="social_post",
            topic="product launch",
            platform="twitter",
            length="short"
        )
        assert request.content_type == "social_post"
        assert request.topic == "product launch"
        assert request.platform == "twitter"
        assert request.length == "short"
    
    def test_content_request_defaults(self):
        """Test content request with defaults"""
        request = ContentRequest(content_type="blog_title")
        assert request.length == "medium"
        assert request.topic is None
        assert request.platform is None


class TestAIBrandManager:
    """Test AIBrandManager class"""
    
    def test_manager_initialization_with_key(self, mock_openai_client):
        """Test manager initialization with API key"""
        manager = AIBrandManager(api_key="test-key")
        assert manager.api_key == "test-key"
        assert manager.brand_identity is None
    
    def test_manager_initialization_without_key(self):
        """Test manager initialization without API key raises error"""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="OpenAI API key is required"):
                AIBrandManager()
    
    def test_manager_initialization_with_env_key(self, mock_openai_client):
        """Test manager initialization with environment variable"""
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'env-test-key'}):
            manager = AIBrandManager()
            assert manager.api_key == "env-test-key"
    
    def test_set_brand_identity(self, sample_brand, mock_openai_client):
        """Test setting brand identity"""
        manager = AIBrandManager(api_key="test-key")
        manager.set_brand_identity(sample_brand)
        assert manager.brand_identity == sample_brand
    
    def test_build_brand_context(self, sample_brand, mock_openai_client):
        """Test building brand context string"""
        manager = AIBrandManager(api_key="test-key")
        manager.set_brand_identity(sample_brand)
        
        context = manager._build_brand_context()
        
        assert "TechFlow" in context
        assert "Empowering Innovation" in context
        assert "Innovation, Integrity, Excellence" in context
        assert "Professional yet approachable" in context
    
    def test_build_brand_context_empty(self, mock_openai_client):
        """Test building brand context with no brand set"""
        manager = AIBrandManager(api_key="test-key")
        context = manager._build_brand_context()
        assert context == ""
    
    def test_generate_tagline_requires_brand(self, mock_openai_client):
        """Test that generate_tagline requires brand identity"""
        manager = AIBrandManager(api_key="test-key")
        
        with pytest.raises(ValueError, match="Brand identity must be set"):
            manager.generate_tagline()
    
    def test_generate_tagline_success(self, sample_brand, mock_openai_client):
        """Test successful tagline generation"""
        manager = AIBrandManager(api_key="test-key")
        manager.set_brand_identity(sample_brand)
        
        # Mock the response with multiple taglines
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        mock_message.content = "Tagline 1\nTagline 2\nTagline 3"
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_openai_client.chat.completions.create.return_value = mock_response
        
        taglines = manager.generate_tagline(variations=3)
        
        assert len(taglines) == 3
        assert "Tagline 1" in taglines
        assert mock_openai_client.chat.completions.create.called
    
    def test_generate_content_requires_brand(self, mock_openai_client):
        """Test that generate_content requires brand identity"""
        manager = AIBrandManager(api_key="test-key")
        request = ContentRequest(content_type="social_post")
        
        with pytest.raises(ValueError, match="Brand identity must be set"):
            manager.generate_content(request)
    
    def test_generate_content_success(self, sample_brand, mock_openai_client):
        """Test successful content generation"""
        manager = AIBrandManager(api_key="test-key")
        manager.set_brand_identity(sample_brand)
        
        # Mock the response
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        mock_message.content = "Generated social media post content"
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_openai_client.chat.completions.create.return_value = mock_response
        
        request = ContentRequest(
            content_type="social_post",
            topic="product launch",
            platform="twitter"
        )
        
        content = manager.generate_content(request)
        
        assert content == "Generated social media post content"
        assert mock_openai_client.chat.completions.create.called
    
    def test_analyze_brand_message_requires_brand(self, mock_openai_client):
        """Test that analyze_brand_message requires brand identity"""
        manager = AIBrandManager(api_key="test-key")
        
        with pytest.raises(ValueError, match="Brand identity must be set"):
            manager.analyze_brand_message("Test message")
    
    def test_analyze_brand_message_success(self, sample_brand, mock_openai_client):
        """Test successful brand message analysis"""
        manager = AIBrandManager(api_key="test-key")
        manager.set_brand_identity(sample_brand)
        
        # Mock the response
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        mock_message.content = "Analysis: Good alignment with brand values"
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_openai_client.chat.completions.create.return_value = mock_response
        
        message = "We believe in innovation and excellence"
        result = manager.analyze_brand_message(message)
        
        assert "analysis" in result
        assert result["message"] == message
        assert "Analysis: Good alignment" in result["analysis"]
    
    def test_get_brand_strategy_advice_requires_brand(self, mock_openai_client):
        """Test that get_brand_strategy_advice requires brand identity"""
        manager = AIBrandManager(api_key="test-key")
        
        with pytest.raises(ValueError, match="Brand identity must be set"):
            manager.get_brand_strategy_advice("How to grow?")
    
    def test_get_brand_strategy_advice_success(self, sample_brand, mock_openai_client):
        """Test successful strategy advice generation"""
        manager = AIBrandManager(api_key="test-key")
        manager.set_brand_identity(sample_brand)
        
        # Mock the response
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        mock_message.content = "Strategic advice: Focus on content marketing"
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_openai_client.chat.completions.create.return_value = mock_response
        
        advice = manager.get_brand_strategy_advice("How can I improve visibility?")
        
        assert "Strategic advice" in advice
        assert mock_openai_client.chat.completions.create.called
    
    def test_brainstorm_campaign_ideas_requires_brand(self, mock_openai_client):
        """Test that brainstorm_campaign_ideas requires brand identity"""
        manager = AIBrandManager(api_key="test-key")
        
        with pytest.raises(ValueError, match="Brand identity must be set"):
            manager.brainstorm_campaign_ideas("Increase awareness")
    
    def test_brainstorm_campaign_ideas_success(self, sample_brand, mock_openai_client):
        """Test successful campaign idea generation"""
        manager = AIBrandManager(api_key="test-key")
        manager.set_brand_identity(sample_brand)
        
        # Mock the response
        mock_response = MagicMock()
        mock_choice = MagicMock()
        mock_message = MagicMock()
        mock_message.content = "Idea 1: Campaign A\nDescription here\n\nIdea 2: Campaign B\nAnother description"
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        mock_openai_client.chat.completions.create.return_value = mock_response
        
        ideas = manager.brainstorm_campaign_ideas("Increase brand awareness", num_ideas=2)
        
        assert len(ideas) > 0
        assert mock_openai_client.chat.completions.create.called
