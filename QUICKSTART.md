# Quick Start Guide - AI Topic Researcher

Get started with AI-powered topic research in just a few minutes.

## Prerequisites

- Python 3.8 or higher
- An OpenAI API key (get one at https://platform.openai.com/api-keys)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/cassandramjaime/BrandManager.git
   cd BrandManager
   ```

2. **Install the package**
   ```bash
   pip install -e .
   ```

3. **Set up your OpenAI API key**
   
   Create a `.env` file in the project directory:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your API key:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

## Your First Topic Research

1. **Research a topic**
   
   ```bash
   topic-research research "artificial intelligence"
   ```
   
   This will give you:
   - A comprehensive summary
   - Key points and insights
   - Current trends
   - Relevant statistics
   - What audiences care about
   - Suggested content angles
   - Important keywords

2. **Quick research (faster)**
   
   ```bash
   topic-research quick "climate change"
   ```

3. **Deep research (more comprehensive)**
   
   ```bash
   topic-research deep "quantum computing"
   ```

## Common Use Cases

### For Blog Post Research

```bash
topic-research research "remote work productivity" --depth deep --focus trends --focus statistics
```

This gives you trends and statistics to cite in your blog post.

### For Social Media Content

```bash
topic-research quick "sustainable living tips"
```

Quick overview perfect for creating social posts.

### For Video Content

```bash
topic-research research "AI content creation" --focus audience_interests --focus content_angles
```

Learn what audiences care about and get ideas for different video angles.

### Save Research for Later

```bash
topic-research research "blockchain technology" --output blockchain-research.json
```

Export the research to reference later.

## Research Depth Options

- **quick** - Fast, 3-5 key points (30-45 seconds)
- **standard** - Balanced, comprehensive (45-60 seconds)
- **deep** - Extensive, detailed analysis (60-90 seconds)

## Focus Areas

Use `--focus` to zero in on specific aspects:

- `trends` - Current trends and developments
- `statistics` - Data points and numbers
- `key_points` - Core facts and insights
- `audience_interests` - What people care about
- `content_angles` - Different perspectives for content
- `keywords` - Important terms and phrases

**Example:**
```bash
topic-research research "electric vehicles" --focus trends --focus statistics --focus keywords
```

## Programmatic Usage

Use in your Python scripts:

```python
from brand_manager.models import TopicResearchRequest
from brand_manager.ai_manager import AITopicResearcher

# Initialize
researcher = AITopicResearcher()

# Research a topic
request = TopicResearchRequest(
    topic="machine learning",
    depth="standard",
    focus_areas=["trends", "statistics"]
)

result = researcher.research_topic(request)

# Use the results
print(result.summary)
for point in result.key_points:
    print(f"• {point}")
```

See `examples/api_usage_example.py` for more examples.

## Tips for Best Results

1. **Be specific with your topic**
   - ✅ "AI in medical diagnostics"
   - ❌ "AI"

2. **Choose the right depth**
   - Quick: Social media, quick reference
   - Standard: Most blog posts
   - Deep: Long-form content, research papers

3. **Use focus areas** when you know what you need
   - Need data? Use `--focus statistics`
   - Need ideas? Use `--focus content_angles`
   - Need SEO? Use `--focus keywords`

4. **Save important research** with `--output`

## Troubleshooting

### "OpenAI API key is required" error
- Make sure you've created a `.env` file with your API key
- Or export it: `export OPENAI_API_KEY=your-key-here`

### Slow responses
- Use `quick` command for faster results
- OpenAI API can be slow during peak times

### Empty results sections
- Try a different depth level
- Make your topic more specific
- Some topics may not have data in all categories

## Next Steps

- Read the full [README.md](README.md) for complete documentation
- Explore the [API example](examples/api_usage_example.py)
- Try different topics and depth levels
- Experiment with focus areas to get exactly what you need

## Need Help?

- File an issue on GitHub
- Check the documentation in README.md
- Review the example scripts in the `examples/` directory
