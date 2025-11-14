"""
Command-line interface for ML/AI Research Paper Monitoring
"""
import click
from datetime import datetime
from pathlib import Path

from .paper_models import PaperFilter, SearchQuery, TopicCategory, PaperSource
from .paper_database import PaperDatabase
from .paper_fetchers import PaperFetcherManager
from .paper_summarizer import PaperSummarizer
from .digest_generator import DigestGenerator


@click.group()
def papers():
    """ML/AI Research Paper Monitoring - Track and summarize recent research papers"""
    pass


@papers.command()
@click.option('--days', type=int, default=30, help='Number of days to look back (30, 60, or 90)')
@click.option('--topic', multiple=True, type=click.Choice([t.value for t in TopicCategory]),
              help='Topic categories to filter by (can be used multiple times)')
@click.option('--source', multiple=True, type=click.Choice([s.value for s in PaperSource]),
              help='Sources to fetch from (can be used multiple times)')
@click.option('--min-citations', type=int, default=0, help='Minimum citation count')
@click.option('--keyword', multiple=True, help='Keywords to search for')
@click.option('--summarize/--no-summarize', default=False, help='Generate AI summaries for papers')
@click.option('--db', type=click.Path(), default='papers.db', help='Database file path')
def fetch(days, topic, source, min_citations, keyword, summarize, db):
    """
    Fetch recent papers from various sources
    
    Example:
        papers fetch --days 30 --topic llms --source arxiv --summarize
    """
    click.echo(f"\n{click.style('Fetching ML/AI Research Papers', fg='cyan', bold=True)}")
    click.echo(f"Days back: {days}")
    if topic:
        click.echo(f"Topics: {', '.join(topic)}")
    if source:
        click.echo(f"Sources: {', '.join(source)}")
    if keyword:
        click.echo(f"Keywords: {', '.join(keyword)}")
    click.echo()
    
    # Build filter
    filters = PaperFilter(
        days_back=days,
        topics=[TopicCategory(t) for t in topic] if topic else [],
        sources=[PaperSource(s) for s in source] if source else [],
        min_citations=min_citations,
        keywords=list(keyword) if keyword else []
    )
    
    # Fetch papers
    fetcher = PaperFetcherManager()
    
    with click.progressbar(length=1, label='Fetching papers') as bar:
        papers = fetcher.fetch_papers(filters)
        bar.update(1)
    
    click.echo(f"\n{click.style('✓', fg='green')} Found {len(papers)} papers")
    
    # Save to database
    database = PaperDatabase(db)
    saved_count = 0
    
    with click.progressbar(papers, label='Saving to database') as papers_bar:
        for paper in papers_bar:
            if database.save_paper(paper):
                saved_count += 1
    
    click.echo(f"{click.style('✓', fg='green')} Saved {saved_count} new papers to database")
    
    # Generate summaries if requested
    if summarize and papers:
        click.echo(f"\n{click.style('Generating AI summaries...', fg='cyan')}")
        
        try:
            summarizer = PaperSummarizer()
            summarized_count = 0
            
            with click.progressbar(papers[:10], label='Summarizing papers') as summary_bar:
                for paper in summary_bar:
                    try:
                        summary = summarizer.summarize_paper(paper)
                        database.save_summary(summary)
                        summarized_count += 1
                    except Exception as e:
                        click.echo(f"\n{click.style('⚠', fg='yellow')} Error summarizing {paper.paper_id}: {e}")
            
            click.echo(f"{click.style('✓', fg='green')} Generated {summarized_count} summaries")
            
        except ValueError as e:
            click.echo(f"\n{click.style('⚠', fg='yellow')} {e}")
            click.echo(f"{click.style('Note:', fg='yellow')} Summaries require OPENAI_API_KEY to be set")
    
    # Show stats
    stats = database.get_stats()
    click.echo(f"\n{click.style('Database Statistics:', fg='cyan', bold=True)}")
    click.echo(f"  Total papers: {stats['total_papers']}")
    click.echo(f"  Total summaries: {stats['total_summaries']}")
    if stats['papers_by_source']:
        click.echo(f"  Papers by source:")
        for source, count in stats['papers_by_source'].items():
            click.echo(f"    - {source}: {count}")


