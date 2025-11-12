#!/usr/bin/env python
"""
Example usage of the Topic Research API (for programmatic use)
"""
import json
from brand_manager.models import TopicResearchRequest
from brand_manager.ai_manager import AITopicResearcher


def main():
    """Example of using Topic Researcher programmatically"""
    
    # Note: Make sure to set OPENAI_API_KEY environment variable
    # or pass it directly to AITopicResearcher(api_key="your-key")
    
    print("=" * 70)
    print("AI Topic Researcher - API Examples")
    print("=" * 70)
    
    try:
        # Initialize the researcher
        researcher = AITopicResearcher()
        
        # Example 1: Basic topic research
        print("\n" + "=" * 70)
        print("Example 1: Basic Topic Research")
        print("=" * 70)
        
        request = TopicResearchRequest(
            topic="sustainable energy solutions",
            depth="standard"
        )
        
        print(f"\nResearching: {request.topic}")
        result = researcher.research_topic(request)
        
        print(f"\nSummary: {result.summary}")
        print(f"\nKey Points ({len(result.key_points)}):")
        for i, point in enumerate(result.key_points, 1):
            print(f"  {i}. {point}")
        
        # Example 2: Focused research
        print("\n" + "=" * 70)
        print("Example 2: Focused Research (Trends & Statistics)")
        print("=" * 70)
        
        request = TopicResearchRequest(
            topic="remote work trends 2024",
            depth="standard",
            focus_areas=["trends", "statistics"]
        )
        
        print(f"\nResearching: {request.topic}")
        print(f"Focus areas: {', '.join(request.focus_areas)}")
        result = researcher.research_topic(request)
        
        print(f"\nCurrent Trends ({len(result.trends)}):")
        for trend in result.trends:
            print(f"  • {trend}")
        
        print(f"\nStatistics ({len(result.statistics)}):")
        for stat in result.statistics:
            print(f"  • {stat}")
        
        # Example 3: Quick research
        print("\n" + "=" * 70)
        print("Example 3: Quick Research")
        print("=" * 70)
        
        request = TopicResearchRequest(
            topic="AI chatbots",
            depth="quick"
        )
        
        print(f"\nResearching (quick): {request.topic}")
        result = researcher.research_topic(request)
        
        print(f"\nSummary: {result.summary}")
        print(f"\nKey Points:")
        for point in result.key_points[:3]:  # Just first 3 for quick
            print(f"  • {point}")
        
        # Example 4: Deep research with content angles
        print("\n" + "=" * 70)
        print("Example 4: Deep Research for Content Creation")
        print("=" * 70)
        
        request = TopicResearchRequest(
            topic="mental health in the workplace",
            depth="deep",
            focus_areas=["audience_interests", "content_angles"]
        )
        
        print(f"\nResearching (deep): {request.topic}")
        result = researcher.research_topic(request)
        
        print(f"\nAudience Interests:")
        for interest in result.audience_interests:
            print(f"  • {interest}")
        
        print(f"\nContent Angles:")
        for angle in result.content_angles:
            print(f"  • {angle}")
        
        print(f"\nKeywords: {', '.join(result.keywords[:10])}")
        
        # Example 5: Saving results to JSON
        print("\n" + "=" * 70)
        print("Example 5: Saving Research Results")
        print("=" * 70)
        
        request = TopicResearchRequest(
            topic="blockchain in supply chain",
            depth="standard"
        )
        
        print(f"\nResearching: {request.topic}")
        result = researcher.research_topic(request)
        
        # Convert to dict and save
        result_dict = result.model_dump()
        
        output_file = "/tmp/research_results.json"
        with open(output_file, 'w') as f:
            json.dump(result_dict, f, indent=2)
        
        print(f"✓ Results saved to {output_file}")
        print(f"\nResult structure:")
        print(f"  - Summary: {len(result.summary)} characters")
        print(f"  - Key Points: {len(result.key_points)} items")
        print(f"  - Trends: {len(result.trends)} items")
        print(f"  - Statistics: {len(result.statistics)} items")
        print(f"  - Audience Interests: {len(result.audience_interests)} items")
        print(f"  - Content Angles: {len(result.content_angles)} items")
        print(f"  - Keywords: {len(result.keywords)} items")
        
        print("\n" + "=" * 70)
        print("Examples completed successfully!")
        print("=" * 70)
        
    except ValueError as e:
        print(f"\nError: {e}")
        print("\nPlease set your OPENAI_API_KEY environment variable:")
        print("  export OPENAI_API_KEY='your-api-key-here'")
        print("\nOr create a .env file with:")
        print("  OPENAI_API_KEY=your-api-key-here")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
