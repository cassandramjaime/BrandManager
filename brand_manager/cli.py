"""
Command-line interface for AI Topic Researcher and Trend Tracker
"""
import json
import click
from dotenv import load_dotenv
from colorama import init, Fore, Style

from .models import TopicResearchRequest
from .ai_manager import AITopicResearcher
from .trend_tracker import TrendTracker

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Load environment variables
load_dotenv()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """BrandManager - AI Topic Research and Consumer Trend Tracking Tool"""
    pass


@cli.command()
@click.argument('topic')
@click.option('--depth', type=click.Choice(['quick', 'standard', 'deep']), default='standard',
              help='Research depth: quick, standard, or deep')
@click.option('--focus', multiple=True,
              help='Specific areas to focus on (can be used multiple times)')
@click.option('--output', '-o', type=click.Path(), help='Save results to JSON file')
def research(topic, depth, focus, output):
    """Research a topic dynamically using AI
    
    Example:
        topic-research research "AI in healthcare" --depth deep --focus trends --focus statistics
    """
    try:
        researcher = AITopicResearcher()
        
        click.echo(f"\n{Fore.CYAN}Researching topic: {Fore.WHITE}{topic}")
        click.echo(f"{Fore.CYAN}Depth: {Fore.WHITE}{depth}")
        if focus:
            click.echo(f"{Fore.CYAN}Focus areas: {Fore.WHITE}{', '.join(focus)}")
        click.echo()
        
        request = TopicResearchRequest(
            topic=topic,
            depth=depth,
            focus_areas=list(focus) if focus else []
        )
        
        with click.progressbar(length=1, label='Conducting research') as bar:
            result = researcher.research_topic(request)
            bar.update(1)
        
        # Display results
        click.echo(f"\n{Fore.GREEN}{'=' * 70}")
        click.echo(f"{Fore.GREEN}RESEARCH RESULTS: {result.topic}")
        click.echo(f"{Fore.GREEN}{'=' * 70}{Style.RESET_ALL}\n")
        
        # Summary
        click.echo(f"{Fore.YELLOW}SUMMARY:{Style.RESET_ALL}")
        click.echo(f"{result.summary}\n")
        
        # Key Points
        if result.key_points:
            click.echo(f"{Fore.YELLOW}KEY POINTS:{Style.RESET_ALL}")
            for point in result.key_points:
                click.echo(f"  • {point}")
            click.echo()
        
        # Trends
        if result.trends:
            click.echo(f"{Fore.YELLOW}CURRENT TRENDS:{Style.RESET_ALL}")
            for trend in result.trends:
                click.echo(f"  • {trend}")
            click.echo()
        
        # Statistics
        if result.statistics:
            click.echo(f"{Fore.YELLOW}STATISTICS & DATA:{Style.RESET_ALL}")
            for stat in result.statistics:
                click.echo(f"  • {stat}")
            click.echo()
        
        # Audience Interests
        if result.audience_interests:
            click.echo(f"{Fore.YELLOW}AUDIENCE INTERESTS:{Style.RESET_ALL}")
            for interest in result.audience_interests:
                click.echo(f"  • {interest}")
            click.echo()
        
        # Content Angles
        if result.content_angles:
            click.echo(f"{Fore.YELLOW}CONTENT ANGLES:{Style.RESET_ALL}")
            for angle in result.content_angles:
                click.echo(f"  • {angle}")
            click.echo()
        
        # Competitor Insights
        if result.competitor_insights:
            click.echo(f"{Fore.YELLOW}COMPETITOR INSIGHTS:{Style.RESET_ALL}")
            for insight in result.competitor_insights:
                click.echo(f"  • {insight}")
            click.echo()
        
        # Keywords
        if result.keywords:
            click.echo(f"{Fore.YELLOW}KEYWORDS:{Style.RESET_ALL}")
            click.echo(f"  {', '.join(result.keywords)}")
            click.echo()
        
        # Save to file if requested
        if output:
            with open(output, 'w') as f:
                json.dump(result.model_dump(), f, indent=2)
            click.echo(f"{Fore.GREEN}✓ Results saved to {output}{Style.RESET_ALL}\n")
        
    except ValueError as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        click.echo(f"{Fore.YELLOW}Make sure you have set OPENAI_API_KEY in your .env file{Style.RESET_ALL}")
        return 1
    except Exception as e:
        click.echo(f"{Fore.RED}Unexpected error: {e}{Style.RESET_ALL}")
        return 1


