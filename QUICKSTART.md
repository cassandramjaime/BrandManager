# Quick Start Guide

This guide will help you get started with the AI Brand Manager in just a few minutes.

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

## Your First Brand

1. **Create your brand identity**
   
   Run the setup command and answer the prompts:
   ```bash
   brand-manager setup
   ```
   
   You'll be asked for:
   - Brand name (required)
   - Tagline (optional)
   - Description (optional)
   - Industry (optional)
   - Brand voice/tone (optional)
   - Target audience (optional)
   - Core values (press Enter to skip)
   - Unique selling points (press Enter to skip)

2. **View your brand**
   ```bash
   brand-manager show
   ```

3. **Generate your first tagline**
   ```bash
   brand-manager generate-tagline --count 5
   ```

## Common Use Cases

### Generate Social Media Content

**Twitter post:**
```bash
brand-manager generate --type social_post --topic "new feature announcement" --platform twitter --length short
```

**LinkedIn post:**
```bash
brand-manager generate --type social_post --topic "company milestone" --platform linkedin --length medium
```

### Create Marketing Copy

**Product description:**
```bash
brand-manager generate --type product_description --topic "eco-friendly water bottle" --length long
```

**Email subject line:**
```bash
brand-manager generate --type email_subject --topic "summer sale"
```

### Check Brand Alignment

Analyze if a message fits your brand:
```bash
brand-manager analyze "We're revolutionizing the industry with AI-powered solutions!"
```

### Get Strategic Advice

Ask for brand strategy recommendations:
```bash
brand-manager advice "How can I improve my social media engagement?"
```

### Brainstorm Campaigns

Generate campaign ideas:
```bash
brand-manager campaign "increase brand awareness among millennials" --count 5
```

## Tips for Best Results

1. **Be specific with your brand identity** - The more detailed your brand information, the better the AI can generate relevant content.

2. **Experiment with different tones** - Use the `--tone` flag to override your brand voice for specific content.

3. **Use the analysis feature** - Before posting content, check if it aligns with your brand.

4. **Iterate on taglines** - Generate multiple variations and pick the best one.

5. **Save good outputs** - The AI generates different results each time, so save content you like.

## Programmatic Usage

You can also use Brand Manager in your Python scripts:

```python
from brand_manager.models import BrandIdentity, ContentRequest
from brand_manager.ai_manager import AIBrandManager

# Create brand
brand = BrandIdentity(
    name="My Brand",
    tagline="Making a Difference",
    values=["Innovation", "Quality"]
)

# Initialize manager
manager = AIBrandManager()
manager.set_brand_identity(brand)

# Generate content
request = ContentRequest(
    content_type="social_post",
    topic="product launch",
    platform="twitter"
)
content = manager.generate_content(request)
print(content)
```

See `examples/api_usage_example.py` for more examples.

## Troubleshooting

### "OpenAI API key is required" error
- Make sure you've created a `.env` file with your API key
- Or export it: `export OPENAI_API_KEY=your-key-here`

### "No brand configured" error
- Run `brand-manager setup` to create your brand identity first

### Rate limit errors
- You may be making too many requests. Wait a moment and try again.
- Consider upgrading your OpenAI plan if you need higher limits.

## Next Steps

- Read the full [README.md](README.md) for complete documentation
- Explore the [API example](examples/api_usage_example.py)
- Check out all available commands: `brand-manager --help`

## Need Help?

- File an issue on GitHub
- Check the documentation in README.md
- Review the example scripts in the `examples/` directory
