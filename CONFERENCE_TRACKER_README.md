# Conference Tracker for Product Managers 🎯

A comprehensive Python application for researching, tracking, and managing product management conferences. Built specifically for PMs to discover relevant conferences with AI/ML focus, quality speakers, and networking opportunities.

## Features ✨

### Conference Discovery
- **Automated Scraping**: Aggregate conferences from multiple sources (Luma, Eventbrite, major PM conference sites)
- **Curated Database**: Pre-loaded with major PM conferences (ProductCon, Mind the Product, Product School, etc.)
- **Smart Filtering**: Filter by date, location type, topic focus, price, and quality scores

### Intelligent Scoring
- **AI Relevance Score**: Measures relevance to AI/ML product management (0-10)
- **Speaker Quality Score**: Evaluates speaker credentials and company prestige (0-10)
- **Networking Score**: Assesses networking opportunities based on format and duration (0-10)
- **Overall Score**: Weighted combination of all factors for easy comparison

### Powerful Search
- Filter by date range
- Location type (virtual/in-person/hybrid)
- Topic focus (AI/ML, consumer products, general PM, etc.)
- Minimum quality score
- Maximum ticket price
- Location keywords

### Export & Reporting
- **CSV Export**: Complete conference data for spreadsheet analysis
- **Summary Reports**: Professional text reports with statistics and recommendations
- **Automated Insights**: Top recommendations based on your criteria

### Scheduling
- Set up weekly or monthly automated searches
- Configure persistent search filters
- Generate reports on schedule

## Installation 🚀

1. Clone the repository:
```bash
git clone https://github.com/cassandramjaime/BrandManager.git
cd BrandManager
```

2. Install the package:
```bash
pip install -e .
```

## Quick Start 🏃

### 1. Update Conference Database

Scrape and score conferences from all sources:

```bash
conference-tracker update
```

### 2. List All Conferences

View top conferences by score:

```bash
conference-tracker list --limit 10
```

### 3. Search with Filters

Find AI/ML conferences with minimum score of 5:

```bash
conference-tracker search --topic "AI/ML" --min-score 5
```

### 4. Export Results

Search and export to CSV:

```bash
conference-tracker search --topic "AI/ML" --output conferences.csv
```

### 5. Generate Reports

Create a summary report with recommendations:

```bash
conference-tracker search --topic "AI/ML" --report ai_conferences.txt
```

## Command Reference 📚

### `update` - Update Conference Database

Scrape conferences from all sources and update the database.

```bash
conference-tracker update [--db PATH]
```

**Options:**
- `--db PATH` - Database file path (default: conferences.db)

**Example:**
```bash
conference-tracker update
```

### `list` - List Conferences

List top conferences from the database.

```bash
conference-tracker list [OPTIONS]
```

**Options:**
- `--limit N` - Number of conferences to display (default: 10)
- `--db PATH` - Database file path (default: conferences.db)

**Example:**
```bash
conference-tracker list --limit 5
```

### `search` - Search Conferences

Search conferences with advanced filters.

```bash
conference-tracker search [OPTIONS]
```

**Options:**
- `--from-date DATE` - Start date (YYYY-MM-DD)
- `--to-date DATE` - End date (YYYY-MM-DD)
- `--location-type TYPE` - Filter by location type (virtual/in-person/hybrid)
- `--topic TOPIC` - Filter by topic focus (can use multiple times)
  - Available topics: AI/ML, consumer products, general PM, enterprise, B2B, B2C, mobile, web, data, design
- `--min-score SCORE` - Minimum overall score (0-10)
- `--max-price PRICE` - Maximum ticket price
- `--location KEYWORD` - Location keywords (can use multiple times)
- `--output FILE` - Export results to CSV file
- `--report FILE` - Generate summary report
- `--db PATH` - Database file path (default: conferences.db)

**Examples:**

Find virtual AI/ML conferences:
```bash
conference-tracker search --location-type virtual --topic "AI/ML"
```

Find conferences in San Francisco with good scores:
```bash
conference-tracker search --location "San Francisco" --min-score 7
```

Find affordable conferences with export:
```bash
conference-tracker search --max-price 300 --output budget_conferences.csv
```

Complex search with report:
```bash
conference-tracker search \
  --from-date 2024-01-01 \
  --to-date 2024-12-31 \
  --topic "AI/ML" \
  --topic "general PM" \
  --min-score 6 \
  --max-price 1000 \
  --output ai_pm_conferences.csv \
  --report ai_pm_report.txt
```

