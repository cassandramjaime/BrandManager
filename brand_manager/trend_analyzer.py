"""
Trend analyzer using LLM for pattern identification and insights
"""
import os
from typing import List, Dict, Any
from openai import OpenAI
from datetime import datetime

from .trend_models import ProductTrend, TrendAnalysis, TrendItem, WeeklyTrendReport


class TrendAnalyzer:
    """Analyzes trends using LLM to identify patterns and opportunities"""
    
    def __init__(self, api_key: str = None):
        """Initialize the trend analyzer"""
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        self.client = OpenAI(api_key=self.api_key)
    
    def analyze_trends(self, trends: List[ProductTrend]) -> TrendAnalysis:
        """
        Analyze a collection of trends to identify patterns and opportunities
        
        Args:
            trends: List of ProductTrend objects to analyze
            
        Returns:
            TrendAnalysis with insights
        """
        # Prepare trend data for analysis
        trend_summaries = []
        for trend in trends[:50]:  # Limit to avoid token limits
            summary = f"- {trend.title} ({trend.category}): {trend.description[:200]}"
            if trend.traction_metrics:
                summary += f" [Metrics: {trend.traction_metrics}]"
            trend_summaries.append(summary)
        
        trends_text = "\n".join(trend_summaries)
        
        prompt = f"""Analyze the following consumer product trends and identify key insights:

{trends_text}

Provide a comprehensive analysis in the following format:

COMMON PATTERNS:
- [Pattern 1]
- [Pattern 2]
- [Pattern 3]
[Continue with 5-7 common patterns across these trends]

EMERGING CATEGORIES:
- [Category 1]
- [Category 2]
- [Category 3]
[List 3-5 emerging or growing categories]

OPPORTUNITIES:
- [Opportunity 1]
- [Opportunity 2]
- [Opportunity 3]
[List 5-7 potential business or product opportunities]

TECHNOLOGIES:
- [Technology 1]
- [Technology 2]
- [Technology 3]
[List 5-7 key technologies being adopted]

SUMMARY:
[A comprehensive 3-4 paragraph summary of the overall trends landscape, what's driving adoption, and key takeaways]
"""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-16k",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert trend analyst specializing in consumer products and technology. You identify patterns, emerging opportunities, and provide strategic insights."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        analysis_text = response.choices[0].message.content.strip()
        return self._parse_analysis(analysis_text)
    
    def rank_trends(self, trends: List[ProductTrend], top_n: int = 10) -> List[TrendItem]:
        """
        Rank trends by traction and generate insights on why they're trending
        
        Args:
            trends: List of trends to rank
            top_n: Number of top trends to return
            
        Returns:
            List of ranked TrendItem objects
        """
        # Calculate traction scores
        scored_trends = []
        for trend in trends:
            score = self._calculate_traction_score(trend)
            scored_trends.append((score, trend))
        
        # Sort by score
        scored_trends.sort(reverse=True, key=lambda x: x[0])
        
        # Get top N trends
        top_trends = scored_trends[:top_n]
        
        # Generate "why trending" analysis for top trends
        trend_items = []
        for rank, (score, trend) in enumerate(top_trends, 1):
            why_trending = self._analyze_why_trending(trend)
            
            item = TrendItem(
                rank=rank,
                title=trend.title,
                description=trend.description[:300],
                category=trend.category,
                traction_score=score,
                why_trending=why_trending,
                sources=[trend.source.name]
            )
            trend_items.append(item)
        
        return trend_items
    
    def _calculate_traction_score(self, trend: ProductTrend) -> float:
        """Calculate a traction score based on available metrics"""
        score = 0.0
        
        # Base score from source credibility
        source_weights = {
            'Product Hunt': 1.5,
            'Hacker News': 1.3,
            'TechCrunch': 1.4,
            'The Verge': 1.2,
            'Reddit r/technology': 1.1,
            'Reddit r/gadgets': 1.0,
            'Reddit r/startups': 1.2
        }
        score += source_weights.get(trend.source.name, 1.0) * 10
        
        # Add metrics-based scoring
        if trend.traction_metrics:
            score += trend.traction_metrics.get('score', 0) * 0.5
            score += trend.traction_metrics.get('upvotes', 0) * 0.3
            score += trend.traction_metrics.get('comments', 0) * 0.2
        
        # Recency bonus (newer trends score higher)
        hours_old = (datetime.utcnow() - trend.discovered_at).total_seconds() / 3600
        recency_multiplier = max(0.5, 1.0 - (hours_old / 168))  # Decay over 1 week
        score *= recency_multiplier
        
        return score
    
    def _analyze_why_trending(self, trend: ProductTrend) -> str:
        """Generate a brief analysis of why this trend is gaining traction"""
        try:
            prompt = f"""Briefly explain in 1-2 sentences why this product/trend is gaining traction:

Title: {trend.title}
Description: {trend.description[:300]}
Category: {trend.category}
Source: {trend.source.name}

Focus on what makes it appealing, timely, or innovative."""
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a trend analyst. Provide concise, insightful explanations."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=100
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Trending in {trend.category} category with strong community interest."
    
    def _parse_analysis(self, analysis_text: str) -> TrendAnalysis:
        """Parse LLM analysis response into structured data"""
        sections = {
            'common_patterns': [],
            'emerging_categories': [],
            'opportunities': [],
            'technologies': [],
            'summary': ''
        }
        
        current_section = None
        
        for line in analysis_text.split('\n'):
            line = line.strip()
            
            if line.startswith('COMMON PATTERNS:'):
                current_section = 'common_patterns'
                continue
            elif line.startswith('EMERGING CATEGORIES:'):
                current_section = 'emerging_categories'
                continue
            elif line.startswith('OPPORTUNITIES:'):
                current_section = 'opportunities'
                continue
            elif line.startswith('TECHNOLOGIES:'):
                current_section = 'technologies'
                continue
            elif line.startswith('SUMMARY:'):
                current_section = 'summary'
                continue
            
            if not line or not current_section:
                continue
            
            if current_section == 'summary':
                sections['summary'] += line + ' '
            elif line.startswith('- ') or line.startswith('* '):
                clean_line = line[2:].strip()
                if clean_line:
                    sections[current_section].append(clean_line)
        
        sections['summary'] = sections['summary'].strip()
        
        return TrendAnalysis(
            common_patterns=sections['common_patterns'],
            emerging_categories=sections['emerging_categories'],
            opportunities=sections['opportunities'],
            technologies=sections['technologies'],
            summary=sections['summary'] or "Analysis completed successfully."
        )
    
    def generate_category_insights(self, trends: List[ProductTrend]) -> Dict[str, Any]:
        """Generate insights about category distribution"""
        category_count = {}
        category_trends = {}
        
        for trend in trends:
            category = trend.category
            if category not in category_count:
                category_count[category] = 0
                category_trends[category] = []
            
            category_count[category] += 1
            category_trends[category].append(trend.title)
        
        return {
            'breakdown': category_count,
            'top_categories': sorted(category_count.items(), key=lambda x: x[1], reverse=True)[:5],
            'category_examples': {cat: trends[:3] for cat, trends in category_trends.items()}
        }
