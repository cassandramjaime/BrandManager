# Consumer Product Trends Tracking

This document explains how to use the BrandManager's consumer product trends tracking system.

## Overview

The trend tracking system aggregates data from multiple sources to identify and analyze consumer product trends. It uses AI to provide insights on patterns, emerging categories, and opportunities.

## Features

- **Multi-Source Data Aggregation**: Collect trends from Product Hunt, TechCrunch, The Verge, Hacker News, and Reddit
- **Google Trends Integration**: Monitor rising search terms in consumer tech categories
- **AI-Powered Analysis**: Use LLM to identify patterns, emerging categories, and opportunities
- **Historical Tracking**: Store and analyze historical data to identify long-term patterns
- **Weekly Reports**: Generate comprehensive reports in PDF and Markdown formats
- **Visualizations**: Create charts, category distributions, and trend timelines
- **Customizable Categories**: Track specific categories (social, fintech, health, productivity, etc.)

## Quick Start

### 1. Collect Current Trends

Collect trending products and news from all sources:

```bash
topic-research collect
```

Customize sources:

```bash
# Exclude Product Hunt, include only specific Reddit subreddits
topic-research collect --no-product-hunt --reddit-subs technology --reddit-subs startups
```

### 2. Generate Weekly Report

Create a comprehensive weekly trend report:

```bash
topic-research report
```

This generates both PDF and Markdown reports with:
- Top 10 trending products/topics
- Category breakdown and analysis
- AI-powered insights on patterns and opportunities
- Visualizations (charts, graphs, timelines)

Generate only Markdown:

```bash
topic-research report --no-pdf
```

### 3. Configure Tracked Categories

Customize which categories to track:

```bash
topic-research configure -c social -c fintech -c health -c ai
```

### 4. View Historical Insights

Analyze historical patterns:

```bash
topic-research insights --days 30
```

### 5. Run Full Collection Cycle

Collect trends and generate report in one command:

```bash
topic-research run
```

## Programmatic Usage

You can also use the trend tracker in your Python scripts:

```python
from brand_manager.trend_tracker import TrendTracker

# Initialize tracker
tracker = TrendTracker(openai_api_key="your-key")

# Collect current trends
trends = tracker.collect_current_trends(
    product_hunt=True,
    tech_news=True,
    hacker_news=True,
    reddit=True,
    reddit_subs=['technology', 'gadgets', 'startups']
)

# Generate weekly report
report = tracker.generate_weekly_report(
    generate_pdf=True,
    generate_markdown=True
)

# Get historical insights
insights = tracker.get_historical_insights(days=30)
```

## Data Sources

### Supported Sources

1. **Product Hunt** - Daily trending products via RSS feed
2. **TechCrunch** - Tech news and startup coverage via RSS feed
3. **The Verge** - Technology news and reviews via RSS feed
4. **Hacker News** - Community-driven tech discussions via API
5. **Reddit** - Subreddits: r/technology, r/gadgets, r/startups
6. **Google Trends** - Rising search terms in tech categories

### Future Sources (Planned)

- Y Combinator directory and funding announcements
- Crunchbase API for startup funding data
- iOS/Android app store trending apps

## Report Structure

### Weekly Trend Report

Each weekly report includes:

1. **Executive Summary** - AI-generated overview of the week's trends
2. **Top 10 Trends** - Ranked by traction score with analysis
3. **Category Breakdown** - Distribution of trends across categories
4. **Pattern Analysis**:
   - Common patterns across trends
   - Emerging categories
   - Identified opportunities
   - Technologies being adopted
5. **Visualizations**:
   - Category distribution pie chart
   - Top trends bar chart
   - Timeline of trend discovery
   - Category trends over time

### Report Formats

- **Markdown (.md)** - Easy to read, version control friendly
- **PDF (.pdf)** - Professional format for sharing

## Storage

All data is stored locally in the `trend_data/` directory:

