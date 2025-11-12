"""
AI Topic Researcher - Dynamic content topic research using OpenAI
"""
import os
from typing import Optional
from openai import OpenAI
from .models import TopicResearchRequest, TopicResearchResult


class AITopicResearcher:
    """AI-powered topic researcher for dynamic content research"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the AI Topic Researcher
        
        Args:
            api_key: OpenAI API key. If not provided, uses OPENAI_API_KEY env var
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        self.client = OpenAI(api_key=self.api_key)
    
    def research_topic(self, request: TopicResearchRequest) -> TopicResearchResult:
        """
        Research a topic dynamically using AI
        
        Args:
            request: Topic research request with topic and parameters
            
        Returns:
            TopicResearchResult with comprehensive research findings
        """
        # Build the research prompt based on depth and focus areas
        depth_instructions = {
            "quick": "Provide a quick overview with 3-5 key points.",
            "standard": "Provide comprehensive research with detailed insights.",
            "deep": "Provide in-depth research with extensive analysis and multiple perspectives."
        }
        
        depth_instruction = depth_instructions.get(request.depth, depth_instructions["standard"])
        
        # Build focus areas instruction
        focus_instruction = ""
        if request.focus_areas:
            focus_instruction = f"\n\nFocus particularly on: {', '.join(request.focus_areas)}"
        
        prompt = f"""Research the following topic and provide comprehensive insights: "{request.topic}"

{depth_instruction}{focus_instruction}

Provide your research in the following structured format:

SUMMARY:
[A 2-3 sentence summary of the topic]

KEY POINTS:
- [Key point 1]
- [Key point 2]
- [Key point 3]
[Continue with 5-8 total key points]

CURRENT TRENDS:
- [Trend 1]
- [Trend 2]
- [Trend 3]
[Continue with 3-5 trends]

STATISTICS & DATA:
- [Statistic 1]
- [Statistic 2]
- [Statistic 3]
[Continue with 3-5 relevant statistics]

AUDIENCE INTERESTS:
- [Interest 1]
- [Interest 2]
- [Interest 3]
[Continue with 3-5 audience interests]

CONTENT ANGLES:
- [Angle 1]
- [Angle 2]
- [Angle 3]
[Continue with 3-5 content angles]

COMPETITOR INSIGHTS:
- [How competitors approach this topic - angle 1]
- [What successful content exists - example 1]
- [Content gaps and opportunities - insight 1]
[Continue with 3-5 competitor insights]

KEYWORDS:
[Comma-separated list of 8-12 important keywords]

Make sure all information is current, accurate, and useful for content creation."""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert researcher and content strategist who provides comprehensive, accurate research on any topic to help inform content creation. Always provide specific, actionable insights."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        # Parse the response
        research_text = response.choices[0].message.content.strip()
        
        # Extract sections from the response
        result = self._parse_research_response(request.topic, research_text)
        
        return result
    
    def _parse_research_response(self, topic: str, research_text: str) -> TopicResearchResult:
        """Parse the AI research response into a structured result"""
        
        sections = {
            "summary": "",
            "key_points": [],
            "trends": [],
            "statistics": [],
            "audience_interests": [],
            "content_angles": [],
            "competitor_insights": [],
            "keywords": []
        }
        
        current_section = None
        
        for line in research_text.split('\n'):
            line = line.strip()
            
            # Detect section headers
            if line.startswith('SUMMARY:'):
                current_section = 'summary'
                continue
            elif line.startswith('KEY POINTS:'):
                current_section = 'key_points'
                continue
            elif line.startswith('CURRENT TRENDS:'):
                current_section = 'trends'
                continue
            elif line.startswith('STATISTICS') or line.startswith('STATISTICS & DATA:'):
                current_section = 'statistics'
                continue
            elif line.startswith('AUDIENCE INTERESTS:'):
                current_section = 'audience_interests'
                continue
            elif line.startswith('CONTENT ANGLES:'):
                current_section = 'content_angles'
                continue
            elif line.startswith('COMPETITOR INSIGHTS:'):
                current_section = 'competitor_insights'
                continue
            elif line.startswith('KEYWORDS:'):
                current_section = 'keywords'
                continue
            
            # Process content based on current section
            if not line or not current_section:
                continue
            
            if current_section == 'summary':
                sections['summary'] += line + ' '
            elif current_section == 'keywords':
                # Split by comma for keywords
                keywords = [k.strip() for k in line.split(',') if k.strip()]
                sections['keywords'].extend(keywords)
            elif line.startswith('- ') or line.startswith('* '):
                # Remove bullet points and add to appropriate list
                clean_line = line[2:].strip()
                if clean_line:
                    sections[current_section].append(clean_line)
        
        # Clean up summary
        sections['summary'] = sections['summary'].strip()
        
        # If summary is empty, create one from the research text
        if not sections['summary']:
            # Take the first few sentences as summary
            sentences = research_text.split('.')[:3]
            sections['summary'] = '. '.join([s.strip() for s in sentences if s.strip()]) + '.'
        
        return TopicResearchResult(
            topic=topic,
            summary=sections['summary'],
            key_points=sections['key_points'],
            trends=sections['trends'],
            statistics=sections['statistics'],
            audience_interests=sections['audience_interests'],
            content_angles=sections['content_angles'],
            competitor_insights=sections['competitor_insights'],
            keywords=sections['keywords']
        )
