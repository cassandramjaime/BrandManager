# Feature Specifications - AI Brand Manager

## 1. Brand Strategy Development

### 1.1 Personal Brand Assessment

#### Feature: Onboarding Questionnaire

**Purpose**: Collect comprehensive information about the user's background, goals, and preferences to create a personalized brand strategy.

**User Flow**:
1. User creates account and is immediately directed to assessment
2. Progress indicator shows completion status (e.g., "Step 3 of 8")
3. Questions are presented in logical sections with explanations
4. User can save progress and return later
5. AI provides real-time feedback on responses
6. Estimated completion time: 15-20 minutes

**Data Collected**:
- Professional background (role, industry, experience level)
- Career goals (short-term and long-term)
- Unique skills and expertise
- Values and what they stand for
- Target audience (who they want to reach)
- Current online presence
- Content preferences (topics, formats, platforms)
- Time commitment capacity
- Success metrics definition

**Technical Requirements**:
- Form validation with helpful error messages
- Auto-save every 30 seconds
- Mobile-responsive design
- Export responses as PDF
- Privacy controls for data usage

**Success Metrics**:
- 85% completion rate
- Average time to complete: 18 minutes
- User satisfaction score: 4.5/5

---

#### Feature: Unique Value Proposition Generator

**Purpose**: Analyze user's background and generate a compelling personal value proposition.

**Input**:
- Questionnaire responses
- LinkedIn profile data (if connected)
- User-written bio or description

**Output**:
- 3-5 unique value proposition options
- Explanation of why each matters
- Examples of how to use it
- Refinement suggestions

**Algorithm**:
```
1. Extract key skills, experiences, and achievements
2. Identify intersection of expertise and market needs
3. Analyze competitive landscape in user's niche
4. Generate differentiation angles
5. Create compelling value proposition statements
6. Validate against target audience needs
```

**User Interface**:
- Card-based layout showing different options
- Ability to mix and match elements
- Edit and refine generated text
- Preview how it looks on different platforms
- Save favorites for later use

**Example Output**:
```
Option 1: "I help mid-sized SaaS companies scale their product teams from 5 to 50+ 
without losing innovation velocity. Former VP at [Company] where I 3xed the product 
org in 18 months."

Option 2: "Product leader who bridges engineering and business. I translate customer 
pain into elegant solutions that drive revenue."

Option 3: "I turn chaotic product processes into high-performing systems. Specialized 
in 0-1 product launches and team scaling."
```

---

### 1.2 Strategy Creation

#### Feature: 90-Day Action Plan

**Purpose**: Provide users with a concrete, actionable roadmap for building their brand over the next 90 days.

**Components**:

**Week 1-2: Foundation**
- Complete profile optimization (LinkedIn, Twitter, etc.)
- Define content pillars and key messages
- Set up editorial calendar
- Create first pieces of content
- Identify 20 key people to engage with

**Week 3-6: Consistency Building**
- Post 2-3 times per week
- Engage with 10+ posts daily
- Reach out to 5 potential connections weekly
- Repurpose one piece of content into 3 formats
- Track initial metrics

**Week 7-10: Amplification**
- Increase posting frequency to 3-4 times per week
- Start collaborating with others (guest posts, comments)
- Launch first major content initiative (article series, video)
- Analyze what's working and double down
- Reach first milestone (e.g., 500 new followers)

**Week 11-12: Optimization**
- Review 90-day performance
- Refine strategy based on data
- Plan next 90 days
- Celebrate wins
- Set new goals

**Deliverables**:
- PDF download of complete plan
- Interactive checklist with progress tracking
- Calendar integration
- Weekly email reminders
- Accountability check-ins

**Customization Options**:
- Adjust time commitment (light/moderate/intensive)
- Focus areas (career advancement/thought leadership/business growth)
- Platform priorities
- Content type preferences

---

## 2. Content Strategy & Creation

### 2.1 Content Planning

#### Feature: AI Editorial Calendar

**Purpose**: Generate a 30-day content calendar with specific topics, formats, and publishing dates.

**Input Parameters**:
- User's content pillars (e.g., leadership, product strategy, career advice)
- Posting frequency preference
- Platform selection
- Current industry trends
- User's expertise areas
- Previous content performance

