"""
Visualization generation for trend reports
"""
import os
from typing import List, Dict, Any
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from pathlib import Path

from .trend_models import ProductTrend, WeeklyTrendReport


class TrendVisualizer:
    """Creates visualizations for trend data"""
    
    def __init__(self, output_dir: str = None):
        """Initialize visualizer with output directory"""
        self.output_dir = Path(output_dir or os.path.join(os.getcwd(), "trend_visualizations"))
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def create_category_distribution_chart(self, 
                                          category_breakdown: Dict[str, int],
                                          filename: str = None) -> str:
        """Create a pie chart of category distribution"""
        if filename is None:
            filename = f"category_distribution_{datetime.utcnow().strftime('%Y%m%d')}.png"
        
        filepath = self.output_dir / filename
        
        # Prepare data
        categories = list(category_breakdown.keys())
        counts = list(category_breakdown.values())
        
        # Create pie chart
        plt.figure(figsize=(10, 8))
        colors = plt.cm.Set3(range(len(categories)))
        plt.pie(counts, labels=categories, autopct='%1.1f%%', colors=colors, startangle=90)
        plt.title('Trend Category Distribution', fontsize=16, fontweight='bold')
        plt.axis('equal')
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(filepath)
    
    def create_trend_timeline_chart(self, 
                                   daily_counts: Dict[str, int],
                                   filename: str = None) -> str:
        """Create a line chart showing trends over time"""
        if filename is None:
            filename = f"trend_timeline_{datetime.utcnow().strftime('%Y%m%d')}.png"
        
        filepath = self.output_dir / filename
        
        # Sort by date
        sorted_dates = sorted(daily_counts.keys())
        counts = [daily_counts[date] for date in sorted_dates]
        
        # Create line chart
        plt.figure(figsize=(12, 6))
        plt.plot(sorted_dates, counts, marker='o', linewidth=2, markersize=6, color='#2E86AB')
        plt.title('Trends Discovered Over Time', fontsize=16, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Number of Trends', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(filepath)
    
    def create_top_trends_chart(self, 
                               top_trends: List[Any],
                               filename: str = None) -> str:
        """Create a horizontal bar chart of top trends"""
        if filename is None:
            filename = f"top_trends_{datetime.utcnow().strftime('%Y%m%d')}.png"
        
        filepath = self.output_dir / filename
        
        # Prepare data (reverse for top-to-bottom display)
        titles = [trend.title[:40] + '...' if len(trend.title) > 40 else trend.title 
                 for trend in reversed(top_trends[:10])]
        scores = [trend.traction_score for trend in reversed(top_trends[:10])]
        
        # Create horizontal bar chart
        plt.figure(figsize=(12, 8))
        colors = plt.cm.viridis(range(len(titles)))
        plt.barh(titles, scores, color=colors)
        plt.title('Top 10 Trending Products', fontsize=16, fontweight='bold')
        plt.xlabel('Traction Score', fontsize=12)
        plt.ylabel('Product/Trend', fontsize=12)
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(filepath)
    
    def create_keyword_cloud(self, 
                            trends: List[ProductTrend],
                            filename: str = None) -> str:
        """Create a word cloud from trend titles and descriptions"""
        if filename is None:
            filename = f"keyword_cloud_{datetime.utcnow().strftime('%Y%m%d')}.png"
        
        filepath = self.output_dir / filename
        
        # Combine all text
        text = ' '.join([
            f"{trend.title} {trend.description}" 
            for trend in trends
        ])
        
        # Create word cloud
        wordcloud = WordCloud(
            width=1200, 
            height=600,
            background_color='white',
            colormap='viridis',
            max_words=100,
            relative_scaling=0.5,
            min_font_size=10
        ).generate(text)
        
        plt.figure(figsize=(15, 8))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.title('Trending Keywords', fontsize=16, fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(filepath)
    
    def create_category_timeline_chart(self,
                                      category_timeline: Dict[str, Dict[str, int]],
                                      filename: str = None) -> str:
        """Create a stacked area chart showing category trends over time"""
        if filename is None:
            filename = f"category_timeline_{datetime.utcnow().strftime('%Y%m%d')}.png"
        
        filepath = self.output_dir / filename
        
        # Prepare data
        dates = sorted(category_timeline.keys())
        
        # Get all categories
        all_categories = set()
        for date_data in category_timeline.values():
            all_categories.update(date_data.keys())
        
        # Build data series for each category
        category_series = {cat: [] for cat in all_categories}
        for date in dates:
            for cat in all_categories:
                category_series[cat].append(category_timeline[date].get(cat, 0))
        
        # Create stacked area chart
        plt.figure(figsize=(14, 7))
        plt.stackplot(dates, 
                     *[category_series[cat] for cat in all_categories],
                     labels=list(all_categories),
                     alpha=0.8)
        
        plt.title('Category Trends Over Time', fontsize=16, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Number of Trends', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.legend(loc='upper left', fontsize=10)
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        plt.close()
        
        return str(filepath)
    
    def create_all_visualizations(self, 
                                 report: WeeklyTrendReport,
                                 historical_data: Dict[str, Any] = None) -> Dict[str, str]:
        """Create all visualizations for a report"""
        viz_paths = {}
        
        # Category distribution
        if report.category_breakdown:
            viz_paths['category_dist'] = self.create_category_distribution_chart(
                report.category_breakdown,
                f"category_dist_{report.report_id}.png"
            )
        
        # Top trends
        if report.top_trends:
            viz_paths['top_trends'] = self.create_top_trends_chart(
                report.top_trends,
                f"top_trends_{report.report_id}.png"
            )
        
        # Historical data visualizations
        if historical_data:
            if 'daily_counts' in historical_data:
                viz_paths['timeline'] = self.create_trend_timeline_chart(
                    historical_data['daily_counts'],
                    f"timeline_{report.report_id}.png"
                )
            
            if 'category_timeline' in historical_data:
                viz_paths['category_timeline'] = self.create_category_timeline_chart(
                    historical_data['category_timeline'],
                    f"category_timeline_{report.report_id}.png"
                )
        
        return viz_paths
