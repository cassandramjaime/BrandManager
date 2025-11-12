# Technical Architecture - AI Brand Manager

## System Overview

The AI Brand Manager is built on a cloud-native, microservices architecture designed for scalability, reliability, and rapid feature development. The system integrates multiple AI models, third-party APIs, and data processing pipelines to deliver personalized brand management services.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Client Layer                             │
├─────────────────────────────────────────────────────────────────┤
│  Web App (React)  │  Mobile Apps (React Native)  │  Browser Ext │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                       API Gateway Layer                          │
├─────────────────────────────────────────────────────────────────┤
│   REST API   │   GraphQL   │   WebSocket   │   Rate Limiting   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    Microservices Layer                           │
├──────────────┬──────────────┬──────────────┬───────────────────┤
│   User       │   Content    │   Analytics  │   Platform        │
│   Service    │   Service    │   Service    │   Integration     │
├──────────────┼──────────────┼──────────────┼───────────────────┤
│   Brand      │   AI/ML      │   Schedule   │   Notification    │
│   Strategy   │   Service    │   Service    │   Service         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                        Data Layer                                │
├──────────────┬──────────────┬──────────────┬───────────────────┤
│  PostgreSQL  │   MongoDB    │    Redis     │   Vector DB       │
│  (Relational)│ (Documents)  │   (Cache)    │  (Embeddings)     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   External Integrations                          │
├──────────────┬──────────────┬──────────────┬───────────────────┤
│   LinkedIn   │   Twitter    │    Medium    │      Stripe       │
│     API      │     API      │     API      │    (Payments)     │
└─────────────────────────────────────────────────────────────────┘
```

## Technology Stack

### Frontend

#### Web Application
- **Framework**: Next.js 14 (React 18)
- **State Management**: Zustand + React Query
- **Styling**: Tailwind CSS + shadcn/ui components
- **Charts**: Recharts / Chart.js
- **Rich Text Editor**: Tiptap / Lexical
- **Authentication**: NextAuth.js
- **Forms**: React Hook Form + Zod validation

#### Mobile Applications (Future Phase)
- **Framework**: React Native with Expo
- **Navigation**: React Navigation
- **State**: Redux Toolkit
- **UI Components**: React Native Paper

#### Browser Extension
- **Manifest**: V3
- **Framework**: React with Plasmo
- **Storage**: Chrome Storage API

### Backend

#### API Layer
- **Framework**: Node.js with Express.js / Fastify
- **GraphQL**: Apollo Server
- **API Documentation**: OpenAPI/Swagger
- **Validation**: Joi / Zod
- **Authentication**: JWT with refresh tokens
- **Rate Limiting**: Redis-backed token bucket

#### Microservices

**User Service**
- User authentication and authorization
- Profile management
- Account settings
- Subscription management
- Tech: Node.js, PostgreSQL

**Brand Strategy Service**
- Onboarding questionnaire processing
- Brand assessment analysis
- Strategy generation
- UVP creation
- Tech: Node.js, PostgreSQL, AI/ML Service integration

**Content Service**
- Content creation and management
- Draft storage and versioning
- Publishing workflow
- Content templates
- Tech: Node.js, MongoDB

**AI/ML Service**
- LLM integration (GPT-4, Claude)
- Content generation
- Voice profile learning
- Sentiment analysis
- Recommendation engine
- Tech: Python (FastAPI), Vector DB, GPU instances

**Analytics Service**
- Data aggregation from platforms
- Metrics calculation
- Insight generation
- Reporting
- Tech: Node.js, PostgreSQL, Time-series DB

**Platform Integration Service**
- OAuth flows for social platforms
- API communication
- Webhook handling
- Rate limit management
- Tech: Node.js, Redis

**Schedule Service**
- Content scheduling
- Automated publishing
- Cron jobs
- Reminder system
- Tech: Node.js, Bull Queue, Redis

**Notification Service**
- Email notifications (SendGrid)
- Push notifications
- In-app notifications
- Webhook delivery
- Tech: Node.js, Redis

### Data Layer

#### PostgreSQL (Primary Database)
**Schema Design**:

```sql
-- Users and Authentication
users
├── id (UUID, PK)
├── email (unique)
├── password_hash
├── subscription_tier
├── created_at
└── updated_at