**Calendar Features**:

**View Options**:
- Month view with overview
- Week view with details
- List view with filters
- Platform-specific views

**Content Suggestions**:
- Topic for each day
- Recommended format (post, article, video, poll)
- Supporting talking points
- Related trending hashtags
- Best time to post
- Estimated engagement potential

**Example Calendar Entry**:
```
Date: November 15, 2025
Platform: LinkedIn
Format: Carousel Post
Topic: "5 Signs Your Product Roadmap is Broken"
Content Pillar: Product Strategy
Talking Points:
  - Overcommitting to features
  - No customer validation
  - Engineering-driven priorities
  - Lack of measurable outcomes
  - No strategic themes
Best Time: 8:00 AM EST (Tuesday)
Hashtags: #ProductManagement #ProductStrategy #ProductRoadmap
```

**Interactive Features**:
- Drag-and-drop to reschedule
- Mark as drafted/scheduled/published
- Bulk actions (reschedule week, duplicate series)
- Export to Google Calendar/Outlook
- Share calendar with team members

**AI Enhancements**:
- Trend integration: "This week, many PM influencers are discussing AI tools"
- Gap analysis: "You haven't posted about career advice in 2 weeks"
- Content mix optimization: "Try adding more personal stories - they get 2x engagement"
- Seasonal relevance: "Q4 planning season - share your framework"

---

#### Feature: Content Mix Optimizer

**Purpose**: Ensure healthy balance of content types and topics for maximum engagement and growth.

**Framework**:

**70-20-10 Rule**:
- 70% Educational/Value-driven content
- 20% Personal stories and experiences
- 10% Promotional/Self-serving content

**Content Type Distribution**:
- Quick tips and insights: 40%
- Personal stories: 20%
- In-depth tutorials: 15%
- Questions and engagement: 15%
- Reposts and commentary: 10%

**Tone Variation**:
- Inspirational: 25%
- Educational: 50%
- Conversational: 20%
- Controversial/Provocative: 5%

**Dashboard Display**:
- Visual pie charts showing current distribution
- Recommendations for next posts
- Alerts when imbalanced (e.g., "Too much self-promotion this week")
- Historical trends
- Comparison to high-performing accounts

---

### 2.2 AI-Powered Content Generation

#### Feature: Intelligent Post Creator

**Purpose**: Generate platform-specific posts that match user's voice and brand guidelines.

**Input Methods**:

**1. Topic-Based**:
- User enters topic: "Product-market fit"
- AI generates complete post

**2. Bullet Points**:
- User provides key points
- AI creates narrative structure

**3. Voice Note**:
- User records 1-2 minute explanation
- AI transcribes and formats

**4. Repurpose Existing**:
- Upload article/presentation
- AI extracts key insights for posts

**Generation Process**:
```
1. Analyze input topic/content
2. Determine post format (story, list, insight, question)
3. Apply user's voice profile
4. Structure content for platform
5. Add engagement elements (hook, CTA)
6. Optimize for readability
7. Suggest visuals/formatting
8. Generate variants
```

**Output Options**:
- 3 variations per request (different angles/tones)
- Length options (short/medium/long)
- Tone adjustments (professional/casual/bold)
- Platform adaptations (LinkedIn/Twitter/Instagram)

**Example Generation**:

*User Input*: "I want to write about the importance of saying no as a product manager"

*AI Output 1 - Story Format*:
```
Early in my PM career, I said yes to everything.

Every stakeholder request. Every "quick" feature. Every meeting invite.

Result? Nothing shipped on time. Team was burned out. Strategy was lost.

The turning point: I started asking "What are we NOT doing?"

Saying no isn't about being difficult. It's about protecting your strategy.

3 questions I ask before saying yes:
→ Does this align with our top 3 priorities?
→ What will we stop doing to make room?
→ Will this matter in 6 months?

The best PMs aren't the ones who ship the most features.

They're the ones who ship the right features.

What's one thing you need to say no to this week?

#ProductManagement #Leadership #PrioritizationStrategy
```

