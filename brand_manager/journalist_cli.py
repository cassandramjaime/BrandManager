"""
Command-line interface for Journalist Opportunity Finder
"""
import json
import click
from datetime import datetime
from dotenv import load_dotenv
from colorama import init, Fore, Style
from tabulate import tabulate

from .journalist_models import (
    UserProfile,
    OpportunitySource,
    OpportunityFilter,
    PublicationTier,
    Urgency
)
from .opportunity_finder import OpportunityFinder
from .opportunity_database import OpportunityDatabase

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Load environment variables
load_dotenv()


@click.group()
@click.version_option(version="0.1.0")
def journalist_cli():
    """Journalist Opportunity Finder - Find journalists seeking AI PM contributors"""
    pass


@journalist_cli.command('setup-profile')
@click.option('--name', prompt='Your name', help='Your full name')
@click.option('--title', prompt='Your professional title', help='e.g., "AI Product Manager"')
@click.option('--experience', prompt='Years of experience', type=int, help='Years of professional experience')
@click.option('--company', prompt='Current company (optional)', default='', help='Your current company')
@click.option('--expertise', prompt='Expertise areas (comma-separated)', help='e.g., "AI, product management, machine learning"')
@click.option('--bio', prompt='Professional bio (brief)', help='1-2 sentence professional bio')
def setup_profile(name, title, experience, company, expertise, bio):
    """Set up your professional profile for pitch personalization
    
    Example:
        journalist-finder setup-profile
    """
    try:
        db = OpportunityDatabase()
        
        expertise_list = [e.strip() for e in expertise.split(',')]
        
        profile = UserProfile(
            name=name,
            title=title,
            expertise_areas=expertise_list,
            experience_years=experience,
            company=company if company else None,
            bio=bio,
            achievements=[],
            contact_info={}
        )
        
        db.save_user_profile(profile)
        
        click.echo(f"\n{Fore.GREEN}✓ Profile saved successfully!{Style.RESET_ALL}")
        click.echo(f"\n{Fore.CYAN}Your Profile:{Style.RESET_ALL}")
        click.echo(f"Name: {name}")
        click.echo(f"Title: {title}")
        click.echo(f"Experience: {experience} years")
        if company:
            click.echo(f"Company: {company}")
        click.echo(f"Expertise: {', '.join(expertise_list)}")
        click.echo(f"Bio: {bio}")
        
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return 1


@journalist_cli.command('add-opportunity')
@click.option('--text', prompt='Opportunity text', help='Paste the opportunity text')
@click.option('--source', type=click.Choice(['haro', 'twitter', 'medium', 'substack', 'linkedin', 'terkel', 'qwoted', 'featured', 'sourcebottle', 'other']),
              prompt='Source platform', help='Platform where you found it')
def add_opportunity(text, source):
    """Add a journalist opportunity from text
    
    Example:
        journalist-finder add-opportunity --source twitter --text "..."
    """
    try:
        finder = OpportunityFinder()
        
        click.echo(f"\n{Fore.CYAN}Processing opportunity...{Style.RESET_ALL}")
        
        source_enum = OpportunitySource(source)
        opportunity_id = finder.add_opportunity_from_text(text, source_enum)
        
        if opportunity_id:
            opportunity = finder.db.get_opportunity(opportunity_id)
            click.echo(f"\n{Fore.GREEN}✓ Opportunity added successfully!{Style.RESET_ALL}")
            click.echo(f"\n{Fore.YELLOW}Opportunity Details:{Style.RESET_ALL}")
            click.echo(f"ID: {opportunity.id}")
            click.echo(f"Publication: {opportunity.publication_name}")
            if opportunity.journalist_name:
                click.echo(f"Journalist: {opportunity.journalist_name}")
            click.echo(f"Topic: {opportunity.topic}")
            click.echo(f"Tier: {opportunity.tier.value}")
            click.echo(f"Urgency: {opportunity.urgency.value}")
            click.echo(f"Relevance Score: {opportunity.relevance_score:.1f}/100")
            if opportunity.deadline:
                click.echo(f"Deadline: {opportunity.deadline.strftime('%Y-%m-%d %H:%M')}")
            click.echo(f"\nContact: {opportunity.contact_method}")
        else:
            click.echo(f"{Fore.RED}Failed to parse opportunity{Style.RESET_ALL}")
            return 1
        
    except ValueError as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        click.echo(f"{Fore.YELLOW}Make sure you have set OPENAI_API_KEY in your .env file{Style.RESET_ALL}")
        return 1
    except Exception as e:
        click.echo(f"{Fore.RED}Unexpected error: {e}{Style.RESET_ALL}")
        return 1


