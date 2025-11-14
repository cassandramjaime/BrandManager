"""
Paper fetchers for various sources (arXiv, Papers with Code, Hugging Face, etc.)
"""
import time
import requests
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Optional
from xml.etree import ElementTree as ET

from .paper_models import Paper, PaperSource, PaperFilter


class RateLimiter:
    """Simple rate limiter to respect API limits"""
    
    def __init__(self, calls_per_second: float = 1.0):
        """
        Initialize rate limiter
        
        Args:
            calls_per_second: Maximum number of calls per second
        """
        self.calls_per_second = calls_per_second
        self.min_interval = 1.0 / calls_per_second
        self.last_call = 0.0
    
    def wait(self):
        """Wait if necessary to respect rate limit"""
        now = time.time()
        time_since_last = now - self.last_call
        if time_since_last < self.min_interval:
            time.sleep(self.min_interval - time_since_last)
        self.last_call = time.time()


class PaperFetcher(ABC):
    """Abstract base class for paper fetchers"""
    
    def __init__(self, rate_limiter: Optional[RateLimiter] = None):
        """
        Initialize paper fetcher
        
        Args:
            rate_limiter: Optional rate limiter
        """
        self.rate_limiter = rate_limiter or RateLimiter(calls_per_second=1.0)
    
    @abstractmethod
    def fetch_papers(self, filters: PaperFilter) -> List[Paper]:
        """
        Fetch papers based on filters
        
        Args:
            filters: PaperFilter object
            
        Returns:
            List of Paper objects
        """
        pass


class ArXivFetcher(PaperFetcher):
    """Fetcher for arXiv papers"""
    
    BASE_URL = "http://export.arxiv.org/api/query"
    
    def __init__(self, rate_limiter: Optional[RateLimiter] = None):
        """Initialize arXiv fetcher with rate limiting (3 seconds per request)"""
        super().__init__(rate_limiter or RateLimiter(calls_per_second=0.33))
    
    def fetch_papers(self, filters: PaperFilter) -> List[Paper]:
        """
        Fetch papers from arXiv
        
        Args:
            filters: PaperFilter object
            
        Returns:
            List of Paper objects
        """
        papers = []
        
        # Map topics to arXiv categories
        categories = self._get_arxiv_categories(filters)
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=filters.days_back)
        
        # Build search query
        search_terms = []
        
        # Add category filters
        if categories:
            cat_query = " OR ".join([f"cat:{cat}" for cat in categories])
            search_terms.append(f"({cat_query})")
        
        # Add keyword filters
        if filters.keywords:
            keyword_query = " OR ".join([f'all:"{kw}"' for kw in filters.keywords])
            search_terms.append(f"({keyword_query})")
        
        # Combine search terms
        search_query = " AND ".join(search_terms) if search_terms else "cat:cs.AI OR cat:cs.LG OR cat:cs.CL"
        
        # Fetch papers in batches
        max_results = 200  # Limit to avoid overloading
        start = 0
        batch_size = 100
        
        while start < max_results:
            self.rate_limiter.wait()
            
            params = {
                'search_query': search_query,
                'start': start,
                'max_results': batch_size,
                'sortBy': 'submittedDate',
                'sortOrder': 'descending'
            }
            
            try:
                response = requests.get(self.BASE_URL, params=params, timeout=30)
                response.raise_for_status()
                
                batch_papers = self._parse_arxiv_response(response.text, start_date, end_date)
                
                if not batch_papers:
                    break  # No more papers in date range
                
                papers.extend(batch_papers)
                start += batch_size
                
                # If we got fewer papers than batch_size, we've reached the end
                if len(batch_papers) < batch_size:
                    break
                    
            except requests.RequestException as e:
                print(f"Error fetching from arXiv: {e}")
                break
        
        return papers
    
    def _get_arxiv_categories(self, filters: PaperFilter) -> List[str]:
        """Map topic filters to arXiv categories"""
        category_map = {
            'llms': ['cs.CL', 'cs.LG'],
            'computer_vision': ['cs.CV'],
            'reinforcement_learning': ['cs.LG', 'cs.AI'],
            'ai_safety': ['cs.AI', 'cs.CY'],
            'nlp': ['cs.CL'],
            'generative_ai': ['cs.LG', 'cs.AI'],
            'multimodal': ['cs.CV', 'cs.CL']
        }
        
        categories = set()
        if filters.topics:
            for topic in filters.topics:
                if topic.value in category_map:
                    categories.update(category_map[topic.value])
        
        # Default categories if none specified
        if not categories:
            categories = {'cs.AI', 'cs.LG', 'cs.CL'}
        
        return list(categories)
    
    def _parse_arxiv_response(self, xml_text: str, start_date: datetime, end_date: datetime) -> List[Paper]:
        """Parse arXiv API XML response"""
        papers = []
        
        try:
            root = ET.fromstring(xml_text)
            
            # Define namespace
            ns = {'atom': 'http://www.w3.org/2005/Atom',
                  'arxiv': 'http://arxiv.org/schemas/atom'}
            
            for entry in root.findall('atom:entry', ns):
                try:
                    # Extract paper ID
                    paper_id = entry.find('atom:id', ns).text.split('/')[-1]
                    
                    # Extract publication date
                    published = entry.find('atom:published', ns).text
                    pub_date = datetime.fromisoformat(published.replace('Z', '+00:00'))
                    
                    # Filter by date range
                    if pub_date < start_date or pub_date > end_date:
                        continue
                    
                    # Extract title
                    title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
                    
                    # Extract authors
                    authors = [author.find('atom:name', ns).text 
                              for author in entry.findall('atom:author', ns)]
                    
                    # Extract abstract
                    abstract = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
                    
                    # Extract URL
                    url = entry.find('atom:id', ns).text
                    
                    # Extract PDF URL
                    pdf_link = entry.find('atom:link[@title="pdf"]', ns)
                    pdf_url = pdf_link.get('href') if pdf_link is not None else None
                    
                    # Extract categories
                    categories = [cat.get('term') for cat in entry.findall('atom:category', ns)]
                    
                    paper = Paper(
                        paper_id=paper_id,
                        title=title,
                        authors=authors,
                        abstract=abstract,
                        publication_date=pub_date,
                        source=PaperSource.ARXIV,
                        url=url,
                        pdf_url=pdf_url,
                        citation_count=0,  # arXiv doesn't provide citation counts
                        categories=categories
                    )
                    
                    papers.append(paper)
                    
                except (AttributeError, ValueError) as e:
                    # Skip malformed entries
                    continue
        
        except ET.ParseError as e:
            print(f"Error parsing arXiv XML: {e}")
        
        return papers


