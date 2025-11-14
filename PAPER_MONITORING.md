# ML/AI Research Paper Monitoring

Automated system for monitoring, summarizing, and organizing recent ML/AI research papers from multiple sources.

## Features

### Paper Sources
- **arXiv**: cs.AI, cs.LG, cs.CL categories
- **Papers with Code**: Latest papers with code implementations
- **Hugging Face**: Daily papers featured on Hugging Face

### Filtering & Search
- Filter by publication date (last 30/60/90 days)
- Filter by topics (LLMs, computer vision, reinforcement learning, AI safety, etc.)
- Filter by citation count threshold
- Full-text search across titles, authors, and abstracts
- Search by keywords

### AI-Powered Summarization
- Concise 2-3 paragraph summaries
- Main contribution extraction
- Methodology overview
- Key results summary
- Relevance to product management

### Categorization
- **Application Area**: Healthcare, Finance, Education, Robotics, etc.
- **Technical Difficulty**: Beginner, Intermediate, Advanced, Expert
- **Production Readiness**: Theoretical, Experimental, Prototype, Production-Ready

### Weekly Digest
- Top 10 papers of the week
- Email/PDF/HTML export formats
- JSON export for further processing
- Text format for easy sharing

### Database
- SQLite with full-text search (FTS5)
- Efficient indexing for fast queries
- Paper metadata and summaries storage
- Search past papers instantly

## Installation

The paper monitoring feature is included in the BrandManager package:

```bash
pip install -e .
```

## Quick Start

### 1. Fetch Recent Papers

Fetch papers from arXiv on LLMs from the last 30 days:

```bash
topic-research papers fetch --days 30 --topic llms --source arxiv
```

Fetch and summarize papers:

```bash
topic-research papers fetch --days 30 --topic llms --source arxiv --summarize
```

### 2. Search Past Papers

Search for papers about transformers:

```bash
topic-research papers search "transformer architecture" --limit 10
```

### 3. Generate Weekly Digest

Create a weekly digest of top papers:

```bash
topic-research papers digest --days 7 --top-n 10 --output weekly_digest.html --format html
```

### 4. View Paper Details

Show full details and summary for a specific paper:

```bash
topic-research papers show 2301.00001
```

### 5. Database Statistics

View statistics about your paper database:

```bash
topic-research papers stats
```

## Command Reference

### `papers fetch`

Fetch recent papers from various sources.

**Options:**
- `--days INTEGER` - Number of days to look back (default: 30)
- `--topic CHOICE` - Topic categories to filter (llms, computer_vision, reinforcement_learning, ai_safety, nlp, generative_ai, multimodal, other)
- `--source CHOICE` - Sources to fetch from (arxiv, papers_with_code, hugging_face)
- `--min-citations INTEGER` - Minimum citation count (default: 0)
- `--keyword TEXT` - Keywords to search for (can be used multiple times)
- `--summarize/--no-summarize` - Generate AI summaries (default: no)
- `--db PATH` - Database file path (default: papers.db)

**Examples:**

```bash
# Fetch papers on LLMs and AI safety from arXiv
topic-research papers fetch --days 60 --topic llms --topic ai_safety --source arxiv

# Fetch and summarize papers with at least 10 citations
topic-research papers fetch --days 30 --min-citations 10 --summarize

# Fetch papers with specific keywords
topic-research papers fetch --days 30 --keyword "GPT" --keyword "transformer"
```

### `papers search`

Search past papers using full-text search.

**Options:**
- `QUERY` - Search query text (required)
- `--limit INTEGER` - Maximum number of results (default: 10)
- `--offset INTEGER` - Offset for pagination (default: 0)
- `--db PATH` - Database file path (default: papers.db)

**Examples:**

```bash
# Search for papers about transformers
topic-research papers search "transformer architecture"

# Search with pagination
topic-research papers search "language model" --limit 5 --offset 10
```

### `papers digest`

Generate a weekly digest of top papers.

**Options:**
- `--days INTEGER` - Number of days for the digest (default: 7)
- `--top-n INTEGER` - Number of top papers to include (default: 10)
- `--output PATH` - Output file path
- `--format CHOICE` - Output format (json, text, html, default: text)
- `--db PATH` - Database file path (default: papers.db)

**Examples:**

```bash
# Generate HTML digest
topic-research papers digest --top-n 10 --output digest.html --format html

# Generate JSON digest for further processing
topic-research papers digest --days 7 --output digest.json --format json

# Display digest to console
topic-research papers digest --days 7 --top-n 15
```

### `papers show`

Show details of a specific paper.

**Options:**
- `PAPER_ID` - Paper ID (required)
- `--db PATH` - Database file path (default: papers.db)

**Examples:**

```bash
# Show paper details and summary
topic-research papers show 2301.00001

# Show paper from specific database
topic-research papers show test_001 --db custom_papers.db
```

### `papers stats`

Show database statistics.

**Options:**
- `--db PATH` - Database file path (default: papers.db)

**Example:**

```bash
topic-research papers stats
```

## Workflow Examples

### Example 1: Weekly Research Review

```bash
# Monday: Fetch last week's papers
topic-research papers fetch --days 7 --topic llms --topic computer_vision --summarize

# Friday: Generate weekly digest
topic-research papers digest --days 7 --top-n 10 --output weekly_digest.html --format html

# Email the digest to your team
```

### Example 2: Topic-Specific Research