*AI Output 2 - Insight Format*:
```
Your ability to say "no" is more valuable than your ability to say "yes."

Why most product roadmaps fail:
- Too many priorities (which means no priorities)
- Every stakeholder gets a feature
- No clear strategy
- Everything is "urgent"

The 3-3-3 rule I use:
→ 3 strategic themes max
→ 3 major initiatives per quarter
→ 3 criteria for accepting new requests

Before adding to the roadmap, ask:
1. Does this serve our top users?
2. Does this drive our key metrics?
3. Can only we build this?

If not all three → the answer is no.

What frameworks help you prioritize?

#ProductStrategy #Prioritization
```

*AI Output 3 - Question Format*:
```
PMs: What's harder for you?

A) Saying "yes" to the right things
B) Saying "no" to the wrong things

I used to think A was the challenge.

But after managing 10+ products, I've learned B is the real skill.

Every "yes" costs:
- Engineering time
- Opportunity cost
- Strategic focus
- Technical debt

Every "no" protects:
- Your roadmap
- Your team's sanity
- Your product vision
- Your ability to ship quality

The best product advice I received:
"Your roadmap should be 1/3 of what you want to build, not everything."

How do you decide what makes the cut?

#ProductManagement #Leadership
```

**Quality Controls**:
- Brand voice consistency score
- Readability metrics (Flesch-Kincaid)
- Engagement prediction score
- Plagiarism check
- Factual accuracy review (for claims)

---

#### Feature: Long-Form Content Assistant

**Purpose**: Help users create blog posts, articles, and newsletters with AI assistance.

**Workflow**:

**1. Outline Generation**:
- User provides topic and key points
- AI creates structured outline
- User reviews and modifies
- AI expands each section

**2. Collaborative Writing**:
- User writes opening paragraph
- AI suggests next section
- User accepts/edits/rewrites
- Iterative process throughout article

**3. Full Draft**:
- User provides comprehensive brief
- AI generates complete first draft
- User edits for personal touches
- AI refines based on edits

**Features**:
- SEO optimization suggestions
- Headline analyzer (10 options generated)
- Reading time estimator
- Internal linking suggestions
- Image placement recommendations
- Pull quote identification
- Social media snippet extraction

**Templates**:
- The Framework Article ("5-step process for...")
- The Case Study ("How we achieved X")
- The Opinion Piece ("Why I believe...")
- The Tutorial ("Complete guide to...")
- The Listicle ("10 lessons from...")
- The Story ("The time when...")

**Quality Enhancements**:
- Transition improvement suggestions
- Active voice recommendations
- Jargon simplification
- Structure optimization
- Engagement element addition

---

### 2.3 Visual Content Support

#### Feature: Brand Visual Guidelines

**Purpose**: Define and maintain consistent visual identity across all content.

**Components**:

**Color Palette**:
- Primary colors (2-3 colors)
- Secondary colors (2-3 colors)
- Accent colors
- Background colors
- Text colors
- Hex codes provided for each

**Typography**:
- Header font selection
- Body text font
- Size hierarchies
- Spacing guidelines

**Logo/Personal Mark**:
- Upload personal logo or headshot
- Guidelines for placement
- Required clear space
- Color variations

**Image Style**:
- Photography style (professional, candid, etc.)
- Filter preferences
- Image composition guidelines
- Stock photo recommendations

**Template Library**:
- LinkedIn carousel templates (10+ designs)
- Instagram post templates
- Twitter header images
- Blog post featured images
- Presentation slide templates
- Email newsletter headers

**AI Features**:
- Color palette generator from uploaded images
- Font pairing recommendations
- Template customization based on brand
- Image filter application
- Auto-branding of uploads

---

## 3. Performance Analytics

### 3.1 Engagement Metrics Dashboard

#### Feature: Unified Analytics Dashboard

**Purpose**: Provide comprehensive view of performance across all platforms in one place.

**Dashboard Sections**:

**Overview Panel**:
- Total followers/connections across platforms
- Follower growth (this week/month/quarter)
- Total engagement (likes + comments + shares)
- Engagement rate
- Top performing post
- Publishing consistency score

