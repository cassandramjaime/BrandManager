"""
Data storage for historical trend tracking
"""
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from pathlib import Path

from .trend_models import ProductTrend, WeeklyTrendReport, GoogleTrendData, StartupInfo, TrackedCategories


class TrendStorage:
    """Handles storage and retrieval of historical trend data"""
    
    def __init__(self, storage_dir: str = None):
        """Initialize storage with directory path"""
        self.storage_dir = Path(storage_dir or os.path.join(os.getcwd(), "trend_data"))
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        self.trends_dir = self.storage_dir / "trends"
        self.reports_dir = self.storage_dir / "reports"
        self.google_trends_dir = self.storage_dir / "google_trends"
        self.startups_dir = self.storage_dir / "startups"
        
        for directory in [self.trends_dir, self.reports_dir, self.google_trends_dir, self.startups_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def save_trends(self, trends: List[ProductTrend], date: datetime = None) -> str:
        """Save trends data to file"""
        if date is None:
            date = datetime.utcnow()
        
        filename = f"trends_{date.strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.trends_dir / filename
        
        data = {
            'timestamp': date.isoformat(),
            'count': len(trends),
            'trends': [trend.model_dump(mode='json') for trend in trends]
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        return str(filepath)
    
    def save_weekly_report(self, report: WeeklyTrendReport) -> str:
        """Save weekly report"""
        filename = f"report_{report.report_id}.json"
        filepath = self.reports_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(report.model_dump(mode='json'), f, indent=2, default=str)
        
        return str(filepath)
    
    def save_google_trends(self, trends_data: List[GoogleTrendData], date: datetime = None) -> str:
        """Save Google Trends data"""
        if date is None:
            date = datetime.utcnow()
        
        filename = f"google_trends_{date.strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.google_trends_dir / filename
        
        data = {
            'timestamp': date.isoformat(),
            'trends': [trend.model_dump(mode='json') for trend in trends_data]
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        return str(filepath)
    
    def save_startups(self, startups: List[StartupInfo], date: datetime = None) -> str:
        """Save startup information"""
        if date is None:
            date = datetime.utcnow()
        
        filename = f"startups_{date.strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.startups_dir / filename
        
        data = {
            'timestamp': date.isoformat(),
            'startups': [startup.model_dump(mode='json') for startup in startups]
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        return str(filepath)
    
    def load_trends(self, start_date: datetime = None, end_date: datetime = None) -> List[ProductTrend]:
        """Load trends within a date range"""
        all_trends = []
        
        for filepath in sorted(self.trends_dir.glob("trends_*.json")):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                file_date = datetime.fromisoformat(data['timestamp'])
                
                # Filter by date range if specified
                if start_date and file_date < start_date:
                    continue
                if end_date and file_date > end_date:
                    continue
                
                for trend_data in data['trends']:
                    trend = ProductTrend(**trend_data)
                    all_trends.append(trend)
            except Exception as e:
                print(f"Error loading {filepath}: {e}")
        
        return all_trends
    
    def load_reports(self, limit: int = 10) -> List[WeeklyTrendReport]:
        """Load most recent weekly reports"""
        reports = []
        
        for filepath in sorted(self.reports_dir.glob("report_*.json"), reverse=True)[:limit]:
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                report = WeeklyTrendReport(**data)
                reports.append(report)
            except Exception as e:
                print(f"Error loading {filepath}: {e}")
        
        return reports
    
    def get_historical_patterns(self, days: int = 30) -> Dict[str, Any]:
        """Analyze historical patterns over the specified period"""
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)
        
        trends = self.load_trends(start_date, end_date)
        
        # Analyze patterns
        category_timeline = {}
        daily_counts = {}
        popular_sources = {}
        
        for trend in trends:
            # Track category trends over time
            date_key = trend.discovered_at.strftime('%Y-%m-%d')
            if date_key not in category_timeline:
                category_timeline[date_key] = {}
                daily_counts[date_key] = 0
            
            if trend.category not in category_timeline[date_key]:
                category_timeline[date_key][trend.category] = 0
            
            category_timeline[date_key][trend.category] += 1
            daily_counts[date_key] += 1
            
            # Track source popularity
            source_name = trend.source.name
            if source_name not in popular_sources:
                popular_sources[source_name] = 0
            popular_sources[source_name] += 1
        
        return {
            'period_days': days,
            'total_trends': len(trends),
            'category_timeline': category_timeline,
            'daily_counts': daily_counts,
            'popular_sources': popular_sources
        }
    
    def save_categories_config(self, config: TrackedCategories) -> str:
        """Save tracked categories configuration"""
        filepath = self.storage_dir / "categories_config.json"
        
        with open(filepath, 'w') as f:
            json.dump(config.model_dump(), f, indent=2)
        
        return str(filepath)
    
    def load_categories_config(self) -> TrackedCategories:
        """Load tracked categories configuration"""
        filepath = self.storage_dir / "categories_config.json"
        
        if not filepath.exists():
            # Return default configuration
            return TrackedCategories()
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            return TrackedCategories(**data)
        except Exception as e:
            print(f"Error loading categories config: {e}")
            return TrackedCategories()
