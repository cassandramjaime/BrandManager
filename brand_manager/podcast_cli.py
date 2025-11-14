"""
CLI for Podcast Guest Opportunity Finder
"""
import click
from datetime import datetime
from pathlib import Path
from colorama import Fore, Style

from .podcast_models import PodcastSearchRequest, ApplicationStatus
from .podcast_searcher import PodcastSearcher
from .podcast_database import PodcastDatabase
from .podcast_exporter import PodcastExporter


@click.group(name='podcast')
def podcast_cli():
    """Podcast Guest Opportunity Finder - Find and track podcast guest opportunities"""
    pass


@podcast_cli.command()
@click.option('--keywords', '-k', multiple=True, 
              help='Keywords to search for (can be used multiple times)')
@click.option('--min-audience', type=int, help='Minimum audience size')
@click.option('--min-score', type=float, default=0.0, help='Minimum relevance score (0-100)')
@click.option('--sources', '-s', multiple=True,
              type=click.Choice(['twitter', 'linkedin', 'podmatch', 'matchmaker', 'podcastguests']),
              help='Sources to search')
@click.option('--max-results', type=int, default=50, help='Maximum number of results')
@click.option('--save-to-db/--no-save-to-db', default=True, 
              help='Save results to database')
@click.option('--db-path', default='podcast_opportunities.db', 
              help='Path to SQLite database')
def search(keywords, min_audience, min_score, sources, max_results, save_to_db, db_path):
    """
    Search for podcast guest opportunities
    
    Example:
        podcast-finder search -k "product manager" -k "AI" --min-score 50
    """
    click.echo(f"\n{Fore.CYAN}Searching for podcast guest opportunities...{Style.RESET_ALL}\n")
    
    # Prepare search request
    search_keywords = list(keywords) if keywords else ["product manager", "AI", "machine learning"]
    search_sources = list(sources) if sources else ["twitter", "linkedin", "podmatch"]
    
    request = PodcastSearchRequest(
        keywords=search_keywords,
        min_audience_size=min_audience,
        min_relevance_score=min_score,
        sources=search_sources,
        max_results=max_results
    )
    
    click.echo(f"{Fore.YELLOW}Search Parameters:{Style.RESET_ALL}")
    click.echo(f"  Keywords: {', '.join(search_keywords)}")
    click.echo(f"  Sources: {', '.join(search_sources)}")
    if min_audience:
        click.echo(f"  Min Audience: {min_audience:,}")
    click.echo(f"  Min Score: {min_score}")
    click.echo()
    
    # Perform search
    searcher = PodcastSearcher()
    result = searcher.search(request)
    
    if not result.opportunities:
        click.echo(f"{Fore.RED}No opportunities found.{Style.RESET_ALL}")
        click.echo(f"{Fore.YELLOW}Note: This is a demo. Actual API integrations would return real results.{Style.RESET_ALL}")
        return
    
    # Display results
    click.echo(f"{Fore.GREEN}Found {result.total_found} opportunities!{Style.RESET_ALL}\n")
    
    for i, opp in enumerate(result.opportunities[:10], 1):  # Show top 10
        click.echo(f"{Fore.CYAN}{i}. {opp.podcast_name}{Style.RESET_ALL}")
        click.echo(f"   Score: {opp.total_score:.1f}/100 (Relevance: {opp.relevance_score:.1f}, Audience: {opp.audience_score:.1f})")
        if opp.host_name:
            click.echo(f"   Host: {opp.host_name}")
        if opp.audience_size:
            click.echo(f"   Audience: {opp.audience_size:,}")
        if opp.fit_reason:
            click.echo(f"   Fit: {opp.fit_reason}")
        click.echo()
    
    if result.total_found > 10:
        click.echo(f"{Fore.YELLOW}... and {result.total_found - 10} more opportunities{Style.RESET_ALL}\n")
    
    # Save to database if requested
    if save_to_db:
        db = PodcastDatabase(db_path)
        saved_count = 0
        for opp in result.opportunities:
            db.add_opportunity(opp)
            saved_count += 1
        click.echo(f"{Fore.GREEN}✓ Saved {saved_count} opportunities to database{Style.RESET_ALL}\n")


@podcast_cli.command()
@click.argument('podcast_name')
@click.option('--host', help='Host name')
@click.option('--contact', help='Contact email or social media')
@click.option('--description', help='Show description')
@click.option('--audience', type=int, help='Audience size')
@click.option('--link', help='Submission link')
@click.option('--source', default='manual', help='Source of this opportunity')
@click.option('--db-path', default='podcast_opportunities.db', help='Path to SQLite database')
def add(podcast_name, host, contact, description, audience, link, source, db_path):
    """
    Manually add a podcast opportunity
    
    Example:
        podcast-finder add "Product Thinking" --host "Melissa Perri" --audience 25000
    """
    searcher = PodcastSearcher()
    
    opportunity = searcher.add_manual_opportunity(
        podcast_name=podcast_name,
        host_name=host,
        host_contact=contact,
        show_description=description,
        audience_size=audience,
        submission_link=link,
        source=source
    )
    
    # Save to database
    db = PodcastDatabase(db_path)
    opp_id = db.add_opportunity(opportunity)
    
    click.echo(f"\n{Fore.GREEN}✓ Added opportunity: {podcast_name}{Style.RESET_ALL}")
    click.echo(f"  ID: {opp_id}")
    click.echo(f"  Total Score: {opportunity.total_score:.1f}/100")
    click.echo(f"  Relevance: {opportunity.relevance_score:.1f}/100")
    click.echo(f"  Fit Reason: {opportunity.fit_reason}\n")