**Platform Breakdown**:
```
LinkedIn:
├── Followers: 2,450 (+125 this month)
├── Engagement Rate: 4.2%
├── Post Frequency: 3.2x/week
├── Best Time to Post: Tuesday 8 AM
└── Top Content: "5 Signs Your Roadmap is Broken" (1,250 reactions)

Twitter:
├── Followers: 1,800 (+89 this month)
├── Engagement Rate: 2.1%
├── Post Frequency: 5x/week
├── Best Time to Post: Wednesday 2 PM
└── Top Content: Thread on product strategy (450 likes)
```

**Content Performance Table**:
| Post | Date | Platform | Impressions | Engagement | Rate |
|------|------|----------|-------------|------------|------|
| "Product-Market Fit Framework" | Nov 5 | LinkedIn | 8,500 | 425 | 5.0% |
| "My biggest PM mistake" | Nov 3 | LinkedIn | 12,000 | 480 | 4.0% |

**Audience Insights**:
- Demographic breakdown
- Geographic distribution
- Industry/job title analysis
- Follower growth trends
- Audience overlap across platforms

**Goal Progress**:
- Visual progress bars for user-defined goals
- Milestone celebrations
- Projected completion dates
- Recommendations to accelerate

**Visualization Options**:
- Line charts for trends over time
- Bar charts for comparisons
- Heat maps for posting patterns
- Engagement funnels

---

#### Feature: AI-Powered Insights Engine

**Purpose**: Translate data into actionable insights and recommendations.

**Insight Types**:

**Performance Insights**:
- "Your LinkedIn posts on Friday get 2.5x more engagement than Monday posts"
- "Posts with personal stories outperform pure educational content by 40%"
- "Your engagement rate is in the top 15% for product managers"
- "Comments drive 3x more reach than likes on your content"

**Content Insights**:
- "Your 'career advice' content gets the most saves - create more"
- "Lists and frameworks consistently perform well for you"
- "Posts with emojis get 30% less engagement from your audience"
- "Your audience responds well to questions in your opening line"

**Audience Insights**:
- "65% of your new followers are Senior PMs and above - great target alignment"
- "You're attracting more founders lately - consider creating startup-focused content"
- "Engagement peaks when you post between 7-9 AM EST"
- "Your audience is most active Tuesday through Thursday"

**Competitive Insights**:
- "You're posting 30% less than top performers in your niche"
- "Your engagement rate is strong, but reach is limited by posting frequency"
- "Similar accounts are finding success with video content"

**Recommendations**:
```
Priority 1: Increase Posting Frequency
Why: Your engagement rate is high (4.2%) but you're only posting 2x/week. 
Analysis shows consistent posters grow 3x faster.
Action: Aim for 3-4 posts per week for next 30 days.

Priority 2: Leverage Personal Stories
Why: Your personal story posts get 85% more comments than other content types.
Action: Mix in 1-2 personal stories per week. They build deeper connections.

Priority 3: Optimize Posting Times
Why: You're posting at random times. Tuesday 8 AM gets your best performance.
Action: Schedule posts during peak engagement windows.
```

**Learning Mode**:
- Track which recommendations were implemented
- Measure impact of changes
- Refine future suggestions
- A/B test different approaches

---

## 4. Community & Network Building

### 4.1 Engagement Assistance

#### Feature: Smart Comment Response Generator

**Purpose**: Help users respond to comments and messages efficiently while maintaining authenticity.

**Functionality**:

**Comment Analysis**:
- Categorizes comments (question, appreciation, disagreement, spam)
- Identifies high-value interactions (influencers, potential clients)
- Flags comments requiring thoughtful response
- Marks spam/low-value for ignore

**Response Generation**:
```
Original Comment: "Great post! How do you handle conflicting priorities from 
different stakeholders?"

AI Generated Responses:

Option 1 (Detailed):
"Great question! I use a simple framework: 
1) Align everyone on the top business metric
2) Score each priority against that metric
3) Let the data drive the conversation

The key is getting stakeholders to agree on what success looks like BEFORE 
discussing features. Happy to share my scoring template if helpful!"

Option 2 (Engaging):
"This is THE challenge isn't it? I've found the trick is getting everyone to 
agree on the success metric first. Once you have that, priorities become clearer.

What's worked for you?"

Option 3 (Brief):
"The key is aligning on the success metric first, then prioritizing against 
that. Changes the conversation entirely!"
```

