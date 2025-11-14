# Podcast Guest Opportunity Finder

An automated tool to find and track podcast guest opportunities for AI/ML and Product Management experts.

## Overview

The Podcast Guest Opportunity Finder helps you discover, score, and track podcast guest opportunities that align with your expertise in AI/ML and Product Management. It includes:

- **Automated searching** across multiple platforms (Twitter/X, LinkedIn, PodMatch, MatchMaker.fm, etc.)
- **Smart scoring system** based on audience size, topic relevance, and engagement metrics
- **SQLite database** for tracking application status
- **Export functionality** to CSV and Markdown formats
- **Command-line interface** for easy management

## Features

### 1. Search for Opportunities

Search across multiple platforms for podcast guest opportunities:

- **Twitter/X**: Posts from hosts seeking guests
- **LinkedIn**: Professional network posts
- **PodMatch**: Dedicated podcast booking platform
- **MatchMaker.fm**: Podcast-guest matching service
- **Podcast Guests**: Database of shows seeking guests

### 2. Intelligent Scoring

Each opportunity is scored on three dimensions:

- **Relevance Score (0-100)**: How well the podcast aligns with AI/ML/PM topics
- **Audience Score (0-100)**: Based on listener/download numbers
- **Engagement Score (0-100)**: Quality of submission process and contact information

These are combined into a **Total Score** using weighted averages (50% relevance, 30% audience, 20% engagement).

### 3. Track Application Status

Monitor your podcast applications through the entire process:

- Not Applied
- Applied
- Responded
- Scheduled
- Completed
- Rejected

### 4. Export to Spreadsheet

Export your opportunities to CSV or Markdown format with all relevant details:

- Podcast name and host information
- Audience size and scores
- Why it's a good fit
- Contact information and submission links
- Application status and notes

## Installation

The podcast finder is included with BrandManager:

```bash
pip install -e .
```

## Quick Start

### Add a Manual Opportunity

```bash
podcast-finder add "Product Thinking Podcast" \
  --host "Melissa Perri" \
  --contact "podcast@productthinking.com" \
  --description "Deep dives into product strategy" \
  --audience 25000 \
  --link "https://productthinking.com/guest"
```

### List All Opportunities

```bash
podcast-finder list
```

Filter by status:
```bash
podcast-finder list --status not_applied --min-score 60
```

### Update Application Status

```bash
podcast-finder update-status 1 applied --notes "Sent pitch email"
```

### Export to Spreadsheet

Export as CSV:
```bash
podcast-finder export --format csv --output opportunities.csv
```

Export as Markdown:
```bash
podcast-finder export --format markdown --output opportunities.md
```

### View Statistics

```bash
podcast-finder stats
```

## Search for New Opportunities

**Note**: The search functionality requires API keys for various services (Twitter API, LinkedIn API, etc.). The framework is in place, but you'll need to add your API credentials.

```bash
podcast-finder search \
  --keywords "product manager" \
  --keywords "AI" \
  --min-score 50 \
  --sources twitter \
  --sources linkedin
```

## Command Reference

### `add` - Manually Add Opportunity

```bash
podcast-finder add PODCAST_NAME [OPTIONS]
```

**Options:**
- `--host TEXT` - Host name
- `--contact TEXT` - Contact email or social media
- `--description TEXT` - Show description
- `--audience INTEGER` - Audience size
- `--link TEXT` - Submission link
- `--source TEXT` - Source of this opportunity (default: manual)

### `list` - List Opportunities

```bash
podcast-finder list [OPTIONS]
```

**Options:**
- `--status [not_applied|applied|responded|scheduled|completed|rejected]`
- `--min-score FLOAT` - Minimum total score
- `--limit INTEGER` - Limit number of results

### `update-status` - Update Application Status

```bash
podcast-finder update-status OPPORTUNITY_ID STATUS [OPTIONS]
```

**Arguments:**
- `OPPORTUNITY_ID` - Database ID of the opportunity
- `STATUS` - New status (not_applied, applied, responded, scheduled, completed, rejected)

**Options:**
- `--notes TEXT` - Additional notes

### `export` - Export to Spreadsheet

```bash
podcast-finder export [OPTIONS]
```

**Options:**
- `--status` - Filter by application status
- `--min-score FLOAT` - Minimum total score
- `--format [csv|markdown]` - Export format (default: csv)
- `--output TEXT` - Output file path (required)

### `stats` - Show Statistics

```bash
podcast-finder stats
```

Shows:
- Total number of opportunities
- Count by application status
- Average scores (total, relevance, audience)

### `search` - Search for Opportunities

```bash
podcast-finder search [OPTIONS]
```

