"""
Database handler for conference tracking using SQLite
"""
import sqlite3
import json
from typing import List, Optional
from datetime import datetime
from pathlib import Path

from .conference_models import Conference, ConferenceSearchFilters, LocationType, TopicFocus


class ConferenceDatabase:
    """SQLite database handler for conferences"""
    
    def __init__(self, db_path: str = "conferences.db"):
        """
        Initialize database connection
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        self._connect()
        self._create_tables()
    
    def _connect(self):
        """Create database connection"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
    
    def _create_tables(self):
        """Create database tables if they don't exist"""
        cursor = self.conn.cursor()
        
        # Main conferences table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                location TEXT NOT NULL,
                location_type TEXT NOT NULL,
                ticket_price_min REAL,
                ticket_price_max REAL,
                notable_speakers TEXT,
                agenda_topics TEXT,
                registration_deadline TEXT,
                url TEXT NOT NULL UNIQUE,
                source TEXT NOT NULL,
                description TEXT,
                topic_focus TEXT,
                relevance_score REAL DEFAULT 0.0,
                speaker_quality_score REAL DEFAULT 0.0,
                networking_score REAL DEFAULT 0.0,
                overall_score REAL DEFAULT 0.0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        
        # Index for faster searches
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_start_date ON conferences(start_date)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_location_type ON conferences(location_type)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_overall_score ON conferences(overall_score)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_url ON conferences(url)
        """)
        
        self.conn.commit()
    
    def add_conference(self, conference: Conference) -> int:
        """
        Add a conference to the database
        
        Args:
            conference: Conference object to add
            
        Returns:
            Conference ID
        """
        cursor = self.conn.cursor()
        
        # Convert lists to JSON strings
        notable_speakers = json.dumps(conference.notable_speakers)
        agenda_topics = json.dumps(conference.agenda_topics)
        topic_focus = json.dumps([t.value for t in conference.topic_focus])
        
        try:
            cursor.execute("""
                INSERT INTO conferences (
                    name, start_date, end_date, location, location_type,
                    ticket_price_min, ticket_price_max, notable_speakers,
                    agenda_topics, registration_deadline, url, source,
                    description, topic_focus, relevance_score,
                    speaker_quality_score, networking_score, overall_score,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                conference.name,
                conference.start_date.isoformat(),
                conference.end_date.isoformat(),
                conference.location,
                conference.location_type.value,
                conference.ticket_price_min,
                conference.ticket_price_max,
                notable_speakers,
                agenda_topics,
                conference.registration_deadline.isoformat() if conference.registration_deadline else None,
                conference.url,
                conference.source,
                conference.description,
                topic_focus,
                conference.relevance_score,
                conference.speaker_quality_score,
                conference.networking_score,
                conference.overall_score,
                conference.created_at.isoformat(),
                conference.updated_at.isoformat()
            ))
            
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            # Conference URL already exists, update instead
            return self.update_conference_by_url(conference)
    
    def update_conference_by_url(self, conference: Conference) -> int:
        """
        Update an existing conference by URL
        
        Args:
            conference: Conference object with updated data
            
        Returns:
            Conference ID
        """
        cursor = self.conn.cursor()
        
        # Convert lists to JSON strings
        notable_speakers = json.dumps(conference.notable_speakers)
        agenda_topics = json.dumps(conference.agenda_topics)
        topic_focus = json.dumps([t.value for t in conference.topic_focus])
        
        cursor.execute("""
            UPDATE conferences SET
                name = ?, start_date = ?, end_date = ?, location = ?,
                location_type = ?, ticket_price_min = ?, ticket_price_max = ?,
                notable_speakers = ?, agenda_topics = ?, registration_deadline = ?,
                source = ?, description = ?, topic_focus = ?,
                relevance_score = ?, speaker_quality_score = ?,
                networking_score = ?, overall_score = ?, updated_at = ?
            WHERE url = ?
        """, (
            conference.name,
            conference.start_date.isoformat(),
            conference.end_date.isoformat(),
            conference.location,
            conference.location_type.value,
            conference.ticket_price_min,
            conference.ticket_price_max,
            notable_speakers,
            agenda_topics,
            conference.registration_deadline.isoformat() if conference.registration_deadline else None,
            conference.source,
            conference.description,
            topic_focus,
            conference.relevance_score,
            conference.speaker_quality_score,
            conference.networking_score,
            conference.overall_score,
            datetime.utcnow().isoformat(),
            conference.url
        ))
        
        self.conn.commit()
        
        # Get the conference ID
        cursor.execute("SELECT id FROM conferences WHERE url = ?", (conference.url,))
        row = cursor.fetchone()
        return row[0] if row else 0
    
    def search_conferences(self, filters: Optional[ConferenceSearchFilters] = None) -> List[Conference]:
        """
        Search conferences based on filters
        
        Args:
            filters: Search filters
            
        Returns:
            List of matching conferences
        """
        cursor = self.conn.cursor()
        
        query = "SELECT * FROM conferences WHERE 1=1"
        params = []
        
        if filters:
            if filters.start_date_from:
                query += " AND start_date >= ?"
                params.append(filters.start_date_from.isoformat())
            
            if filters.start_date_to:
                query += " AND start_date <= ?"
                params.append(filters.start_date_to.isoformat())
            
            if filters.location_type:
                query += " AND location_type = ?"
                params.append(filters.location_type.value)
            
            if filters.min_score is not None:
                query += " AND overall_score >= ?"
                params.append(filters.min_score)
            
            if filters.max_price is not None:
                query += " AND (ticket_price_min <= ? OR ticket_price_min IS NULL)"
                params.append(filters.max_price)
            
            if filters.location_keywords:
                location_conditions = " OR ".join(["location LIKE ?" for _ in filters.location_keywords])
                query += f" AND ({location_conditions})"
                params.extend([f"%{keyword}%" for keyword in filters.location_keywords])
        
        # Order by score and date
        query += " ORDER BY overall_score DESC, start_date ASC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        conferences = []
        for row in rows:
            conference = self._row_to_conference(row)
            
            # Filter by topic focus if specified
            if filters and filters.topic_focus:
                if any(topic in conference.topic_focus for topic in filters.topic_focus):
                    conferences.append(conference)
            else:
                conferences.append(conference)
        
        return conferences
    
    def get_conference_by_id(self, conference_id: int) -> Optional[Conference]:
        """
        Get a conference by ID
        
        Args:
            conference_id: Conference ID
            
        Returns:
            Conference object or None
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM conferences WHERE id = ?", (conference_id,))
        row = cursor.fetchone()
        
        if row:
            return self._row_to_conference(row)
        return None
    
    def get_all_conferences(self) -> List[Conference]:
        """
        Get all conferences
        
        Returns:
            List of all conferences
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM conferences ORDER BY start_date DESC")
        rows = cursor.fetchall()
        
        return [self._row_to_conference(row) for row in rows]
    
    def delete_conference(self, conference_id: int) -> bool:
        """
        Delete a conference
        
        Args:
            conference_id: Conference ID to delete
            
        Returns:
            True if deleted, False otherwise
        """
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM conferences WHERE id = ?", (conference_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def _row_to_conference(self, row: sqlite3.Row) -> Conference:
        """Convert database row to Conference object"""
        return Conference(
            id=row['id'],
            name=row['name'],
            start_date=datetime.fromisoformat(row['start_date']),
            end_date=datetime.fromisoformat(row['end_date']),
            location=row['location'],
            location_type=LocationType(row['location_type']),
            ticket_price_min=row['ticket_price_min'],
            ticket_price_max=row['ticket_price_max'],
            notable_speakers=json.loads(row['notable_speakers']) if row['notable_speakers'] else [],
            agenda_topics=json.loads(row['agenda_topics']) if row['agenda_topics'] else [],
            registration_deadline=datetime.fromisoformat(row['registration_deadline']) if row['registration_deadline'] else None,
            url=row['url'],
            source=row['source'],
            description=row['description'],
            topic_focus=[TopicFocus(t) for t in json.loads(row['topic_focus'])] if row['topic_focus'] else [],
            relevance_score=row['relevance_score'],
            speaker_quality_score=row['speaker_quality_score'],
            networking_score=row['networking_score'],
            overall_score=row['overall_score'],
            created_at=datetime.fromisoformat(row['created_at']),
            updated_at=datetime.fromisoformat(row['updated_at'])
        )
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
