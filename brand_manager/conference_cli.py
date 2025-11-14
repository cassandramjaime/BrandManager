"""
CLI interface for conference tracking
"""
import click
import json
from datetime import datetime, timedelta
from pathlib import Path
from colorama import init, Fore, Style

from .conference_models import ConferenceSearchFilters, LocationType, TopicFocus
from .conference_db import ConferenceDatabase
from .conference_scrapers import ConferenceAggregator
from .conference_scorer import ConferenceScorer
from .conference_exporter import ConferenceExporter
from .conference_scheduler import ConferenceScheduler

# Initialize colorama
init(autoreset=True)


@click.group()
def conference_cli():
    """Conference tracking and research tool for product managers"""
    pass


@conference_cli.command('update')
@click.option('--db', default='conferences.db', help='Database file path')
def update_conferences(db):
    """Scrape and update conference database from all sources"""
    click.echo(f"\n{Fore.CYAN}Updating conference database...{Style.RESET_ALL}")
    
    try:
        # Aggregate conferences from all sources
        aggregator = ConferenceAggregator()
        click.echo(f"{Fore.YELLOW}Scraping conferences from sources...{Style.RESET_ALL}")
        conferences = aggregator.aggregate_conferences()
        
        if not conferences:
            click.echo(f"{Fore.RED}No conferences found{Style.RESET_ALL}")
            return
        
        click.echo(f"{Fore.GREEN}Found {len(conferences)} conferences{Style.RESET_ALL}")
        
        # Score conferences
        click.echo(f"{Fore.YELLOW}Scoring conferences...{Style.RESET_ALL}")
        scorer = ConferenceScorer()
        scored_conferences = [scorer.score_conference(conf) for conf in conferences]
        
        # Save to database
        click.echo(f"{Fore.YELLOW}Saving to database...{Style.RESET_ALL}")
        with ConferenceDatabase(db) as db_conn:
            for conf in scored_conferences:
                db_conn.add_conference(conf)
        
        click.echo(f"{Fore.GREEN}✓ Database updated successfully!{Style.RESET_ALL}\n")
        
    except Exception as e:
        click.echo(f"{Fore.RED}Error updating database: {e}{Style.RESET_ALL}")
        return 1


@conference_cli.command('search')
@click.option('--from-date', help='Start date (YYYY-MM-DD)')
@click.option('--to-date', help='End date (YYYY-MM-DD)')
@click.option('--location-type', type=click.Choice(['virtual', 'in-person', 'hybrid']), 
              help='Filter by location type')
@click.option('--topic', multiple=True, 
              type=click.Choice([t.value for t in TopicFocus]),
              help='Filter by topic focus (can use multiple times)')
