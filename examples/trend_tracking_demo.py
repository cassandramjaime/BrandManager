"""
Demo script for Consumer Product Trends Tracking

This script demonstrates the basic functionality of the trend tracking system.
Run with: python examples/trend_tracking_demo.py
"""
import os
from datetime import datetime
from brand_manager.trend_tracker import TrendTracker
from brand_manager.trend_models import ProductTrend, TrendSource

def demo_basic_functionality():
    """Demonstrate basic trend tracking functionality"""
    
    print("=" * 70)
    print("Consumer Product Trends Tracking Demo")
    print("=" * 70)
    print()
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not set")
        print("   Set it in your .env file to enable AI analysis")
        print()
    
    try:
        # Initialize tracker
        print("1. Initializing Trend Tracker...")
        tracker = TrendTracker()
        print("   ✓ Tracker initialized")
        print()
        
        # Configure categories
        print("2. Configuring tracked categories...")
        config = tracker.track_categories(
            categories=['social', 'fintech', 'health', 'productivity', 'ai']
        )
        print(f"   ✓ Tracking {len(config.categories)} categories")
        print()
        
        # Create sample trends for demo
        print("3. Creating sample trend data...")
        sample_trends = create_sample_trends()
        print(f"   ✓ Created {len(sample_trends)} sample trends")
        print()
        
        # Save sample trends
        print("4. Saving trends to storage...")
        saved_path = tracker.storage.save_trends(sample_trends)
        print(f"   ✓ Saved to {saved_path}")
        print()
        
        # Load trends back
        print("5. Loading trends from storage...")
        loaded_trends = tracker.storage.load_trends()
        print(f"   ✓ Loaded {len(loaded_trends)} trends")
        print()
        
        # Display sample trends
        print("6. Sample Trends:")
        for i, trend in enumerate(sample_trends[:5], 1):
            print(f"   {i}. {trend.title} ({trend.category})")
            print(f"      Source: {trend.source.name}")
            if trend.traction_metrics:
                metrics = ", ".join([f"{k}: {v}" for k, v in trend.traction_metrics.items()])
                print(f"      Metrics: {metrics}")
        print()
        
        # Get historical insights
        print("7. Analyzing historical patterns...")
        insights = tracker.get_historical_insights(days=7)
        print(f"   ✓ Total trends in last 7 days: {insights['total_trends']}")
        if insights['popular_sources']:
            print(f"   ✓ Sources: {len(insights['popular_sources'])}")
        print()
        
        print("=" * 70)
        print("Demo completed successfully!")
        print("=" * 70)
        print()
        print("Next steps:")
        print("  1. Run: topic-research collect")
        print("     (Collect real trends from live sources)")
        print()
        print("  2. Run: topic-research report")
        print("     (Generate comprehensive weekly report)")
        print()
        print("  3. Run: topic-research insights --days 30")
        print("     (View historical trend patterns)")
        print()
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()


def create_sample_trends():
    """Create sample trend data for demonstration"""
    trends = []
    
    sample_data = [
        {
            "title": "AI-Powered Health Monitoring App",
            "description": "Revolutionary health app using AI to provide real-time health insights",
            "category": "health",
            "source": "Product Hunt",
            "url": "https://example.com/health-app",
            "metrics": {"upvotes": 342, "comments": 56}
        },
        {
            "title": "Decentralized Finance Platform Launch",
            "description": "New DeFi platform enables peer-to-peer lending with zero fees",
            "category": "fintech",
            "source": "TechCrunch",
            "url": "https://example.com/defi",
            "metrics": {"score": 250}
        },
        {
            "title": "Productivity Tool with AI Assistant",
            "description": "Smart productivity tool that learns your workflow and suggests optimizations",
            "category": "productivity",
            "source": "Hacker News",
            "url": "https://example.com/productivity",
            "metrics": {"score": 180, "comments": 45}
        },
        {
            "title": "Social Network for Creators",
            "description": "New social platform designed specifically for content creators",
            "category": "social",
            "source": "The Verge",
            "url": "https://example.com/social",
            "metrics": {"upvotes": 125}
        },
        {
            "title": "Machine Learning Platform for Startups",
            "description": "Easy-to-use ML platform that requires no coding experience",
            "category": "ai",
            "source": "Reddit r/technology",
            "url": "https://example.com/ml-platform",
            "metrics": {"upvotes": 890, "comments": 123}
        }
    ]
    
    for item in sample_data:
        source = TrendSource(
            name=item["source"],
            url=item["url"]
        )
        
        trend = ProductTrend(
            title=item["title"],
            description=item["description"],
            category=item["category"],
            source=source,
            url=item["url"],
            traction_metrics=item["metrics"]
        )
        trends.append(trend)
    
    return trends


if __name__ == "__main__":
    demo_basic_functionality()