@journalist_cli.command('list')
@click.option('--min-score', type=float, default=0.0, help='Minimum relevance score')
@click.option('--tier', type=click.Choice(['tier_1', 'tier_2', 'tier_3']), multiple=True, help='Filter by publication tier')
@click.option('--urgency', type=click.Choice(['high', 'medium', 'low']), multiple=True, help='Filter by urgency')
@click.option('--not-pitched', is_flag=True, help='Show only opportunities not yet pitched')
@click.option('--limit', type=int, default=20, help='Maximum number to display')
def list_opportunities(min_score, tier, urgency, not_pitched, limit):
    """List journalist opportunities
    
    Example:
        journalist-finder list --min-score 70 --tier tier_1 --tier tier_2 --not-pitched
    """
    try:
        db = OpportunityDatabase()
        
        # Build filter
        filter_params = OpportunityFilter(
            min_relevance_score=min_score,
            tiers=[PublicationTier(t) for t in tier] if tier else [],
            urgency_levels=[Urgency(u) for u in urgency] if urgency else [],
            only_not_pitched=not_pitched
        )
        
        opportunities = db.list_opportunities(filter_params)
        
        if not opportunities:
            click.echo(f"\n{Fore.YELLOW}No opportunities found matching your criteria{Style.RESET_ALL}")
            return
        
        # Display as table
        click.echo(f"\n{Fore.GREEN}Found {len(opportunities)} opportunities{Style.RESET_ALL}\n")
        
        table_data = []
        for i, opp in enumerate(opportunities[:limit], 1):
            deadline_str = opp.deadline.strftime('%m/%d') if opp.deadline else 'N/A'
            pitched = '✓' if opp.pitch_sent else ''
            
            table_data.append([
                i,
                opp.id[:15] + '...' if len(opp.id) > 15 else opp.id,
                opp.publication_name[:25],
                opp.topic[:40] + '...' if len(opp.topic) > 40 else opp.topic,
                f"{opp.relevance_score:.0f}",
                opp.tier.value,
                opp.urgency.value,
                deadline_str,
                pitched
            ])
        
        headers = ['#', 'ID', 'Publication', 'Topic', 'Score', 'Tier', 'Urgency', 'Deadline', 'Pitched']
        click.echo(tabulate(table_data, headers=headers, tablefmt='simple'))
        
        if len(opportunities) > limit:
            click.echo(f"\n{Fore.CYAN}Showing {limit} of {len(opportunities)} opportunities. Use --limit to see more.{Style.RESET_ALL}")
        
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return 1


@journalist_cli.command('show')
@click.argument('opportunity_id')
def show_opportunity(opportunity_id):
    """Show detailed information about an opportunity
    
    Example:
        journalist-finder show TechCrunch_20251114120000
    """
    try:
        db = OpportunityDatabase()
        opportunity = db.get_opportunity(opportunity_id)
        
        if not opportunity:
            click.echo(f"{Fore.RED}Opportunity not found: {opportunity_id}{Style.RESET_ALL}")
            return 1
        
        click.echo(f"\n{Fore.GREEN}{'=' * 70}")
        click.echo(f"OPPORTUNITY DETAILS")
        click.echo(f"{'=' * 70}{Style.RESET_ALL}\n")
        
        click.echo(f"{Fore.YELLOW}Publication:{Style.RESET_ALL} {opportunity.publication_name}")
        if opportunity.journalist_name:
            click.echo(f"{Fore.YELLOW}Journalist:{Style.RESET_ALL} {opportunity.journalist_name}")
        click.echo(f"{Fore.YELLOW}Topic:{Style.RESET_ALL} {opportunity.topic}")
        
        click.echo(f"\n{Fore.YELLOW}Classification:{Style.RESET_ALL}")
        click.echo(f"  Tier: {opportunity.tier.value}")
        click.echo(f"  Urgency: {opportunity.urgency.value}")
        click.echo(f"  Source: {opportunity.source.value}")
        click.echo(f"  Relevance Score: {opportunity.relevance_score:.1f}/100")
        
        click.echo(f"\n{Fore.YELLOW}Requirements:{Style.RESET_ALL}")
        click.echo(f"  {opportunity.requirements}")
        
        click.echo(f"\n{Fore.YELLOW}Contact:{Style.RESET_ALL}")
        click.echo(f"  {opportunity.contact_method}")
        
        if opportunity.deadline:
            click.echo(f"\n{Fore.YELLOW}Deadline:{Style.RESET_ALL} {opportunity.deadline.strftime('%Y-%m-%d %H:%M')}")
        
        if opportunity.keywords:
            click.echo(f"\n{Fore.YELLOW}Keywords:{Style.RESET_ALL} {', '.join(opportunity.keywords)}")
        
        click.echo(f"\n{Fore.YELLOW}Tracking:{Style.RESET_ALL}")
        click.echo(f"  Found: {opportunity.found_at.strftime('%Y-%m-%d %H:%M')}")
        click.echo(f"  Pitched: {'Yes' if opportunity.pitch_sent else 'No'}")
        if opportunity.pitch_sent_at:
            click.echo(f"  Pitched At: {opportunity.pitch_sent_at.strftime('%Y-%m-%d %H:%M')}")
        click.echo(f"  Response: {'Yes' if opportunity.response_received else 'No'}")
        if opportunity.response_received_at:
            click.echo(f"  Response At: {opportunity.response_received_at.strftime('%Y-%m-%d %H:%M')}")
        
        if opportunity.notes:
            click.echo(f"\n{Fore.YELLOW}Notes:{Style.RESET_ALL}")
            click.echo(f"  {opportunity.notes}")
        
        click.echo()
        
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return 1


