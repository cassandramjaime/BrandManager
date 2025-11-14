"""
Database manager for Podcast Guest Opportunities
"""
import sqlite3
from datetime import datetime
from typing import List, Optional
from pathlib import Path
from .podcast_models import PodcastOpportunity, ApplicationStatus


class PodcastDatabase:
    """Manages SQLite database for podcast opportunities"""
    
    def __init__(self, db_path: str = "podcast_opportunities.db"):
        """Initialize database connection and create tables if needed"""
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Create database tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS podcast_opportunities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                podcast_name TEXT NOT NULL,
                host_name TEXT,
                host_contact TEXT,
                show_description TEXT,
                typical_guest_profile TEXT,
                audience_size INTEGER,
                submission_link TEXT,
                submission_process TEXT,
                source TEXT,
                source_url TEXT,
                relevance_score REAL DEFAULT 0.0,
                audience_score REAL DEFAULT 0.0,
                engagement_score REAL DEFAULT 0.0,
                total_score REAL DEFAULT 0.0,
                found_date TEXT NOT NULL,
                deadline TEXT,
                application_status TEXT DEFAULT 'not_applied',
                applied_date TEXT,
                notes TEXT,
                fit_reason TEXT
            )
        """)
        
        # Create indexes for common queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_status 
            ON podcast_opportunities(application_status)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_total_score 
            ON podcast_opportunities(total_score)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_found_date 
            ON podcast_opportunities(found_date)
        """)
        
        conn.commit()
        conn.close()
    
    def add_opportunity(self, opportunity: PodcastOpportunity) -> int:
        """Add a new podcast opportunity to the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO podcast_opportunities (
                podcast_name, host_name, host_contact, show_description,
                typical_guest_profile, audience_size, submission_link,
                submission_process, source, source_url, relevance_score,
                audience_score, engagement_score, total_score, found_date,
                deadline, application_status, applied_date, notes, fit_reason
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            opportunity.podcast_name,
            opportunity.host_name,
            opportunity.host_contact,
            opportunity.show_description,
            opportunity.typical_guest_profile,
            opportunity.audience_size,
            opportunity.submission_link,
            opportunity.submission_process,
            opportunity.source,
            opportunity.source_url,
            opportunity.relevance_score,
            opportunity.audience_score,
            opportunity.engagement_score,
            opportunity.total_score,
            opportunity.found_date.isoformat(),
            opportunity.deadline.isoformat() if opportunity.deadline else None,
            opportunity.application_status.value,
            opportunity.applied_date.isoformat() if opportunity.applied_date else None,
            opportunity.notes,
            opportunity.fit_reason
        ))
        
        opportunity_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return opportunity_id
    
    def get_opportunity(self, opportunity_id: int) -> Optional[PodcastOpportunity]:
        """Get a specific opportunity by ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT * FROM podcast_opportunities WHERE id = ?",
            (opportunity_id,)
        )
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_opportunity(row)
        return None
    
    def get_all_opportunities(
        self,
        status: Optional[ApplicationStatus] = None,
        min_score: float = 0.0,
        limit: Optional[int] = None
    ) -> List[PodcastOpportunity]:
        """Get all opportunities with optional filtering"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT * FROM podcast_opportunities WHERE total_score >= ?"
        params = [min_score]
        
        if status:
            query += " AND application_status = ?"
            params.append(status.value)
        
        query += " ORDER BY total_score DESC"
        
        if limit:
            query += " LIMIT ?"
            params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_opportunity(row) for row in rows]
    
    def update_status(
        self,
        opportunity_id: int,
        status: ApplicationStatus,
        notes: Optional[str] = None
    ):
        """Update the application status of an opportunity"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        applied_date = datetime.now().isoformat() if status == ApplicationStatus.APPLIED else None
        
        if notes:
            cursor.execute("""
                UPDATE podcast_opportunities 
                SET application_status = ?, applied_date = ?, notes = ?
                WHERE id = ?
            """, (status.value, applied_date, notes, opportunity_id))
        else:
            cursor.execute("""
                UPDATE podcast_opportunities 
                SET application_status = ?, applied_date = ?
                WHERE id = ?
            """, (status.value, applied_date, opportunity_id))
        
        conn.commit()
        conn.close()
    
    def search_opportunities(
        self,
        search_term: str,
        min_score: float = 0.0
    ) -> List[PodcastOpportunity]:
        """Search opportunities by podcast name or host name"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM podcast_opportunities 
            WHERE (podcast_name LIKE ? OR host_name LIKE ?)
            AND total_score >= ?
            ORDER BY total_score DESC
        """, (f"%{search_term}%", f"%{search_term}%", min_score))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_opportunity(row) for row in rows]
    
    def _row_to_opportunity(self, row: sqlite3.Row) -> PodcastOpportunity:
        """Convert a database row to a PodcastOpportunity object"""
        return PodcastOpportunity(
            id=row['id'],
            podcast_name=row['podcast_name'],
            host_name=row['host_name'],
            host_contact=row['host_contact'],
            show_description=row['show_description'],
            typical_guest_profile=row['typical_guest_profile'],
            audience_size=row['audience_size'],
            submission_link=row['submission_link'],
            submission_process=row['submission_process'],
            source=row['source'],
            source_url=row['source_url'],
            relevance_score=row['relevance_score'],
            audience_score=row['audience_score'],
            engagement_score=row['engagement_score'],
            total_score=row['total_score'],
            found_date=datetime.fromisoformat(row['found_date']),
            deadline=datetime.fromisoformat(row['deadline']) if row['deadline'] else None,
            application_status=ApplicationStatus(row['application_status']),
            applied_date=datetime.fromisoformat(row['applied_date']) if row['applied_date'] else None,
            notes=row['notes'],
            fit_reason=row['fit_reason']
        )
    
    def get_statistics(self) -> dict:
        """Get statistics about opportunities in the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Total count
        cursor.execute("SELECT COUNT(*) FROM podcast_opportunities")
        stats['total'] = cursor.fetchone()[0]
        
        # Count by status
        cursor.execute("""
            SELECT application_status, COUNT(*) 
            FROM podcast_opportunities 
            GROUP BY application_status
        """)
        stats['by_status'] = dict(cursor.fetchall())
        
        # Average scores
        cursor.execute("""
            SELECT AVG(total_score), AVG(relevance_score), AVG(audience_score)
            FROM podcast_opportunities
        """)
        avg_total, avg_relevance, avg_audience = cursor.fetchone()
        stats['avg_total_score'] = avg_total or 0.0
        stats['avg_relevance_score'] = avg_relevance or 0.0
        stats['avg_audience_score'] = avg_audience or 0.0
        
        conn.close()
        return stats
