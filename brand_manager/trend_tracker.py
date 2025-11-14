"""
Main trend tracker orchestrator
"""
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from .data_sources import TrendDataAggregator
from .trend_analyzer import TrendAnalyzer
from .storage import TrendStorage
from .visualizations import TrendVisualizer
from .report_generator import ReportGenerator
from .trend_models import WeeklyTrendReport, TrackedCategories


class TrendTracker:
    """Main orchestrator for consumer product trend tracking"""
    
    def __init__(self, 
                 openai_api_key: str = None,
                 storage_dir: str = None,
                 viz_dir: str = None,
                 report_dir: str = None):
        """Initialize the trend tracker"""
        self.aggregator = TrendDataAggregator()
        self._analyzer = None
        self._openai_api_key = openai_api_key
        self.storage = TrendStorage(storage_dir=storage_dir)
        self.visualizer = TrendVisualizer(output_dir=viz_dir)
        self.report_generator = ReportGenerator(output_dir=report_dir)
    
    @property
    def analyzer(self):
        """Lazy-load analyzer to allow initialization without API key"""
        if self._analyzer is None:
            self._analyzer = TrendAnalyzer(api_key=self._openai_api_key)
        return self._analyzer
    
    def collect_current_trends(self,
                               product_hunt: bool = True,
                               tech_news: bool = True,
                               hacker_news: bool = True,
                               reddit: bool = True,
                               reddit_subs: List[str] = None) -> List:
        """
        Collect current trends from all sources
        
        Args:
            product_hunt: Include Product Hunt
            tech_news: Include TechCrunch and The Verge
            hacker_news: Include Hacker News
            reddit: Include Reddit
            reddit_subs: List of subreddits to track
            
        Returns:
            List of ProductTrend objects
        """
        if reddit_subs is None:
            reddit_subs = ['technology', 'gadgets', 'startups']
        
        print("🔍 Collecting trends from data sources...")
        
        trends = self.aggregator.collect_all_trends(
            include_product_hunt=product_hunt,
            include_tech_news=tech_news,
            include_hacker_news=hacker_news,
            include_reddit=reddit,
            subreddits=reddit_subs if reddit else []
        )
        
        print(f"✓ Collected {len(trends)} trends from {sum([product_hunt, tech_news, hacker_news, reddit])} source groups")
        
        # Save to storage
        saved_path = self.storage.save_trends(trends)
        print(f"✓ Saved trends to {saved_path}")
        
        return trends
    
    def collect_google_trends(self, keywords: List[str] = None, category: str = 'tech') -> List:
        """
        Collect Google Trends data
        
        Args:
            keywords: List of keywords to track
            category: Category for the keywords
            
        Returns:
            List of GoogleTrendData objects
        """
        if keywords is None:
            keywords = ['ai', 'fintech', 'health tech', 'productivity app', 'social network']
        
        print(f"📊 Collecting Google Trends for {len(keywords)} keywords...")
        
        trends_data = self.aggregator.collect_google_trends(keywords, category)
        
        if trends_data:
            saved_path = self.storage.save_google_trends(trends_data)
            print(f"✓ Saved Google Trends to {saved_path}")
        
        return trends_data
    
    def generate_weekly_report(self,
                              start_date: datetime = None,
                              end_date: datetime = None,
                              generate_pdf: bool = True,
                              generate_markdown: bool = True) -> WeeklyTrendReport:
        """
        Generate a comprehensive weekly trend report
        
        Args:
            start_date: Start of the reporting period (defaults to 7 days ago)
            end_date: End of the reporting period (defaults to now)
            generate_pdf: Whether to generate PDF report
            generate_markdown: Whether to generate Markdown report
            
        Returns:
            WeeklyTrendReport object
        """
        # Default to last 7 days
        if end_date is None:
            end_date = datetime.utcnow()
        if start_date is None:
            start_date = end_date - timedelta(days=7)
        
        print(f"\n📊 Generating weekly trend report...")
        print(f"   Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        
        # Load trends from storage
        print("   Loading trend data...")
        trends = self.storage.load_trends(start_date, end_date)
        
        if not trends:
            print("   ⚠️  No trends found in the specified period")
            return None
        
        print(f"   ✓ Loaded {len(trends)} trends")
        
        # Analyze trends
        print("   Analyzing trends with AI...")
        analysis = self.analyzer.analyze_trends(trends)
        print("   ✓ Analysis complete")
        
        # Rank top trends
        print("   Ranking top trends...")
        top_trends = self.analyzer.rank_trends(trends, top_n=10)
        print("   ✓ Top 10 trends identified")
        
        # Category breakdown
        print("   Calculating category breakdown...")
        category_insights = self.analyzer.generate_category_insights(trends)
        category_breakdown = category_insights['breakdown']
        print(f"   ✓ Found {len(category_breakdown)} categories")
        
        # Get tracked categories
        config = self.storage.load_categories_config()
        
        # Create report
        report_id = f"{start_date.strftime('%Y-W%U')}"
        report = WeeklyTrendReport(
            report_id=report_id,
            week_start=start_date,
            week_end=end_date,
            top_trends=top_trends,
            category_breakdown=category_breakdown,
            analysis=analysis,
            total_items_analyzed=len(trends),
            categories_tracked=config.categories
        )
        
        # Save report
        print("   Saving report...")
        saved_report_path = self.storage.save_weekly_report(report)
        print(f"   ✓ Report saved to {saved_report_path}")
        
        # Generate visualizations
        print("   Creating visualizations...")
        historical_data = self.storage.get_historical_patterns(days=30)
        viz_paths = self.visualizer.create_all_visualizations(report, historical_data)
        print(f"   ✓ Created {len(viz_paths)} visualizations")
        
        # Generate output reports
        output_paths = {}
        
        if generate_markdown:
            print("   Generating Markdown report...")
            md_path = self.report_generator.generate_markdown_report(report, viz_paths)
            output_paths['markdown'] = md_path
            print(f"   ✓ Markdown report: {md_path}")
        
        if generate_pdf:
            print("   Generating PDF report...")
            pdf_path = self.report_generator.generate_pdf_report(report, viz_paths)
            output_paths['pdf'] = pdf_path
            print(f"   ✓ PDF report: {pdf_path}")
        
        print(f"\n✅ Weekly report generation complete!")
        print(f"   Report ID: {report_id}")
        print(f"   Trends analyzed: {len(trends)}")
        print(f"   Top categories: {', '.join([cat for cat, _ in category_insights['top_categories'][:3]])}")
        
        return report
    
    def track_categories(self, categories: List[str] = None, custom_keywords: Dict[str, List[str]] = None):
        """
        Update tracked categories configuration
        
        Args:
            categories: List of categories to track
            custom_keywords: Dictionary mapping categories to custom keywords
        """
        config = TrackedCategories(
            categories=categories or ["social", "fintech", "health", "productivity", "education", "ecommerce"],
            custom_keywords=custom_keywords or {}
        )
        
        saved_path = self.storage.save_categories_config(config)
        print(f"✓ Updated tracked categories: {', '.join(config.categories)}")
        print(f"  Saved to {saved_path}")
        
        return config
    
    def get_historical_insights(self, days: int = 30) -> Dict[str, Any]:
        """
        Get historical pattern analysis
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Dictionary with historical insights
        """
        print(f"📈 Analyzing historical patterns over {days} days...")
        
        insights = self.storage.get_historical_patterns(days=days)
        
        print(f"✓ Analysis complete")
        print(f"  Total trends: {insights['total_trends']}")
        print(f"  Sources: {len(insights['popular_sources'])}")
        print(f"  Days with data: {len(insights['daily_counts'])}")
        
        return insights
    
    def run_full_collection_and_report(self) -> WeeklyTrendReport:
        """
        Run a complete collection cycle and generate a report
        This is useful for scheduled/automated runs
        """
        print("🚀 Starting full trend collection and analysis cycle...\n")
        
        # Collect current trends
        trends = self.collect_current_trends()
        
        # Collect Google Trends
        google_trends = self.collect_google_trends()
        
        # Generate report from last 7 days
        report = self.generate_weekly_report()
        
        return report