@cli.command()
@click.argument('topic')
@click.option('--output', '-o', type=click.Path(), help='Save results to JSON file')
def quick(topic, output):
    """Quick research on a topic (faster, less detailed)
    
    Example:
        topic-research quick "sustainable fashion"
    """
    ctx = click.get_current_context()
    ctx.invoke(research, topic=topic, depth='quick', focus=(), output=output)


@cli.command()
@click.argument('topic')
@click.option('--output', '-o', type=click.Path(), help='Save results to JSON file')
def deep(topic, output):
    """Deep research on a topic (slower, more detailed)
    
    Example:
        topic-research deep "quantum computing applications"
    """
    ctx = click.get_current_context()
    ctx.invoke(research, topic=topic, depth='deep', focus=(), output=output)


# Trend Tracking Commands

@cli.command()
@click.option('--product-hunt/--no-product-hunt', default=True, help='Include Product Hunt')
@click.option('--tech-news/--no-tech-news', default=True, help='Include TechCrunch and The Verge')
@click.option('--hacker-news/--no-hacker-news', default=True, help='Include Hacker News')
@click.option('--reddit/--no-reddit', default=True, help='Include Reddit')
@click.option('--reddit-subs', multiple=True, default=['technology', 'gadgets', 'startups'],
              help='Reddit subreddits to track')