**Options:**
- `--keywords TEXT` - Keywords to search for (can use multiple times)
- `--min-audience INTEGER` - Minimum audience size
- `--min-score FLOAT` - Minimum relevance score (0-100)
- `--sources [twitter|linkedin|podmatch|matchmaker|podcastguests]` - Sources to search
- `--max-results INTEGER` - Maximum number of results (default: 50)

## Scoring System Details

### Relevance Score (0-100)

Calculated based on keyword matching:

**AI/ML Keywords** (weighted 60%):
- ai, artificial intelligence, machine learning, ml, deep learning
- neural network, data science, nlp, computer vision, robotics
- automation, chatbot, llm, gpt, generative ai

**Product Management Keywords** (weighted 40%):
- product manager, product management, product leader, product strategy
- pm, product, saas, software, tech, startup, roadmap
- product development, agile, scrum, innovation

**Bonuses:**
- +10 points for "product manager" or "product management"
- +10 points for "artificial intelligence" or "machine learning"

### Audience Score (0-100)

Based on estimated audience size:

- 100K+ listeners: 100 points
- 50K-100K: 90 points
- 25K-50K: 80 points
- 10K-25K: 70 points
- 5K-10K: 60 points
- 2K-5K: 50 points
- 1K-2K: 40 points
- 500-1K: 30 points
- Under 500: 20 points
- Unknown: 10 points

### Engagement Score (0-100)

Based on information completeness and source credibility:

- Submission form available: 40 points
- Contact information available: 20 points
- Detailed description: 20 points
- Source credibility:
  - PodMatch/MatchMaker/PodcastGuests: 20 points
  - LinkedIn: 15 points
  - Website: 15 points
  - Twitter: 10 points
  - Unknown: 5 points

### Total Score

Weighted average: `(Relevance × 0.5) + (Audience × 0.3) + (Engagement × 0.2)`

## Database Storage

Opportunities are stored in a local SQLite database (`podcast_opportunities.db` by default).

**Database Schema:**
- Podcast details (name, host, contact, description)
- Audience metrics
- Scoring data
- Application status tracking
- Timestamps and deadlines
- Notes and fit reasons

## Extending the Search Functionality

The search framework is designed to be extended with actual API integrations. To add real search capabilities:

1. **Twitter/X Integration**: Implement `_search_twitter()` using the Twitter API v2
2. **LinkedIn Integration**: Add `_search_linkedin()` using LinkedIn API
3. **PodMatch Integration**: Connect to PodMatch API or scraping
4. **Website Scraping**: Add web scraping for podcast submission pages

See `brand_manager/podcast_searcher.py` for placeholder methods ready to be implemented.

## Example Workflow

1. **Search for opportunities** (when API integration is complete):
   ```bash
   podcast-finder search --min-score 60
   ```

2. **Review and filter**:
   ```bash
   podcast-finder list --status not_applied --min-score 70
   ```

3. **Export top opportunities**:
   ```bash
   podcast-finder export --min-score 70 --format csv --output top_opportunities.csv
   ```

4. **Apply to podcasts** and update status:
   ```bash
   podcast-finder update-status 5 applied --notes "Sent pitch focusing on AI product frameworks"
   ```

5. **Track progress**:
   ```bash
   podcast-finder list --status applied
   podcast-finder stats
   ```

6. **When scheduled**:
   ```bash
   podcast-finder update-status 5 scheduled --notes "Recording on Dec 15"
   ```

## Tips for Best Results

1. **Be Specific**: Add detailed descriptions when manually adding opportunities
2. **Update Regularly**: Keep application statuses current
3. **Use Notes**: Record what angle you pitched and any responses
4. **Filter Smart**: Use min-score to focus on best-fit opportunities
5. **Export Often**: Keep a spreadsheet for easy sharing and planning

## Programmatic Usage

You can also use the podcast finder in your Python scripts:

```python
from brand_manager.podcast_searcher import PodcastSearcher
from brand_manager.podcast_database import PodcastDatabase
from brand_manager.podcast_exporter import PodcastExporter

# Add a manual opportunity
searcher = PodcastSearcher()
opportunity = searcher.add_manual_opportunity(
    podcast_name="Tech Leaders Podcast",
    host_name="Jane Doe",
    show_description="Interviews with tech leaders about AI and product",
    audience_size=20000
)

# Save to database
db = PodcastDatabase()
opp_id = db.add_opportunity(opportunity)

# Export opportunities
exporter = PodcastExporter()
all_opps = db.get_all_opportunities(min_score=60)
exporter.export_to_csv(all_opps, "opportunities.csv")
```

## Future Enhancements

Planned features for future releases:

- Live API integration with Twitter, LinkedIn, PodMatch
- Automated weekly opportunity digests
- Email notifications for high-scoring opportunities
- Integration with calendar for scheduled interviews
- Pitch template generator
- Post-interview follow-up tracking
- Analytics on successful podcast appearances

## Support

For issues or questions, please open an issue on GitHub.