@podcast_cli.command()
@click.option('--status', type=click.Choice(['not_applied', 'applied', 'responded', 'scheduled', 'completed', 'rejected']),
              help='Filter by application status')
@click.option('--min-score', type=float, default=0.0, help='Minimum total score')
@click.option('--limit', type=int, help='Limit number of results')
@click.option('--db-path', default='podcast_opportunities.db', help='Path to SQLite database')
def list(status, min_score, limit, db_path):
    """
    List podcast opportunities from database
    
    Example:
        podcast-finder list --status not_applied --min-score 60
    """
    db = PodcastDatabase(db_path)
    
    status_filter = ApplicationStatus(status) if status else None
    opportunities = db.get_all_opportunities(
        status=status_filter,
        min_score=min_score,
        limit=limit
    )
    
    if not opportunities:
        click.echo(f"{Fore.YELLOW}No opportunities found matching criteria.{Style.RESET_ALL}")
        return
    
    click.echo(f"\n{Fore.GREEN}Found {len(opportunities)} opportunities:{Style.RESET_ALL}\n")
    
    for opp in opportunities:
        click.echo(f"{Fore.CYAN}[{opp.id}] {opp.podcast_name}{Style.RESET_ALL}")
        click.echo(f"    Score: {opp.total_score:.1f}/100 | Status: {opp.application_status.value}")
        if opp.host_name:
            click.echo(f"    Host: {opp.host_name}")
        if opp.audience_size:
            click.echo(f"    Audience: {opp.audience_size:,}")
        if opp.submission_link:
            click.echo(f"    Apply: {opp.submission_link}")
        click.echo()


@podcast_cli.command()
@click.argument('opportunity_id', type=int)
@click.argument('status', type=click.Choice(['not_applied', 'applied', 'responded', 'scheduled', 'completed', 'rejected']))
@click.option('--notes', help='Additional notes')
@click.option('--db-path', default='podcast_opportunities.db', help='Path to SQLite database')
def update_status(opportunity_id, status, notes, db_path):
    """
    Update the status of a podcast opportunity
    
    Example:
        podcast-finder update-status 1 applied --notes "Sent pitch email"
    """
    db = PodcastDatabase(db_path)
    
    status_enum = ApplicationStatus(status)
    db.update_status(opportunity_id, status_enum, notes)
    
    click.echo(f"{Fore.GREEN}✓ Updated opportunity {opportunity_id} to status: {status}{Style.RESET_ALL}")
    if notes:
        click.echo(f"  Notes: {notes}")


@podcast_cli.command()
@click.option('--status', type=click.Choice(['not_applied', 'applied', 'responded', 'scheduled', 'completed', 'rejected']),
              help='Filter by application status')
@click.option('--min-score', type=float, default=0.0, help='Minimum total score')
@click.option('--format', type=click.Choice(['csv', 'markdown']), default='csv',
              help='Export format')
@click.option('--output', '-o', required=True, help='Output file path')
@click.option('--db-path', default='podcast_opportunities.db', help='Path to SQLite database')
def export(status, min_score, format, output, db_path):
    """
    Export opportunities to spreadsheet
    
    Example:
        podcast-finder export --format csv --output opportunities.csv
    """
    db = PodcastDatabase(db_path)
    
    status_filter = ApplicationStatus(status) if status else None
    opportunities = db.get_all_opportunities(
        status=status_filter,
        min_score=min_score
    )
    
    if not opportunities:
        click.echo(f"{Fore.YELLOW}No opportunities found to export.{Style.RESET_ALL}")
        return
    
    exporter = PodcastExporter()
    
    try:
        if format == 'csv':
            exporter.export_to_csv(opportunities, output)
        elif format == 'markdown':
            exporter.export_to_markdown(opportunities, output)
        
        click.echo(f"{Fore.GREEN}✓ Exported {len(opportunities)} opportunities to {output}{Style.RESET_ALL}")
    except Exception as e:
        click.echo(f"{Fore.RED}Error exporting: {e}{Style.RESET_ALL}")


@podcast_cli.command()
@click.option('--db-path', default='podcast_opportunities.db', help='Path to SQLite database')
def stats(db_path):
    """
    Show statistics about opportunities in database
    
    Example:
        podcast-finder stats
    """
    db = PodcastDatabase(db_path)
    statistics = db.get_statistics()
    
    click.echo(f"\n{Fore.CYAN}Podcast Opportunity Statistics{Style.RESET_ALL}\n")
    click.echo(f"Total Opportunities: {statistics['total']}")
    click.echo()
    
    if statistics['by_status']:
        click.echo(f"{Fore.YELLOW}By Status:{Style.RESET_ALL}")
        for status, count in statistics['by_status'].items():
            click.echo(f"  {status}: {count}")
        click.echo()
    
    click.echo(f"{Fore.YELLOW}Average Scores:{Style.RESET_ALL}")
    click.echo(f"  Total: {statistics['avg_total_score']:.1f}/100")
    click.echo(f"  Relevance: {statistics['avg_relevance_score']:.1f}/100")
    click.echo(f"  Audience: {statistics['avg_audience_score']:.1f}/100")
    click.echo()


def main():
    """Entry point for the podcast-finder CLI"""
    podcast_cli()


if __name__ == '__main__':
    main()