user_profiles
├── id (UUID, PK)
├── user_id (FK -> users)
├── full_name
├── headline
├── bio
├── industry
├── experience_level
├── profile_image_url
└── brand_data (JSONB)

-- Brand Strategy
brand_strategies
├── id (UUID, PK)
├── user_id (FK -> users)
├── value_proposition
├── target_audience (JSONB)
├── content_pillars (JSONB)
├── goals (JSONB)
└── created_at

-- Platform Connections
platform_connections
├── id (UUID, PK)
├── user_id (FK -> users)
├── platform (enum: linkedin, twitter, etc.)
├── access_token (encrypted)
├── refresh_token (encrypted)
├── expires_at
└── platform_user_id

-- Content Scheduling
scheduled_content
├── id (UUID, PK)
├── user_id (FK -> users)
├── content_id (FK -> content)
├── platforms (array)
├── scheduled_for
├── status (enum: pending, published, failed)
└── published_at

-- Analytics
analytics_snapshots
├── id (UUID, PK)
├── user_id (FK -> users)
├── platform
├── metric_type
├── metric_value
├── snapshot_date
└── metadata (JSONB)
```

#### MongoDB (Document Store)
**Collections**:

```javascript
// Content drafts and published content
content {
  _id: ObjectId,
  userId: UUID,
  type: "post" | "article" | "video_script",
  title: String,
  body: String,
  platform: ["linkedin", "twitter"],
  metadata: {
    wordCount: Number,
    readingTime: Number,
    hashtags: [String],
    mentions: [String]
  },
  versions: [{
    body: String,
    updatedAt: Date,
    updatedBy: String
  }],
  aiMetadata: {
    generatedFrom: String,
    modelUsed: String,
    voiceScore: Number
  },
  status: "draft" | "scheduled" | "published",
  performanceData: {
    impressions: Number,
    engagement: Number,
    engagementRate: Number
  },
  createdAt: Date,
  updatedAt: Date
}

// Editorial calendar
editorial_calendar {
  _id: ObjectId,
  userId: UUID,
  month: Date,
  entries: [{
    date: Date,
    topic: String,
    contentPillar: String,
    format: String,
    platform: [String],
    status: String,
    contentId: ObjectId
  }],
  updatedAt: Date
}

// AI learning data
user_voice_profiles {
  _id: ObjectId,
  userId: UUID,
  writingSamples: [String],
  voiceCharacteristics: {
    tonePreferences: [String],
    sentenceStructure: Object,
    vocabularyPatterns: Object,
    engagementStyle: String
  },
  learningData: [{
    content: String,
    userFeedback: "accept" | "edit" | "reject",
    timestamp: Date
  }],
  lastTrainedAt: Date
}
```

#### Redis (Cache & Queue)
**Usage**:
- Session management
- API rate limiting
- Background job queues (Bull)
- Real-time data caching
- Pub/Sub for real-time features

**Key Patterns**:
```
user:session:{userId} -> session data (TTL: 7 days)
api:ratelimit:{userId}:{endpoint} -> request counter (TTL: 1 hour)
cache:analytics:{userId}:{platform} -> analytics data (TTL: 1 hour)
queue:content:publish -> publishing jobs
queue:ai:generation -> AI generation jobs
queue:analytics:fetch -> analytics fetching jobs
```

#### Vector Database (Pinecone / Weaviate)
**Purpose**: Semantic search and recommendations

**Collections**:
```
content_embeddings
├── vector (1536 dimensions for OpenAI embeddings)
├── metadata
│   ├── contentId
│   ├── userId
│   ├── platform
│   ├── performanceScore
│   └── timestamp
└── text (original content)