@journalist_cli.command('generate-pitch')
@click.argument('opportunity_id')
@click.option('--save', is_flag=True, help='Save pitch to file')
@click.option('--output', '-o', type=click.Path(), help='Output file path')
def generate_pitch(opportunity_id, save, output):
    """Generate a personalized pitch for an opportunity
    
    Example:
        journalist-finder generate-pitch TechCrunch_20251114120000 --save
    """
    try:
        finder = OpportunityFinder()
        opportunity = finder.db.get_opportunity(opportunity_id)
        
        if not opportunity:
            click.echo(f"{Fore.RED}Opportunity not found: {opportunity_id}{Style.RESET_ALL}")
            return 1
        
        click.echo(f"\n{Fore.CYAN}Generating personalized pitch...{Style.RESET_ALL}")
        
        pitch = finder.generate_pitch(opportunity)
        
        click.echo(f"\n{Fore.GREEN}{'=' * 70}")
        click.echo(f"GENERATED PITCH")
        click.echo(f"{'=' * 70}{Style.RESET_ALL}\n")
        
        click.echo(f"{Fore.YELLOW}Subject:{Style.RESET_ALL} {pitch.subject_line}\n")
        click.echo(pitch.full_pitch)
        click.echo()
        
        if save or output:
            filename = output or f"pitch_{opportunity_id}.txt"
            with open(filename, 'w') as f:
                f.write(f"Subject: {pitch.subject_line}\n\n")
                f.write(pitch.full_pitch)
            click.echo(f"{Fore.GREEN}✓ Pitch saved to {filename}{Style.RESET_ALL}\n")
        
    except ValueError as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        if "profile" in str(e).lower():
            click.echo(f"{Fore.YELLOW}Run 'journalist-finder setup-profile' first to set up your profile{Style.RESET_ALL}")
        return 1
    except Exception as e:
        click.echo(f"{Fore.RED}Unexpected error: {e}{Style.RESET_ALL}")
        return 1


@journalist_cli.command('mark-pitched')
@click.argument('opportunity_id')
@click.option('--pitch-text', prompt='Pitch text (brief summary)', help='Summary of what you sent')
def mark_pitched(opportunity_id, pitch_text):
    """Mark an opportunity as pitched
    
    Example:
        journalist-finder mark-pitched TechCrunch_20251114120000
    """
    try:
        db = OpportunityDatabase()
        opportunity = db.get_opportunity(opportunity_id)
        
        if not opportunity:
            click.echo(f"{Fore.RED}Opportunity not found: {opportunity_id}{Style.RESET_ALL}")
            return 1
        
        db.mark_pitch_sent(opportunity_id, pitch_text)
        
        click.echo(f"\n{Fore.GREEN}✓ Marked as pitched!{Style.RESET_ALL}")
        click.echo(f"Opportunity: {opportunity.publication_name} - {opportunity.topic}")
        
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return 1


