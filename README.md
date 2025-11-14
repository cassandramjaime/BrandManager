# BrandManager 🎨

AI-powered content and media outreach toolkit with two main features:

1. **Content Topic Research**: Research any topic dynamically using AI
2. **Journalist Opportunity Finder**: Find and track journalists seeking AI PM contributors

## Features ✨

### Content Topic Research
- **Dynamic Topic Research**: Research any topic using AI to get comprehensive insights
- **Structured Results**: Get organized research with key points, trends, statistics, and more
- **Multiple Depth Levels**: Choose from quick, standard, or deep research based on your needs
- **Focus Areas**: Specify particular aspects to focus on (trends, statistics, audience interests, etc.)
- **Competitor Analysis**: Understand how competitors approach the topic and identify content gaps
- **Content Angles**: Get suggested angles for creating content on your researched topic
- **Keyword Extraction**: Identify important keywords and phrases related to the topic
- **Export Results**: Save research results to JSON for later use

### Journalist Opportunity Finder (NEW!)
- **AI-Powered Discovery**: Find journalists and publications seeking AI PM contributors
- **Multi-Platform Monitoring**: Track opportunities from HARO, Twitter/X, Medium, Substack, LinkedIn, and more
- **Smart Categorization**: Automatically classify by publication tier (WSJ/NYT, TechCrunch, blogs, etc.)
- **Relevance Scoring**: AI rates each opportunity (0-100) based on your expertise
- **Personalized Pitches**: Generate professional, tailored pitch emails automatically
- **Response Tracking**: Track opportunities found, pitches sent, and responses received
- **Daily Digest**: Get prioritized summaries of new opportunities
- **Database Storage**: SQLite database tracks all opportunities and activity

## What is Content Topic Dynamic Research?

Content topic dynamic research uses AI to automatically research and analyze any topic you're interested in writing about. Instead of spending hours manually researching, you get:

- **Comprehensive Summary**: Quick overview of the topic
- **Key Points**: Most important facts and insights
- **Current Trends**: What's trending related to this topic
- **Statistics & Data**: Relevant numbers and data points
- **Audience Interests**: What people care about regarding this topic
- **Content Angles**: Different perspectives and approaches for creating content
- **Competitor Insights**: How competitors approach this topic and what content opportunities exist
- **Keywords**: Important terms and phrases to include

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

3. Set up your OpenAI API key:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Quick Start 🚀

### Topic Research

Research a topic with standard depth:
```bash
topic-research research "AI in healthcare"
```

Quick research (faster, less detail):
```bash
topic-research quick "sustainable fashion"
```

Deep research (slower, more comprehensive):
```bash
topic-research deep "quantum computing applications"
```

