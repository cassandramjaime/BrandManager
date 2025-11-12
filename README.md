# BrandManager 🎨

AI-powered content topic research tool that helps you research any topic dynamically to create better, more informed content.

## 🚀 Quick Run (3 Simple Steps)

**Step 1: Clone and Navigate**
```bash
git clone https://github.com/cassandramjaime/BrandManager.git
cd BrandManager
```

**Step 2: Setup (One-Time)**
```bash
# Option A: Using Make (Recommended)
make setup

# Option B: Using run.sh
./run.sh setup

# Option C: Manual setup
pip install -e .
cp .env.example .env
# Then edit .env and add your OpenAI API key
```

**Step 3: Run the Tool**
```bash
# Using Make
make run TOPIC="AI in healthcare"

# Using run.sh
./run.sh research "AI in healthcare"

# Using the command directly
topic-research research "AI in healthcare"
```

That's it! You now have comprehensive topic research. 🎉

## Features ✨

- **Dynamic Topic Research**: Research any topic using AI to get comprehensive insights
- **Structured Results**: Get organized research with key points, trends, statistics, and more
- **Multiple Depth Levels**: Choose from quick, standard, or deep research based on your needs
- **Focus Areas**: Specify particular aspects to focus on (trends, statistics, audience interests, etc.)
- **Competitor Analysis**: Understand how competitors approach the topic and identify content gaps
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
- **Competitor Insights**: How competitors approach this topic and what content opportunities exist
- **Keywords**: Important terms and phrases to include

## Installation 🚀

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- An OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation Methods

**Method 1: Quick Setup with Make (Recommended)**
```bash
git clone https://github.com/cassandramjaime/BrandManager.git
cd BrandManager
make setup
# Edit .env and add your OpenAI API key, then you're ready to go!
```

**Method 2: Quick Setup with run.sh**
```bash
git clone https://github.com/cassandramjaime/BrandManager.git
cd BrandManager
./run.sh setup
# Edit .env and add your OpenAI API key, then you're ready to go!
```

**Method 3: Manual Installation**

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

## Running the Tool 🏃

BrandManager provides **three easy ways** to run topic research:

### Option 1: Using Make Commands (Simplest)

```bash
# Standard research
make run TOPIC="AI in healthcare"

# Quick research (faster)
make quick TOPIC="sustainable fashion"

# Deep research (more comprehensive)
make deep TOPIC="quantum computing"

# Save results to a file
make run TOPIC="blockchain" OUTPUT="results.json"

# See all available commands
make help
```

### Option 2: Using the run.sh Script

```bash
# Standard research
./run.sh research "AI in healthcare"

# Quick research
./run.sh quick "sustainable fashion"

# Deep research
./run.sh deep "quantum computing"

# See all available commands
./run.sh help
```

### Option 3: Using the topic-research Command Directly

```bash
# Standard research
topic-research research "AI in healthcare"

# Quick research
topic-research quick "sustainable fashion"

# Deep research
topic-research deep "quantum computing"

# With specific focus areas
topic-research research "electric vehicles" --focus trends --focus statistics

# Save to JSON file
topic-research research "crypto" --output crypto-research.json
```

## Quick Start 📖

Now that you have the tool installed, here are common usage patterns:

### Basic Research

Research any topic with standard depth:
```bash
# Using Make
make run TOPIC="AI in healthcare"

# Using run.sh
./run.sh research "AI in healthcare"

# Using command directly
topic-research research "AI in healthcare"
```

### Quick Research (Faster, Less Detail)

Perfect for quick content ideas or social media posts:
```bash
# Using Make
make quick TOPIC="sustainable fashion"

# Using run.sh
./run.sh quick "sustainable fashion"

# Using command directly
topic-research quick "sustainable fashion"
```

### Deep Research (Slower, More Comprehensive)

For long-form content or in-depth articles:
```bash
# Using Make
make deep TOPIC="quantum computing applications"

# Using run.sh
./run.sh deep "quantum computing applications"

# Using command directly
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

## Command Reference 📚

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

## Convenient Command Reference 🛠️

### Make Commands

The Makefile provides the simplest way to run the tool:

```bash
# See all available commands
make help

# One-time setup
make setup

# Install or reinstall the package
make install

# Run topic research
make run TOPIC="your topic"
make quick TOPIC="your topic"
make deep TOPIC="your topic"

# Save results to a file
make run TOPIC="your topic" OUTPUT="output.json"

# Run tests
make test

# Clean build artifacts
make clean
```

### run.sh Script Commands

The run.sh script provides an alternative way to run the tool:

```bash
# See all available commands
./run.sh help

# One-time setup
./run.sh setup

# Install the package
./run.sh install

# Run topic research
./run.sh research "your topic"
./run.sh quick "your topic"
./run.sh deep "your topic"
```

## Research Output Structure

The tool provides structured research in these categories:

1. **SUMMARY** - 2-3 sentence overview of the topic
2. **KEY POINTS** - 5-8 most important facts and insights
3. **CURRENT TRENDS** - 3-5 trends related to the topic
4. **STATISTICS & DATA** - 3-5 relevant statistics
5. **AUDIENCE INTERESTS** - 3-5 things audiences care about
6. **CONTENT ANGLES** - 3-5 suggested approaches for content
7. **COMPETITOR INSIGHTS** - 3-5 insights on how competitors approach the topic and content opportunities
8. **KEYWORDS** - 8-12 important keywords and phrases
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