@journalist_cli.command('mark-response')
@click.argument('opportunity_id')
@click.option('--response-text', prompt='Response summary (optional)', default='', help='Summary of response received')
def mark_response(opportunity_id, response_text):
    """Mark that a response was received
    
    Example:
        journalist-finder mark-response TechCrunch_20251114120000
    """
    try:
        db = OpportunityDatabase()
        opportunity = db.get_opportunity(opportunity_id)
        
        if not opportunity:
            click.echo(f"{Fore.RED}Opportunity not found: {opportunity_id}{Style.RESET_ALL}")
            return 1
        
        db.mark_response_received(opportunity_id, response_text)
        
        click.echo(f"\n{Fore.GREEN}✓ Marked as responded!{Style.RESET_ALL}")
        click.echo(f"Opportunity: {opportunity.publication_name} - {opportunity.topic}")
        
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return 1


@journalist_cli.command('daily-digest')
@click.option('--min-score', type=float, default=50.0, help='Minimum relevance score to include')
def daily_digest(min_score):
    """Generate daily digest of opportunities
    
    Example:
        journalist-finder daily-digest --min-score 70
    """
    try:
        finder = OpportunityFinder()
        digest = finder.generate_daily_digest()
        
        click.echo(f"\n{Fore.GREEN}{'=' * 70}")
        click.echo(f"DAILY DIGEST - {digest.date.strftime('%Y-%m-%d')}")
        click.echo(f"{'=' * 70}{Style.RESET_ALL}\n")
        
        click.echo(f"{Fore.CYAN}Total Opportunities Found (last 24h):{Style.RESET_ALL} {digest.total_opportunities}\n")
        
        # High Priority
        high_filtered = [o for o in digest.high_priority if o.relevance_score >= min_score]
        if high_filtered:
            click.echo(f"{Fore.RED}🔥 HIGH PRIORITY ({len(high_filtered)}):{Style.RESET_ALL}")
            for opp in high_filtered[:5]:
                click.echo(f"  • {opp.publication_name} ({opp.tier.value}) - {opp.topic[:50]}")
                click.echo(f"    Score: {opp.relevance_score:.0f} | Urgency: {opp.urgency.value} | ID: {opp.id}")
            click.echo()
        
        # Medium Priority
        medium_filtered = [o for o in digest.medium_priority if o.relevance_score >= min_score]
        if medium_filtered:
            click.echo(f"{Fore.YELLOW}⚡ MEDIUM PRIORITY ({len(medium_filtered)}):{Style.RESET_ALL}")
            for opp in medium_filtered[:5]:
                click.echo(f"  • {opp.publication_name} ({opp.tier.value}) - {opp.topic[:50]}")
                click.echo(f"    Score: {opp.relevance_score:.0f} | ID: {opp.id}")
            click.echo()
        
        # Low Priority
        low_filtered = [o for o in digest.low_priority if o.relevance_score >= min_score]
        if low_filtered:
            click.echo(f"{Fore.CYAN}💡 LOW PRIORITY ({len(low_filtered)}):{Style.RESET_ALL}")
            for opp in low_filtered[:3]:
                click.echo(f"  • {opp.publication_name} - {opp.topic[:50]}")
            click.echo()
        
        if not high_filtered and not medium_filtered and not low_filtered:
            click.echo(f"{Fore.YELLOW}No opportunities found in the last 24 hours with score >= {min_score}{Style.RESET_ALL}\n")
        
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return 1


@journalist_cli.command('stats')
def show_stats():
    """Show statistics about opportunities
    
    Example:
        journalist-finder stats
    """
    try:
        db = OpportunityDatabase()
        stats = db.get_statistics()
        
        click.echo(f"\n{Fore.GREEN}{'=' * 70}")
        click.echo(f"OPPORTUNITY STATISTICS")
        click.echo(f"{'=' * 70}{Style.RESET_ALL}\n")
        
        click.echo(f"{Fore.CYAN}Overview:{Style.RESET_ALL}")
        click.echo(f"  Total Opportunities: {stats['total_opportunities']}")
        click.echo(f"  Pitches Sent: {stats['pitches_sent']}")
        click.echo(f"  Responses Received: {stats['responses_received']}")
        click.echo(f"  Response Rate: {stats['response_rate']:.1f}%")
        
        if stats.get('by_tier'):
            click.echo(f"\n{Fore.CYAN}By Tier:{Style.RESET_ALL}")
            for tier, count in stats['by_tier'].items():
                click.echo(f"  {tier}: {count}")
        
        if stats.get('by_urgency'):
            click.echo(f"\n{Fore.CYAN}By Urgency:{Style.RESET_ALL}")
            for urgency, count in stats['by_urgency'].items():
                click.echo(f"  {urgency}: {count}")
        
        click.echo()
        
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return 1


def main():
    """Entry point for the journalist finder CLI"""
    journalist_cli()


if __name__ == '__main__':
    main()