class PapersWithCodeFetcher(PaperFetcher):
    """Fetcher for Papers with Code"""
    
    BASE_URL = "https://paperswithcode.com/api/v1/papers/"
    
    def fetch_papers(self, filters: PaperFilter) -> List[Paper]:
        """
        Fetch papers from Papers with Code
        
        Args:
            filters: PaperFilter object
            
        Returns:
            List of Paper objects
        """
        papers = []
        
        # Papers with Code API doesn't require authentication but has rate limits
        self.rate_limiter.wait()
        
        try:
            params = {
                'ordering': '-published',
                'items_per_page': 100
            }
            
            response = requests.get(self.BASE_URL, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=filters.days_back)
            
            for item in data.get('results', []):
                try:
                    # Parse publication date
                    pub_date_str = item.get('published')
                    if not pub_date_str:
                        continue
                    
                    pub_date = datetime.fromisoformat(pub_date_str.replace('Z', '+00:00'))
                    
                    # Filter by date
                    if pub_date < start_date or pub_date > end_date:
                        continue
                    
                    # Extract paper info
                    paper_id = item.get('id', item.get('arxiv_id', ''))
                    
                    paper = Paper(
                        paper_id=f"pwc_{paper_id}",
                        title=item.get('title', ''),
                        authors=item.get('authors', []),
                        abstract=item.get('abstract', ''),
                        publication_date=pub_date,
                        source=PaperSource.PAPERS_WITH_CODE,
                        url=item.get('url_abs', ''),
                        pdf_url=item.get('url_pdf'),
                        citation_count=0,  # May not be available
                        categories=[]
                    )
                    
                    papers.append(paper)
                    
                except (ValueError, KeyError) as e:
                    continue
        
        except requests.RequestException as e:
            print(f"Error fetching from Papers with Code: {e}")
        
        return papers


class HuggingFaceFetcher(PaperFetcher):
    """Fetcher for Hugging Face papers"""
    
    BASE_URL = "https://huggingface.co/api/daily_papers"
    
    def fetch_papers(self, filters: PaperFilter) -> List[Paper]:
        """
        Fetch papers from Hugging Face daily papers
        
        Args:
            filters: PaperFilter object
            
        Returns:
            List of Paper objects
        """
        papers = []
        
        self.rate_limiter.wait()
        
        try:
            response = requests.get(self.BASE_URL, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=filters.days_back)
            
            for item in data:
                try:
                    # Parse date from the item
                    pub_date_str = item.get('publishedAt')
                    if not pub_date_str:
                        # Use current date if not available
                        pub_date = datetime.now()
                    else:
                        pub_date = datetime.fromisoformat(pub_date_str.replace('Z', '+00:00'))
                    
                    # Filter by date
                    if pub_date < start_date:
                        continue
                    
                    # Extract paper info
                    paper = Paper(
                        paper_id=f"hf_{item.get('id', '')}",
                        title=item.get('title', ''),
                        authors=item.get('authors', []),
                        abstract=item.get('summary', ''),
                        publication_date=pub_date,
                        source=PaperSource.HUGGING_FACE,
                        url=item.get('url', ''),
                        pdf_url=None,
                        citation_count=item.get('upvotes', 0),
                        categories=[]
                    )
                    
                    papers.append(paper)
                    
                except (ValueError, KeyError) as e:
                    continue
        
        except requests.RequestException as e:
            print(f"Error fetching from Hugging Face: {e}")
        
        return papers


class PaperFetcherManager:
    """Manager for coordinating multiple paper fetchers"""
    
    def __init__(self):
        """Initialize the fetcher manager"""
        self.fetchers = {
            PaperSource.ARXIV: ArXivFetcher(),
            PaperSource.PAPERS_WITH_CODE: PapersWithCodeFetcher(),
            PaperSource.HUGGING_FACE: HuggingFaceFetcher(),
        }
    
    def fetch_papers(self, filters: PaperFilter) -> List[Paper]:
        """
        Fetch papers from all specified sources
        
        Args:
            filters: PaperFilter object
            
        Returns:
            Combined list of Paper objects from all sources
        """
        all_papers = []
        
        # Determine which sources to use
        sources = filters.sources if filters.sources else list(self.fetchers.keys())
        
        for source in sources:
            if source in self.fetchers:
                print(f"Fetching papers from {source.value}...")
                try:
                    papers = self.fetchers[source].fetch_papers(filters)
                    all_papers.extend(papers)
                    print(f"  Found {len(papers)} papers from {source.value}")
                except Exception as e:
                    print(f"  Error fetching from {source.value}: {e}")
        
        # Remove duplicates by paper_id
        unique_papers = {}
        for paper in all_papers:
            if paper.paper_id not in unique_papers:
                unique_papers[paper.paper_id] = paper
        
        return list(unique_papers.values())