```
trend_data/
├── trends/          # Raw trend data
├── reports/         # Weekly report data
├── google_trends/   # Google Trends data
├── startups/        # Startup information
└── categories_config.json
```

Visualizations are saved in `trend_visualizations/`

Reports are saved in `trend_reports/`

## Customization

### Category Configuration

Default categories:
- social
- fintech
- health
- productivity
- education
- ecommerce

Add custom categories:

```python
from brand_manager.trend_tracker import TrendTracker

tracker = TrendTracker()
tracker.track_categories(
    categories=['social', 'fintech', 'ai', 'blockchain'],
    custom_keywords={
        'ai': ['artificial intelligence', 'machine learning', 'llm'],
        'blockchain': ['crypto', 'web3', 'nft']
    }
)
```

### Custom Data Collection

Collect trends for specific time periods:

```python
from datetime import datetime, timedelta

tracker = TrendTracker()

# Generate report for last month
end_date = datetime.utcnow()
start_date = end_date - timedelta(days=30)

report = tracker.generate_weekly_report(
    start_date=start_date,
    end_date=end_date
)
```

## Analysis Capabilities

### Traction Scoring

Trends are scored based on:
- Source credibility
- Engagement metrics (upvotes, comments, score)
- Recency (newer trends score higher)

### AI Analysis

The system uses OpenAI's GPT models to:
- Identify common patterns across trends
- Detect emerging categories
- Suggest business opportunities
- Track technology adoption
- Explain why specific trends are gaining traction

### Historical Patterns

Analyze long-term patterns:
- Category trends over time
- Popular data sources
- Daily trend counts
- Seasonal variations

## Best Practices

1. **Regular Collection**: Run `topic-research collect` daily to build historical data
2. **Weekly Reports**: Generate reports weekly to track changes over time
3. **Category Customization**: Adjust tracked categories based on your focus area
4. **Historical Analysis**: Review 30+ days of data to identify meaningful patterns
5. **Data Backup**: The `trend_data/` directory contains all historical data - back it up regularly

## Troubleshooting

### No trends found

If you get "No trends found" when generating a report:
1. Make sure you've run `topic-research collect` first
2. Check that the date range includes collected data
3. Verify the `trend_data/trends/` directory has data files

### API Rate Limits

Some sources may have rate limits:
- **Reddit**: Respects API guidelines, may need delays between requests
- **Google Trends**: Limited number of requests per hour
- **Hacker News**: Generally no limits on public API

### OpenAI API Key

Make sure your `.env` file has:
```
OPENAI_API_KEY=your-api-key-here
```

## Examples

### Example 1: Daily Trend Collection

```bash
# Morning: Collect trends
topic-research collect

# Review insights
topic-research insights --days 7
```

### Example 2: Weekly Report Generation

```bash
# End of week: Generate comprehensive report
topic-research report

# Check output in trend_reports/ directory
ls trend_reports/
```

### Example 3: Category Focus

```bash
# Focus on specific categories
topic-research configure -c health -c fintech

# Collect with specific Reddit sources
topic-research collect --reddit-subs health --reddit-subs fintech
```

## Output Examples

### Console Output

```
🔍 Collecting trends from data sources...
Collecting from Product Hunt...
Collecting from TechCrunch...
Collecting from The Verge...
Collecting from Hacker News...
Collecting from Reddit r/technology...
✓ Collected 45 trends from 4 source groups
✓ Saved trends to /path/to/trend_data/trends/trends_20250114_153022.json
```

### Report Output

Reports include:
- Full analysis of trending products
- Category distribution charts
- Timeline visualizations
- Keyword clouds
- PDF and Markdown versions

Check the `trend_reports/` directory for generated files.

## Integration with Topic Research

The trend tracking system works alongside the original topic research functionality:

```bash
# Research a specific trend
topic-research research "AI-powered health apps" --depth deep

# Collect trends
topic-research collect

# Generate report
topic-research report
```

Both features share the same OpenAI API key and can be used together for comprehensive market research.
