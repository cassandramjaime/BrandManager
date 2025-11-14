#!/usr/bin/env python
"""
Example usage of the Journalist Opportunity Finder (for programmatic use)
"""
import os
from datetime import datetime, timedelta
from brand_manager.journalist_models import (
    UserProfile,
    JournalistOpportunity,
    OpportunitySource,
    PublicationTier,
    Urgency,
    OpportunityFilter
)
from brand_manager.opportunity_finder import OpportunityFinder
from brand_manager.opportunity_database import OpportunityDatabase


def main():
    """Example of using Journalist Finder programmatically"""
    
    print("=" * 70)
    print("Journalist Opportunity Finder - API Examples")
    print("=" * 70)
    
    # Note: Make sure to set OPENAI_API_KEY environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("\nError: OPENAI_API_KEY environment variable not set")
        print("Please set it before running this example:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        return
    
    try:
        # Initialize the finder with a temporary database for demo
        db_path = "/tmp/journalist_finder_demo.db"
        finder = OpportunityFinder(db_path=db_path)
        
        # Example 1: Set up user profile
        print("\n" + "=" * 70)
        print("Example 1: Setting Up User Profile")
        print("=" * 70)
        
        profile = UserProfile(
            name="Jane Smith",
            title="AI Product Manager",
            expertise_areas=["artificial intelligence", "product management", "machine learning", "AI ethics"],
            experience_years=8,
            company="TechCorp",
            bio="AI Product Manager with 8 years of experience building ML-powered products. Led multiple AI product launches and grew user base by 200%.",
            achievements=[
                "Led AI product launch that achieved 1M users in 6 months",
                "Grew user engagement by 200% through ML-powered recommendations",
                "Published articles on AI ethics and responsible AI development"
            ],
            contact_info={
                "email": "jane.smith@example.com",
                "linkedin": "linkedin.com/in/janesmith",
                "twitter": "@janesmith"
            }
        )
        
        finder.db.save_user_profile(profile)
        print(f"\n✓ Profile created for {profile.name}")
        print(f"  Title: {profile.title}")
        print(f"  Experience: {profile.experience_years} years")
        print(f"  Expertise: {', '.join(profile.expertise_areas)}")
        
        # Example 2: Add opportunities manually
        print("\n" + "=" * 70)
        print("Example 2: Adding Opportunities Manually")
        print("=" * 70)
        
        # Create sample opportunities
        opp1 = JournalistOpportunity(
            publication_name="TechCrunch",
            journalist_name="Sarah Johnson",
            topic="AI in Product Management - Future Trends",
            deadline=datetime.now() + timedelta(days=3),
            requirements="Looking for AI PM experts to discuss how AI is transforming product management practices",
            contact_method="sarah.johnson@techcrunch.com",
            tier=PublicationTier.TIER_2,
            urgency=Urgency.MEDIUM,
            source=OpportunitySource.TWITTER,
            relevance_score=92.0,
            keywords=["AI", "product management", "machine learning", "automation"]
        )
        
        opp2 = JournalistOpportunity(
            publication_name="Forbes",
            journalist_name="Michael Chen",
            topic="Ethical AI Development in Tech Companies",
            deadline=datetime.now() + timedelta(days=1),
            requirements="Seeking experts on AI ethics and responsible AI development for feature article",
            contact_method="m.chen@forbes.com",
            tier=PublicationTier.TIER_1,
            urgency=Urgency.HIGH,
            source=OpportunitySource.LINKEDIN,
            relevance_score=95.0,
            keywords=["AI ethics", "responsible AI", "AI governance", "tech leadership"]
        )
        
        opp1_id = finder.db.add_opportunity(opp1)
        opp2_id = finder.db.add_opportunity(opp2)
        
        print(f"\n✓ Added 2 opportunities")
        print(f"  1. {opp1.publication_name} - Score: {opp1.relevance_score}")
        print(f"  2. {opp2.publication_name} - Score: {opp2.relevance_score}")
        
        # Example 3: Parse opportunity from text
        print("\n" + "=" * 70)
        print("Example 3: Parsing Opportunity from Text (AI-Powered)")
        print("=" * 70)
        
        opportunity_text = """
        VentureBeat is looking for AI product management experts to contribute to our 
        upcoming feature on "The Future of Product Management in the AI Era". 
        We're particularly interested in practitioners who have led AI product teams 
        and can discuss practical challenges and solutions.
        
        Deadline: November 25, 2024
        Contact: editors@venturebeat.com
        """
        
        print("\nParsing opportunity text...")
        opp3_id = finder.add_opportunity_from_text(
            opportunity_text,
            OpportunitySource.OTHER,
            profile
        )
        
        if opp3_id:
            opp3 = finder.db.get_opportunity(opp3_id)
            print(f"\n✓ Successfully parsed opportunity")
            print(f"  Publication: {opp3.publication_name}")
            print(f"  Topic: {opp3.topic}")
            print(f"  Tier: {opp3.tier.value}")
            print(f"  Relevance Score: {opp3.relevance_score:.1f}")
        
        # Example 4: Filter and list opportunities
        print("\n" + "=" * 70)
        print("Example 4: Filtering Opportunities")
        print("=" * 70)
        
        # High priority opportunities
        high_priority_filter = OpportunityFilter(
            min_relevance_score=90.0,
            tiers=[PublicationTier.TIER_1, PublicationTier.TIER_2],
            only_not_pitched=True
        )
        
        high_priority = finder.db.list_opportunities(high_priority_filter)
        
        print(f"\nHigh Priority Opportunities (Score ≥90, Tier 1-2):")
        for opp in high_priority:
            print(f"  • {opp.publication_name} ({opp.tier.value}) - Score: {opp.relevance_score:.0f}")
            print(f"    Topic: {opp.topic[:60]}...")
            if opp.deadline:
                print(f"    Deadline: {opp.deadline.strftime('%Y-%m-%d')}")
        
        # Example 5: Generate personalized pitch
        print("\n" + "=" * 70)
        print("Example 5: Generating Personalized Pitch")
        print("=" * 70)
        
        # Get the Forbes opportunity (highest priority)
        forbes_opp = finder.db.get_opportunity(opp2_id)
        
        print(f"\nGenerating pitch for: {forbes_opp.publication_name}")
        print(f"Topic: {forbes_opp.topic}")
        print("\nGenerating personalized pitch using AI...")
        
        pitch = finder.generate_pitch(forbes_opp, profile)
        
        print(f"\n{'-' * 70}")
        print(f"Subject: {pitch.subject_line}")
        print(f"{'-' * 70}")
        print(f"\n{pitch.full_pitch}")
        print(f"\n{'-' * 70}")
        
        # Example 6: Track pitch activity
        print("\n" + "=" * 70)
        print("Example 6: Tracking Pitch Activity")
        print("=" * 70)
        
        # Mark Forbes opportunity as pitched
        finder.db.mark_pitch_sent(opp2_id, pitch.full_pitch)
        print(f"\n✓ Marked Forbes opportunity as pitched")
        
        # Simulate receiving a response
        finder.db.mark_response_received(opp2_id, "Positive response - scheduled interview")
        print(f"✓ Marked response received for Forbes opportunity")
        
        # Example 7: View statistics
        print("\n" + "=" * 70)
        print("Example 7: Viewing Statistics")
        print("=" * 70)
        
        stats = finder.db.get_statistics()
        
        print(f"\nActivity Statistics:")
        print(f"  Total Opportunities: {stats['total_opportunities']}")
        print(f"  Pitches Sent: {stats['pitches_sent']}")
        print(f"  Responses Received: {stats['responses_received']}")
        print(f"  Response Rate: {stats['response_rate']:.1f}%")
        
        if stats.get('by_tier'):
            print(f"\n  By Tier:")
            for tier, count in stats['by_tier'].items():
                print(f"    {tier}: {count}")
        
        # Example 8: Generate daily digest
        print("\n" + "=" * 70)
        print("Example 8: Generating Daily Digest")
        print("=" * 70)
        
        digest = finder.generate_daily_digest()
        
        print(f"\nDaily Digest for {digest.date.strftime('%Y-%m-%d')}:")
        print(f"Total Opportunities Found (last 24h): {digest.total_opportunities}")
        
        print(f"\n🔥 High Priority ({len(digest.high_priority)}):")
        for opp in digest.high_priority[:3]:
            print(f"  • {opp.publication_name} - {opp.topic[:50]}...")
            print(f"    Score: {opp.relevance_score:.0f} | Urgency: {opp.urgency.value}")
        
        print(f"\n⚡ Medium Priority ({len(digest.medium_priority)}):")
        for opp in digest.medium_priority[:3]:
            print(f"  • {opp.publication_name} - {opp.topic[:50]}...")
        
        # Cleanup
        print("\n" + "=" * 70)
        print("Examples completed successfully!")
        print("=" * 70)
        print(f"\nNote: Demo database created at {db_path}")
        print("You can delete it or use it for testing.")
        
    except ValueError as e:
        print(f"\nError: {e}")
        print("\nPlease set your OPENAI_API_KEY environment variable:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