@papers.command()
@click.argument('query')
@click.option('--limit', type=int, default=10, help='Maximum number of results')
@click.option('--offset', type=int, default=0, help='Offset for pagination')
@click.option('--db', type=click.Path(), default='papers.db', help='Database file path')
def search(query, limit, offset, db):
    """
    Search past papers using full-text search
    
    Example:
        papers search "transformer architecture" --limit 5
    """
    click.echo(f"\n{click.style('Searching papers:', fg='cyan')} {query}")
    click.echo()
    
    database = PaperDatabase(db)
    
    search_query = SearchQuery(
        query=query,
        limit=limit,
        offset=offset
    )
    
    results = database.search_papers(search_query)
    
    if not results:
        click.echo(f"{click.style('No papers found', fg='yellow')}")
        return
    
    click.echo(f"Found {len(results)} papers:\n")
    
    for i, paper in enumerate(results, 1):
        click.echo(f"{click.style(f'{i}.', fg='cyan', bold=True)} {click.style(paper.title, bold=True)}")
        click.echo(f"   Authors: {', '.join(paper.authors[:3])}")
        if len(paper.authors) > 3:
            click.echo(f"            (and {len(paper.authors) - 3} others)")
        click.echo(f"   Published: {paper.publication_date.strftime('%Y-%m-%d')}")
        click.echo(f"   Source: {paper.source.value}")
        click.echo(f"   Citations: {paper.citation_count}")
        click.echo(f"   URL: {paper.url}")
        
        # Show summary if available
        summary = database.get_summary(paper.paper_id)
        if summary:
            click.echo(f"   {click.style('Summary:', fg='green')}")
            # Show first 200 characters of summary
            summary_preview = summary.concise_summary[:200]
            if len(summary.concise_summary) > 200:
                summary_preview += "..."
            click.echo(f"   {summary_preview}")
        click.echo()


@papers.command()
@click.option('--days', type=int, default=7, help='Number of days for the digest')
@click.option('--top-n', type=int, default=10, help='Number of top papers to include')
@click.option('--output', type=click.Path(), help='Output file path (JSON, TXT, or HTML)')
@click.option('--format', type=click.Choice(['json', 'text', 'html']), default='text',
              help='Output format')
@click.option('--db', type=click.Path(), default='papers.db', help='Database file path')
def digest(days, top_n, output, format, db):
    """
    Generate a weekly digest of top papers
    
    Example:
        papers digest --days 7 --top-n 10 --output digest.html --format html
    """
    click.echo(f"\n{click.style('Generating Weekly Digest', fg='cyan', bold=True)}")
    click.echo(f"Period: Last {days} days")
    click.echo(f"Top papers: {top_n}")
    click.echo()
    
    database = PaperDatabase(db)
    generator = DigestGenerator(database)
    
    # Generate digest
    with click.progressbar(length=1, label='Generating digest') as bar:
        weekly_digest = generator.generate_weekly_digest(top_n=top_n)
        bar.update(1)
    
    click.echo(f"\n{click.style('✓', fg='green')} Digest generated")
    click.echo(f"  Papers reviewed: {weekly_digest.total_papers_reviewed}")
    click.echo(f"  Top papers selected: {len(weekly_digest.top_papers)}")
    click.echo(f"  Summaries included: {len(weekly_digest.summaries)}")
    
    # Export if output path specified
    if output:
        # Determine format from extension if not specified
        if not format:
            ext = Path(output).suffix.lower()
            if ext == '.json':
                format = 'json'
            elif ext == '.html':
                format = 'html'
            else:
                format = 'text'
        
        click.echo(f"\nExporting to {format.upper()} format...")
        
        if format == 'json':
            generator.export_to_json(weekly_digest, output)
        elif format == 'html':
            generator.export_to_html(weekly_digest, output)
        else:
            generator.export_to_text(weekly_digest, output)
        
        click.echo(f"{click.style('✓', fg='green')} Digest saved to {output}")
    else:
        # Display text digest to console
        text = generator.generate_text_digest(weekly_digest)
        click.echo("\n" + text)


