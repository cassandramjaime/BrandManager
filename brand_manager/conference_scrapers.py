"""
Base scraper class and specific implementations for conference data sources
"""
import re
import requests
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

from .conference_models import Conference, LocationType, TopicFocus


class ConferenceScraper(ABC):
    """Base class for conference scrapers"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    @abstractmethod
    def scrape_conferences(self) -> List[Conference]:
        """Scrape conferences from the source"""
        pass
    
    def _parse_date(self, date_str: str) -> Optional[datetime]:
        """Parse various date formats"""
        # Common date formats
        formats = [
            "%Y-%m-%d",
            "%B %d, %Y",
            "%b %d, %Y",
            "%m/%d/%Y",
            "%d/%m/%Y",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S"
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str.strip(), fmt)
            except ValueError:
                continue
        
        return None
    
    def _extract_price(self, price_str: str) -> Optional[float]:
        """Extract price from string"""
        if not price_str or price_str.lower() in ['free', 'tbd', 'tba']:
            return None
        
        # Remove currency symbols and extract number
        price_match = re.search(r'[\d,]+\.?\d*', price_str.replace(',', ''))
        if price_match:
            try:
                return float(price_match.group())
            except ValueError:
                return None
        return None


class ManualConferenceScraper(ConferenceScraper):
    """Manual scraper for well-known PM conferences with static data"""
    
    def scrape_conferences(self) -> List[Conference]:
        """Return a curated list of well-known PM conferences"""
        conferences = []
        
        # ProductCon
        conferences.append(Conference(
            name="ProductCon - San Francisco",
            start_date=datetime(2024, 10, 15, 9, 0),
            end_date=datetime(2024, 10, 15, 18, 0),
            location="San Francisco, CA",
            location_type=LocationType.IN_PERSON,
            ticket_price_min=299.0,
            ticket_price_max=799.0,
            notable_speakers=[
                "Product Leaders from Google, Meta, Amazon",
                "VP of Product - Airbnb",
                "CPO - Stripe"
            ],
            agenda_topics=[
                "AI in Product Management",
                "Product Strategy & Vision",
                "User Research & Analytics",
                "Product-Led Growth"
            ],
            registration_deadline=datetime(2024, 10, 10, 23, 59),
            url="https://productcon.com/sf",
            source="ProductCon",
            description="The largest product management conference for learning and networking",
            topic_focus=[TopicFocus.AI_ML, TopicFocus.GENERAL_PM, TopicFocus.ENTERPRISE]
        ))
        
        # Mind the Product
        conferences.append(Conference(
            name="Mind the Product - San Francisco",
            start_date=datetime(2024, 11, 8, 9, 0),
            end_date=datetime(2024, 11, 9, 18, 0),
            location="San Francisco, CA",
            location_type=LocationType.IN_PERSON,
            ticket_price_min=599.0,
            ticket_price_max=999.0,
            notable_speakers=[
                "Marty Cagan - Silicon Valley Product Group",
                "Teresa Torres - Product Discovery Coach",
                "Gibson Biddle - Former VP Product at Netflix"
            ],
            agenda_topics=[
                "Product Discovery",
                "Product Leadership",
                "Building Product Teams",
                "AI & Machine Learning Products"
            ],
            registration_deadline=datetime(2024, 11, 1, 23, 59),
            url="https://www.mindtheproduct.com/mtpcon/san-francisco/",
            source="Mind the Product",
            description="Premier product management conference with focus on leadership and discovery",
            topic_focus=[TopicFocus.GENERAL_PM, TopicFocus.AI_ML, TopicFocus.B2B]
        ))
        
        # Product School Summit
        conferences.append(Conference(
            name="Product School Summit - Virtual",
            start_date=datetime(2024, 12, 5, 10, 0),
            end_date=datetime(2024, 12, 5, 16, 0),
            location="Virtual",
            location_type=LocationType.VIRTUAL,
            ticket_price_min=0.0,
            ticket_price_max=199.0,
            notable_speakers=[
                "Product Directors from Microsoft, Adobe",
                "AI Product Leaders",
                "Product Design Experts"
            ],
            agenda_topics=[
                "AI-Powered Product Management",
                "Product Metrics & Analytics",
                "Product Design Thinking",
                "Career Growth for PMs"
            ],
            registration_deadline=datetime(2024, 12, 4, 23, 59),
            url="https://productschool.com/product-summit",
            source="Product School",
            description="Virtual summit focused on AI and modern product management practices",
            topic_focus=[TopicFocus.AI_ML, TopicFocus.GENERAL_PM, TopicFocus.DATA]
        ))
        
        # Industry - The Product Conference
        conferences.append(Conference(
            name="Industry: The Product Conference - Dublin",
            start_date=datetime(2024, 9, 25, 9, 0),
            end_date=datetime(2024, 9, 27, 18, 0),
            location="Dublin, Ireland",
            location_type=LocationType.IN_PERSON,
            ticket_price_min=450.0,
            ticket_price_max=850.0,
            notable_speakers=[
                "Product Leaders from European Tech Companies",
                "Design & Product Integration Experts"
            ],
            agenda_topics=[
                "Product Strategy",
                "Design & Product Collaboration",
                "European Product Market",
                "AI Integration"
            ],
            registration_deadline=datetime(2024, 9, 20, 23, 59),
            url="https://industryconference.com",
            source="Industry Conference",
            description="Europe's leading product conference bringing together product & design",
            topic_focus=[TopicFocus.GENERAL_PM, TopicFocus.DESIGN, TopicFocus.B2B]
        ))
        
        # Product Drive
        conferences.append(Conference(
            name="Product Drive - Online Summit",
            start_date=datetime(2024, 10, 20, 8, 0),
            end_date=datetime(2024, 10, 21, 17, 0),
            location="Virtual",
            location_type=LocationType.VIRTUAL,
            ticket_price_min=0.0,
            ticket_price_max=99.0,
            notable_speakers=[
                "Product Managers from Fortune 500",
                "Startup Product Leaders"
            ],
            agenda_topics=[
                "Product Roadmapping",
                "Stakeholder Management",
                "Product Analytics",
                "AI Tools for PMs"
            ],
            registration_deadline=datetime(2024, 10, 19, 23, 59),
            url="https://productdrive.io",
            source="Product Drive",
            description="Virtual conference for product managers at all career stages",
            topic_focus=[TopicFocus.GENERAL_PM, TopicFocus.AI_ML, TopicFocus.B2C]
        ))
        
        # Web Summit (Product Track)
        conferences.append(Conference(
            name="Web Summit - Lisbon (Product Track)",
            start_date=datetime(2024, 11, 11, 9, 0),
            end_date=datetime(2024, 11, 14, 19, 0),
            location="Lisbon, Portugal",
            location_type=LocationType.IN_PERSON,
            ticket_price_min=895.0,
            ticket_price_max=2495.0,
            notable_speakers=[
                "CEOs and Product Leaders from Global Tech Companies",
                "AI Researchers & Product Innovators"
            ],
            agenda_topics=[
                "Future of AI Products",
                "Product Innovation",
                "Global Tech Trends",
                "Consumer Technology"
            ],
            registration_deadline=datetime(2024, 11, 5, 23, 59),
            url="https://websummit.com",
            source="Web Summit",
            description="One of the world's largest tech conferences with extensive product tracks",
            topic_focus=[TopicFocus.AI_ML, TopicFocus.CONSUMER_PRODUCTS, TopicFocus.ENTERPRISE]
        ))
        
        # AI Product Summit
        conferences.append(Conference(
            name="AI Product Summit - New York",
            start_date=datetime(2024, 12, 12, 9, 0),
            end_date=datetime(2024, 12, 13, 18, 0),
            location="New York, NY",
            location_type=LocationType.HYBRID,
            ticket_price_min=399.0,
            ticket_price_max=899.0,
            notable_speakers=[
                "AI Product Leaders from OpenAI, Google DeepMind",
                "ML Product Managers",
                "AI Ethics Experts"
            ],
            agenda_topics=[
                "Building AI-First Products",
                "ML Model Integration",
                "AI Product Ethics & Safety",
                "Generative AI Applications"
            ],
            registration_deadline=datetime(2024, 12, 8, 23, 59),
            url="https://aiproductsummit.com",
            source="AI Product Summit",
            description="Specialized conference for AI and ML product management",
            topic_focus=[TopicFocus.AI_ML, TopicFocus.DATA, TopicFocus.ENTERPRISE]
        ))
        
        # Product Management Festival
        conferences.append(Conference(
            name="Product Management Festival - Zurich",
            start_date=datetime(2024, 10, 10, 9, 0),
            end_date=datetime(2024, 10, 11, 18, 0),
            location="Zurich, Switzerland",
            location_type=LocationType.IN_PERSON,
            ticket_price_min=550.0,
            ticket_price_max=950.0,
            notable_speakers=[
                "European Product Leaders",
                "Product Strategy Consultants"
            ],
            agenda_topics=[
                "Product Vision & Strategy",
                "Team Leadership",
                "Product Discovery Methods",
                "Innovation in Product"
            ],
            registration_deadline=datetime(2024, 10, 5, 23, 59),
            url="https://productmanagementfestival.com",
            source="Product Management Festival",
            description="Bringing together product professionals from across Europe",
            topic_focus=[TopicFocus.GENERAL_PM, TopicFocus.B2B, TopicFocus.ENTERPRISE]
        ))
        
        return conferences


class EventbriteConferenceScraper(ConferenceScraper):
    """Scraper for Eventbrite (uses mock data for demo)"""
    
    def scrape_conferences(self) -> List[Conference]:
        """
        Scrape conferences from Eventbrite
        Note: This is a simplified version that returns sample data.
        Real implementation would use Eventbrite API with proper authentication.
        """
        # In production, use Eventbrite API: https://www.eventbrite.com/platform/api
        # For now, return sample conferences
        conferences = []
        
        conferences.append(Conference(
            name="Product Leaders Meetup - Seattle",
            start_date=datetime(2024, 11, 15, 18, 0),
            end_date=datetime(2024, 11, 15, 21, 0),
            location="Seattle, WA",
            location_type=LocationType.IN_PERSON,
            ticket_price_min=25.0,
            ticket_price_max=50.0,
            notable_speakers=["Local Product Leaders"],
            agenda_topics=["Networking", "Product Trends", "Career Development"],
            registration_deadline=datetime(2024, 11, 14, 23, 59),
            url="https://eventbrite.com/e/product-leaders-seattle",
            source="Eventbrite",
            description="Monthly meetup for product professionals in Seattle",
            topic_focus=[TopicFocus.GENERAL_PM]
        ))
        
        return conferences


class LumaConferenceScraper(ConferenceScraper):
    """Scraper for Luma events (uses mock data for demo)"""
    
    def scrape_conferences(self) -> List[Conference]:
        """
        Scrape conferences from Luma
        Note: This is a simplified version that returns sample data.
        Real implementation would scrape Luma or use their API if available.
        """
        conferences = []
        
        conferences.append(Conference(
            name="AI Product Managers Virtual Meetup",
            start_date=datetime(2024, 10, 30, 12, 0),
            end_date=datetime(2024, 10, 30, 13, 30),
            location="Virtual",
            location_type=LocationType.VIRTUAL,
            ticket_price_min=0.0,
            ticket_price_max=0.0,
            notable_speakers=["AI PM Community Leaders"],
            agenda_topics=["AI Product Challenges", "LLM Integration", "AI Ethics"],
            registration_deadline=datetime(2024, 10, 29, 23, 59),
            url="https://lu.ma/ai-pm-meetup",
            source="Luma",
            description="Virtual meetup for AI product managers",
            topic_focus=[TopicFocus.AI_ML]
        ))
        
        return conferences


class ConferenceAggregator:
    """Aggregates conferences from multiple sources"""
    
    def __init__(self):
        self.scrapers = [
            ManualConferenceScraper(),
            EventbriteConferenceScraper(),
            LumaConferenceScraper()
        ]
    
    def aggregate_conferences(self) -> List[Conference]:
        """
        Aggregate conferences from all sources
        
        Returns:
            List of all conferences from all sources
        """
        all_conferences = []
        
        for scraper in self.scrapers:
            try:
                conferences = scraper.scrape_conferences()
                all_conferences.extend(conferences)
            except Exception as e:
                print(f"Error scraping from {scraper.__class__.__name__}: {e}")
                continue
        
        return all_conferences