For more details, see the full [Topic Research Documentation](#topic-research-commands) below.

### Journalist Opportunity Finder (NEW!)

Set up your profile (first time only):
```bash
journalist-finder setup-profile
```

Add an opportunity:
```bash
journalist-finder add-opportunity --source twitter --text "TechCrunch looking for AI PM experts..."
```

List opportunities:
```bash
journalist-finder list --min-score 70 --not-pitched
```

Generate a personalized pitch:
```bash
journalist-finder generate-pitch OpportunityID
```

For complete documentation, see [JOURNALIST_FINDER.md](JOURNALIST_FINDER.md).

## Usage Examples 📖

### Topic Research Examples

#### Example 1: Research for a Blog Post

```bash
topic-research research "AI ethics" --depth deep --focus trends --focus audience_interests
```

This will give you:
- Current trends in AI ethics
- What audiences care about
- Key points to cover
- Statistics to cite
- Content angles to explore
- Competitor insights and content gaps

### Example 2: Quick Social Media Research

```bash
topic-research quick "plant-based diet benefits"
```

Get a fast overview perfect for social media posts.

### Example 3: Comprehensive Article Research

```bash
topic-research deep "climate change solutions" --focus statistics --focus trends --output climate-research.json
```

Deep dive with focus on data and trends, saved for reference.

### Journalist Finder Examples

#### Example 1: Complete Workflow

```bash
# Set up profile (first time)
journalist-finder setup-profile

# Add opportunities from Twitter
journalist-finder add-opportunity --source twitter \
  --text "Forbes seeking AI PM experts for article. Deadline Nov 25."

# List high-priority opportunities
journalist-finder list --min-score 75 --tier tier_1 --tier tier_2

# Generate a pitch
journalist-finder generate-pitch Forbes_20251114120000 --save

# Mark as pitched after sending
journalist-finder mark-pitched Forbes_20251114120000

# Check daily digest
journalist-finder daily-digest --min-score 70
```

## Command Reference 📚

### Topic Research Commands

### `research` - Main Research Command

```bash
topic-research research TOPIC [OPTIONS]
```

**Options:**
- `--depth [quick|standard|deep]` - Research depth (default: standard)
- `--focus AREA` - Focus area (can be used multiple times)
  - Available areas: `trends`, `statistics`, `key_points`, `audience_interests`, `content_angles`, `competitor_insights`, `keywords`
- `--output FILE` - Save results to JSON file

**Examples:**
```bash
topic-research research "blockchain technology"
topic-research research "mental health" --depth deep
topic-research research "AI art" --focus trends --focus statistics
topic-research research "crypto" --output crypto-research.json
```

### `quick` - Quick Research

```bash
topic-research quick TOPIC [OPTIONS]
```

Fast research with less detail. Perfect for quick content ideas.

**Example:**
```bash
topic-research quick "NFTs"
```

### `deep` - Deep Research

```bash
topic-research deep TOPIC [OPTIONS]
```

Comprehensive research with extensive analysis.

**Example:**
```bash
topic-research deep "machine learning in medicine"
```

### Journalist Finder Commands

For complete documentation of all journalist finder commands, see [JOURNALIST_FINDER.md](JOURNALIST_FINDER.md).

**Quick Reference:**
- `journalist-finder setup-profile` - Set up your professional profile
- `journalist-finder add-opportunity` - Add a new opportunity
- `journalist-finder list` - List opportunities with filtering
- `journalist-finder show ID` - Show opportunity details
- `journalist-finder generate-pitch ID` - Generate personalized pitch
- `journalist-finder mark-pitched ID` - Mark opportunity as pitched
- `journalist-finder mark-response ID` - Mark response received
- `journalist-finder daily-digest` - Generate daily digest
- `journalist-finder stats` - View statistics

## Research Output Structure

The topic research tool provides structured research in these categories:

1. **SUMMARY** - 2-3 sentence overview of the topic
2. **KEY POINTS** - 5-8 most important facts and insights
3. **CURRENT TRENDS** - 3-5 trends related to the topic
4. **STATISTICS & DATA** - 3-5 relevant statistics
5. **AUDIENCE INTERESTS** - 3-5 things audiences care about
6. **CONTENT ANGLES** - 3-5 suggested approaches for content
7. **COMPETITOR INSIGHTS** - 3-5 insights on how competitors approach the topic and content opportunities
8. **KEYWORDS** - 8-12 important keywords and phrases

## Programmatic Usage

### Topic Research

You can use the topic research tool in your Python scripts:

```python
from brand_manager.models import TopicResearchRequest
from brand_manager.ai_manager import AITopicResearcher

# Initialize researcher
researcher = AITopicResearcher()

# Create research request
request = TopicResearchRequest(
    topic="artificial intelligence ethics",
    depth="deep",
    focus_areas=["trends", "statistics", "audience_interests"]
)

# Conduct research
result = researcher.research_topic(request)

# Access results
print(result.summary)
print(result.key_points)
print(result.trends)
print(result.statistics)
```

### Journalist Opportunity Finder

```python
from brand_manager.opportunity_finder import OpportunityFinder
from brand_manager.journalist_models import OpportunitySource, UserProfile

# Initialize finder
finder = OpportunityFinder()

# Set up user profile
profile = UserProfile(
    name="Jane Smith",
    title="AI Product Manager",
    expertise_areas=["AI", "product management", "machine learning"],
    experience_years=8,
    bio="AI PM with 8 years of experience"
)
finder.db.save_user_profile(profile)

# Add an opportunity
opportunity_id = finder.add_opportunity_from_text(
    text="TechCrunch looking for AI PM experts...",
    source=OpportunitySource.TWITTER
)

# Generate pitch
pitch = finder.generate_pitch(finder.db.get_opportunity(opportunity_id))
print(pitch.full_pitch)
```

## Use Cases 💡

### Topic Research
- **Content Writers**: Research topics before writing articles, blogs, or social posts
- **Marketers**: Understand trending topics and audience interests
- **Researchers**: Get quick overviews and key points on new topics
- **Social Media Managers**: Find current trends and content angles
- **Educators**: Research topics for lesson planning

### Journalist Opportunity Finder
- **Thought Leaders**: Build media presence and share expertise
- **Product Managers**: Discuss AI and product management trends
- **Consultants**: Establish credibility with tier 1 & 2 publications
- **Startup Founders**: Get press coverage for your company
- **Executives**: Position yourself as an industry expert
- **Authors/Speakers**: Build authority and promote your work

## Requirements 📋

- Python 3.8+
- OpenAI API key (required for both tools)
- Dependencies listed in `requirements.txt`
  - openai>=1.0.0
  - python-dotenv>=1.0.0
  - pydantic>=2.0.0
  - click>=8.0.0
  - colorama>=0.4.6
  - tabulate>=0.9.0

## Development 🛠️

### Running Tests

```bash
pytest tests/
```

### Project Structure

```
BrandManager/
├── brand_manager/
│   ├── __init__.py
│   ├── models.py          # Pydantic models for requests/results
│   ├── ai_manager.py      # Core AI research functionality
│   └── cli.py             # Command-line interface
├── tests/
│   └── test_topic_research.py
├── examples/
│   └── api_usage_example.py
├── setup.py
├── requirements.txt
└── README.md
```

## Tips for Best Results 💡

1. **Be Specific**: More specific topics yield better results
   - Good: "AI in healthcare diagnostics"
   - Less good: "AI"

2. **Use Focus Areas**: Narrow down to what you need
   - `--focus trends` for latest developments
   - `--focus statistics` for data and numbers
   - `--focus content_angles` for writing ideas

3. **Choose Appropriate Depth**: 
   - `quick` for social media or quick reference
   - `standard` for most blog posts and articles
   - `deep` for comprehensive research or long-form content

4. **Save Important Research**: Use `--output` to keep research for later reference

## License 📄

MIT License

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## Support 💬

If you encounter any issues or have questions, please file an issue on GitHub.