**Smart Features**:
- Tone matching to comment style
- Question prompts to encourage dialogue
- Name personalization
- Context awareness (references post content)
- Follow-up suggestions

**Bulk Response Mode**:
- Process multiple comments at once
- Similar comments get similar responses
- One-click to approve and post
- Queue management
- Response time tracking

---

#### Feature: Networking Recommendations

**Purpose**: Identify valuable connections and facilitate relationship building.

**Recommendation Engine**:

**People to Connect With**:
```
High Priority Connections:

1. Sarah Kim - VP Product at Salesforce
   - In your target industry
   - Engaged with your last 3 posts
   - Shares similar content themes
   - Action: Send connection request with note
   - Suggested message: "Hi Sarah, I've noticed we share similar perspectives 
     on product strategy. Would love to connect!"

2. Michael Chen - Product Coach
   - Posted content you could comment on
   - Has audience you want to reach
   - Potential collaboration opportunity
   - Action: Comment on his recent post about OKRs

3. Lisa Patel - Director of PM at Stripe
   - Works at your target company
   - Mutual connections (3)
   - Recently posted about hiring PMs
   - Action: Engage with content, then connect in 1 week
```

**Engagement Opportunities**:
- Posts from target connections to comment on
- Conversation threads to join
- Questions to answer in groups
- Events to attend (virtual/in-person)

**Relationship Tracking**:
- Last interaction date
- Interaction frequency
- Relationship strength score
- Follow-up reminders
- Notes and context

**Collaboration Matching**:
- Guest post opportunities
- Podcast appearance suggestions
- Co-creation potential
- Mutual benefit analysis

---

## 5. Media Opportunities & Thought Leadership

### 5.1 Article Writing Opportunities (HARO-Style)

#### Feature: Journalist Query Feed

**Purpose**: Connect users with journalist requests seeking expert sources for articles, matching them to relevant opportunities.

**User Flow**:
1. User opens Media Opportunities dashboard
2. Views daily feed of 3-5 journalist queries matched to their expertise
3. Clicks on query to see full details
4. Reviews AI-generated pitch response
5. Customizes pitch with specific examples
6. Submits response via platform or copies to email
7. Tracks submission status and follow-ups

**Data Collected**:
- User expertise areas and content pillars
- Past media appearances and credibility signals
- Preferred publication types and audience size
- Time availability for interviews/quotes
- Geographic and industry preferences

**Technical Requirements**:
- Integration with HARO API
- Social media monitoring for journalist requests (Twitter/X, LinkedIn)
- Industry publication database
- Query categorization by topic, industry, urgency
- Match scoring algorithm (expertise + content pillars + deadlines)
- Email template generation
- Submission tracking system
- Publication impact metrics

**Query Display Format**:
```
🎯 MATCH SCORE: 92/100

Journalist Request:
"Tech journalist seeking product management experts for TechCrunch article 
on AI integration in product roadmaps"

Publication: TechCrunch
Reach: 500K+ monthly readers
Deadline: 24 hours
Category: Product Management, AI, Technology

Why This Matches:
✓ Aligns with your "Product Strategy" content pillar
✓ TechCrunch audience overlaps with your target demographic
✓ You've published on AI and roadmapping before

Your Suggested Angle:
"Share your framework for evaluating AI features using customer value metrics"

What They Need:
- 3-5 specific examples or data points
- 200-300 word expert quote
- Professional headshot and bio
- Response by: Nov 13, 5:00 PM EST
```

**AI Pitch Generation**:
```
Input: User expertise + query details + content history
Output: Personalized pitch email

Example:
---
Subject: PM Expert for AI Roadmap Article - [Your Name]

Hi [Journalist Name],

I saw your query seeking product management experts for your TechCruch article 
on AI in roadmapping. I'd be happy to contribute.

I'm [Your Name], [Your Title] with 8+ years leading product teams at [Companies]. 
I specialize in AI feature prioritization and have written extensively about 
product strategy on my Substack (5K subscribers).

Unique angles I can provide:
• Framework for scoring AI features against customer value metrics
• Real example: How we evaluated 50+ AI feature ideas down to 3 priorities
• Data on AI feature adoption rates vs traditional features (from my research)

I can provide:
- 3-5 specific, quotable insights with data
- 300-word expert perspective
- Professional headshot and bio
- Response within 8 hours

My previous features: [Link to media portfolio]

Available for follow-up questions at [phone/email].

Best regards,
[Your Name]
---
```

