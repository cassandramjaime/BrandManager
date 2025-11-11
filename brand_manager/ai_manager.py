"""
AI Brand Manager - Core AI functionality using OpenAI
"""
import os
from typing import List, Optional, Dict, Any
from openai import OpenAI
from .models import BrandIdentity, ContentRequest


class AIBrandManager:
    """AI-powered brand manager using OpenAI for intelligent brand management"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the AI Brand Manager
        
        Args:
            api_key: OpenAI API key. If not provided, uses OPENAI_API_KEY env var
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.brand_identity: Optional[BrandIdentity] = None
    
    def set_brand_identity(self, brand_identity: BrandIdentity):
        """Set the brand identity for this manager"""
        self.brand_identity = brand_identity
    
    def _build_brand_context(self) -> str:
        """Build a context string from the brand identity"""
        if not self.brand_identity:
            return ""
        
        context_parts = [f"Brand Name: {self.brand_identity.name}"]
        
        if self.brand_identity.tagline:
            context_parts.append(f"Tagline: {self.brand_identity.tagline}")
        
        if self.brand_identity.description:
            context_parts.append(f"Description: {self.brand_identity.description}")
        
        if self.brand_identity.values:
            context_parts.append(f"Core Values: {', '.join(self.brand_identity.values)}")
        
        if self.brand_identity.target_audience:
            context_parts.append(f"Target Audience: {self.brand_identity.target_audience}")
        
        if self.brand_identity.voice:
            context_parts.append(f"Brand Voice: {self.brand_identity.voice}")
        
        if self.brand_identity.industry:
            context_parts.append(f"Industry: {self.brand_identity.industry}")
        
        if self.brand_identity.unique_selling_points:
            context_parts.append(f"Unique Selling Points: {', '.join(self.brand_identity.unique_selling_points)}")
        
        return "\n".join(context_parts)
    
    def generate_tagline(self, variations: int = 3) -> List[str]:
        """
        Generate tagline suggestions for the brand
        
        Args:
            variations: Number of tagline variations to generate
            
        Returns:
            List of tagline suggestions
        """
        if not self.brand_identity:
            raise ValueError("Brand identity must be set before generating content")
        
        context = self._build_brand_context()
        
        prompt = f"""Based on the following brand information, generate {variations} compelling, memorable taglines.
Each tagline should be concise (3-7 words), capture the brand essence, and resonate with the target audience.

{context}

Provide {variations} tagline options, one per line, without numbering or bullets."""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert brand strategist and copywriter specializing in creating memorable brand taglines."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=200
        )
        
        taglines = response.choices[0].message.content.strip().split('\n')
        return [t.strip() for t in taglines if t.strip()]
    
    def generate_content(self, request: ContentRequest) -> str:
        """
        Generate brand content based on the request
        
        Args:
            request: Content generation request
            
        Returns:
            Generated content string
        """
        if not self.brand_identity:
            raise ValueError("Brand identity must be set before generating content")
        
        context = self._build_brand_context()
        
        # Build content-specific prompt
        content_type_prompts = {
            "social_post": "a social media post",
            "blog_title": "a blog post title",
            "slogan": "a marketing slogan",
            "product_description": "a product description",
            "email_subject": "an email subject line",
            "ad_copy": "advertisement copy"
        }
        
        content_desc = content_type_prompts.get(request.content_type, request.content_type)
        
        prompt_parts = [
            f"Create {content_desc} for the following brand:",
            "",
            context,
            ""
        ]
        
        if request.topic:
            prompt_parts.append(f"Topic: {request.topic}")
        
        if request.platform:
            prompt_parts.append(f"Platform: {request.platform}")
        
        if request.length:
            length_guidance = {
                "short": "Keep it brief and punchy (1-2 sentences or under 100 characters).",
                "medium": "Make it engaging and informative (2-4 sentences or 100-200 characters).",
                "long": "Provide detailed and comprehensive content (multiple paragraphs if needed)."
            }
            prompt_parts.append(length_guidance.get(request.length, ""))
        
        tone = request.tone or self.brand_identity.voice
        if tone:
            prompt_parts.append(f"Tone: {tone}")
        
        prompt_parts.append("\nGenerate the content now:")
        
        prompt = "\n".join(prompt_parts)
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert content creator and brand strategist who creates compelling, on-brand content."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content.strip()
    
    def analyze_brand_message(self, message: str) -> Dict[str, Any]:
        """
        Analyze if a message aligns with the brand identity
        
        Args:
            message: The message to analyze
            
        Returns:
            Dictionary with analysis results
        """
        if not self.brand_identity:
            raise ValueError("Brand identity must be set before analyzing content")
        
        context = self._build_brand_context()
        
        prompt = f"""Analyze the following message for brand alignment with the brand described below.

Brand Information:
{context}

Message to Analyze:
"{message}"

Provide analysis in the following format:
1. Alignment Score (0-100): [score]
2. Tone Match: [Yes/No and explanation]
3. Value Alignment: [How well it reflects brand values]
4. Suggestions: [Any improvements to make it more on-brand]

Keep your response clear and structured."""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a brand consultant analyzing content for brand consistency and alignment."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=400
        )
        
        analysis_text = response.choices[0].message.content.strip()
        
        # Parse the response
        return {
            "analysis": analysis_text,
            "message": message
        }
    
    def get_brand_strategy_advice(self, question: str) -> str:
        """
        Get strategic advice for the brand
        
        Args:
            question: The strategic question or area of concern
            
        Returns:
            AI-generated strategic advice
        """
        if not self.brand_identity:
            raise ValueError("Brand identity must be set before getting advice")
        
        context = self._build_brand_context()
        
        prompt = f"""As a senior brand strategist, provide strategic advice for the following brand:

{context}

Question/Concern:
{question}

Provide actionable, specific advice that aligns with the brand's values and target audience."""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a senior brand strategist with expertise in brand development, positioning, and growth strategies."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=600
        )
        
        return response.choices[0].message.content.strip()
    
    def brainstorm_campaign_ideas(self, campaign_goal: str, num_ideas: int = 5) -> List[str]:
        """
        Brainstorm campaign ideas for the brand
        
        Args:
            campaign_goal: The goal or objective of the campaign
            num_ideas: Number of ideas to generate
            
        Returns:
            List of campaign ideas
        """
        if not self.brand_identity:
            raise ValueError("Brand identity must be set before brainstorming")
        
        context = self._build_brand_context()
        
        prompt = f"""Brainstorm {num_ideas} creative campaign ideas for the following brand:

{context}

Campaign Goal: {campaign_goal}

For each idea, provide:
- A catchy campaign name
- A brief description (2-3 sentences)
- Key channels/tactics

Format each idea clearly and separately."""
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a creative marketing strategist known for innovative campaign ideas."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=800
        )
        
        ideas_text = response.choices[0].message.content.strip()
        
        # Split into individual ideas (this is a simple split, could be improved)
        ideas = [idea.strip() for idea in ideas_text.split('\n\n') if idea.strip()]
        
        return ideas
