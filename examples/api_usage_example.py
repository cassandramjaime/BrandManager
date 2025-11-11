#!/usr/bin/env python
"""
Example usage of the Brand Manager API (for programmatic use)
"""
import os
from brand_manager.models import BrandIdentity, ContentRequest
from brand_manager.ai_manager import AIBrandManager


def main():
    """Example of using BrandManager programmatically"""
    
    # Note: Make sure to set OPENAI_API_KEY environment variable
    # or pass it directly to AIBrandManager(api_key="your-key")
    
    # Create a brand identity
    brand = BrandIdentity(
        name="EcoTech Solutions",
        tagline="Green Technology for a Better Tomorrow",
        description="A sustainable technology company focused on renewable energy solutions",
        values=["Sustainability", "Innovation", "Transparency"],
        target_audience="Environmentally conscious businesses and consumers",
        voice="Inspiring and educational",
        industry="Renewable Energy",
        unique_selling_points=[
            "100% carbon neutral operations",
            "Cutting-edge solar technology",
            "Community-driven approach"
        ]
    )
    
    print("=" * 60)
    print("Brand Manager API Example")
    print("=" * 60)
    print(f"\nBrand Name: {brand.name}")
    print(f"Tagline: {brand.tagline}")
    print(f"Values: {', '.join(brand.values)}")
    
    # Initialize the AI Brand Manager
    # This will raise an error if OPENAI_API_KEY is not set
    try:
        manager = AIBrandManager()
        manager.set_brand_identity(brand)
        
        print("\n" + "=" * 60)
        print("Example 1: Generate Taglines")
        print("=" * 60)
        print("\nGenerating tagline suggestions...")
        taglines = manager.generate_tagline(variations=3)
        for i, tagline in enumerate(taglines, 1):
            print(f"{i}. {tagline}")
        
        print("\n" + "=" * 60)
        print("Example 2: Generate Social Media Content")
        print("=" * 60)
        request = ContentRequest(
            content_type="social_post",
            topic="new solar panel product launch",
            platform="linkedin",
            length="medium"
        )
        print(f"\nGenerating LinkedIn post about: {request.topic}")
        content = manager.generate_content(request)
        print(f"\n{content}")
        
        print("\n" + "=" * 60)
        print("Example 3: Analyze Brand Message")
        print("=" * 60)
        message = "Join us in revolutionizing clean energy! Our innovative solar solutions are changing the game."
        print(f"\nAnalyzing message: '{message}'")
        analysis = manager.analyze_brand_message(message)
        print(f"\n{analysis['analysis']}")
        
        print("\n" + "=" * 60)
        print("Example 4: Get Strategy Advice")
        print("=" * 60)
        question = "How can we better engage with younger demographics on social media?"
        print(f"\nQuestion: {question}")
        advice = manager.get_brand_strategy_advice(question)
        print(f"\nAdvice:\n{advice}")
        
        print("\n" + "=" * 60)
        print("Example 5: Brainstorm Campaign Ideas")
        print("=" * 60)
        goal = "Launch awareness campaign for Earth Day"
        print(f"\nCampaign Goal: {goal}")
        ideas = manager.brainstorm_campaign_ideas(goal, num_ideas=3)
        for i, idea in enumerate(ideas, 1):
            print(f"\nIdea {i}:")
            print(idea)
        
        print("\n" + "=" * 60)
        print("Examples completed successfully!")
        print("=" * 60)
        
    except ValueError as e:
        print(f"\nError: {e}")
        print("\nPlease set your OPENAI_API_KEY environment variable:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        print("\nOr create a .env file with:")
        print("  OPENAI_API_KEY=your-api-key-here")


if __name__ == "__main__":
    main()