def collect(product_hunt, tech_news, hacker_news, reddit, reddit_subs):
    """Collect current trends from data sources
    
    Example:
        topic-research collect
        topic-research collect --no-product-hunt --reddit-subs technology --reddit-subs startups
    """
    try:
        tracker = TrendTracker()
        
        click.echo(f"\n{Fore.CYAN}Collecting consumer product trends...{Style.RESET_ALL}\n")
        
        trends = tracker.collect_current_trends(
            product_hunt=product_hunt,
            tech_news=tech_news,
            hacker_news=hacker_news,
            reddit=reddit,
            reddit_subs=list(reddit_subs) if reddit else []
        )
        
        click.echo(f"\n{Fore.GREEN}✓ Successfully collected {len(trends)} trends{Style.RESET_ALL}\n")
        
        # Show sample
        if trends:
            click.echo(f"{Fore.YELLOW}Sample trends:{Style.RESET_ALL}")
            for trend in trends[:5]:
                click.echo(f"  • {trend.title} ({trend.category}) - {trend.source.name}")
        
    except ValueError as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        click.echo(f"{Fore.YELLOW}Make sure you have set OPENAI_API_KEY in your .env file{Style.RESET_ALL}")
        return 1
    except Exception as e:
        click.echo(f"{Fore.RED}Unexpected error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        return 1


@cli.command()
@click.option('--pdf/--no-pdf', default=True, help='Generate PDF report')
@click.option('--markdown/--no-markdown', default=True, help='Generate Markdown report')
def report(pdf, markdown):
    """Generate weekly trend report
    
    Example:
        topic-research report
        topic-research report --no-pdf
    """
    try:
        tracker = TrendTracker()
        
        click.echo(f"\n{Fore.CYAN}Generating weekly trend report...{Style.RESET_ALL}\n")
        
        weekly_report = tracker.generate_weekly_report(
            generate_pdf=pdf,
            generate_markdown=markdown
        )
        
        if weekly_report:
            click.echo(f"\n{Fore.GREEN}✓ Report generated successfully!{Style.RESET_ALL}")
            click.echo(f"\n{Fore.YELLOW}Report Summary:{Style.RESET_ALL}")
            click.echo(f"  Report ID: {weekly_report.report_id}")
            click.echo(f"  Trends analyzed: {weekly_report.total_items_analyzed}")
            click.echo(f"  Top category: {list(weekly_report.category_breakdown.keys())[0] if weekly_report.category_breakdown else 'N/A'}")
            
            if weekly_report.top_trends:
                click.echo(f"\n{Fore.YELLOW}Top 3 Trends:{Style.RESET_ALL}")
                for trend in weekly_report.top_trends[:3]:
                    click.echo(f"  {trend.rank}. {trend.title} (Score: {trend.traction_score:.1f})")
        else:
            click.echo(f"{Fore.YELLOW}No trends found in the specified period{Style.RESET_ALL}")
        
    except ValueError as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        click.echo(f"{Fore.YELLOW}Make sure you have set OPENAI_API_KEY in your .env file{Style.RESET_ALL}")
        return 1
    except Exception as e:
        click.echo(f"{Fore.RED}Unexpected error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        return 1


@cli.command()
@click.option('--categories', '-c', multiple=True, 
              default=['social', 'fintech', 'health', 'productivity', 'education', 'ecommerce'],
              help='Categories to track')
def configure(categories):
    """Configure tracked categories
    
    Example:
        topic-research configure -c social -c fintech -c health
    """
    try:
        tracker = TrendTracker()
        
        click.echo(f"\n{Fore.CYAN}Configuring tracked categories...{Style.RESET_ALL}\n")
        
        config = tracker.track_categories(categories=list(categories))
        
        click.echo(f"\n{Fore.GREEN}✓ Configuration updated{Style.RESET_ALL}")
        click.echo(f"  Categories: {', '.join(config.categories)}")
        
    except Exception as e:
        click.echo(f"{Fore.RED}Unexpected error: {e}{Style.RESET_ALL}")
        return 1


@cli.command()
@click.option('--days', '-d', default=30, help='Number of days to analyze')
def insights(days):
    """View historical trend insights
    
    Example:
        topic-research insights --days 30
    """
    try:
        tracker = TrendTracker()
        
        click.echo(f"\n{Fore.CYAN}Analyzing historical patterns...{Style.RESET_ALL}\n")
        
        historical_insights = tracker.get_historical_insights(days=days)
        
        click.echo(f"\n{Fore.YELLOW}Historical Insights ({days} days):{Style.RESET_ALL}")
        click.echo(f"  Total trends: {historical_insights['total_trends']}")
        click.echo(f"  Days with data: {len(historical_insights['daily_counts'])}")
        
        if historical_insights['popular_sources']:
            click.echo(f"\n{Fore.YELLOW}Top Sources:{Style.RESET_ALL}")
            sorted_sources = sorted(historical_insights['popular_sources'].items(), 
                                   key=lambda x: x[1], reverse=True)[:5]
            for source, count in sorted_sources:
                click.echo(f"  • {source}: {count} trends")
        
    except Exception as e:
        click.echo(f"{Fore.RED}Unexpected error: {e}{Style.RESET_ALL}")
        return 1


@cli.command()
def run():
    """Run full collection and generate report
    
    Example:
        topic-research run
    """
    try:
        tracker = TrendTracker()
        
        click.echo(f"\n{Fore.CYAN}Running full trend tracking cycle...{Style.RESET_ALL}\n")
        
        report = tracker.run_full_collection_and_report()
        
        if report:
            click.echo(f"\n{Fore.GREEN}✓ Full cycle completed successfully!{Style.RESET_ALL}")
        
    except ValueError as e:
        click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        click.echo(f"{Fore.YELLOW}Make sure you have set OPENAI_API_KEY in your .env file{Style.RESET_ALL}")
        return 1
    except Exception as e:
        click.echo(f"{Fore.RED}Unexpected error: {e}{Style.RESET_ALL}")
        import traceback
        traceback.print_exc()
        return 1


def main():
    """Entry point for the CLI"""
    cli()


if __name__ == '__main__':
    main()