topic_embeddings
├── vector
├── metadata
│   ├── topic
│   ├── category
│   └── popularity
└── description
```

### AI/ML Components

#### Language Model Integration

**Primary Model**: GPT-4 Turbo
- Content generation
- Strategy formulation
- Insight generation

**Fine-tuned Models**:
- User voice replication
- Platform-specific optimization
- Engagement prediction

**Model Pipeline**:
```python
class ContentGenerator:
    def __init__(self):
        self.base_model = "gpt-4-turbo"
        self.voice_adapter = load_user_voice_model()
        
    async def generate_post(self, user_id, topic, platform):
        # 1. Retrieve user voice profile
        voice_profile = await get_voice_profile(user_id)
        
        # 2. Get relevant context from vector DB
        context = await get_similar_content(topic, user_id)
        
        # 3. Build prompt with voice characteristics
        prompt = build_prompt(
            topic=topic,
            platform=platform,
            voice_profile=voice_profile,
            context=context,
            examples=get_high_performing_examples(user_id)
        )
        
        # 4. Generate content
        response = await openai.chat.completions.create(
            model=self.base_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        # 5. Post-process and validate
        content = post_process(response.choices[0].message.content)
        
        # 6. Calculate confidence scores
        scores = {
            "voice_match": calculate_voice_similarity(content, voice_profile),
            "engagement_prediction": predict_engagement(content, platform),
            "brand_alignment": check_brand_alignment(content, user_id)
        }
        
        return {
            "content": content,
            "scores": scores,
            "variants": await generate_variants(content, n=2)
        }
```

#### Recommendation Engine

```python
class RecommendationEngine:
    def __init__(self):
        self.vector_db = get_vector_db_client()
        self.analytics_db = get_analytics_db()
        
    async def recommend_topics(self, user_id, count=10):
        # Get user's content pillars and interests
        pillars = await get_content_pillars(user_id)
        
        # Get trending topics in user's industry
        trends = await get_industry_trends(user_id)
        
        # Get topics user hasn't covered recently
        content_history = await get_recent_content(user_id, days=30)
        covered_topics = extract_topics(content_history)
        
        # Find gaps and opportunities
        recommendations = []
        
        # Trend-based recommendations
        for trend in trends:
            if trend not in covered_topics:
                relevance = calculate_relevance(trend, pillars)
                recommendations.append({
                    "topic": trend,
                    "type": "trending",
                    "relevance": relevance,
                    "engagement_potential": predict_engagement(trend)
                })
        
        # Semantic search for related topics
        for pillar in pillars:
            similar = await self.vector_db.search(
                pillar,
                filter={"userId": {"$ne": user_id}},
                top_k=5
            )
            recommendations.extend(similar)
        
        # Score and rank
        ranked = rank_recommendations(
            recommendations,
            user_preferences=await get_user_preferences(user_id),
            historical_performance=await get_performance_data(user_id)
        )
        
        return ranked[:count]
```

#### Analytics & Insights

```python
class InsightGenerator:
    async def generate_monthly_insights(self, user_id):
        # Fetch data
        current_month = await get_analytics(user_id, period="month")
        previous_month = await get_analytics(user_id, period="previous_month")
        
        insights = []
        
        # Performance comparison
        if current_month.engagement_rate > previous_month.engagement_rate * 1.2:
            insights.append({
                "type": "positive",
                "category": "engagement",
                "message": f"Your engagement rate increased by {calculate_pct_change()}%",
                "recommendation": "Keep posting similar content types"
            })
        
        # Content analysis
        top_content = analyze_top_performing_content(current_month)
        patterns = detect_patterns(top_content)
        
        for pattern in patterns:
            insights.append({
                "type": "insight",
                "category": "content",
                "message": f"Posts about {pattern.topic} get {pattern.boost}x more engagement",
                "recommendation": f"Create more content about {pattern.topic}"
            })
        
        # Timing optimization
        best_times = analyze_posting_times(current_month)
        insights.append({
            "type": "optimization",
            "category": "timing",
            "message": f"Your best posting time is {best_times[0]}",
            "recommendation": f"Schedule important posts for {best_times[0]}"
        })
        
        # Competitive analysis
        competitor_data = await get_competitor_benchmarks(user_id)
        comparison = compare_performance(current_month, competitor_data)
        
        insights.append({
            "type": "benchmark",
            "category": "competitive",
            "message": f"You're in the top {comparison.percentile}% for engagement rate",
            "recommendation": comparison.recommendation
        })
        
        return {
            "insights": insights,
            "summary": generate_summary(insights),
            "action_items": extract_action_items(insights)
        }
```

### Infrastructure

#### Cloud Provider: AWS (Primary)

**Compute**:
- ECS/Fargate for containerized microservices
- Lambda for serverless functions (webhooks, scheduled jobs)
- EC2 GPU instances for ML model inference

**Storage**:
- S3 for file storage (images, documents)
- CloudFront CDN for static assets
- EBS for database volumes

**Database**:
- RDS PostgreSQL (Multi-AZ)
- DocumentDB (MongoDB-compatible)
- ElastiCache Redis (cluster mode)

**Networking**:
- VPC with public and private subnets
- Application Load Balancer
- API Gateway
- Route 53 for DNS

**Security**:
- Secrets Manager for credentials
- KMS for encryption
- WAF for DDoS protection
- IAM roles and policies

**Monitoring**:
- CloudWatch for logs and metrics
- X-Ray for distributed tracing
- SNS for alerts

#### CI/CD Pipeline

```yaml
# GitHub Actions workflow
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npm test
      - run: npm run lint
      
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: docker/build-push-action@v4
        with:
          push: true
          tags: ${{ secrets.ECR_REGISTRY }}/api:latest
          
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster production \
            --service api \
            --force-new-deployment
```

#### Scalability Considerations

**Horizontal Scaling**:
- Auto-scaling groups for microservices
- Load balancing across instances
- Stateless service design

**Vertical Scaling**:
- Database read replicas
- Caching layers
- CDN for static content

**Performance Optimization**:
- Database indexing strategy
- Query optimization
- Connection pooling
- Lazy loading
- Pagination

**Cost Optimization**:
- Reserved instances for base load
- Spot instances for batch processing
- S3 lifecycle policies
- CloudWatch cost alerts

### Security Architecture

#### Authentication & Authorization

**User Authentication**:
```javascript
// JWT-based authentication
const authMiddleware = async (req, res, next) => {
  try {
    const token = req.headers.authorization?.split(' ')[1];
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    
    // Check token in Redis (for revocation)
    const isValid = await redis.get(`token:${decoded.jti}`);
    if (!isValid) throw new Error('Token revoked');
    
    req.user = await User.findById(decoded.userId);
    next();
  } catch (error) {
    res.status(401).json({ error: 'Unauthorized' });
  }
};

// Role-based access control
const requireRole = (roles) => {
  return (req, res, next) => {
    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ error: 'Forbidden' });
    }
    next();
  };
};
```

**Platform OAuth**:
- OAuth 2.0 for third-party integrations
- Encrypted token storage
- Automatic token refresh
- Scope validation

#### Data Security

**Encryption**:
- TLS 1.3 for data in transit
- AES-256 for data at rest
- Field-level encryption for sensitive data

**Data Privacy**:
- GDPR compliance
- Data retention policies
- User data export
- Right to deletion

**API Security**:
- Rate limiting (100 req/min per user)
- Request validation
- SQL injection prevention
- XSS protection
- CORS configuration

### Monitoring & Observability

#### Metrics

**Application Metrics**:
- Request rate, latency, error rate
- Service health checks
- Queue depths
- Cache hit rates

**Business Metrics**:
- User signups and conversions
- Content creation rate
- Publishing frequency
- Platform connection success rate

**Custom Metrics**:
```javascript
// Example custom metrics
metrics.increment('content.generated', {
  platform: 'linkedin',
  tier: user.subscription_tier
});

