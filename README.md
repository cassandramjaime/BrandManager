# BrandManager 🎨

AI-powered personal brand manager that helps you create, manage, and maintain a consistent brand identity using artificial intelligence.

## Features ✨

- **Brand Identity Management**: Define and store your brand's core identity including name, tagline, values, voice, and more
- **AI-Powered Content Generation**: Generate on-brand content for social media, blogs, ads, and more
- **Tagline Creation**: Get creative tagline suggestions that capture your brand essence
- **Brand Alignment Analysis**: Check if your messages align with your brand identity
- **Strategic Advice**: Get AI-powered strategic recommendations for your brand
- **Campaign Brainstorming**: Generate creative campaign ideas for specific goals
- **Easy CLI Interface**: Simple command-line interface for all features

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

## Quick Start 🏁

### 1. Set Up Your Brand Identity

```bash
brand-manager setup
```

This interactive command will guide you through setting up your brand identity including:
- Brand name
- Tagline
- Description
- Core values
- Target audience
- Brand voice/tone
- Industry
- Unique selling points

### 2. View Your Brand

```bash
brand-manager show
```

### 3. Generate Taglines

```bash
brand-manager generate-tagline --count 5
```

### 4. Generate Content

```bash
# Generate a social media post
brand-manager generate --type social_post --topic "product launch" --platform twitter

# Generate a blog title
brand-manager generate --type blog_title --topic "sustainability"

# Generate ad copy
brand-manager generate --type ad_copy --topic "new feature" --length long
```

### 5. Analyze Brand Alignment

```bash
brand-manager analyze "Your message text here"
```

### 6. Get Strategic Advice

```bash
brand-manager advice "How can I improve my social media presence?"
```

### 7. Brainstorm Campaigns

```bash
brand-manager campaign "increase brand awareness" --count 3
```

## Usage Examples 📖

### Setting Up a Tech Startup Brand

```bash
brand-manager setup \
  --name "TechFlow" \
  --tagline "Empowering Innovation" \
  --description "A cutting-edge technology consultancy" \
  --industry "Technology Consulting" \
  --voice "Professional yet approachable"
```

### Generating Social Media Content

```bash
# Twitter post about a new feature
brand-manager generate \
  --type social_post \
  --topic "AI-powered analytics dashboard" \
  --platform twitter \
  --length short

# LinkedIn post
brand-manager generate \
  --type social_post \
  --topic "team expansion" \
  --platform linkedin \
  --length medium \
  --tone professional
```

### Getting Campaign Ideas

```bash
brand-manager campaign "launch new product line" --count 5
```

## Commands Reference 📚

| Command | Description | Options |
|---------|-------------|---------|
| `setup` | Set up your brand identity | `--name`, `--tagline`, `--description`, `--industry`, `--voice`, `--target-audience` |
| `show` | Display current brand identity | - |
| `generate-tagline` | Generate tagline suggestions | `--count` (default: 3) |
| `generate` | Generate brand content | `--type`, `--topic`, `--platform`, `--length`, `--tone` |
| `analyze` | Analyze message for brand alignment | `MESSAGE` (required argument) |
| `advice` | Get strategic brand advice | `QUESTION` (required argument) |
| `campaign` | Brainstorm campaign ideas | `GOAL` (required), `--count` (default: 5) |

### Content Types for `generate` Command

- `social_post` - Social media posts
- `blog_title` - Blog post titles
- `slogan` - Marketing slogans
- `product_description` - Product descriptions
- `email_subject` - Email subject lines
- `ad_copy` - Advertisement copy

## Configuration 🔧

Your brand configuration is stored in `brand_config.json` in the current directory. This file contains all your brand identity information and can be edited manually if needed.

Example `brand_config.json`:
```json
{
  "name": "TechFlow",
  "tagline": "Empowering Innovation",
  "description": "A cutting-edge technology consultancy",
  "values": ["Innovation", "Integrity", "Excellence"],
  "target_audience": "Tech startups and SMBs",
  "voice": "Professional yet approachable",
  "industry": "Technology Consulting",
  "unique_selling_points": ["AI-first approach", "24/7 support"]
}
```

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
│   ├── models.py          # Pydantic models
│   ├── ai_manager.py      # Core AI functionality
│   └── cli.py             # Command-line interface
├── tests/
│   └── test_brand_manager.py
├── setup.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## License 📄

MIT License

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## Support 💬

If you encounter any issues or have questions, please file an issue on GitHub.
