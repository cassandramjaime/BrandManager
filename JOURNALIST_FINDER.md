# Journalist Opportunity Finder

AI-powered tool to find and track journalists and publications seeking AI PM contributors.

## Features ✨

### Opportunity Discovery
- **AI-Powered Parsing**: Automatically extract structured data from opportunity posts
- **Multi-Platform Support**: Monitor HARO, Twitter/X, Medium, Substack, LinkedIn, and more
- **Smart Classification**: Automatically categorize by publication tier (Tier 1/2/3) and urgency

### Intelligent Matching
- **Relevance Scoring**: AI-powered scoring (0-100) based on your expertise
- **Profile-Based Matching**: Personalized recommendations based on your background
- **Keyword Tracking**: Track opportunities by topic keywords

### Pitch Generation
- **AI-Generated Pitches**: Create personalized, professional pitches automatically
- **Profile Integration**: Pitches tailored to your experience and achievements
- **Save & Track**: Save pitches and track which ones you've sent

### Tracking & Analytics
- **Database Storage**: SQLite database tracks all opportunities
- **Response Tracking**: Track pitches sent and responses received
- **Statistics Dashboard**: View success rates and activity metrics
- **Daily Digest**: Get prioritized daily summaries of new opportunities

## Installation 🚀

1. Make sure you have the base package installed (see main README.md)

2. The journalist finder is included - no additional installation needed

3. Set up your OpenAI API key in `.env` (same as for topic research)

## Quick Start 🎯

### 1. Set Up Your Profile

First, create your professional profile for personalized matching and pitch generation:

```bash
journalist-finder setup-profile
```

You'll be prompted for:
- Your name
- Professional title (e.g., "AI Product Manager")
- Years of experience
- Current company (optional)
- Expertise areas (comma-separated)
- Professional bio

### 2. Add Opportunities

Add opportunities you find on various platforms:

```bash
journalist-finder add-opportunity --source twitter --text "TechCrunch looking for AI PM experts to discuss how AI is transforming product management. Deadline Nov 20. Contact: jane@techcrunch.com"
```

The AI will automatically extract:
- Publication name
- Journalist/editor name
- Topic and requirements
- Deadline
- Contact method
- Keywords

### 3. Browse Opportunities

List all opportunities with filtering:

```bash
# List all opportunities
journalist-finder list

# Filter by relevance score
journalist-finder list --min-score 70

# Filter by tier (Tier 1 publications only)
journalist-finder list --tier tier_1 --tier tier_2

# Show only opportunities you haven't pitched yet
journalist-finder list --not-pitched --min-score 60
```

### 4. View Details

See full details about an opportunity:

```bash
journalist-finder show TechCrunch_20251114120000
```

### 5. Generate Personalized Pitches

Let AI create a professional, personalized pitch:

```bash
# Generate and display pitch
journalist-finder generate-pitch TechCrunch_20251114120000

# Generate and save to file
journalist-finder generate-pitch TechCrunch_20251114120000 --save
```

The AI creates a complete pitch email with:
- Compelling subject line
- Professional greeting
- Value proposition based on your expertise
- Specific examples from your achievements
- Clear call to action

### 6. Track Your Pitches

Mark when you send pitches:

```bash
journalist-finder mark-pitched TechCrunch_20251114120000
```

Mark when you receive responses:

```bash
journalist-finder mark-response TechCrunch_20251114120000
```

### 7. Daily Digest

Get a prioritized summary of recent opportunities:

```bash
journalist-finder daily-digest --min-score 50
```

This shows:
- **High Priority**: Score ≥70 or urgent deadlines with score ≥50
- **Medium Priority**: Score 50-69, not urgent
- **Low Priority**: Score <50

### 8. View Statistics

Track your performance:

```bash
journalist-finder stats
```

Shows:
- Total opportunities tracked
- Pitches sent
- Responses received
- Response rate
- Breakdown by tier and urgency

## Command Reference 📚

### `setup-profile`
Set up your professional profile for pitch personalization.

```bash
journalist-finder setup-profile
```

