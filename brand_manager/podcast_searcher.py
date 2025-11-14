"""
Podcast opportunity searcher
This module provides a framework for searching various sources for podcast guest opportunities.
Note: Actual API integrations require API keys and proper authentication.
"""
from typing import List, Optional
from datetime import datetime, timedelta
import re
from .podcast_models import PodcastOpportunity, PodcastSearchRequest, PodcastSearchResult
from .podcast_scorer import PodcastScorer


class PodcastSearcher:
    """Search for podcast guest opportunities across various sources"""
    
    def __init__(self):
        """Initialize the searcher"""
        self.scorer = PodcastScorer()
    
    def search(self, request: PodcastSearchRequest) -> PodcastSearchResult:
        """
        Search for podcast opportunities based on the request parameters
        
        Args:
            request: PodcastSearchRequest with search criteria
            
        Returns:
            PodcastSearchResult with found opportunities
        """
        opportunities = []
        sources_searched = []
        
        # Search each requested source
        if 'twitter' in request.sources:
            twitter_results = self._search_twitter(request)
            opportunities.extend(twitter_results)
            sources_searched.append('twitter')
        
        if 'linkedin' in request.sources:
            linkedin_results = self._search_linkedin(request)
            opportunities.extend(linkedin_results)
            sources_searched.append('linkedin')
        
        if 'podmatch' in request.sources:
            podmatch_results = self._search_podmatch(request)
            opportunities.extend(podmatch_results)
            sources_searched.append('podmatch')
        
        if 'matchmaker' in request.sources:
            matchmaker_results = self._search_matchmaker(request)
            opportunities.extend(matchmaker_results)
            sources_searched.append('matchmaker')
        
        if 'podcastguests' in request.sources:
            podcastguests_results = self._search_podcastguests(request)
            opportunities.extend(podcastguests_results)
            sources_searched.append('podcastguests')
        
        # Filter and score opportunities
        filtered_opportunities = self._filter_and_score(
            opportunities,
            request.min_audience_size,
            request.min_relevance_score
        )
        
        # Limit results
        if len(filtered_opportunities) > request.max_results:
            filtered_opportunities = filtered_opportunities[:request.max_results]
        
        return PodcastSearchResult(
            opportunities=filtered_opportunities,
            total_found=len(filtered_opportunities),
            search_date=datetime.now(),
            sources_searched=sources_searched
        )
    
    def _search_twitter(self, request: PodcastSearchRequest) -> List[PodcastOpportunity]:
        """
        Search Twitter/X for podcast guest opportunities
        
        Note: This is a placeholder. Real implementation would use Twitter API v2
        with search queries like:
        - "looking for podcast guests" + "product manager"
        - "seeking guests" + "AI"
        - "podcast interview" + "machine learning"
        """
        # Placeholder implementation
        # In a real implementation, you would:
        # 1. Use tweepy or Twitter API v2
        # 2. Search for tweets with keywords
        # 3. Extract podcast information from tweets
        # 4. Parse contact information and submission details
        
        opportunities = []
        
        # Example of what a real result might look like
        # This would come from actual Twitter API in production
        example_opportunity = PodcastOpportunity(
            podcast_name="Example Tech Podcast (Twitter)",
            host_name="Tech Host",
            host_contact="@techhost",
            show_description="Tech podcast looking for AI and PM experts",
            typical_guest_profile="Product managers and AI practitioners",
            audience_size=5000,
            source="twitter",
            source_url="https://twitter.com/example/status/123",
            submission_process="DM on Twitter or email"
        )
        
        # Don't add example data in production
        # opportunities.append(example_opportunity)
        
        return opportunities
    
    def _search_linkedin(self, request: PodcastSearchRequest) -> List[PodcastOpportunity]:
        """
        Search LinkedIn for podcast host posts seeking guests
        
        Note: This is a placeholder. Real implementation would use LinkedIn API
        """
        opportunities = []
        
        # Placeholder for LinkedIn API integration
        # In production, you would:
        # 1. Use LinkedIn API
        # 2. Search for posts from podcast hosts
        # 3. Look for keywords: "looking for guests", "podcast interview"
        # 4. Extract contact and show information
        
        return opportunities
    
    def _search_podmatch(self, request: PodcastSearchRequest) -> List[PodcastOpportunity]:
        """
        Search PodMatch platform for opportunities
        
        Note: This is a placeholder. Real implementation would use PodMatch API/scraping
        """
        opportunities = []
        
        # Placeholder for PodMatch integration
        # In production, you would:
        # 1. Use PodMatch API if available
        # 2. Or scrape PodMatch website (with permission)
        # 3. Filter for AI/PM related podcasts
        # 4. Extract show details and host information
        
        return opportunities
    
    def _search_matchmaker(self, request: PodcastSearchRequest) -> List[PodcastOpportunity]:
        """
        Search MatchMaker.fm for opportunities
        
        Note: This is a placeholder. Real implementation would integrate with MatchMaker.fm
        """
        opportunities = []
        
        # Placeholder for MatchMaker.fm integration
        
        return opportunities
    
    def _search_podcastguests(self, request: PodcastSearchRequest) -> List[PodcastOpportunity]:
        """
        Search PodcastGuests.com for opportunities
        
        Note: This is a placeholder. Real implementation would integrate with PodcastGuests
        """
        opportunities = []
        
        # Placeholder for PodcastGuests.com integration
        
        return opportunities
    
    def _filter_and_score(
        self,
        opportunities: List[PodcastOpportunity],
        min_audience_size: Optional[int],
        min_relevance_score: float
    ) -> List[PodcastOpportunity]:
        """Filter and score opportunities based on criteria"""
        scored_opportunities = []
        
        for opp in opportunities:
            # Calculate scores
            relevance_score = self.scorer.calculate_relevance_score(
                opp.podcast_name,
                opp.show_description,
                opp.typical_guest_profile
            )
            
            audience_score = self.scorer.calculate_audience_score(opp.audience_size)
            
            engagement_score = self.scorer.calculate_engagement_score(
                has_submission_form=bool(opp.submission_link),
                has_contact=bool(opp.host_contact),
                has_description=bool(opp.show_description),
                source_credibility=opp.source or "unknown"
            )
            
            total_score = self.scorer.calculate_total_score(
                relevance_score,
                audience_score,
                engagement_score
            )
            
            # Generate fit reason
            fit_reason = self.scorer.generate_fit_reason(
                opp.podcast_name,
                relevance_score,
                audience_score,
                opp.show_description
            )
            
            # Update opportunity with scores
            opp.relevance_score = relevance_score
            opp.audience_score = audience_score
            opp.engagement_score = engagement_score
            opp.total_score = total_score
            opp.fit_reason = fit_reason
            
            # Apply filters
            if min_audience_size and opp.audience_size:
                if opp.audience_size < min_audience_size:
                    continue
            
            if relevance_score < min_relevance_score:
                continue
            
            scored_opportunities.append(opp)
        
        # Sort by total score (highest first)
        scored_opportunities.sort(key=lambda x: x.total_score, reverse=True)
        
        return scored_opportunities
    
    def add_manual_opportunity(
        self,
        podcast_name: str,
        host_name: Optional[str] = None,
        host_contact: Optional[str] = None,
        show_description: Optional[str] = None,
        typical_guest_profile: Optional[str] = None,
        audience_size: Optional[int] = None,
        submission_link: Optional[str] = None,
        submission_process: Optional[str] = None,
        source: str = "manual",
        source_url: Optional[str] = None
    ) -> PodcastOpportunity:
        """
        Manually add a podcast opportunity
        Useful for adding opportunities found outside automated searches
        """
        opportunity = PodcastOpportunity(
            podcast_name=podcast_name,
            host_name=host_name,
            host_contact=host_contact,
            show_description=show_description,
            typical_guest_profile=typical_guest_profile,
            audience_size=audience_size,
            submission_link=submission_link,
            submission_process=submission_process,
            source=source,
            source_url=source_url
        )
        
        # Calculate scores
        relevance_score = self.scorer.calculate_relevance_score(
            podcast_name,
            show_description,
            typical_guest_profile
        )
        
        audience_score = self.scorer.calculate_audience_score(audience_size)
        
        engagement_score = self.scorer.calculate_engagement_score(
            has_submission_form=bool(submission_link),
            has_contact=bool(host_contact),
            has_description=bool(show_description),
            source_credibility=source
        )
        
        total_score = self.scorer.calculate_total_score(
            relevance_score,
            audience_score,
            engagement_score
        )
        
        fit_reason = self.scorer.generate_fit_reason(
            podcast_name,
            relevance_score,
            audience_score,
            show_description
        )
        
        opportunity.relevance_score = relevance_score
        opportunity.audience_score = audience_score
        opportunity.engagement_score = engagement_score
        opportunity.total_score = total_score
        opportunity.fit_reason = fit_reason
        
        return opportunity
