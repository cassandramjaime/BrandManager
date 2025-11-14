"""
Data source collectors for consumer product trends
"""
import os
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup
import feedparser
from pytrends.request import TrendReq

from .trend_models import ProductTrend, TrendSource, StartupInfo, GoogleTrendData


class DataCollector:
    """Base class for data collectors"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })


class ProductHuntCollector(DataCollector):
    """Collector for Product Hunt trending products"""
    
    def collect_trending(self, limit: int = 10) -> List[ProductTrend]:
        """
        Collect trending products from Product Hunt
        
        Note: This uses RSS feed as the API requires authentication.
        For production use, consider using Product Hunt API with proper credentials.
        """
        trends = []
        try:
            feed = feedparser.parse('https://www.producthunt.com/feed')
            
            for entry in feed.entries[:limit]:
                source = TrendSource(
                    name="Product Hunt",
                    url=entry.get('link', ''),
                    fetched_at=datetime.utcnow()
                )
                
                # Extract category from tags if available
                category = "productivity"
                if hasattr(entry, 'tags') and entry.tags:
                    category = entry.tags[0].term.lower() if entry.tags else "productivity"
                
                trend = ProductTrend(
                    title=entry.title,
                    description=entry.get('summary', ''),
                    category=self._categorize(entry.title, entry.get('summary', '')),
                    source=source,
                    url=entry.get('link', ''),
                    traction_metrics={'source': 'producthunt'}
                )
                trends.append(trend)
        except Exception as e:
            print(f"Error collecting from Product Hunt: {e}")
        
        return trends
    
    def _categorize(self, title: str, description: str) -> str:
        """Simple categorization based on keywords"""
        text = (title + " " + description).lower()
        
        if any(word in text for word in ['health', 'fitness', 'wellness', 'medical']):
            return 'health'
        elif any(word in text for word in ['finance', 'fintech', 'banking', 'crypto', 'payment']):
            return 'fintech'
        elif any(word in text for word in ['social', 'community', 'chat', 'messaging']):
            return 'social'
        elif any(word in text for word in ['productivity', 'task', 'project', 'workflow']):
            return 'productivity'
        elif any(word in text for word in ['education', 'learning', 'course', 'teaching']):
            return 'education'
        else:
            return 'other'


class TechNewsCollector(DataCollector):
    """Collector for tech news from TechCrunch and The Verge"""
    
    def collect_techcrunch(self, limit: int = 10) -> List[ProductTrend]:
        """Collect from TechCrunch RSS feed"""
        trends = []
        try:
            feed = feedparser.parse('https://techcrunch.com/feed/')
            
            for entry in feed.entries[:limit]:
                source = TrendSource(
                    name="TechCrunch",
                    url=entry.get('link', ''),
                    fetched_at=datetime.utcnow()
                )
                
                trend = ProductTrend(
                    title=entry.title,
                    description=entry.get('summary', '')[:500],  # Truncate long descriptions
                    category=self._categorize_from_tags(entry),
                    source=source,
                    url=entry.get('link', ''),
                    traction_metrics={'source': 'techcrunch'}
                )
                trends.append(trend)
        except Exception as e:
            print(f"Error collecting from TechCrunch: {e}")
        
        return trends
    
    def collect_theverge(self, limit: int = 10) -> List[ProductTrend]:
        """Collect from The Verge RSS feed"""
        trends = []
        try:
            feed = feedparser.parse('https://www.theverge.com/rss/index.xml')
            
            for entry in feed.entries[:limit]:
                source = TrendSource(
                    name="The Verge",
                    url=entry.get('link', ''),
                    fetched_at=datetime.utcnow()
                )
                
                trend = ProductTrend(
                    title=entry.title,
                    description=entry.get('summary', '')[:500],
                    category=self._categorize_from_tags(entry),
                    source=source,
                    url=entry.get('link', ''),
                    traction_metrics={'source': 'theverge'}
                )
                trends.append(trend)
        except Exception as e:
            print(f"Error collecting from The Verge: {e}")
        
        return trends
    
    def _categorize_from_tags(self, entry) -> str:
        """Categorize based on entry tags or title"""
        text = entry.title.lower() + " " + entry.get('summary', '').lower()
        
        if any(word in text for word in ['ai', 'artificial intelligence', 'machine learning', 'llm']):
            return 'ai'
        elif any(word in text for word in ['health', 'medical', 'fitness']):
            return 'health'
        elif any(word in text for word in ['finance', 'fintech', 'crypto', 'blockchain']):
            return 'fintech'
        elif any(word in text for word in ['social', 'messaging', 'community']):
            return 'social'
        elif any(word in text for word in ['app', 'mobile', 'software']):
            return 'productivity'
        else:
            return 'tech'


class HackerNewsCollector(DataCollector):
    """Collector for Hacker News trending items"""
    
    BASE_URL = "https://hacker-news.firebaseio.com/v0"
    
    def collect_top_stories(self, limit: int = 10) -> List[ProductTrend]:
        """Collect top stories from Hacker News"""
        trends = []
        try:
            # Get top story IDs
            response = self.session.get(f"{self.BASE_URL}/topstories.json")
            story_ids = response.json()[:limit]
            
            for story_id in story_ids:
                story_response = self.session.get(f"{self.BASE_URL}/item/{story_id}.json")
                story = story_response.json()
                
                if not story or story.get('type') != 'story':
                    continue
                
                source = TrendSource(
                    name="Hacker News",
                    url=f"https://news.ycombinator.com/item?id={story_id}",
                    fetched_at=datetime.utcnow()
                )
                
                trend = ProductTrend(
                    title=story.get('title', ''),
                    description=story.get('text', story.get('title', ''))[:500],
                    category='tech',
                    source=source,
                    url=story.get('url', f"https://news.ycombinator.com/item?id={story_id}"),
                    traction_metrics={
                        'score': story.get('score', 0),
                        'comments': story.get('descendants', 0)
                    }
                )
                trends.append(trend)
        except Exception as e:
            print(f"Error collecting from Hacker News: {e}")
        
        return trends


class RedditCollector(DataCollector):
    """Collector for Reddit posts from tech-related subreddits"""
    
    def collect_from_subreddit(self, subreddit: str, limit: int = 10) -> List[ProductTrend]:
        """Collect top posts from a subreddit"""
        trends = []
        try:
            url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
            response = self.session.get(url)
            data = response.json()
            
            if 'data' not in data or 'children' not in data['data']:
                return trends
            
            for post in data['data']['children']:
                post_data = post['data']
                
                source = TrendSource(
                    name=f"Reddit r/{subreddit}",
                    url=f"https://reddit.com{post_data.get('permalink', '')}",
                    fetched_at=datetime.utcnow()
                )
                
                trend = ProductTrend(
                    title=post_data.get('title', ''),
                    description=post_data.get('selftext', '')[:500] if post_data.get('selftext') else post_data.get('title', ''),
                    category=self._categorize_subreddit(subreddit),
                    source=source,
                    url=post_data.get('url', ''),
                    traction_metrics={
                        'upvotes': post_data.get('ups', 0),
                        'comments': post_data.get('num_comments', 0),
                        'upvote_ratio': post_data.get('upvote_ratio', 0)
                    }
                )
                trends.append(trend)
        except Exception as e:
            print(f"Error collecting from Reddit r/{subreddit}: {e}")
        
        return trends
    
    def _categorize_subreddit(self, subreddit: str) -> str:
        """Map subreddit to category"""
        mapping = {
            'technology': 'tech',
            'gadgets': 'tech',
            'startups': 'startups',
            'entrepreneur': 'startups',
            'fintech': 'fintech',
            'health': 'health',
            'productivity': 'productivity'
        }
        return mapping.get(subreddit.lower(), 'other')


class YCombinatorCollector(DataCollector):
    """Collector for Y Combinator companies"""
    
    def collect_latest_batch(self, limit: int = 20) -> List[StartupInfo]:
        """
        Collect latest YC batch companies
        Note: This is a simplified version. For production, use proper YC API or scraping with permission.
        """
        startups = []
        try:
            # Using YC's companies page (public data)
            url = "https://www.ycombinator.com/companies"
            response = self.session.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # This is a placeholder - actual implementation would parse the page structure
            # For now, returning empty list as YC page structure requires more complex parsing
            print("YC Collector: Page structure parsing not fully implemented")
            
        except Exception as e:
            print(f"Error collecting from Y Combinator: {e}")
        
        return startups


class GoogleTrendsCollector:
    """Collector for Google Trends data"""
    
    def __init__(self):
        self._pytrends = None
    
    @property
    def pytrends(self):
        """Lazy-load pytrends to avoid network calls on initialization"""
        if self._pytrends is None:
            from pytrends.request import TrendReq
            self._pytrends = TrendReq(hl='en-US', tz=360)
        return self._pytrends
    
    def collect_rising_trends(self, keywords: List[str], category: str = 'tech') -> List[GoogleTrendData]:
        """Collect Google Trends data for keywords"""
        trends_data = []
        
        try:
            # Build payload for keywords
            self.pytrends.build_payload(keywords, cat=0, timeframe='now 7-d', geo='US')
            
            # Get interest over time
            interest_df = self.pytrends.interest_over_time()
            
            # Get related queries
            related_queries = self.pytrends.related_queries()
            
            for keyword in keywords:
                interest_data = []
                if keyword in interest_df.columns:
                    for idx, row in interest_df.iterrows():
                        interest_data.append({
                            'date': str(idx),
                            'interest': int(row[keyword])
                        })
                
                related = []
                if keyword in related_queries and related_queries[keyword]['rising'] is not None:
                    related = related_queries[keyword]['rising']['query'].tolist()[:5]
                
                trend_data = GoogleTrendData(
                    keyword=keyword,
                    interest_over_time=interest_data,
                    related_queries=related,
                    category=category
                )
                trends_data.append(trend_data)
                
        except Exception as e:
            print(f"Error collecting Google Trends data: {e}")
        
        return trends_data


class TrendDataAggregator:
    """Aggregates data from all sources"""
    
    def __init__(self):
        self.ph_collector = ProductHuntCollector()
        self.tech_collector = TechNewsCollector()
        self.hn_collector = HackerNewsCollector()
        self.reddit_collector = RedditCollector()
        self.yc_collector = YCombinatorCollector()
        self.google_trends = GoogleTrendsCollector()
    
    def collect_all_trends(self, 
                          include_product_hunt: bool = True,
                          include_tech_news: bool = True,
                          include_hacker_news: bool = True,
                          include_reddit: bool = True,
                          subreddits: List[str] = None) -> List[ProductTrend]:
        """Collect trends from all enabled sources"""
        all_trends = []
        
        if include_product_hunt:
            print("Collecting from Product Hunt...")
            all_trends.extend(self.ph_collector.collect_trending(limit=10))
        
        if include_tech_news:
            print("Collecting from TechCrunch...")
            all_trends.extend(self.tech_collector.collect_techcrunch(limit=10))
            print("Collecting from The Verge...")
            all_trends.extend(self.tech_collector.collect_theverge(limit=10))
        
        if include_hacker_news:
            print("Collecting from Hacker News...")
            all_trends.extend(self.hn_collector.collect_top_stories(limit=10))
        
        if include_reddit and subreddits:
            for subreddit in subreddits:
                print(f"Collecting from Reddit r/{subreddit}...")
                all_trends.extend(self.reddit_collector.collect_from_subreddit(subreddit, limit=5))
        
        return all_trends
    
    def collect_google_trends(self, keywords: List[str], category: str = 'tech') -> List[GoogleTrendData]:
        """Collect Google Trends data for specified keywords"""
        print(f"Collecting Google Trends for keywords: {', '.join(keywords)}")
        return self.google_trends.collect_rising_trends(keywords, category)
    
    def collect_startups(self) -> List[StartupInfo]:
        """Collect startup information"""
        print("Collecting YC startup data...")
        return self.yc_collector.collect_latest_batch(limit=20)