### `add-opportunity`
Add a journalist opportunity from text you found online.

**Options:**
- `--source` - Platform where found (haro, twitter, medium, substack, linkedin, terkel, qwoted, featured, sourcebottle, other)
- `--text` - The opportunity text (can be prompted)

**Example:**
```bash
journalist-finder add-opportunity \
  --source twitter \
  --text "Forbes seeking AI experts for article on ML in product development. Email: editor@forbes.com. Deadline: Nov 25"
```

### `list`
List journalist opportunities with optional filtering.

**Options:**
- `--min-score FLOAT` - Minimum relevance score (0-100)
- `--tier CHOICE` - Filter by tier (tier_1, tier_2, tier_3) - can use multiple times
- `--urgency CHOICE` - Filter by urgency (high, medium, low) - can use multiple times
- `--not-pitched` - Show only opportunities not yet pitched
- `--limit INT` - Maximum number to display (default: 20)

**Examples:**
```bash
# High-quality tier 1 & 2 opportunities
journalist-finder list --min-score 75 --tier tier_1 --tier tier_2

# Urgent opportunities not yet pitched
journalist-finder list --urgency high --not-pitched

# All opportunities with score above 60
journalist-finder list --min-score 60 --limit 50
```

### `show`
Show detailed information about a specific opportunity.

**Arguments:**
- `opportunity_id` - ID of the opportunity

**Example:**
```bash
journalist-finder show TechCrunch_20251114120000
```

### `generate-pitch`
Generate a personalized pitch for an opportunity.

**Arguments:**
- `opportunity_id` - ID of the opportunity

**Options:**
- `--save` - Save pitch to file
- `--output PATH` - Custom output file path

**Examples:**
```bash
# Display pitch
journalist-finder generate-pitch Forbes_20251114120000

# Save to default file
journalist-finder generate-pitch Forbes_20251114120000 --save

# Save to custom file
journalist-finder generate-pitch Forbes_20251114120000 -o my_pitch.txt
```

### `mark-pitched`
Mark an opportunity as pitched.

**Arguments:**
- `opportunity_id` - ID of the opportunity

**Example:**
```bash
journalist-finder mark-pitched TechCrunch_20251114120000
```

### `mark-response`
Mark that a response was received.

**Arguments:**
- `opportunity_id` - ID of the opportunity

**Example:**
```bash
journalist-finder mark-response TechCrunch_20251114120000
```

### `daily-digest`
Generate a daily digest of opportunities.

**Options:**
- `--min-score FLOAT` - Minimum relevance score to include (default: 50.0)

**Example:**
```bash
journalist-finder daily-digest --min-score 70
```

### `stats`
Show statistics about your opportunities.

**Example:**
```bash
journalist-finder stats
```

## Publication Tiers

The tool automatically classifies publications into three tiers:

### Tier 1 - Premier Publications
- Wall Street Journal, New York Times, Forbes
- Bloomberg, Financial Times, The Economist
- Reuters, Associated Press, Washington Post
- USA Today, Time Magazine

### Tier 2 - Major Tech/Business Publications
- TechCrunch, VentureBeat, Wired, The Verge
- Ars Technica, Mashable, Engadget, Gizmodo
- Fast Company, Inc, Entrepreneur
- Business Insider, CNET, ZDNet

### Tier 3 - Niche & Smaller Publications
- All other publications
- Industry-specific blogs
- Regional publications
- Emerging media outlets

## Urgency Levels

Opportunities are classified by urgency based on deadline:

- **High**: Deadline within 24-48 hours
- **Medium**: Deadline within 3-7 days
- **Low**: Deadline more than 7 days out or no deadline specified

## Relevance Scoring

The AI scores each opportunity on a 0-100 scale based on:

**Without Profile (Basic Matching):**
- 85: Matches both "AI" and "product management" keywords
- 60: Matches either "AI" or "product management"
- 30: Limited keyword match