metrics.timing('ai.generation.latency', duration, {
  model: 'gpt-4',
  content_type: 'post'
});

metrics.gauge('users.active', activeUserCount, {
  period: '24h'
});
```

#### Logging

**Structured Logging**:
```javascript
logger.info('Content generated', {
  userId: user.id,
  contentId: content.id,
  platform: 'linkedin',
  generationTime: duration,
  voiceScore: scores.voice_match
});
```

**Log Aggregation**:
- CloudWatch Logs
- Log retention: 30 days
- Searchable with CloudWatch Insights

#### Alerting

**Critical Alerts**:
- Service downtime (> 1 min)
- Error rate > 5%
- Database connection failures
- Payment processing errors

**Warning Alerts**:
- High latency (p95 > 2s)
- Queue backlog > 1000
- Cache hit rate < 80%
- Disk usage > 80%

### Disaster Recovery

**Backup Strategy**:
- Database: Daily automated backups, 30-day retention
- Point-in-time recovery enabled
- S3 versioning for files
- Cross-region replication for critical data

**Recovery Procedures**:
- RTO (Recovery Time Objective): 4 hours
- RPO (Recovery Point Objective): 1 hour
- Documented runbooks
- Regular disaster recovery drills

### Development Environment

#### Local Setup

```bash
# Clone repository
git clone https://github.com/brandmanager/api.git
cd api

# Install dependencies
npm install

# Setup environment
cp .env.example .env

# Start local services (Docker Compose)
docker-compose up -d