@papers.command()
@click.option('--db', type=click.Path(), default='papers.db', help='Database file path')
def stats(db):
    """
    Show database statistics
    
    Example:
        papers stats
    """
    database = PaperDatabase(db)
    stats = database.get_stats()
    
    click.echo(f"\n{click.style('Database Statistics', fg='cyan', bold=True)}")
    click.echo(f"{'=' * 50}")
    click.echo(f"Total papers: {stats['total_papers']}")
    click.echo(f"Total summaries: {stats['total_summaries']}")
    
    if stats['papers_by_source']:
        click.echo(f"\nPapers by source:")
        for source, count in stats['papers_by_source'].items():
            click.echo(f"  {source:20s}: {count:5d}")
    
    # Get recent papers
    recent = database.get_recent_papers(days=30, limit=5)
    if recent:
        click.echo(f"\nMost recent papers (last 30 days):")
        for i, paper in enumerate(recent[:5], 1):
            click.echo(f"  {i}. {paper.title[:60]}...")
            click.echo(f"     Published: {paper.publication_date.strftime('%Y-%m-%d')}")
    
    click.echo()


@papers.command()
@click.argument('paper_id')
@click.option('--db', type=click.Path(), default='papers.db', help='Database file path')
def show(paper_id, db):
    """
    Show details of a specific paper
    
    Example:
        papers show 2301.00001
    """
    database = PaperDatabase(db)
    
    paper = database.get_paper(paper_id)
    if not paper:
        click.echo(f"{click.style('Error:', fg='red')} Paper not found: {paper_id}")
        return
    
    # Display paper details
    click.echo(f"\n{click.style('=' * 80, fg='cyan')}")
    click.echo(f"{click.style(paper.title, fg='cyan', bold=True)}")
    click.echo(f"{click.style('=' * 80, fg='cyan')}\n")
    
    click.echo(f"{click.style('Paper ID:', bold=True)} {paper.paper_id}")
    click.echo(f"{click.style('Authors:', bold=True)} {', '.join(paper.authors)}")
    click.echo(f"{click.style('Published:', bold=True)} {paper.publication_date.strftime('%Y-%m-%d')}")
    click.echo(f"{click.style('Source:', bold=True)} {paper.source.value}")
    click.echo(f"{click.style('Citations:', bold=True)} {paper.citation_count}")
    click.echo(f"{click.style('URL:', bold=True)} {paper.url}")
    
    if paper.categories:
        click.echo(f"{click.style('Categories:', bold=True)} {', '.join(paper.categories)}")
    
    click.echo(f"\n{click.style('Abstract:', bold=True)}")
    click.echo(paper.abstract)
    
    # Show summary if available
    summary = database.get_summary(paper.paper_id)
    if summary:
        click.echo(f"\n{click.style('=' * 80, fg='green')}")
        click.echo(f"{click.style('AI-GENERATED SUMMARY', fg='green', bold=True)}")
        click.echo(f"{click.style('=' * 80, fg='green')}\n")
        
        click.echo(f"{click.style('Summary:', bold=True)}")
        click.echo(summary.concise_summary)
        
        click.echo(f"\n{click.style('Main Contribution:', bold=True)}")
        click.echo(summary.main_contribution)
        
        click.echo(f"\n{click.style('Methodology:', bold=True)}")
        click.echo(summary.methodology_summary)
        
        click.echo(f"\n{click.style('Results:', bold=True)}")
        click.echo(summary.results_summary)
        
        click.echo(f"\n{click.style('Product Relevance:', bold=True)}")
        click.echo(summary.relevance_to_product)
        
        click.echo(f"\n{click.style('Categorization:', bold=True)}")
        click.echo(f"  Application Area: {summary.application_area.value}")
        click.echo(f"  Technical Difficulty: {summary.technical_difficulty.value}")
        click.echo(f"  Production Readiness: {summary.production_readiness.value}")
    
    click.echo()
