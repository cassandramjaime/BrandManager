"""
Example usage of the ML/AI Research Paper Monitoring system
"""
from datetime import datetime
from brand_manager.paper_models import (
    PaperFilter, TopicCategory, PaperSource,
    SearchQuery
)
from brand_manager.paper_database import PaperDatabase
from brand_manager.paper_fetchers import PaperFetcherManager
from brand_manager.paper_summarizer import PaperSummarizer
from brand_manager.digest_generator import DigestGenerator


def main():
    """Example workflow for paper monitoring"""
    
    print("=" * 80)
    print("ML/AI Research Paper Monitoring - Example Usage")
    print("=" * 80)
    print()
    
    # Initialize database
    db = PaperDatabase('example_papers.db')
    
    # Example 1: Fetch papers from arXiv
    print("1. Fetching papers from arXiv...")
    print("-" * 80)
    
    filters = PaperFilter(
        days_back=7,  # Last 7 days
        topics=[TopicCategory.LLMS],  # Focus on LLMs
        sources=[PaperSource.ARXIV],
        min_citations=0
    )
    
    fetcher = PaperFetcherManager()
    papers = fetcher.fetch_papers(filters)
    
    print(f"Found {len(papers)} papers")
    print()
    
    # Example 2: Save papers to database
    print("2. Saving papers to database...")
    print("-" * 80)
    
    saved_count = 0
    for paper in papers:
        if db.save_paper(paper):
            saved_count += 1
    
    print(f"Saved {saved_count} new papers")
    print()
    
    # Example 3: Generate summaries (if OPENAI_API_KEY is set)
    print("3. Generating AI summaries (requires OPENAI_API_KEY)...")
    print("-" * 80)
    
    try:
        summarizer = PaperSummarizer()
        
        # Summarize first 3 papers as example
        for i, paper in enumerate(papers[:3], 1):
            print(f"Summarizing paper {i}/{min(3, len(papers))}: {paper.title[:60]}...")
            try:
                summary = summarizer.summarize_paper(paper)
                db.save_summary(summary)
                print(f"  ✓ Summary saved")
            except Exception as e:
                print(f"  ✗ Error: {e}")
        
        print()
        
    except ValueError as e:
        print(f"Skipping summaries: {e}")
        print("Set OPENAI_API_KEY environment variable to enable summaries")
        print()
    
    # Example 4: Search papers
    print("4. Searching papers...")
    print("-" * 80)
    
    search_query = SearchQuery(
        query="language model",
        limit=5
    )
    
    results = db.search_papers(search_query)
    print(f"Found {len(results)} papers matching 'language model'")
    
    for i, paper in enumerate(results, 1):
        print(f"\n{i}. {paper.title}")
        print(f"   Authors: {', '.join(paper.authors[:2])}")
        if len(paper.authors) > 2:
            print(f"           (and {len(paper.authors) - 2} others)")
        print(f"   Published: {paper.publication_date.strftime('%Y-%m-%d')}")
        print(f"   URL: {paper.url}")
    
    print()
    
    # Example 5: Generate weekly digest
    print("5. Generating weekly digest...")
    print("-" * 80)
    
    generator = DigestGenerator(db)
    digest = generator.generate_weekly_digest(top_n=10)
    
    print(f"Digest generated:")
    print(f"  Week: {digest.week_start.strftime('%Y-%m-%d')} to {digest.week_end.strftime('%Y-%m-%d')}")
    print(f"  Total papers reviewed: {digest.total_papers_reviewed}")
    print(f"  Top papers selected: {len(digest.top_papers)}")
    print(f"  Summaries included: {len(digest.summaries)}")
    print()
    
    # Export digest to different formats
    print("Exporting digest to files...")
    generator.export_to_json(digest, 'example_digest.json')
    print("  ✓ Saved to example_digest.json")
    
    generator.export_to_html(digest, 'example_digest.html')
    print("  ✓ Saved to example_digest.html")
    
    generator.export_to_text(digest, 'example_digest.txt')
    print("  ✓ Saved to example_digest.txt")
    print()
    
    # Example 6: Database statistics
    print("6. Database statistics...")
    print("-" * 80)
    
    stats = db.get_stats()
    print(f"Total papers: {stats['total_papers']}")
    print(f"Total summaries: {stats['total_summaries']}")
    print(f"\nPapers by source:")
    for source, count in stats['papers_by_source'].items():
        print(f"  {source}: {count}")
    print()
    
    # Example 7: Get recent papers
    print("7. Recent papers (last 7 days)...")
    print("-" * 80)
    
    recent = db.get_recent_papers(days=7, limit=5)
    print(f"Found {len(recent)} recent papers\n")
    
    for i, paper in enumerate(recent, 1):
        print(f"{i}. {paper.title}")
        print(f"   Published: {paper.publication_date.strftime('%Y-%m-%d')}")
        print(f"   Citations: {paper.citation_count}")
        
        # Show summary if available
        summary = db.get_summary(paper.paper_id)
        if summary:
            print(f"   Summary: {summary.concise_summary[:150]}...")
        print()
    
    print("=" * 80)
    print("Example complete!")
    print("=" * 80)
    print()
    print("Files created:")
    print("  - example_papers.db (SQLite database)")
    print("  - example_digest.json (JSON format)")
    print("  - example_digest.html (HTML format)")
    print("  - example_digest.txt (Text format)")
    print()
    print("Try the CLI commands:")
    print("  topic-research papers fetch --days 30 --topic llms --summarize")
    print("  topic-research papers search 'transformer'")
    print("  topic-research papers digest --top-n 10 --output digest.html --format html")
    print()


if __name__ == '__main__':
    main()
