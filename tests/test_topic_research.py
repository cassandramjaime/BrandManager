"""
Tests for Topic Research functionality
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from brand_manager.models import TopicResearchRequest, TopicResearchResult
from brand_manager.ai_manager import AITopicResearcher


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
        
        # Sample research response
        mock_message.content = """SUMMARY:
AI in healthcare is revolutionizing medical diagnosis and treatment. It offers improved accuracy and efficiency in patient care.

KEY POINTS:
- AI assists in early disease detection
- Machine learning improves diagnostic accuracy
- Automation reduces healthcare costs
- AI enables personalized treatment plans
- Predictive analytics improves patient outcomes

CURRENT TRENDS:
- Growing adoption of AI diagnostic tools
- Integration of AI in telemedicine platforms
- Increased use of AI for drug discovery

STATISTICS & DATA:
- AI can reduce diagnostic errors by up to 85%
- Healthcare AI market expected to reach $188 billion by 2030
- 60% of hospitals are investing in AI technologies

AUDIENCE INTERESTS:
- Patient safety and care quality
- Cost reduction in healthcare
- Privacy and data security concerns

CONTENT ANGLES:
- How AI is transforming patient diagnosis
- The future of personalized medicine
- Balancing AI efficiency with human care

KEYWORDS:
AI healthcare, medical AI, diagnostic tools, machine learning, patient care, telemedicine, predictive analytics, personalized medicine"""
        
        mock_choice.message = mock_message
        mock_response.choices = [mock_choice]
        
        mock_client.chat.completions.create.return_value = mock_response
        
        yield mock_client


class TestTopicResearchRequest:
    """Test TopicResearchRequest model"""
    
    def test_request_creation(self):
        """Test creating a topic research request"""
        request = TopicResearchRequest(
            topic="AI in healthcare",
            depth="standard",
            focus_areas=["trends", "statistics"]
        )
        assert request.topic == "AI in healthcare"
        assert request.depth == "standard"
        assert request.focus_areas == ["trends", "statistics"]
    
    def test_request_defaults(self):
        """Test request with default values"""
        request = TopicResearchRequest(topic="test topic")
        assert request.topic == "test topic"
        assert request.depth == "standard"
        assert request.focus_areas == []
    
    def test_request_serialization(self):
        """Test request can be serialized to dict"""
        request = TopicResearchRequest(
            topic="blockchain",
            depth="deep"
        )
        request_dict = request.model_dump()
        assert request_dict['topic'] == "blockchain"
        assert request_dict['depth'] == "deep"
        assert isinstance(request_dict, dict)


class TestTopicResearchResult:
    """Test TopicResearchResult model"""
    
    def test_result_creation(self):
        """Test creating a topic research result"""
        result = TopicResearchResult(
            topic="AI",
            summary="AI is transforming industries",
            key_points=["Point 1", "Point 2"],
            trends=["Trend 1"],
            statistics=["Stat 1"],
            audience_interests=["Interest 1"],
            content_angles=["Angle 1"],
            keywords=["AI", "machine learning"]
        )
        assert result.topic == "AI"
        assert len(result.key_points) == 2
        assert len(result.keywords) == 2
    
    def test_result_defaults(self):
        """Test result with minimal data"""
        result = TopicResearchResult(
            topic="test",
            summary="Test summary"
        )
        assert result.topic == "test"
        assert result.summary == "Test summary"
        assert result.key_points == []
        assert result.trends == []


class TestAITopicResearcher:
    """Test AITopicResearcher class"""
    
    def test_researcher_initialization_with_key(self, mock_openai_client):
        """Test researcher initialization with API key"""
        researcher = AITopicResearcher(api_key="test-key")
        assert researcher.api_key == "test-key"
    
    def test_researcher_initialization_without_key(self):
        """Test researcher initialization without API key raises error"""
        with patch.dict('os.environ', {}, clear=True):
            with pytest.raises(ValueError, match="OpenAI API key is required"):
                AITopicResearcher()
    
    def test_researcher_initialization_with_env_key(self, mock_openai_client):
        """Test researcher initialization with environment variable"""
        with patch.dict('os.environ', {'OPENAI_API_KEY': 'env-test-key'}):
            researcher = AITopicResearcher()
            assert researcher.api_key == "env-test-key"
    
    def test_research_topic_success(self, mock_openai_client):
        """Test successful topic research"""
        researcher = AITopicResearcher(api_key="test-key")
        
        request = TopicResearchRequest(
            topic="AI in healthcare",
            depth="standard"
        )
        
        result = researcher.research_topic(request)
        
        assert isinstance(result, TopicResearchResult)
        assert result.topic == "AI in healthcare"
        assert len(result.summary) > 0
        assert len(result.key_points) > 0
        assert len(result.trends) > 0
        assert len(result.statistics) > 0
        assert mock_openai_client.chat.completions.create.called
    
    def test_research_topic_with_focus_areas(self, mock_openai_client):
        """Test research with specific focus areas"""
        researcher = AITopicResearcher(api_key="test-key")
        
        request = TopicResearchRequest(
            topic="blockchain",
            depth="deep",
            focus_areas=["trends", "statistics"]
        )
        
        result = researcher.research_topic(request)
        
        assert isinstance(result, TopicResearchResult)
        assert mock_openai_client.chat.completions.create.called
        
        # Verify the prompt included focus areas
        call_args = mock_openai_client.chat.completions.create.call_args
        prompt = call_args[1]['messages'][1]['content']
        assert "trends" in prompt.lower()
        assert "statistics" in prompt.lower()
    
    def test_research_topic_quick_depth(self, mock_openai_client):
        """Test quick depth research"""
        researcher = AITopicResearcher(api_key="test-key")
        
        request = TopicResearchRequest(
            topic="test topic",
            depth="quick"
        )
        
        result = researcher.research_topic(request)
        
        assert isinstance(result, TopicResearchResult)
        
        # Verify quick depth instruction in prompt
        call_args = mock_openai_client.chat.completions.create.call_args
        prompt = call_args[1]['messages'][1]['content']
        assert "quick overview" in prompt.lower()
    
    def test_research_topic_deep_depth(self, mock_openai_client):
        """Test deep depth research"""
        researcher = AITopicResearcher(api_key="test-key")
        
        request = TopicResearchRequest(
            topic="test topic",
            depth="deep"
        )
        
        result = researcher.research_topic(request)
        
        assert isinstance(result, TopicResearchResult)
        
        # Verify deep depth instruction in prompt
        call_args = mock_openai_client.chat.completions.create.call_args
        prompt = call_args[1]['messages'][1]['content']
        assert "in-depth" in prompt.lower()
    
    def test_parse_research_response(self, mock_openai_client):
        """Test parsing of research response"""
        researcher = AITopicResearcher(api_key="test-key")
        
        sample_response = """SUMMARY:
This is a test summary about the topic.

KEY POINTS:
- First key point
- Second key point
- Third key point

CURRENT TRENDS:
- Trend one
- Trend two

STATISTICS & DATA:
- 50% increase in adoption
- $100 billion market size

AUDIENCE INTERESTS:
- Interest in sustainability
- Cost effectiveness

CONTENT ANGLES:
- How-to guide approach
- Expert interview format

KEYWORDS:
test, example, research, topic, AI, technology"""
        
        result = researcher._parse_research_response("test topic", sample_response)
        
        assert result.topic == "test topic"
        assert "test summary" in result.summary.lower()
        assert len(result.key_points) == 3
        assert len(result.trends) == 2
        assert len(result.statistics) == 2
        assert len(result.audience_interests) == 2
        assert len(result.content_angles) == 2
        assert len(result.keywords) > 0
    
    def test_parse_research_response_handles_missing_sections(self, mock_openai_client):
        """Test parsing handles missing sections gracefully"""
        researcher = AITopicResearcher(api_key="test-key")
        
        minimal_response = """SUMMARY:
Just a summary with nothing else."""
        
        result = researcher._parse_research_response("test", minimal_response)
        
        assert result.topic == "test"
        assert len(result.summary) > 0
        # Other fields should be empty lists
        assert result.key_points == []
        assert result.trends == []
