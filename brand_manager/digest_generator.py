"""
Weekly digest generator for top research papers
"""
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path

from .paper_models import Paper, PaperSummary, WeeklyDigest
from .paper_database import PaperDatabase


class DigestGenerator:
    """Generator for weekly paper digests"""
    
    def __init__(self, database: PaperDatabase):
        """
        Initialize the digest generator
        
        Args:
            database: PaperDatabase instance
        """
        self.database = database
    
    def generate_weekly_digest(
        self, 
        week_start: Optional[datetime] = None,
        top_n: int = 10
    ) -> WeeklyDigest:
        """
        Generate a weekly digest of top papers
        
        Args:
            week_start: Start of the week (defaults to 7 days ago)
            top_n: Number of top papers to include
            
        Returns:
            WeeklyDigest object
        """
        # Calculate week boundaries
        if week_start is None:
            week_end = datetime.now()
            week_start = week_end - timedelta(days=7)
        else:
            week_end = week_start + timedelta(days=7)
        
        # Get top papers from the week
        top_papers = self.database.get_top_papers(days=7, limit=top_n)
        
        # Get summaries for each paper
        summaries = {}
        for paper in top_papers:
            summary = self.database.get_summary(paper.paper_id)
            if summary:
                summaries[paper.paper_id] = summary
        
        # Count total papers reviewed
        all_papers = self.database.get_recent_papers(days=7, limit=1000)
        
        return WeeklyDigest(
            week_start=week_start,
            week_end=week_end,
            top_papers=top_papers,
            summaries=summaries,
            total_papers_reviewed=len(all_papers)
        )
    
    def export_to_json(self, digest: WeeklyDigest, output_path: str) -> None:
        """
        Export digest to JSON file
        
        Args:
            digest: WeeklyDigest object
            output_path: Path to output JSON file
        """
        # Convert to dictionary
        digest_dict = {
            'week_start': digest.week_start.isoformat(),
            'week_end': digest.week_end.isoformat(),
            'total_papers_reviewed': digest.total_papers_reviewed,
            'top_papers': [paper.model_dump() for paper in digest.top_papers],
            'summaries': {
                paper_id: summary.model_dump() 
                for paper_id, summary in digest.summaries.items()
            }
        }
        
        # Convert datetime objects to strings
        for paper in digest_dict['top_papers']:
            if isinstance(paper['publication_date'], datetime):
                paper['publication_date'] = paper['publication_date'].isoformat()
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(digest_dict, f, indent=2, default=str)
    
    def generate_text_digest(self, digest: WeeklyDigest) -> str:
        """
        Generate a text version of the digest
        
        Args:
            digest: WeeklyDigest object
            
        Returns:
            Formatted text digest
        """
        lines = []
        
        # Header
        lines.append("=" * 80)
        lines.append("WEEKLY ML/AI RESEARCH PAPER DIGEST")
        lines.append("=" * 80)
        lines.append(f"Week: {digest.week_start.strftime('%Y-%m-%d')} to {digest.week_end.strftime('%Y-%m-%d')}")
        lines.append(f"Total papers reviewed: {digest.total_papers_reviewed}")
        lines.append(f"Top papers: {len(digest.top_papers)}")
        lines.append("=" * 80)
        lines.append("")
        
        # Top papers
        for i, paper in enumerate(digest.top_papers, 1):
            lines.append(f"\n{'#' * 80}")
            lines.append(f"#{i:2d}. {paper.title}")
            lines.append('#' * 80)
            lines.append("")
            
            # Authors
            lines.append(f"Authors: {', '.join(paper.authors[:3])}")
            if len(paper.authors) > 3:
                lines.append(f"         (and {len(paper.authors) - 3} others)")
            lines.append("")
            
            # Metadata
            lines.append(f"Published: {paper.publication_date.strftime('%Y-%m-%d')}")
            lines.append(f"Source: {paper.source.value}")
            lines.append(f"Citations: {paper.citation_count}")
            lines.append(f"URL: {paper.url}")
            lines.append("")
            
            # Summary if available
            if paper.paper_id in digest.summaries:
                summary = digest.summaries[paper.paper_id]
                
                lines.append("SUMMARY:")
                lines.append(self._wrap_text(summary.concise_summary, 78))
                lines.append("")
                
                lines.append("Main Contribution:")
                lines.append(self._wrap_text(summary.main_contribution, 78))
                lines.append("")
                
                lines.append("Methodology:")
                lines.append(self._wrap_text(summary.methodology_summary, 78))
                lines.append("")
                
                lines.append("Key Results:")
                lines.append(self._wrap_text(summary.results_summary, 78))
                lines.append("")
                
                lines.append("Relevance to Product Management:")
                lines.append(self._wrap_text(summary.relevance_to_product, 78))
                lines.append("")
                
                # Categorization
                lines.append(f"Application Area: {summary.application_area.value}")
                lines.append(f"Technical Difficulty: {summary.technical_difficulty.value}")
                lines.append(f"Production Readiness: {summary.production_readiness.value}")
            else:
                lines.append("ABSTRACT:")
                lines.append(self._wrap_text(paper.abstract, 78))
            
            lines.append("")
        
        # Footer
        lines.append("\n" + "=" * 80)
        lines.append("End of Weekly Digest")
        lines.append("=" * 80)
        
        return '\n'.join(lines)
    
    def export_to_text(self, digest: WeeklyDigest, output_path: str) -> None:
        """
        Export digest to text file
        
        Args:
            digest: WeeklyDigest object
            output_path: Path to output text file
        """
        text = self.generate_text_digest(digest)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
    
    def _wrap_text(self, text: str, width: int = 78) -> str:
        """
        Wrap text to specified width
        
        Args:
            text: Text to wrap
            width: Maximum line width
            
        Returns:
            Wrapped text
        """
        if not text:
            return ""
        
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            word_length = len(word)
            
            if current_length + word_length + len(current_line) <= width:
                current_line.append(word)
                current_length += word_length
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                current_length = word_length
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return '\n'.join(lines)
    
    def generate_email_html(self, digest: WeeklyDigest) -> str:
        """
        Generate HTML version for email
        
        Args:
            digest: WeeklyDigest object
            
        Returns:
            HTML content
        """
        html_parts = []
        
        # Header
        html_parts.append("""
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }
        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
        h2 { color: #34495e; margin-top: 30px; }
        .paper { background: #f8f9fa; border-left: 4px solid #3498db; padding: 15px; margin: 20px 0; }
        .metadata { color: #7f8c8d; font-size: 0.9em; }
        .summary-section { margin: 15px 0; }
        .label { font-weight: bold; color: #2c3e50; }
        .tags { margin: 10px 0; }
        .tag { display: inline-block; background: #ecf0f1; padding: 5px 10px; margin: 2px; border-radius: 3px; font-size: 0.85em; }
    </style>
</head>
<body>
""")
        
        html_parts.append(f"""
    <h1>Weekly ML/AI Research Paper Digest</h1>
    <p class="metadata">
        Week: {digest.week_start.strftime('%Y-%m-%d')} to {digest.week_end.strftime('%Y-%m-%d')}<br>
        Total papers reviewed: {digest.total_papers_reviewed}<br>
        Top papers: {len(digest.top_papers)}
    </p>
""")
        
        # Papers
        for i, paper in enumerate(digest.top_papers, 1):
            html_parts.append(f"""
    <div class="paper">
        <h2>{i}. {paper.title}</h2>
        <p class="metadata">
            <strong>Authors:</strong> {', '.join(paper.authors[:5])}{' et al.' if len(paper.authors) > 5 else ''}<br>
            <strong>Published:</strong> {paper.publication_date.strftime('%Y-%m-%d')} | 
            <strong>Source:</strong> {paper.source.value} | 
            <strong>Citations:</strong> {paper.citation_count}<br>
            <strong>URL:</strong> <a href="{paper.url}">{paper.url}</a>
        </p>
""")
            
            if paper.paper_id in digest.summaries:
                summary = digest.summaries[paper.paper_id]
                
                html_parts.append(f"""
        <div class="summary-section">
            <p><span class="label">Summary:</span> {summary.concise_summary}</p>
        </div>
        <div class="summary-section">
            <p><span class="label">Main Contribution:</span> {summary.main_contribution}</p>
        </div>
        <div class="summary-section">
            <p><span class="label">Product Relevance:</span> {summary.relevance_to_product}</p>
        </div>
        <div class="tags">
            <span class="tag">📱 {summary.application_area.value}</span>
            <span class="tag">🎯 {summary.technical_difficulty.value}</span>
            <span class="tag">🚀 {summary.production_readiness.value}</span>
        </div>
""")
            else:
                html_parts.append(f"""
        <div class="summary-section">
            <p><span class="label">Abstract:</span> {paper.abstract}</p>
        </div>
""")
            
            html_parts.append("    </div>")
        
        # Footer
        html_parts.append("""
</body>
</html>
""")
        
        return '\n'.join(html_parts)
    
    def export_to_html(self, digest: WeeklyDigest, output_path: str) -> None:
        """
        Export digest to HTML file
        
        Args:
            digest: WeeklyDigest object
            output_path: Path to output HTML file
        """
        html = self.generate_email_html(digest)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