@click.option('--min-score', type=float, help='Minimum overall score (0-10)')
@click.option('--max-price', type=float, help='Maximum ticket price')
@click.option('--location', multiple=True, help='Location keywords (can use multiple times)')
@click.option('--output', '-o', help='Output CSV file path')
@click.option('--report', '-r', help='Output report file path')
@click.option('--db', default='conferences.db', help='Database file path')
def search_conferences(from_date, to_date, location_type, topic, min_score, max_price, location, output, report, db):
    """Search conferences with filters"""
    click.echo(f"\n{Fore.CYAN}Searching conferences...{Style.RESET_ALL}\n")
    
    try:
        # Build filters
        filters = ConferenceSearchFilters()
        
        if from_date:
            filters.start_date_from = datetime.strptime(from_date, '%Y-%m-%d')
        
        if to_date:
            filters.start_date_to = datetime.strptime(to_date, '%Y-%m-%d')
        
        if location_type:
            filters.location_type = LocationType(location_type)
        
        if topic:
            filters.topic_focus = [TopicFocus(t) for t in topic]
        
        if min_score is not None:
            filters.min_score = min_score
        
        if max_price is not None:
            filters.max_price = max_price
        
        if location:
            filters.location_keywords = list(location)
        
        # Display active filters
        if any([from_date, to_date, location_type, topic, min_score, max_price, location]):
            click.echo(f"{Fore.YELLOW}Active filters:{Style.RESET_ALL}")
            if from_date:
                click.echo(f"  • From date: {from_date}")
            if to_date:
                click.echo(f"  • To date: {to_date}")
            if location_type:
                click.echo(f"  • Location type: {location_type}")
            if topic:
                click.echo(f"  • Topic focus: {', '.join(topic)}")
            if min_score:
                click.echo(f"  • Min score: {min_score}")
            if max_price:
                click.echo(f"  • Max price: ${max_price}")
            if location:
                click.echo(f"  • Location keywords: {', '.join(location)}")
            click.echo()
        
        # Search database
        with ConferenceDatabase(db) as db_conn:
            conferences = db_conn.search_conferences(filters)
        
        if not conferences:
            click.echo(f"{Fore.YELLOW}No conferences found matching your criteria{Style.RESET_ALL}\n")
            return
        
        click.echo(f"{Fore.GREEN}Found {len(conferences)} conferences{Style.RESET_ALL}\n")
        
        # Display results
        _display_conferences(conferences)
        
        # Export to CSV if requested
        if output:
            exporter = ConferenceExporter()
            exporter.export_to_csv(conferences, output)
            click.echo(f"\n{Fore.GREEN}✓ Results exported to {output}{Style.RESET_ALL}")
        
        # Generate report if requested
        if report:
            exporter = ConferenceExporter()
            summary = exporter.generate_summary_report(conferences, filters)
            exporter.save_text_report(summary, report)
            click.echo(f"{Fore.GREEN}✓ Report saved to {report}{Style.RESET_ALL}")
            
            # Display recommendations
            click.echo(f"\n{Fore.CYAN}{'=' * 70}{Style.RESET_ALL}")
            click.echo(f"{Fore.CYAN}RECOMMENDATIONS{Style.RESET_ALL}")
            click.echo(f"{Fore.CYAN}{'=' * 70}{Style.RESET_ALL}\n")
            for i, rec in enumerate(summary.recommendations, 1):
                click.echo(f"{i}. {rec}")
            click.echo()
        
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        return 1


@conference_cli.command('list')
@click.option('--limit', type=int, default=10, help='Number of conferences to display')
@click.option('--db', default='conferences.db', help='Database file path')
def list_conferences(limit, db):
    """List all conferences in the database"""
    click.echo(f"\n{Fore.CYAN}Listing conferences...{Style.RESET_ALL}\n")
    
    try:
        with ConferenceDatabase(db) as db_conn:
            conferences = db_conn.get_all_conferences()
        
        if not conferences:
            click.echo(f"{Fore.YELLOW}No conferences in database. Run 'conference-tracker update' first.{Style.RESET_ALL}\n")
            return
        
        # Sort by score
        conferences.sort(key=lambda x: x.overall_score, reverse=True)
        
        # Limit results
        display_conferences = conferences[:limit]
        
        click.echo(f"{Fore.GREEN}Total conferences in database: {len(conferences)}{Style.RESET_ALL}")
        click.echo(f"{Fore.GREEN}Displaying top {len(display_conferences)}{Style.RESET_ALL}\n")
        
        _display_conferences(display_conferences)
        
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return 1