### `report` - Generate Summary Report

Generate a comprehensive summary report of all conferences in the database.

```bash
conference-tracker report --output FILE [OPTIONS]
```

**Options:**
- `--output FILE` - Output report file path (required)
- `--format TYPE` - Report format: text or json (default: text)
- `--db PATH` - Database file path (default: conferences.db)

**Example:**
```bash
conference-tracker report --output conferences_2024.txt
conference-tracker report --output conferences.json --format json
```

### `schedule` - Manage Scheduled Searches

Set up and manage automated conference searches.

```bash
conference-tracker schedule ACTION [OPTIONS]
```

**Actions:**
- `setup` - Configure a new schedule
- `status` - Show current schedule status
- `run` - Run scheduled search now
- `enable` - Enable scheduled searches
- `disable` - Disable scheduled searches

**Options:**
- `--frequency TYPE` - Schedule frequency: weekly or monthly (required for setup)
- `--from-date DATE` - Start date filter (YYYY-MM-DD)
- `--to-date DATE` - End date filter (YYYY-MM-DD)
- `--location-type TYPE` - Filter by location type
- `--topic TOPIC` - Filter by topic focus (can use multiple times)
- `--min-score SCORE` - Minimum overall score
- `--max-price PRICE` - Maximum ticket price
- `--output-dir DIR` - Output directory for reports (default: current directory)
- `--force` - Force run even if not scheduled (for run action)
- `--db PATH` - Database file path (default: conferences.db)

**Examples:**

Set up weekly AI/ML conference search:
```bash
conference-tracker schedule setup --frequency weekly --topic "AI/ML" --min-score 5
```

Check schedule status:
```bash
conference-tracker schedule status
```

Force run scheduled search:
```bash
conference-tracker schedule run --force --output-dir /path/to/reports
```

Disable schedule:
```bash
conference-tracker schedule disable
```

## Understanding Scores 📊

### AI Relevance Score (0-10)
Measures how relevant the conference is to AI/ML product management:
- **8-10**: Highly focused on AI/ML (e.g., "AI Product Summit")
- **5-7**: Significant AI/ML content mixed with general PM topics
- **0-4**: Minimal or no AI/ML focus

Factors:
- Topic focus includes AI/ML
- Conference name mentions AI
- Agenda topics mention AI/ML
- Description mentions AI

### Speaker Quality Score (0-10)
Evaluates the caliber of speakers:
- **8-10**: VPs, CPOs, and leaders from top tech companies (Google, Meta, OpenAI, etc.)
- **5-7**: Directors and senior PMs from recognized companies
- **0-4**: General speakers or limited speaker information

Factors:
- Number of notable speakers
- Speaker titles (VP, CPO, Director, etc.)
- Company prestige (FAANG, unicorns, etc.)

### Networking Score (0-10)
Assesses networking opportunities:
- **8-10**: Multi-day in-person conferences with high-end pricing
- **5-7**: In-person or hybrid conferences, or well-established virtual events
- **0-4**: Short virtual meetups or single-session events

Factors:
- Location type (in-person > hybrid > virtual)
- Conference duration (longer = better)
- Conference prestige (inferred from price and speakers)

### Overall Score (0-10)
Weighted average of all scores:
- AI Relevance: 40%
- Speaker Quality: 30%
- Networking: 30%

## Data Sources 🌐

The application aggregates conferences from:

1. **Manual Curation**: Major PM conferences
   - ProductCon
   - Mind the Product
   - Product School
   - Web Summit
   - AI Product Summit
   - Product Management Festival
   - Industry Conference

2. **Eventbrite**: Popular event platform (stub implementation, ready for API integration)

3. **Luma**: Modern event platform (stub implementation, ready for expansion)

## Database Schema 💾

Conferences are stored in SQLite with the following structure:

```sql
CREATE TABLE conferences (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    location TEXT NOT NULL,
    location_type TEXT NOT NULL,
    ticket_price_min REAL,
    ticket_price_max REAL,
    notable_speakers TEXT,  -- JSON array
    agenda_topics TEXT,     -- JSON array
    registration_deadline TEXT,
    url TEXT NOT NULL UNIQUE,
    source TEXT NOT NULL,
    description TEXT,
    topic_focus TEXT,       -- JSON array
    relevance_score REAL,
    speaker_quality_score REAL,
    networking_score REAL,
    overall_score REAL,
    created_at TEXT,
    updated_at TEXT
);
```

