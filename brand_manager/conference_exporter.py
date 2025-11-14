"""
CSV export and report generation for conferences
"""
import csv
from typing import List
from datetime import datetime
from pathlib import Path

from .conference_models import Conference, ConferenceSummaryReport


class ConferenceExporter:
    """Export conferences to CSV and generate reports"""
    
    def export_to_csv(self, conferences: List[Conference], output_file: str):
        """
        Export conferences to CSV file
        
        Args:
            conferences: List of conferences to export
            output_file: Path to output CSV file
        """
        if not conferences:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['No conferences found'])
            return
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow([
                'Name',
                'Start Date',
                'End Date',
                'Location',
                'Location Type',
                'Min Price ($)',
                'Max Price ($)',
                'Registration Deadline',
                'URL',
                'Source',
                'Notable Speakers',
                'Agenda Topics',
                'Topic Focus',
                'Overall Score',
                'Relevance Score',
                'Speaker Quality Score',
                'Networking Score',
                'Description'
            ])
            
            # Write conference data
            for conf in conferences:
                writer.writerow([
                    conf.name,
                    conf.start_date.strftime('%Y-%m-%d %H:%M'),
                    conf.end_date.strftime('%Y-%m-%d %H:%M'),
                    conf.location,
                    conf.location_type.value,
                    conf.ticket_price_min if conf.ticket_price_min is not None else 'N/A',
                    conf.ticket_price_max if conf.ticket_price_max is not None else 'N/A',
                    conf.registration_deadline.strftime('%Y-%m-%d') if conf.registration_deadline else 'N/A',
                    conf.url,
                    conf.source,
                    '; '.join(conf.notable_speakers) if conf.notable_speakers else 'N/A',
                    '; '.join(conf.agenda_topics) if conf.agenda_topics else 'N/A',
                    ', '.join([t.value for t in conf.topic_focus]) if conf.topic_focus else 'N/A',
                    conf.overall_score,
                    conf.relevance_score,
                    conf.speaker_quality_score,
                    conf.networking_score,
                    conf.description if conf.description else 'N/A'
                ])
    
    def generate_summary_report(self, conferences: List[Conference], filters=None) -> ConferenceSummaryReport:
        """
        Generate a summary report for conferences
        
        Args:
            conferences: List of conferences
            filters: Optional search filters used
            
        Returns:
            ConferenceSummaryReport object
        """
        if not conferences:
            return ConferenceSummaryReport(
                total_conferences=0,
                date_range="No conferences found",
                top_conferences=[],
                recommendations=["No conferences found matching your criteria"],
                statistics={}
            )
        
        # Calculate statistics
        total = len(conferences)
        
        # Date range
        start_dates = [c.start_date for c in conferences]
        min_date = min(start_dates)
        max_date = max(start_dates)
        date_range = f"{min_date.strftime('%b %Y')} - {max_date.strftime('%b %Y')}"
        
        # Top conferences (top 5 by score)
        sorted_conferences = sorted(conferences, key=lambda x: x.overall_score, reverse=True)
        top_conferences = sorted_conferences[:5]
        
        # Statistics
        virtual_count = sum(1 for c in conferences if c.location_type.value == 'virtual')
        in_person_count = sum(1 for c in conferences if c.location_type.value == 'in-person')
        hybrid_count = sum(1 for c in conferences if c.location_type.value == 'hybrid')
        
        prices = [c.ticket_price_min for c in conferences if c.ticket_price_min is not None and c.ticket_price_min > 0]
        avg_price = sum(prices) / len(prices) if prices else 0
        
        free_count = sum(1 for c in conferences if c.ticket_price_min == 0 or c.ticket_price_min is None)
        
        # AI-focused count
        ai_focused_count = sum(1 for c in conferences if c.relevance_score >= 7.0)
        
        statistics = {
            'total': total,
            'virtual': virtual_count,
            'in_person': in_person_count,
            'hybrid': hybrid_count,
            'avg_price': round(avg_price, 2),
            'free_count': free_count,
            'ai_focused': ai_focused_count,
            'avg_overall_score': round(sum(c.overall_score for c in conferences) / total, 1),
            'avg_relevance_score': round(sum(c.relevance_score for c in conferences) / total, 1),
        }
        
        # Generate recommendations
        recommendations = self._generate_recommendations(conferences, statistics)
        
        return ConferenceSummaryReport(
            total_conferences=total,
            date_range=date_range,
            top_conferences=top_conferences,
            recommendations=recommendations,
            statistics=statistics
        )
    
    def _generate_recommendations(self, conferences: List[Conference], statistics: dict) -> List[str]:
        """Generate personalized recommendations based on conference data"""
        recommendations = []
        
        if not conferences:
            return ["No conferences found matching your criteria"]
        
        # Top conference recommendation
        top_conf = max(conferences, key=lambda x: x.overall_score)
        recommendations.append(
            f"Top recommended: '{top_conf.name}' (Score: {top_conf.overall_score}/10) - "
            f"{top_conf.start_date.strftime('%B %d, %Y')}"
        )
        
        # AI-focused recommendation
        ai_conferences = [c for c in conferences if c.relevance_score >= 7.0]
        if ai_conferences:
            best_ai = max(ai_conferences, key=lambda x: x.relevance_score)
            recommendations.append(
                f"Best for AI/ML focus: '{best_ai.name}' (AI Relevance: {best_ai.relevance_score}/10)"
            )
        
        # Networking recommendation
        best_networking = max(conferences, key=lambda x: x.networking_score)
        if best_networking.networking_score >= 7.0:
            recommendations.append(
                f"Best for networking: '{best_networking.name}' (Networking Score: {best_networking.networking_score}/10)"
            )
        
        # Budget-friendly recommendation
        free_conferences = [c for c in conferences if c.ticket_price_min == 0 or c.ticket_price_min is None]
        if free_conferences:
            best_free = max(free_conferences, key=lambda x: x.overall_score)
            recommendations.append(
                f"Best free option: '{best_free.name}' (Score: {best_free.overall_score}/10)"
            )
        
        # Virtual option recommendation
        virtual_conferences = [c for c in conferences if c.location_type.value == 'virtual']
        if virtual_conferences:
            best_virtual = max(virtual_conferences, key=lambda x: x.overall_score)
            recommendations.append(
                f"Best virtual option: '{best_virtual.name}' (Score: {best_virtual.overall_score}/10)"
            )
        
        # Timing recommendation
        upcoming_soon = [c for c in conferences if (c.start_date - datetime.utcnow()).days <= 30]
        if upcoming_soon:
            next_conf = min(upcoming_soon, key=lambda x: x.start_date)
            recommendations.append(
                f"Coming up soon: '{next_conf.name}' on {next_conf.start_date.strftime('%B %d, %Y')}"
            )
        
        return recommendations
    
    def save_text_report(self, report: ConferenceSummaryReport, output_file: str):
        """
        Save summary report as a text file
        
        Args:
            report: ConferenceSummaryReport object
            output_file: Path to output text file
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("CONFERENCE RESEARCH SUMMARY REPORT\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Total Conferences Found: {report.total_conferences}\n")
            f.write(f"Date Range: {report.date_range}\n\n")
            
            f.write("-" * 80 + "\n")
            f.write("STATISTICS\n")
            f.write("-" * 80 + "\n")
            for key, value in report.statistics.items():
                f.write(f"{key.replace('_', ' ').title()}: {value}\n")
            f.write("\n")
            
            f.write("-" * 80 + "\n")
            f.write("RECOMMENDATIONS\n")
            f.write("-" * 80 + "\n")
            for i, rec in enumerate(report.recommendations, 1):
                f.write(f"{i}. {rec}\n")
            f.write("\n")
            
            f.write("-" * 80 + "\n")
            f.write("TOP CONFERENCES (by Overall Score)\n")
            f.write("-" * 80 + "\n\n")
            
            for i, conf in enumerate(report.top_conferences, 1):
                f.write(f"{i}. {conf.name}\n")
                f.write(f"   Date: {conf.start_date.strftime('%B %d, %Y')}")
                if conf.start_date.date() != conf.end_date.date():
                    f.write(f" - {conf.end_date.strftime('%B %d, %Y')}")
                f.write("\n")
                f.write(f"   Location: {conf.location} ({conf.location_type.value})\n")
                f.write(f"   Price: ${conf.ticket_price_min or 0} - ${conf.ticket_price_max or 'N/A'}\n")
                f.write(f"   Overall Score: {conf.overall_score}/10\n")
                f.write(f"   AI Relevance: {conf.relevance_score}/10 | ")
                f.write(f"Speaker Quality: {conf.speaker_quality_score}/10 | ")
                f.write(f"Networking: {conf.networking_score}/10\n")
                f.write(f"   URL: {conf.url}\n")
                if conf.notable_speakers:
                    f.write(f"   Notable Speakers: {', '.join(conf.notable_speakers[:3])}")
                    if len(conf.notable_speakers) > 3:
                        f.write(f" (and {len(conf.notable_speakers) - 3} more)")
                    f.write("\n")
                f.write("\n")
            
            f.write("=" * 80 + "\n")
            f.write(f"Report generated on: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC\n")
            f.write("=" * 80 + "\n")