**Success Metrics**:
- Query match accuracy: 80%+ relevance based on user feedback
- Pitch generation time: < 2 minutes
- Response submission: 40% of high-match queries receive user response
- Acceptance rate: 25% of submitted pitches result in publication
- Time saved: 15 minutes per opportunity vs manual search and draft

---

#### Feature: Publication Impact Tracking

**Purpose**: Monitor and measure the impact of published articles on brand growth.

**Tracking Capabilities**:
- Published article URL submission
- Publication date and outlet
- Estimated reach (publication audience size)
- Backlinks to user's platforms
- Referral traffic from article
- Follower growth correlation
- Social shares and engagement

**Impact Dashboard**:
```
Article Performance

"5 Product Strategy Mistakes" - TechCrunch
Published: Nov 10, 2025
Reach: 500K readers
Impact:
├─ Referral Traffic: 2,500 visits to your Substack
├─ New Followers: +45 LinkedIn, +30 Substack subscribers
├─ Backlinks: 3 high-authority links
├─ Social Shares: 850 shares
└─ Estimated ROI: 10x (time invested vs reach gained)

Growth Correlation:
During publication week: +35% follower growth vs baseline
```

---

### 5.2 Podcast Guest Opportunities

#### Feature: Podcast Discovery & Matching

**Purpose**: Connect users with podcast hosts actively seeking guests in their expertise area.

**Discovery Sources**:
- PodMatch platform integration
- MatchMaker.fm API
- PodcastGuests.com database
- Social media monitoring (hosts posting guest callouts)
- Podcast directory scanning (Apple Podcasts, Spotify)
- Guest request communities (Reddit, LinkedIn groups)
- Reverse engineering (where similar experts appeared)

**Matching Algorithm**:
```
Score = (Topic Alignment × 0.30) 
      + (Audience Overlap × 0.25)
      + (Show Quality × 0.20)
      + (Growth Potential × 0.15)
      + (Host Credibility × 0.10)

Topic Alignment: Match between show topics and user's content pillars
Audience Overlap: Show listener demographics vs user's target audience
Show Quality: Production quality, consistency, listener reviews
Growth Potential: Show growth trajectory and audience engagement
Host Credibility: Host background, guest caliber, industry reputation
```

**Opportunity Display**:
```
🎙️ MATCH SCORE: 88/100

Product Thinking Podcast
Host: Melissa Perri
Audience: 25K per episode • B2B Product Leaders
Format: 45-60 min deep-dive interviews
Frequency: Weekly

Why This Matches:
✓ 95% topic alignment (product strategy, team scaling)
✓ Audience is 80% your target demographic (B2B PMs, Directors)
✓ High show quality (professional production, consistent schedule)
✓ Growing audience (+15% monthly)

Recent Guest Topics:
- "Building product organizations from 5 to 50"
- "Transitioning from IC to product leadership"
- "Metrics that actually matter for product teams"

Your Pitch Angle:
"Scaling product teams without losing innovation velocity"

Suggested Episode Topics (choose 1-2):
1. "The 3-phase framework for scaling product orgs"
2. "Hiring vs promoting: Building your product leadership bench"
3. "Maintaining product velocity as teams grow"

Application Process:
Apply via: Website form
Lead Time: 4-6 weeks from application to recording
Preparation: 30-min pre-call with producer

Impact Potential: High (large, engaged audience in your niche)
```

**User Flow**:
1. Browse daily podcast opportunity feed (5-7 shows)
2. Filter by audience size, topic, format, time commitment
3. Click opportunity to view show details:
   - Recent episode list and topics
   - Guest profile analysis
   - Listener demographics
   - Host interview style
   - Application requirements
4. Generate personalized pitch
5. Review and customize pitch email
6. Submit application via platform or email
7. Track application status
8. Receive booking confirmation
9. Access interview preparation materials

---

#### Feature: Interview Preparation Assistant

**Purpose**: Help users prepare for podcast interviews with talking points and key messages.

**Preparation Workflow**:

**1. Pre-Interview Brief** (Generated 1 week before recording)
```
Interview Prep: Product Thinking Podcast
Recording Date: Dec 15, 2025, 2:00 PM EST
Format: 60-minute conversation
Host: Melissa Perri

YOUR KEY MESSAGES (Aligned with content pillars):

1. Product Strategy Pillar:
   → Main Message: "Scaling product teams requires deliberate systems, not just headcount"
   → Supporting Points:
     • The 3-phase scaling framework (0-10, 10-50, 50+ people)
     • Metrics that matter at each phase
     • Common pitfalls to avoid

2. Leadership Pillar:
   → Main Message: "Great product leaders build decision-making frameworks, not make all decisions"
   → Supporting Points:
     • Delegation without chaos
     • Hiring for judgment vs experience
     • Creating autonomous teams

3. Career Development Pillar:
   → Main Message: "The IC to leadership transition is a skill shift, not a promotion"
   → Supporting Points:
     • Skills that got you here won't get you there
     • Learning to lead through others
     • Measuring success differently
```

**2. Story Bank** (Curated from user's content and profile)
```
YOUR BEST STORIES TO SHARE:

High-Impact Stories:
1. "The roadmap that killed innovation"
   Setup: Team grew from 5 to 30, suddenly nothing shipped
   Conflict: Too many features, no focus, burned out team
   Resolution: Implemented 3-priority system, shipped 3x in next quarter
   Lesson: "Your roadmap should be 1/3 of what you want to build"
   Use when: Discussing scaling challenges, prioritization

2. "The PM I almost didn't hire"
   Setup: Candidate didn't fit traditional PM mold
   Conflict: Debate with hiring team about unconventional background
   Resolution: Hired anyway, became star performer
   Lesson: "Hire for judgment and curiosity, not resume checkboxes"
   Use when: Discussing hiring, team building, talent identification

3. "Saying no to the CEO"
   Setup: CEO wanted pet feature on roadmap
   Conflict: Feature didn't align with strategy or customer needs
   Resolution: Presented data, offered alternative, CEO agreed
   Lesson: "Product strategy means protecting what you say no to"
   Use when: Discussing stakeholder management, strategy, courage
```

**3. Likely Questions & Answers**
```
EXPECT THESE QUESTIONS:

Q: "What's the biggest mistake you see product leaders make when scaling?"
Your Answer:
"Trying to scale the team before scaling the systems. Leaders hire 10 PMs 
but don't create frameworks for decision-making, prioritization, or communication. 
You end up with more people but less clarity.

My framework: For every 5 people you add, create 1 new system. At 10 people, 
you need clear prioritization frameworks. At 20, product strategy documents. 
At 30, decision-making authorities defined.

Story: [Use "The roadmap that killed innovation" story]"

Q: "How do you maintain innovation as teams grow?"
Your Answer:
[AI-generated based on your content pillars and past writing]

Q: "What advice would you give someone making the IC to manager transition?"
Your Answer:
[AI-generated based on your career pillar content]
```

**4. Technical & Logistics Checklist**
```
RECORDING SETUP:

Equipment:
☐ Test microphone (use [recommended mic])
☐ Check audio levels in quiet space
☐ Have headphones ready
☐ Close background apps/notifications

Environment:
☐ Quiet room, minimal echo
☐ "Recording - Do Not Disturb" sign on door
☐ Turn off phone notifications
☐ Have water nearby (muted sips only!)

Pre-Recording:
☐ Join 5 minutes early
☐ Quick audio/video check with producer
☐ Have notes/story bank visible but not reading
☐ Relaxed and conversational tone

During Recording:
☐ Speak clearly and with energy
☐ Use specific examples and stories
☐ Tie back to key messages
☐ Be yourself, authentic > perfect
```

**5. Post-Interview Action Plan**
```
AFTER RECORDING (Execute within 24 hours):

Immediate:
☐ Send thank you email to host/producer
☐ Connect with host on LinkedIn
☐ Share recording date on social media (teaser)
☐ Add to media portfolio tracking

When Episode Publishes:
☐ Share on all platforms (LinkedIn, Twitter, Substack)
☐ Tag host and show in posts
☐ Create derivative content:
   - LinkedIn post with key insights
   - Twitter thread of best quotes
   - Substack article expanding on main topic
   - YouTube clip (if video podcast)
☐ Thank engaged listeners in comments
☐ Monitor referral traffic and new followers
☐ Update media portfolio with metrics

Repurposing Plan:
Week 1: Share episode announcement
Week 2: LinkedIn carousel of key frameworks discussed
Week 3: Substack article: "Expanded thoughts from my podcast appearance"
Week 4: YouTube clip of best 5-minute segment
```

---

#### Feature: Media Portfolio & ROI Tracking

**Purpose**: Centralized dashboard of all media appearances with impact analytics.

**Portfolio Display**:
```
YOUR MEDIA PORTFOLIO

Total Appearances: 12
Total Reach: 850K people
Average ROI: 8.5x (time invested vs reach gained)

ARTICLES (7)
──────────────────────────────────────────────
TechCrunch: "AI in Product Roadmaps"
Date: Nov 10, 2025
Reach: 500K readers
Impact: +45 LinkedIn followers, 2.5K website visits
ROI: 12x

SaaStr: "Scaling Product Teams"
Date: Oct 15, 2025
Reach: 80K readers
Impact: +15 followers, 500 visits, 3 quality leads
ROI: 6x

[View all articles →]

PODCASTS (5)
──────────────────────────────────────────────
Product Thinking Podcast
Date: Dec 1, 2025
Reach: 25K downloads
Impact: +120 Substack subscribers, +60 LinkedIn
ROI: 10x
Content Created: 1 article, 3 social posts, 1 video clip

The PM Career Show
Date: Oct 20, 2025
Reach: 5K downloads
Impact: +25 followers, high engagement
ROI: 5x

[View all podcasts →]

IMPACT TRENDS
──────────────────────────────────────────────
[Graph showing follower growth correlation with media appearances]

Best Performing Media Type: High-authority publications (12x avg ROI)
Optimal Frequency: 2-3 appearances per month
Peak Growth Period: Week following publication/episode release
```

**Impact Metrics Tracked**:
- Publication/episode reach (audience size)
- Referral traffic to owned platforms
- Follower growth correlation (spike analysis)
- Backlinks and domain authority
- Social media mentions and shares
- Lead generation (for business-focused creators)
- Speaking opportunity leads from media
- Time invested vs reach gained (ROI)

---

## 6. Implementation Priorities

### Phase 1: MVP (Must-Have)
1. Brand assessment and strategy generation
2. Content creation for LinkedIn
3. Editorial calendar
4. Basic analytics dashboard
5. Publishing to LinkedIn

### Phase 2: Enhanced (Should-Have)
1. Multi-platform support (Twitter, Medium)
2. Advanced analytics and insights
3. Comment response assistance
4. Long-form content support
5. Visual brand guidelines
6. **Media Opportunities: Article writing queries (HARO integration)**
7. **AI pitch generation for journalist requests**

### Phase 3: Advanced (Nice-to-Have)
1. Video content support
2. Networking recommendations
3. A/B testing
4. Competitor analysis
5. Mobile apps
6. **Podcast guest opportunities (PodMatch integration)**
7. **Interview preparation assistant**
8. **Media portfolio and impact tracking**

---

## Success Metrics by Feature

| Feature | Success Metric | Target |
|---------|---------------|---------|
| Onboarding | Completion rate | 85% |
| Content Generation | Posts created per week | 3+ |
| Publishing | Time from draft to publish | < 5 min |
| Analytics | Weekly dashboard visits | 70% of users |
| Engagement | Comments responded to | 60% |
| Calendar | Posts scheduled in advance | 80% |
| Strategy | Users hitting 90-day goals | 55% |
| Media Query Matching | Relevance score accuracy | 80%+ |
| Pitch Generation | Time to create pitch | < 2 min |
| Media Engagement | Users responding to opportunities | 40%+ |
| Pitch Success | Acceptance rate | 25%+ |
| Podcast Discovery | Matched shows per week | 5-7 |
| Interview Prep | Users accessing prep materials | 90% |
| Media ROI | Average reach multiplier | 8-10x |
| Portfolio Growth | Appearances per quarter | 2-3 |