@conference_cli.command('report')
@click.option('--output', '-o', required=True, help='Output report file path')
@click.option('--format', type=click.Choice(['text', 'json']), default='text', help='Report format')
@click.option('--db', default='conferences.db', help='Database file path')
def generate_report(output, format, db):
    """Generate a summary report of all conferences"""
    click.echo(f"\n{Fore.CYAN}Generating conference report...{Style.RESET_ALL}\n")
    
    try:
        with ConferenceDatabase(db) as db_conn:
            conferences = db_conn.get_all_conferences()
        
        if not conferences:
            click.echo(f"{Fore.YELLOW}No conferences in database. Run 'conference-tracker update' first.{Style.RESET_ALL}\n")
            return
        
        exporter = ConferenceExporter()
        summary = exporter.generate_summary_report(conferences)
        
        if format == 'text':
            exporter.save_text_report(summary, output)
        else:  # json
            with open(output, 'w') as f:
                json.dump(summary.model_dump(), f, indent=2, default=str)
        
        click.echo(f"{Fore.GREEN}✓ Report saved to {output}{Style.RESET_ALL}\n")
        
        # Display preview
        click.echo(f"{Fore.CYAN}Report Preview:{Style.RESET_ALL}")
        click.echo(f"Total Conferences: {summary.total_conferences}")
        click.echo(f"Date Range: {summary.date_range}\n")
        
        click.echo(f"{Fore.YELLOW}Top Recommendations:{Style.RESET_ALL}")
        for i, rec in enumerate(summary.recommendations[:5], 1):
            click.echo(f"{i}. {rec}")
        click.echo()
        
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return 1


def _display_conferences(conferences):
    """Helper function to display conferences"""
    for i, conf in enumerate(conferences, 1):
        click.echo(f"{Fore.GREEN}{'=' * 70}{Style.RESET_ALL}")
        click.echo(f"{Fore.GREEN}{i}. {conf.name}{Style.RESET_ALL}")
        click.echo(f"{Fore.GREEN}{'=' * 70}{Style.RESET_ALL}")
        
        # Basic info
        click.echo(f"{Fore.YELLOW}Date:{Style.RESET_ALL} {conf.start_date.strftime('%B %d, %Y')}", nl=False)
        if conf.start_date.date() != conf.end_date.date():
            click.echo(f" - {conf.end_date.strftime('%B %d, %Y')}")
        else:
            click.echo()
        
        click.echo(f"{Fore.YELLOW}Location:{Style.RESET_ALL} {conf.location} ({conf.location_type.value})")
        
        # Price
        if conf.ticket_price_min is not None and conf.ticket_price_max is not None:
            if conf.ticket_price_min == 0 and conf.ticket_price_max == 0:
                click.echo(f"{Fore.YELLOW}Price:{Style.RESET_ALL} Free")
            elif conf.ticket_price_min == conf.ticket_price_max:
                click.echo(f"{Fore.YELLOW}Price:{Style.RESET_ALL} ${conf.ticket_price_min}")
            else:
                click.echo(f"{Fore.YELLOW}Price:{Style.RESET_ALL} ${conf.ticket_price_min} - ${conf.ticket_price_max}")
        elif conf.ticket_price_min == 0:
            click.echo(f"{Fore.YELLOW}Price:{Style.RESET_ALL} Free")
        
        # Scores
        click.echo(f"{Fore.YELLOW}Scores:{Style.RESET_ALL}")
        click.echo(f"  Overall: {_score_with_color(conf.overall_score)}/10 | ", nl=False)
        click.echo(f"AI Relevance: {_score_with_color(conf.relevance_score)}/10 | ", nl=False)
        click.echo(f"Speaker Quality: {_score_with_color(conf.speaker_quality_score)}/10 | ", nl=False)
        click.echo(f"Networking: {_score_with_color(conf.networking_score)}/10")
        
        # URL
        click.echo(f"{Fore.YELLOW}URL:{Style.RESET_ALL} {conf.url}")
        
        # Registration deadline
        if conf.registration_deadline:
            days_until = (conf.registration_deadline - datetime.utcnow()).days
            if days_until < 0:
                click.echo(f"{Fore.RED}Registration deadline passed{Style.RESET_ALL}")
            elif days_until <= 7:
                click.echo(f"{Fore.RED}Registration deadline: {conf.registration_deadline.strftime('%B %d, %Y')} ({days_until} days left){Style.RESET_ALL}")
            else:
                click.echo(f"{Fore.YELLOW}Registration deadline:{Style.RESET_ALL} {conf.registration_deadline.strftime('%B %d, %Y')}")
        
        # Notable speakers
        if conf.notable_speakers:
            click.echo(f"{Fore.YELLOW}Notable Speakers:{Style.RESET_ALL}")
            for speaker in conf.notable_speakers[:3]:
                click.echo(f"  • {speaker}")
            if len(conf.notable_speakers) > 3:
                click.echo(f"  • ... and {len(conf.notable_speakers) - 3} more")
        
        # Topics
        if conf.agenda_topics:
            click.echo(f"{Fore.YELLOW}Topics:{Style.RESET_ALL} {', '.join(conf.agenda_topics[:5])}")
        
        click.echo()


