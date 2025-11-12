# BrandManager 🎨

AI-powered content topic research tool that helps you research any topic dynamically to create better, more informed content.

## Features ✨

- **Dynamic Topic Research**: Research any topic using AI to get comprehensive insights
- **Structured Results**: Get organized research with key points, trends, statistics, and more
- **Multiple Depth Levels**: Choose from quick, standard, or deep research based on your needs
- **Focus Areas**: Specify particular aspects to focus on (trends, statistics, audience interests, etc.)
- **Content Angles**: Get suggested angles for creating content on your researched topic
- **Keyword Extraction**: Identify important keywords and phrases related to the topic
- **Export Results**: Save research results to JSON for later use

## What is Content Topic Dynamic Research?

Content topic dynamic research uses AI to automatically research and analyze any topic you're interested in writing about. Instead of spending hours manually researching, you get:

- **Comprehensive Summary**: Quick overview of the topic
- **Key Points**: Most important facts and insights
- **Current Trends**: What's trending related to this topic
- **Statistics & Data**: Relevant numbers and data points
- **Audience Interests**: What people care about regarding this topic
- **Content Angles**: Different perspectives and approaches for creating content
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

## Quick Start ��

### Basic Usage

Research a topic with standard depth:
```bash
topic-research research "AI in healthcare"
```

### Quick Research (Faster, Less Detail)

```bash
topic-research quick "sustainable fashion"
```

### Deep Research (Slower, More Comprehensive)

```bash
topic-research deep "quantum computing applications"
```

### Focused Research

Focus on specific aspects:
```bash
topic-research research "electric vehicles" --focus trends --focus statistics
```

### Save Results

Export research to a JSON file:
```bash
topic-research research "remote work trends" --output results.json
```

## Usage Examples 📖

### Example 1: Research for a Blog Post

```bash
topic-research research "AI ethics" --depth deep --focus trends --focus audience_interests
```

This will give you:
- Current trends in AI ethics
- What audiences care about
- Key points to cover
- Statistics to cite
- Content angles to explore

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

## Command Reference 📚

### `research` - Main Research Command

```bash
topic-research research TOPIC [OPTIONS]
```

**Options:**
- `--depth [quick|standard|deep]` - Research depth (default: standard)
- `--focus AREA` - Focus area (can be used multiple times)
  - Available areas: `trends`, `statistics`, `key_points`, `audience_interests`, `content_angles`, `keywords`
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

## Research Output Structure

The tool provides structured research in these categories:

1. **SUMMARY** - 2-3 sentence overview of the topic
2. **KEY POINTS** - 5-8 most important facts and insights
3. **CURRENT TRENDS** - 3-5 trends related to the topic
4. **STATISTICS & DATA** - 3-5 relevant statistics
5. **AUDIENCE INTERESTS** - 3-5 things audiences care about
6. **CONTENT ANGLES** - 3-5 suggested approaches for content
7. **KEYWORDS** - 8-12 important keywords and phrases

## Programmatic Usage

You can also use the tool in your Python scripts:

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

## Use Cases 💡

- **Content Writers**: Research topics before writing articles, blogs, or social posts
- **Marketers**: Understand trending topics and audience interests
- **Researchers**: Get quick overviews and key points on new topics
- **Social Media Managers**: Find current trends and content angles
- **Educators**: Research topics for lesson planning
- **Anyone**: Learn about any topic quickly with structured information

## Requirements 📋

- Python 3.8+
- OpenAI API key
- Dependencies listed in `requirements.txt`

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
