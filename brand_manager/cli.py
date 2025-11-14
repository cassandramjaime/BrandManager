"""
Command-line interface for AI Topic Researcher and Podcast Finder
"""
import json
import click
from dotenv import load_dotenv
from colorama import init, Fore, Style

from .models import TopicResearchRequest
from .ai_manager import AITopicResearcher
from .podcast_cli import podcast_cli

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Load environment variables
load_dotenv()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """BrandManager - Topic research and podcast guest opportunity finder"""
    pass


# Add podcast subcommand
cli.add_command(podcast_cli)


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


def main():
    """Entry point for the CLI"""
    cli()


if __name__ == '__main__':
    main()