def _score_with_color(score):
    """Return score with color based on value"""
    if score >= 7.5:
        return f"{Fore.GREEN}{score}{Style.RESET_ALL}"
    elif score >= 5.0:
        return f"{Fore.YELLOW}{score}{Style.RESET_ALL}"
    else:
        return f"{Fore.RED}{score}{Style.RESET_ALL}"


@conference_cli.command('schedule')
@click.argument('action', type=click.Choice(['setup', 'status', 'run', 'enable', 'disable']))
@click.option('--frequency', type=click.Choice(['weekly', 'monthly']), help='Schedule frequency')
@click.option('--from-date', help='Start date filter (YYYY-MM-DD)')
@click.option('--to-date', help='End date filter (YYYY-MM-DD)')
@click.option('--location-type', type=click.Choice(['virtual', 'in-person', 'hybrid']), 
              help='Filter by location type')
@click.option('--topic', multiple=True, 
              type=click.Choice([t.value for t in TopicFocus]),
              help='Filter by topic focus (can use multiple times)')
@click.option('--min-score', type=float, help='Minimum overall score (0-10)')
@click.option('--max-price', type=float, help='Maximum ticket price')
@click.option('--output-dir', default='.', help='Output directory for reports')
@click.option('--force', is_flag=True, help='Force run even if not scheduled (for run action)')
@click.option('--db', default='conferences.db', help='Database file path')
def schedule_command(action, frequency, from_date, to_date, location_type, topic, 
                     min_score, max_price, output_dir, force, db):
    """Manage scheduled conference searches
    
    Actions:
        setup - Set up a new schedule
        status - Show current schedule status
        run - Run scheduled search now
        enable - Enable scheduled searches
        disable - Disable scheduled searches
    
    Examples:
        conference-tracker schedule setup --frequency weekly --topic "AI/ML"
        conference-tracker schedule status
        conference-tracker schedule run
    """
    scheduler = ConferenceScheduler()
    
    try:
        if action == 'setup':
            if not frequency:
                click.echo(f"{Fore.RED}Error: --frequency is required for setup{Style.RESET_ALL}")
                return 1
            
            # Build filters
            filters = ConferenceSearchFilters()
            
            if from_date:
                filters.start_date_from = datetime.strptime(from_date, '%Y-%m-%d')
            
            if to_date:
                filters.start_date_to = datetime.strptime(to_date, '%Y-%m-%d')
            
            if location_type:
                filters.location_type = LocationType(location_type)
            
            if topic:
                filters.topic_focus = [TopicFocus(t) for t in topic]
            
            if min_score is not None:
                filters.min_score = min_score
            
            if max_price is not None:
                filters.max_price = max_price
            
            scheduler.set_schedule(frequency, filters)
            
            click.echo(f"\n{Fore.GREEN}✓ Schedule configured successfully!{Style.RESET_ALL}")
            click.echo(f"{Fore.CYAN}Frequency:{Style.RESET_ALL} {frequency}")
            click.echo(f"{Fore.CYAN}Next run:{Style.RESET_ALL} {scheduler.config.next_run.strftime('%Y-%m-%d %H:%M UTC')}")
            
            if any([from_date, to_date, location_type, topic, min_score, max_price]):
                click.echo(f"\n{Fore.YELLOW}Active filters:{Style.RESET_ALL}")
                if from_date:
                    click.echo(f"  • From date: {from_date}")
                if to_date:
                    click.echo(f"  • To date: {to_date}")
                if location_type:
                    click.echo(f"  • Location type: {location_type}")
                if topic:
                    click.echo(f"  • Topic focus: {', '.join(topic)}")
                if min_score:
                    click.echo(f"  • Min score: {min_score}")
                if max_price:
                    click.echo(f"  • Max price: ${max_price}")
            click.echo()
        
        elif action == 'status':
            status = scheduler.get_status()
            
            click.echo(f"\n{Fore.CYAN}Schedule Status{Style.RESET_ALL}")
            click.echo(f"{'=' * 50}")
            
            enabled_str = f"{Fore.GREEN}Enabled{Style.RESET_ALL}" if status['enabled'] else f"{Fore.RED}Disabled{Style.RESET_ALL}"
            click.echo(f"Status: {enabled_str}")
            click.echo(f"Frequency: {status['frequency']}")
            
            if status['last_run']:
                last_run = datetime.fromisoformat(status['last_run'])
                click.echo(f"Last run: {last_run.strftime('%Y-%m-%d %H:%M UTC')}")
            else:
                click.echo("Last run: Never")
            
            if status['next_run']:
                next_run = datetime.fromisoformat(status['next_run'])
                click.echo(f"Next run: {next_run.strftime('%Y-%m-%d %H:%M UTC')}")
            else:
                click.echo("Next run: Not scheduled")
            
            # Show filters if any are set
            filters = status['filters']
            has_filters = any([
                filters.get('start_date_from'),
                filters.get('start_date_to'),
                filters.get('location_type'),
                filters.get('topic_focus'),
                filters.get('min_score') is not None,
                filters.get('max_price') is not None
            ])
            
            if has_filters:
                click.echo(f"\n{Fore.YELLOW}Active filters:{Style.RESET_ALL}")
                if filters.get('start_date_from'):
                    click.echo(f"  • From date: {filters['start_date_from']}")
                if filters.get('start_date_to'):
                    click.echo(f"  • To date: {filters['start_date_to']}")
                if filters.get('location_type'):
                    click.echo(f"  • Location type: {filters['location_type']}")
                if filters.get('topic_focus'):
                    click.echo(f"  • Topic focus: {', '.join(filters['topic_focus'])}")
                if filters.get('min_score') is not None:
                    click.echo(f"  • Min score: {filters['min_score']}")
                if filters.get('max_price') is not None:
                    click.echo(f"  • Max price: ${filters['max_price']}")
            click.echo()
        
        elif action == 'run':
            click.echo(f"\n{Fore.CYAN}Running scheduled search...{Style.RESET_ALL}\n")
            
            result = scheduler.run_scheduled_search(db, output_dir, force=force)
            
            if result:
                click.echo(f"{Fore.GREEN}✓ Scheduled search completed!{Style.RESET_ALL}\n")
                click.echo(f"Conferences found: {result['num_conferences']}")
                click.echo(f"CSV saved to: {result['csv_path']}")
                click.echo(f"Report saved to: {result['report_path']}\n")
                
                # Show recommendations
                if result['summary'].recommendations:
                    click.echo(f"{Fore.CYAN}Top Recommendations:{Style.RESET_ALL}")
                    for i, rec in enumerate(result['summary'].recommendations[:3], 1):
                        click.echo(f"{i}. {rec}")
                    click.echo()
            else:
                click.echo(f"{Fore.YELLOW}Schedule is disabled or not yet due to run. Use --force to run anyway.{Style.RESET_ALL}\n")
        
        elif action == 'enable':
            scheduler.enable_schedule()
            click.echo(f"\n{Fore.GREEN}✓ Schedule enabled{Style.RESET_ALL}\n")
        
        elif action == 'disable':
            scheduler.disable_schedule()
            click.echo(f"\n{Fore.YELLOW}Schedule disabled{Style.RESET_ALL}\n")
    
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    conference_cli()
