"""
Export podcast opportunities to spreadsheet formats
"""
import csv
from typing import List
from pathlib import Path
from datetime import datetime
from .podcast_models import PodcastOpportunity


class PodcastExporter:
    """Export podcast opportunities to various formats"""
    
    def export_to_csv(
        self,
        opportunities: List[PodcastOpportunity],
        output_path: str
    ):
        """
        Export opportunities to CSV file
        
        Args:
            opportunities: List of PodcastOpportunity objects
            output_path: Path to output CSV file
        """
        if not opportunities:
            raise ValueError("No opportunities to export")
        
        # Define CSV columns
        fieldnames = [
            'Podcast Name',
            'Host Name',
            'Contact',
            'Description',
            'Typical Guest Profile',
            'Audience Size',
            'Submission Link',
            'Submission Process',
            'Source',
            'Source URL',
            'Total Score',
            'Relevance Score',
            'Audience Score',
            'Engagement Score',
            'Why Good Fit',
            'Application Status',
            'Found Date',
            'Deadline',
            'Applied Date',
            'Notes'
        ]
        
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for opp in opportunities:
                writer.writerow({
                    'Podcast Name': opp.podcast_name,
                    'Host Name': opp.host_name or '',
                    'Contact': opp.host_contact or '',
                    'Description': opp.show_description or '',
                    'Typical Guest Profile': opp.typical_guest_profile or '',
                    'Audience Size': opp.audience_size if opp.audience_size else '',
                    'Submission Link': opp.submission_link or '',
                    'Submission Process': opp.submission_process or '',
                    'Source': opp.source or '',
                    'Source URL': opp.source_url or '',
                    'Total Score': f"{opp.total_score:.2f}",
                    'Relevance Score': f"{opp.relevance_score:.2f}",
                    'Audience Score': f"{opp.audience_score:.2f}",
                    'Engagement Score': f"{opp.engagement_score:.2f}",
                    'Why Good Fit': opp.fit_reason or '',
                    'Application Status': opp.application_status.value,
                    'Found Date': opp.found_date.strftime('%Y-%m-%d'),
                    'Deadline': opp.deadline.strftime('%Y-%m-%d') if opp.deadline else '',
                    'Applied Date': opp.applied_date.strftime('%Y-%m-%d') if opp.applied_date else '',
                    'Notes': opp.notes or ''
                })
    
    def export_to_markdown(
        self,
        opportunities: List[PodcastOpportunity],
        output_path: str
    ):
        """
        Export opportunities to a formatted Markdown file
        
        Args:
            opportunities: List of PodcastOpportunity objects
            output_path: Path to output Markdown file
        """
        if not opportunities:
            raise ValueError("No opportunities to export")
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("# Podcast Guest Opportunities\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            f.write(f"Total Opportunities: {len(opportunities)}\n\n")
            f.write("---\n\n")
            
            for i, opp in enumerate(opportunities, 1):
                f.write(f"## {i}. {opp.podcast_name}\n\n")
                
                # Basic info
                if opp.host_name:
                    f.write(f"**Host:** {opp.host_name}\n\n")
                
                if opp.host_contact:
                    f.write(f"**Contact:** {opp.host_contact}\n\n")
                
                if opp.show_description:
                    f.write(f"**Description:** {opp.show_description}\n\n")
                
                if opp.typical_guest_profile:
                    f.write(f"**Typical Guests:** {opp.typical_guest_profile}\n\n")
                
                # Metrics
                f.write("### Metrics\n\n")
                if opp.audience_size:
                    f.write(f"- **Audience Size:** {opp.audience_size:,} listeners/episode\n")
                f.write(f"- **Total Score:** {opp.total_score:.1f}/100\n")
                f.write(f"- **Relevance Score:** {opp.relevance_score:.1f}/100\n")
                f.write(f"- **Audience Score:** {opp.audience_score:.1f}/100\n")
                f.write(f"- **Engagement Score:** {opp.engagement_score:.1f}/100\n")
                f.write("\n")
                
                # Why it's a good fit
                if opp.fit_reason:
                    f.write(f"**Why Good Fit:** {opp.fit_reason}\n\n")
                
                # Application info
                f.write("### Application\n\n")
                f.write(f"- **Status:** {opp.application_status.value}\n")
                
                if opp.submission_link:
                    f.write(f"- **Submission Link:** {opp.submission_link}\n")
                
                if opp.submission_process:
                    f.write(f"- **How to Apply:** {opp.submission_process}\n")
                
                if opp.deadline:
                    f.write(f"- **Deadline:** {opp.deadline.strftime('%Y-%m-%d')}\n")
                
                if opp.source_url:
                    f.write(f"- **Source:** [{opp.source}]({opp.source_url})\n")
                elif opp.source:
                    f.write(f"- **Source:** {opp.source}\n")
                
                f.write("\n")
                
                if opp.notes:
                    f.write(f"**Notes:** {opp.notes}\n\n")
                
                f.write("---\n\n")
    
    def create_quick_summary(
        self,
        opportunities: List[PodcastOpportunity],
        top_n: int = 10
    ) -> str:
        """
        Create a quick text summary of top opportunities
        
        Args:
            opportunities: List of PodcastOpportunity objects
            top_n: Number of top opportunities to include
            
        Returns:
            Formatted string summary
        """
        if not opportunities:
            return "No opportunities found."
        
        # Sort by total score
        sorted_opps = sorted(opportunities, key=lambda x: x.total_score, reverse=True)
        top_opps = sorted_opps[:top_n]
        
        summary = f"Top {len(top_opps)} Podcast Opportunities\n"
        summary += "=" * 50 + "\n\n"
        
        for i, opp in enumerate(top_opps, 1):
            summary += f"{i}. {opp.podcast_name} (Score: {opp.total_score:.1f}/100)\n"
            if opp.host_name:
                summary += f"   Host: {opp.host_name}\n"
            if opp.audience_size:
                summary += f"   Audience: {opp.audience_size:,}\n"
            summary += f"   Status: {opp.application_status.value}\n"
            if opp.fit_reason:
                summary += f"   Fit: {opp.fit_reason}\n"
            summary += "\n"
        
        return summary
