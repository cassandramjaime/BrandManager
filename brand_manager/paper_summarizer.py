"""
AI-powered paper summarization and categorization
"""
import os
from typing import Optional
from openai import OpenAI

from .paper_models import (
    Paper, PaperSummary, ApplicationArea, 
    TechnicalDifficulty, ProductionReadiness
)


class PaperSummarizer:
    """AI-powered research paper summarizer"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize the paper summarizer
        
        Args:
            api_key: OpenAI API key. If not provided, uses OPENAI_API_KEY env var
            model: OpenAI model to use (default: gpt-3.5-turbo)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key is required. Set OPENAI_API_KEY environment variable "
                "or pass api_key parameter."
            )
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
    
    def summarize_paper(self, paper: Paper) -> PaperSummary:
        """
        Generate an intelligent summary of a research paper
        
        Args:
            paper: Paper object to summarize
            
        Returns:
            PaperSummary object with categorization
        """
        prompt = self._build_summarization_prompt(paper)
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert AI/ML researcher and product manager who specializes in 
summarizing technical research papers for a product management audience. You provide concise, 
actionable summaries that highlight practical applications and production readiness."""
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
        summary_text = response.choices[0].message.content.strip()
        
        # Extract structured information
        summary = self._parse_summary_response(paper.paper_id, summary_text)
        
        return summary
    
    def _build_summarization_prompt(self, paper: Paper) -> str:
        """Build the summarization prompt"""
        return f"""Analyze and summarize the following research paper for a product management audience:

Title: {paper.title}

Authors: {', '.join(paper.authors)}

Abstract: {paper.abstract}

Categories: {', '.join(paper.categories) if paper.categories else 'Not specified'}

Please provide a comprehensive analysis in the following format:

CONCISE SUMMARY:
[Write a 2-3 paragraph summary that explains what the paper is about, its significance, and potential impact. 
Make it accessible to someone with general tech knowledge but not deep ML expertise.]

MAIN CONTRIBUTION:
[One paragraph describing the key innovation or contribution of this paper]

METHODOLOGY:
[One paragraph summarizing the approach/methods used in the research]

RESULTS:
[One paragraph highlighting the key findings and performance metrics]

PRODUCT RELEVANCE:
[One paragraph explaining how this could be relevant to product managers, including potential applications, 
business value, and considerations for product development]

APPLICATION AREA:
[Choose ONE: healthcare, finance, education, robotics, autonomous_vehicles, natural_language, 
computer_vision, or general]

TECHNICAL DIFFICULTY:
[Choose ONE: beginner, intermediate, advanced, or expert - based on the complexity of implementation]

PRODUCTION READINESS:
[Choose ONE: theoretical, experimental, prototype, or production_ready - based on how ready this is 
for real-world deployment]

Make sure to use clear section headers exactly as shown above."""
    
    def _parse_summary_response(self, paper_id: str, summary_text: str) -> PaperSummary:
        """Parse the AI summary response into a structured PaperSummary object"""
        
        sections = {
            'concise_summary': '',
            'main_contribution': '',
            'methodology_summary': '',
            'results_summary': '',
            'relevance_to_product': '',
            'application_area': 'general',
            'technical_difficulty': 'intermediate',
            'production_readiness': 'experimental'
        }
        
        current_section = None
        
        for line in summary_text.split('\n'):
            line = line.strip()
            
            # Detect section headers
            if line.startswith('CONCISE SUMMARY:'):
                current_section = 'concise_summary'
                continue
            elif line.startswith('MAIN CONTRIBUTION:'):
                current_section = 'main_contribution'
                continue
            elif line.startswith('METHODOLOGY:'):
                current_section = 'methodology_summary'
                continue
            elif line.startswith('RESULTS:'):
                current_section = 'results_summary'
                continue
            elif line.startswith('PRODUCT RELEVANCE:'):
                current_section = 'relevance_to_product'
                continue
            elif line.startswith('APPLICATION AREA:'):
                current_section = 'application_area'
                # Extract value from the same line
                value = line.replace('APPLICATION AREA:', '').strip().lower()
                if value in [e.value for e in ApplicationArea]:
                    sections['application_area'] = value
                continue
            elif line.startswith('TECHNICAL DIFFICULTY:'):
                current_section = 'technical_difficulty'
                # Extract value from the same line
                value = line.replace('TECHNICAL DIFFICULTY:', '').strip().lower()
                if value in [e.value for e in TechnicalDifficulty]:
                    sections['technical_difficulty'] = value
                continue
            elif line.startswith('PRODUCTION READINESS:'):
                current_section = 'production_readiness'
                # Extract value from the same line
                value = line.replace('PRODUCTION READINESS:', '').strip().lower()
                if value in [e.value for e in ProductionReadiness]:
                    sections['production_readiness'] = value
                continue
            
            # Process content based on current section
            if not line or not current_section:
                continue
            
            # For text sections, accumulate content
            if current_section in ['concise_summary', 'main_contribution', 
                                   'methodology_summary', 'results_summary', 
                                   'relevance_to_product']:
                sections[current_section] += line + ' '
            # For enum sections, try to extract value if not yet found
            elif current_section == 'application_area' and not sections['application_area']:
                value = line.lower().strip()
                if value in [e.value for e in ApplicationArea]:
                    sections['application_area'] = value
            elif current_section == 'technical_difficulty' and sections['technical_difficulty'] == 'intermediate':
                value = line.lower().strip()
                if value in [e.value for e in TechnicalDifficulty]:
                    sections['technical_difficulty'] = value
            elif current_section == 'production_readiness' and sections['production_readiness'] == 'experimental':
                value = line.lower().strip()
                if value in [e.value for e in ProductionReadiness]:
                    sections['production_readiness'] = value
        
        # Clean up text sections
        for key in ['concise_summary', 'main_contribution', 'methodology_summary', 
                    'results_summary', 'relevance_to_product']:
            sections[key] = sections[key].strip()
            # If empty, provide a default
            if not sections[key]:
                sections[key] = "Summary not available."
        
        return PaperSummary(
            paper_id=paper_id,
            concise_summary=sections['concise_summary'],
            main_contribution=sections['main_contribution'],
            methodology_summary=sections['methodology_summary'],
            results_summary=sections['results_summary'],
            relevance_to_product=sections['relevance_to_product'],
            application_area=ApplicationArea(sections['application_area']),
            technical_difficulty=TechnicalDifficulty(sections['technical_difficulty']),
            production_readiness=ProductionReadiness(sections['production_readiness'])
        )