**With Profile (AI-Powered):**
- 90-100: Perfect match - your expertise is ideal
- 70-89: Strong match - you're well-qualified
- 50-69: Good match - relevant experience
- 30-49: Moderate match - some relevance
- 0-29: Poor match - limited relevance

## Sources Supported

The tool tracks opportunities from:

- **HARO (Help a Reporter Out)** - Email-based journalist requests
- **Twitter/X** - #journorequest, "seeking sources", expert calls
- **Medium** - Publications accepting submissions
- **Substack** - Newsletter collaboration opportunities
- **LinkedIn** - Professional networking opportunities
- **Terkel** - Expert panel service
- **Qwoted** - Media matching platform
- **Featured** - Expert source platform
- **SourceBottle** - Journalist request service
- **Other** - Any other source

## Tips for Best Results 💡

### 1. Set Up a Complete Profile
The more detailed your profile, the better the relevance scoring and pitch generation:
- Include all relevant expertise areas
- Add key achievements and metrics
- Keep your bio current and compelling

### 2. Act on High-Priority Opportunities
- Focus on opportunities with score ≥70
- Respond quickly to high-urgency items
- Tier 1 publications can significantly boost visibility

### 3. Track Everything
- Mark pitches as sent immediately
- Record responses for better statistics
- Add notes to opportunities for context

### 4. Use Daily Digest
- Check daily digest each morning
- Filter by minimum score to focus on quality
- Set up a routine for reviewing opportunities

### 5. Customize Generated Pitches
- Review AI-generated pitches before sending
- Add specific examples relevant to the topic
- Adjust tone to match publication style
- Keep pitches concise (250-300 words)

### 6. Monitor Multiple Sources
- Add opportunities from all platforms
- Don't rely on just one source
- Check Twitter #journorequest daily
- Subscribe to HARO if applicable

## Database Storage

Opportunities are stored in `opportunities.db` SQLite database with:

- All opportunity details
- User profile
- Pitch history
- Response tracking
- Timestamps for all activities

The database is automatically created in your working directory.

## Integration with Topic Research

You can combine journalist finder with the topic research tool:

```bash
# Research a topic
topic-research research "AI in healthcare" --output research.json

# Use insights to identify opportunities
journalist-finder list --min-score 70

# Generate informed pitch using research
journalist-finder generate-pitch OpportunityID_123
```

## Privacy & Data

- All data is stored locally in SQLite database
- No data is shared with third parties
- API calls to OpenAI only for AI features (scoring, pitch generation)
- You control all opportunity data

## Limitations

- Twitter/X integration requires API credentials (not included)
- HARO monitoring requires email subscription
- Some platforms may require separate authentication
- Relevance scoring requires OpenAI API key

## Future Enhancements

Potential additions (not yet implemented):
- Direct Twitter API integration
- Automated HARO email parsing
- Chrome extension for one-click opportunity capture
- Email notifications for high-priority matches
- CRM integration
- Advanced analytics dashboard

## Support & Issues

For questions or issues:
1. Check this documentation
2. Review examples in the repository
3. File an issue on GitHub

## Example Workflow

Here's a complete example workflow:

```bash
# 1. Set up your profile (first time only)
journalist-finder setup-profile

# 2. Add an opportunity you found on Twitter
journalist-finder add-opportunity \
  --source twitter \
  --text "TechCrunch: Looking for AI PM experts to discuss the future of product management with AI. Deadline Nov 25. DM or email sarah@tc.com"

# 3. View all high-quality opportunities
journalist-finder list --min-score 70 --not-pitched

# 4. Check details of a promising one
journalist-finder show TechCrunch_20251114120000

# 5. Generate a pitch
journalist-finder generate-pitch TechCrunch_20251114120000 --save

# 6. Review the pitch, customize if needed, then send

# 7. Mark as pitched
journalist-finder mark-pitched TechCrunch_20251114120000

# 8. When you get a response
journalist-finder mark-response TechCrunch_20251114120000

# 9. Check your stats
journalist-finder stats

# 10. Daily routine - check digest
journalist-finder daily-digest --min-score 60
```

## License

Same as the main BrandManager package (MIT License).