# Run migrations
npm run migrate

# Start development server
npm run dev
```

#### Docker Compose Configuration

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: brandmanager
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: dev
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  mongodb:
    image: mongo:6
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  api:
    build: .
    ports:
      - "3000:3000"
    depends_on:
      - postgres
      - mongodb
      - redis
    environment:
      DATABASE_URL: postgresql://dev:dev@postgres:5432/brandmanager
      MONGODB_URL: mongodb://mongodb:27017/brandmanager
      REDIS_URL: redis://redis:6379

volumes:
  postgres_data:
  mongo_data:
```

## API Design

### REST Endpoints

```
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh
POST   /api/v1/auth/logout

GET    /api/v1/users/me
PATCH  /api/v1/users/me
DELETE /api/v1/users/me

POST   /api/v1/brand/assessment
GET    /api/v1/brand/strategy
PATCH  /api/v1/brand/strategy

GET    /api/v1/content
POST   /api/v1/content
GET    /api/v1/content/:id
PATCH  /api/v1/content/:id
DELETE /api/v1/content/:id

POST   /api/v1/content/generate
POST   /api/v1/content/:id/publish
GET    /api/v1/content/:id/analytics

GET    /api/v1/calendar
POST   /api/v1/calendar/entries

GET    /api/v1/platforms
POST   /api/v1/platforms/:platform/connect
DELETE /api/v1/platforms/:platform/disconnect

GET    /api/v1/analytics/overview
GET    /api/v1/analytics/insights
GET    /api/v1/analytics/platforms/:platform
```

### GraphQL Schema

```graphql
type User {
  id: ID!
  email: String!
  profile: UserProfile!
  subscription: Subscription!
  platforms: [PlatformConnection!]!
  createdAt: DateTime!
}

type UserProfile {
  fullName: String!
  headline: String
  bio: String
  industry: String
  brandStrategy: BrandStrategy
}

type BrandStrategy {
  valueProposition: String!
  contentPillars: [String!]!
  targetAudience: TargetAudience!
  goals: [Goal!]!
}

type Content {
  id: ID!
  type: ContentType!
  title: String
  body: String!
  platforms: [Platform!]!
  status: ContentStatus!
  scheduledFor: DateTime
  performance: ContentPerformance
  createdAt: DateTime!
}

type Query {
  me: User!
  content(id: ID!): Content
  contents(filter: ContentFilter, limit: Int, offset: Int): [Content!]!
  analytics(period: AnalyticsPeriod!): Analytics!
  insights: [Insight!]!
  recommendations: Recommendations!
}

type Mutation {
  generateContent(input: GenerateContentInput!): Content!
  publishContent(id: ID!, platforms: [Platform!]!): PublishResult!
  connectPlatform(platform: Platform!, code: String!): PlatformConnection!
}

type Subscription {
  contentPublished(userId: ID!): Content!
  analyticsUpdated(userId: ID!): Analytics!
}
```

## Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| API Response Time (p95) | < 200ms | CloudWatch |
| AI Content Generation | < 10s | Application metrics |
| Page Load Time | < 2s | Web Vitals |
| Uptime | 99.9% | Status page |
| Error Rate | < 0.1% | Error tracking |
| Database Query Time (p95) | < 50ms | RDS metrics |

## Cost Estimation (Monthly)

**Infrastructure**:
- Compute (ECS): $500
- Database (RDS): $300
- Cache (Redis): $150
- Storage (S3): $100
- CDN: $200
- Total: $1,250

**AI/ML**:
- OpenAI API (10K users, avg 100 requests/user): $5,000
- Vector DB: $200
- Total: $5,200

**Third-party Services**:
- Email (SendGrid): $100
- Monitoring (Datadog): $200
- Error tracking: $50
- Total: $350

**Grand Total**: ~$6,800/month (for 10K users)
**Per-user cost**: $0.68/month

## Conclusion

This architecture is designed to be:
- **Scalable**: Handle growth from 1K to 100K+ users
- **Reliable**: 99.9% uptime with disaster recovery
- **Secure**: Enterprise-grade security practices
- **Cost-effective**: Efficient resource utilization
- **Maintainable**: Clear service boundaries and documentation
- **Observable**: Comprehensive monitoring and logging

The microservices architecture allows for independent scaling and development of features, while the AI/ML pipeline provides personalized experiences at scale.