```bash
# Fetch papers on AI safety
topic-research papers fetch --days 60 --topic ai_safety --source arxiv --summarize

# Search for specific techniques
topic-research papers search "constitutional AI"

# Generate a focused digest
topic-research papers digest --days 60 --top-n 5 --output ai_safety_digest.txt
```

### Example 3: Comprehensive Multi-Source Monitoring

```bash
# Fetch from all sources
topic-research papers fetch --days 30 \
  --topic llms \
  --source arxiv \
  --source papers_with_code \
  --source hugging_face \
  --summarize

# Generate monthly digest
topic-research papers digest --days 30 --top-n 20 --output monthly_digest.html --format html
```

## Configuration

### API Keys

Set your OpenAI API key for AI summarization:

```bash
# In .env file
OPENAI_API_KEY=your_api_key_here
```

Or set it as an environment variable:

```bash
export OPENAI_API_KEY=your_api_key_here
```

### Rate Limiting

The system automatically respects API rate limits:
- **arXiv**: 1 request per 3 seconds
- **Papers with Code**: 1 request per second
- **Hugging Face**: 1 request per second

### Database

Papers are stored in SQLite with full-text search enabled:
- Default location: `papers.db` in current directory
- Customizable with `--db` option
- Full-text search on titles, authors, abstracts
- Indexed by date, source, citations

## Output Formats

### JSON Format

Structured data for programmatic access:

```json
{
  "week_start": "2024-01-01T00:00:00",
  "week_end": "2024-01-07T23:59:59",
  "total_papers_reviewed": 150,
  "top_papers": [...],
  "summaries": {...}
}
```

### HTML Format

Beautiful email-ready format with:
- Responsive design
- Color-coded tags
- Direct links to papers
- Summaries and categorization

### Text Format

Simple plain text format:
- Easy to read in terminal
- Copy-paste friendly
- Great for documentation

## Programmatic Usage

Use the paper monitoring system in your Python scripts:

```python
from brand_manager.paper_models import PaperFilter, TopicCategory, PaperSource
from brand_manager.paper_database import PaperDatabase
from brand_manager.paper_fetchers import PaperFetcherManager
from brand_manager.paper_summarizer import PaperSummarizer
from brand_manager.digest_generator import DigestGenerator

# Create a filter
filters = PaperFilter(
    days_back=30,
    topics=[TopicCategory.LLMS],
    sources=[PaperSource.ARXIV],
    min_citations=10
)

# Fetch papers
fetcher = PaperFetcherManager()
papers = fetcher.fetch_papers(filters)

# Save to database
db = PaperDatabase('papers.db')
for paper in papers:
    db.save_paper(paper)

# Generate summaries
summarizer = PaperSummarizer()
for paper in papers[:5]:  # Summarize top 5
    summary = summarizer.summarize_paper(paper)
    db.save_summary(summary)

# Generate digest
generator = DigestGenerator(db)
digest = generator.generate_weekly_digest(top_n=10)
generator.export_to_html(digest, 'digest.html')
```

## Tips for Best Results

### 1. Regular Fetching
Run fetch weekly to stay up-to-date:
```bash
# Add to cron or scheduler
topic-research papers fetch --days 7 --topic llms --summarize
```

### 2. Targeted Topics
Focus on specific topics for better results:
```bash
# Instead of all topics, choose 2-3 relevant ones
topic-research papers fetch --days 30 --topic llms --topic ai_safety
```

### 3. Citation Filtering
Filter by citations for high-impact papers:
```bash
topic-research papers fetch --days 60 --min-citations 20 --summarize
```

### 4. Keyword Precision
Use specific keywords for focused results:
```bash
topic-research papers fetch --days 30 --keyword "GPT-4" --keyword "RLHF"
```

### 5. Digest Customization
Adjust digest size based on your needs:
```bash
# Quick weekly update
topic-research papers digest --days 7 --top-n 5

# Comprehensive monthly review
topic-research papers digest --days 30 --top-n 20
```

## Troubleshooting

### No papers found

**Possible causes:**
- Date range too narrow - try increasing `--days`
- Topics too specific - try broader categories
- No papers in selected sources - try multiple sources

**Solution:**
```bash
# Broader search
topic-research papers fetch --days 90 --source arxiv --source papers_with_code
```

### Summarization errors

**Possible causes:**
- Missing OPENAI_API_KEY
- API rate limits
- Network issues

**Solution:**
```bash
# Check API key
echo $OPENAI_API_KEY

# Reduce batch size
topic-research papers fetch --days 7 --summarize  # Fewer papers
```

### Search returns no results

**Possible causes:**
- Database empty - fetch papers first
- Query too specific

**Solution:**
```bash
# First fetch papers
topic-research papers fetch --days 30

# Then search with simpler query
topic-research papers search "transformer"
```

## Limitations

- **arXiv rate limit**: 3 seconds per request
- **Google Scholar**: Not currently implemented (requires special handling)
- **Summarization cost**: Uses OpenAI API (credits required)
- **FTS5 search**: Requires SQLite 3.9.0+

## Future Enhancements

Planned features:
- [ ] Email notifications for new papers
- [ ] PDF download and analysis
- [ ] Citation network visualization
- [ ] Semantic search using embeddings
- [ ] Google Scholar integration
- [ ] Custom notification rules
- [ ] Multi-user support
- [ ] Web dashboard

## Support

For issues or questions:
1. Check this documentation
2. Review examples in `examples/`
3. File an issue on GitHub
4. Check API logs for errors

## License

MIT License - See LICENSE file for details
