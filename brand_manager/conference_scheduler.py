"""
Scheduling functionality for automated conference searches
"""
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

from .conference_models import ScheduleConfig, ConferenceSearchFilters
from .conference_db import ConferenceDatabase
from .conference_scrapers import ConferenceAggregator
from .conference_scorer import ConferenceScorer
from .conference_exporter import ConferenceExporter


class ConferenceScheduler:
    """Handles scheduled conference searches"""
    
    def __init__(self, config_path: str = "schedule_config.json"):
        """
        Initialize scheduler
        
        Args:
            config_path: Path to schedule configuration file
        """
        self.config_path = config_path
        self.config = None
        self._load_config()
    
    def _load_config(self):
        """Load schedule configuration from file"""
        if os.path.exists(self.config_path) and os.path.getsize(self.config_path) > 0:
            try:
                with open(self.config_path, 'r') as f:
                    data = json.load(f)
                    self.config = ScheduleConfig(**data)
            except (json.JSONDecodeError, ValueError):
                # If config is corrupted, create a new one
                self._create_default_config()
        else:
            # Create default config
            self._create_default_config()
    
    def _create_default_config(self):
        """Create default configuration"""
        self.config = ScheduleConfig(
            frequency='weekly',
            filters=ConferenceSearchFilters(),
            enabled=False
        )
        self._save_config()
    
    def _save_config(self):
        """Save schedule configuration to file"""
        with open(self.config_path, 'w') as f:
            json.dump(self.config.model_dump(), f, indent=2, default=str)
    
    def set_schedule(
        self,
        frequency: str,
        filters: Optional[ConferenceSearchFilters] = None,
        email_recipients: Optional[list] = None
    ):
        """
        Set up a schedule for automated searches
        
        Args:
            frequency: 'weekly' or 'monthly'
            filters: Search filters to apply
            email_recipients: Email addresses to send reports to
        """
        if frequency not in ['weekly', 'monthly']:
            raise ValueError("Frequency must be 'weekly' or 'monthly'")
        
        self.config.frequency = frequency
        self.config.filters = filters or ConferenceSearchFilters()
        self.config.email_recipients = email_recipients or []
        self.config.enabled = True
        
        # Calculate next run time
        now = datetime.utcnow()
        if frequency == 'weekly':
            self.config.next_run = now + timedelta(weeks=1)
        else:  # monthly
            self.config.next_run = now + timedelta(days=30)
        
        self._save_config()
    
    def disable_schedule(self):
        """Disable scheduled searches"""
        self.config.enabled = False
        self._save_config()
    
    def enable_schedule(self):
        """Enable scheduled searches"""
        self.config.enabled = True
        self._save_config()
    
    def should_run(self) -> bool:
        """
        Check if scheduled search should run
        
        Returns:
            True if search should run now
        """
        if not self.config.enabled:
            return False
        
        if not self.config.next_run:
            return True
        
        return datetime.utcnow() >= self.config.next_run
    
    def run_scheduled_search(self, db_path: str = "conferences.db", output_dir: str = ".", force: bool = False):
        """
        Run a scheduled conference search
        
        Args:
            db_path: Path to database
            output_dir: Directory to save reports
            force: Force run even if not scheduled
        """
        if not force and not self.should_run():
            return None
        
        # Update database
        aggregator = ConferenceAggregator()
        conferences = aggregator.aggregate_conferences()
        
        scorer = ConferenceScorer()
        scored_conferences = [scorer.score_conference(conf) for conf in conferences]
        
        with ConferenceDatabase(db_path) as db:
            for conf in scored_conferences:
                db.add_conference(conf)
        
        # Search with filters
        with ConferenceDatabase(db_path) as db:
            results = db.search_conferences(self.config.filters)
        
        # Generate reports
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        
        exporter = ConferenceExporter()
        
        # CSV export
        csv_path = os.path.join(output_dir, f"conferences_{timestamp}.csv")
        exporter.export_to_csv(results, csv_path)
        
        # Text report
        report_path = os.path.join(output_dir, f"conference_report_{timestamp}.txt")
        summary = exporter.generate_summary_report(results, self.config.filters)
        exporter.save_text_report(summary, report_path)
        
        # Update last run and calculate next run
        self.config.last_run = datetime.utcnow()
        
        if self.config.frequency == 'weekly':
            self.config.next_run = self.config.last_run + timedelta(weeks=1)
        else:  # monthly
            self.config.next_run = self.config.last_run + timedelta(days=30)
        
        self._save_config()
        
        return {
            'csv_path': csv_path,
            'report_path': report_path,
            'num_conferences': len(results),
            'summary': summary
        }
    
    def get_status(self) -> dict:
        """
        Get scheduler status
        
        Returns:
            Dictionary with scheduler status
        """
        return {
            'enabled': self.config.enabled,
            'frequency': self.config.frequency,
            'last_run': self.config.last_run.isoformat() if self.config.last_run else None,
            'next_run': self.config.next_run.isoformat() if self.config.next_run else None,
            'filters': self.config.filters.model_dump(),
            'email_recipients': self.config.email_recipients
        }