## Use Cases 💡

### For Individual PMs

**Finding Your Next Conference:**
```bash
# Step 1: Update database
conference-tracker update

# Step 2: Search for relevant conferences
conference-tracker search \
  --topic "AI/ML" \
  --min-score 6 \
  --max-price 1000 \
  --output my_conferences.csv \
  --report recommendations.txt

# Step 3: Review recommendations in the report
cat recommendations.txt
```

**Tracking Virtual Options:**
```bash
conference-tracker search \
  --location-type virtual \
  --topic "AI/ML" \
  --topic "general PM" \
  --max-price 200
```

### For Product Leaders

**Quarterly Conference Planning:**
```bash
# Set up automated quarterly searches
conference-tracker schedule setup \
  --frequency monthly \
  --min-score 7 \
  --topic "AI/ML" \
  --topic "enterprise"

# Generate reports for team
conference-tracker report --output Q1_conferences.txt
```

### For Learning & Development Teams

**Budget Planning:**
```bash
# Find all conferences under $500
conference-tracker search \
  --max-price 500 \
  --output budget_options.csv

# Find high-value free options
conference-tracker search \
  --max-price 0 \
  --min-score 5 \
  --location-type virtual
```

## Development 🛠️

### Project Structure

```
BrandManager/
├── brand_manager/
│   ├── __init__.py
│   ├── models.py                  # Topic research models
│   ├── ai_manager.py              # AI topic research
│   ├── cli.py                     # Topic research CLI
│   ├── conference_models.py       # Conference data models
│   ├── conference_db.py           # SQLite database handler
│   ├── conference_scrapers.py     # Web scrapers
│   ├── conference_scorer.py       # Scoring/ranking system
│   ├── conference_exporter.py     # CSV/report generation
│   ├── conference_cli.py          # Conference CLI
│   └── conference_scheduler.py    # Scheduling functionality
├── tests/
│   ├── test_topic_research.py
│   └── test_conference_tracking.py
├── requirements.txt
├── setup.py
└── README.md
```

### Running Tests

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=brand_manager

# Run specific test file
pytest tests/test_conference_tracking.py -v
```

### Adding New Data Sources

To add a new conference scraper:

1. Create a new scraper class inheriting from `ConferenceScraper`
2. Implement the `scrape_conferences()` method
3. Add the scraper to `ConferenceAggregator`

Example:

```python
class NewSourceScraper(ConferenceScraper):
    def scrape_conferences(self) -> List[Conference]:
        conferences = []
        # Scraping logic here
        return conferences

# In ConferenceAggregator.__init__:
self.scrapers = [
    ManualConferenceScraper(),
    EventbriteConferenceScraper(),
    LumaConferenceScraper(),
    NewSourceScraper(),  # Add here
]
```

## Tips for Best Results 💡

1. **Update Regularly**: Run `conference-tracker update` weekly to get the latest conferences

2. **Use Multiple Filters**: Combine filters for more targeted results
   ```bash
   conference-tracker search --topic "AI/ML" --min-score 7 --location-type virtual
   ```

3. **Set Up Schedules**: Automate your conference research
   ```bash
   conference-tracker schedule setup --frequency weekly --topic "AI/ML"
   ```

4. **Export for Analysis**: Use CSV exports to compare conferences in spreadsheets
   ```bash
   conference-tracker search --topic "AI/ML" --output conferences.csv
   ```

5. **Read the Reports**: Generated reports include valuable recommendations
   ```bash
   conference-tracker search --topic "AI/ML" --report insights.txt
   ```

## Requirements 📋

- Python 3.8+
- Dependencies listed in `requirements.txt`:
  - beautifulsoup4>=4.12.0
  - requests>=2.31.0
  - pydantic>=2.0.0
  - click>=8.0.0
  - colorama>=0.4.6

## License 📄

MIT License

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

Areas for contribution:
- Additional conference sources (APIs, RSS feeds)
- Improved scoring algorithms
- Email notification support for scheduled searches
- Web UI/dashboard
- Calendar integration
- Conference comparison features

## Support 💬

If you encounter any issues or have questions, please file an issue on GitHub.
