"""
Database manager for journalist opportunities
"""
import sqlite3
import json
from typing import List, Optional, Dict
from datetime import datetime
from pathlib import Path
from .journalist_models import (
    JournalistOpportunity, 
    PublicationTier, 
    Urgency, 
    OpportunitySource,
    OpportunityFilter,
    UserProfile
)


class OpportunityDatabase:
    """Database manager for journalist opportunities"""
    
    def __init__(self, db_path: str = "opportunities.db"):
        """
        Initialize database connection
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create opportunities table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS opportunities (
                id TEXT PRIMARY KEY,
                publication_name TEXT NOT NULL,
                journalist_name TEXT,
                topic TEXT NOT NULL,
                deadline TIMESTAMP,
                requirements TEXT NOT NULL,
                contact_method TEXT NOT NULL,
                tier TEXT NOT NULL,
                urgency TEXT NOT NULL,
                source TEXT NOT NULL,
                relevance_score REAL DEFAULT 0.0,
                keywords TEXT,
                found_at TIMESTAMP NOT NULL,
                pitch_sent INTEGER DEFAULT 0,
                pitch_sent_at TIMESTAMP,
                response_received INTEGER DEFAULT 0,
                response_received_at TIMESTAMP,
                notes TEXT DEFAULT ''
            )
        """)
        
        # Create user profile table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_profile (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                title TEXT NOT NULL,
                expertise_areas TEXT,
                experience_years INTEGER,
                company TEXT,
                bio TEXT,
                achievements TEXT,
                contact_info TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create pitch history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pitch_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                opportunity_id TEXT NOT NULL,
                pitch_text TEXT NOT NULL,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                response_text TEXT,
                response_at TIMESTAMP,
                FOREIGN KEY (opportunity_id) REFERENCES opportunities(id)
            )
        """)
        
        # Create indexes for better query performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_opportunities_tier 
            ON opportunities(tier)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_opportunities_urgency 
            ON opportunities(urgency)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_opportunities_source 
            ON opportunities(source)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_opportunities_relevance 
            ON opportunities(relevance_score)
        """)
        
        conn.commit()
        conn.close()
    
    def add_opportunity(self, opportunity: JournalistOpportunity) -> str:
        """
        Add a new opportunity to the database
        
        Args:
            opportunity: JournalistOpportunity object
            
        Returns:
            ID of the added opportunity
        """
        if not opportunity.id:
            # Generate ID based on publication, topic, and timestamp
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            safe_pub = "".join(c for c in opportunity.publication_name if c.isalnum())[:20]
            opportunity.id = f"{safe_pub}_{timestamp}"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO opportunities (
                id, publication_name, journalist_name, topic, deadline,
                requirements, contact_method, tier, urgency, source,
                relevance_score, keywords, found_at, pitch_sent,
                pitch_sent_at, response_received, response_received_at, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            opportunity.id,
            opportunity.publication_name,
            opportunity.journalist_name,
            opportunity.topic,
            opportunity.deadline,
            opportunity.requirements,
            opportunity.contact_method,
            opportunity.tier.value,
            opportunity.urgency.value,
            opportunity.source.value,
            opportunity.relevance_score,
            json.dumps(opportunity.keywords),
            opportunity.found_at,
            1 if opportunity.pitch_sent else 0,
            opportunity.pitch_sent_at,
            1 if opportunity.response_received else 0,
            opportunity.response_received_at,
            opportunity.notes
        ))
        
        conn.commit()
        conn.close()
        
        return opportunity.id
    
    def get_opportunity(self, opportunity_id: str) -> Optional[JournalistOpportunity]:
        """
        Get an opportunity by ID
        
        Args:
            opportunity_id: Opportunity ID
            
        Returns:
            JournalistOpportunity object or None if not found
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM opportunities WHERE id = ?
        """, (opportunity_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return self._row_to_opportunity(row)
    
    def list_opportunities(self, filter_params: Optional[OpportunityFilter] = None) -> List[JournalistOpportunity]:
        """
        List opportunities with optional filtering
        
        Args:
            filter_params: Optional filter parameters
            
        Returns:
            List of JournalistOpportunity objects
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT * FROM opportunities WHERE 1=1"
        params = []
        
        if filter_params:
            if filter_params.min_relevance_score > 0:
                query += " AND relevance_score >= ?"
                params.append(filter_params.min_relevance_score)
            
            if filter_params.tiers:
                tier_placeholders = ",".join("?" * len(filter_params.tiers))
                query += f" AND tier IN ({tier_placeholders})"
                params.extend([t.value for t in filter_params.tiers])
            
            if filter_params.urgency_levels:
                urgency_placeholders = ",".join("?" * len(filter_params.urgency_levels))
                query += f" AND urgency IN ({urgency_placeholders})"
                params.extend([u.value for u in filter_params.urgency_levels])
            
            if filter_params.sources:
                source_placeholders = ",".join("?" * len(filter_params.sources))
                query += f" AND source IN ({source_placeholders})"
                params.extend([s.value for s in filter_params.sources])
            
            if filter_params.only_not_pitched:
                query += " AND pitch_sent = 0"
        
        query += " ORDER BY relevance_score DESC, found_at DESC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        opportunities = [self._row_to_opportunity(row) for row in rows]
        
        # Apply keyword filtering in Python (since keywords are JSON)
        if filter_params and filter_params.keywords:
            opportunities = [
                opp for opp in opportunities
                if any(kw.lower() in " ".join(opp.keywords).lower() for kw in filter_params.keywords)
            ]
        
        return opportunities
    
    def update_opportunity(self, opportunity: JournalistOpportunity):
        """
        Update an existing opportunity
        
        Args:
            opportunity: JournalistOpportunity object with updated data
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE opportunities SET
                publication_name = ?,
                journalist_name = ?,
                topic = ?,
                deadline = ?,
                requirements = ?,
                contact_method = ?,
                tier = ?,
                urgency = ?,
                source = ?,
                relevance_score = ?,
                keywords = ?,
                pitch_sent = ?,
                pitch_sent_at = ?,
                response_received = ?,
                response_received_at = ?,
                notes = ?
            WHERE id = ?
        """, (
            opportunity.publication_name,
            opportunity.journalist_name,
            opportunity.topic,
            opportunity.deadline,
            opportunity.requirements,
            opportunity.contact_method,
            opportunity.tier.value,
            opportunity.urgency.value,
            opportunity.source.value,
            opportunity.relevance_score,
            json.dumps(opportunity.keywords),
            1 if opportunity.pitch_sent else 0,
            opportunity.pitch_sent_at,
            1 if opportunity.response_received else 0,
            opportunity.response_received_at,
            opportunity.notes,
            opportunity.id
        ))
        
        conn.commit()
        conn.close()
    
    def mark_pitch_sent(self, opportunity_id: str, pitch_text: str):
        """
        Mark an opportunity as pitched
        
        Args:
            opportunity_id: Opportunity ID
            pitch_text: The pitch that was sent
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now()
        
        # Update opportunity
        cursor.execute("""
            UPDATE opportunities SET
                pitch_sent = 1,
                pitch_sent_at = ?
            WHERE id = ?
        """, (now, opportunity_id))
        
        # Add to pitch history
        cursor.execute("""
            INSERT INTO pitch_history (opportunity_id, pitch_text, sent_at)
            VALUES (?, ?, ?)
        """, (opportunity_id, pitch_text, now))
        
        conn.commit()
        conn.close()
    
    def mark_response_received(self, opportunity_id: str, response_text: str = ""):
        """
        Mark that a response was received for an opportunity
        
        Args:
            opportunity_id: Opportunity ID
            response_text: Optional response text
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now()
        
        # Update opportunity
        cursor.execute("""
            UPDATE opportunities SET
                response_received = 1,
                response_received_at = ?
            WHERE id = ?
        """, (now, opportunity_id))
        
        # Update pitch history if response text provided
        if response_text:
            cursor.execute("""
                UPDATE pitch_history SET
                    response_text = ?,
                    response_at = ?
                WHERE opportunity_id = ?
                ORDER BY sent_at DESC
                LIMIT 1
            """, (response_text, now, opportunity_id))
        
        conn.commit()
        conn.close()
    
    def get_statistics(self) -> Dict:
        """
        Get statistics about opportunities
        
        Returns:
            Dictionary with statistics
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Total opportunities
        cursor.execute("SELECT COUNT(*) FROM opportunities")
        stats['total_opportunities'] = cursor.fetchone()[0]
        
        # Opportunities by tier
        cursor.execute("""
            SELECT tier, COUNT(*) as count
            FROM opportunities
            GROUP BY tier
        """)
        stats['by_tier'] = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Opportunities by urgency
        cursor.execute("""
            SELECT urgency, COUNT(*) as count
            FROM opportunities
            GROUP BY urgency
        """)
        stats['by_urgency'] = {row[0]: row[1] for row in cursor.fetchall()}
        
        # Pitch statistics
        cursor.execute("SELECT COUNT(*) FROM opportunities WHERE pitch_sent = 1")
        stats['pitches_sent'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM opportunities WHERE response_received = 1")
        stats['responses_received'] = cursor.fetchone()[0]
        
        # Response rate
        if stats['pitches_sent'] > 0:
            stats['response_rate'] = (stats['responses_received'] / stats['pitches_sent']) * 100
        else:
            stats['response_rate'] = 0.0
        
        conn.close()
        
        return stats
    
    def save_user_profile(self, profile: UserProfile):
        """
        Save or update user profile
        
        Args:
            profile: UserProfile object
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if profile exists
        cursor.execute("SELECT COUNT(*) FROM user_profile")
        count = cursor.fetchone()[0]
        
        if count > 0:
            # Update existing
            cursor.execute("""
                UPDATE user_profile SET
                    name = ?,
                    title = ?,
                    expertise_areas = ?,
                    experience_years = ?,
                    company = ?,
                    bio = ?,
                    achievements = ?,
                    contact_info = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = (SELECT MIN(id) FROM user_profile)
            """, (
                profile.name,
                profile.title,
                json.dumps(profile.expertise_areas),
                profile.experience_years,
                profile.company,
                profile.bio,
                json.dumps(profile.achievements),
                json.dumps(profile.contact_info)
            ))
        else:
            # Insert new
            cursor.execute("""
                INSERT INTO user_profile (
                    name, title, expertise_areas, experience_years,
                    company, bio, achievements, contact_info
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                profile.name,
                profile.title,
                json.dumps(profile.expertise_areas),
                profile.experience_years,
                profile.company,
                profile.bio,
                json.dumps(profile.achievements),
                json.dumps(profile.contact_info)
            ))
        
        conn.commit()
        conn.close()
    
    def get_user_profile(self) -> Optional[UserProfile]:
        """
        Get the user profile
        
        Returns:
            UserProfile object or None if not set
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM user_profile ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return UserProfile(
            name=row['name'],
            title=row['title'],
            expertise_areas=json.loads(row['expertise_areas']) if row['expertise_areas'] else [],
            experience_years=row['experience_years'],
            company=row['company'],
            bio=row['bio'],
            achievements=json.loads(row['achievements']) if row['achievements'] else [],
            contact_info=json.loads(row['contact_info']) if row['contact_info'] else {}
        )
    
    def _row_to_opportunity(self, row: sqlite3.Row) -> JournalistOpportunity:
        """Convert database row to JournalistOpportunity object"""
        return JournalistOpportunity(
            id=row['id'],
            publication_name=row['publication_name'],
            journalist_name=row['journalist_name'],
            topic=row['topic'],
            deadline=datetime.fromisoformat(row['deadline']) if row['deadline'] else None,
            requirements=row['requirements'],
            contact_method=row['contact_method'],
            tier=PublicationTier(row['tier']),
            urgency=Urgency(row['urgency']),
            source=OpportunitySource(row['source']),
            relevance_score=row['relevance_score'],
            keywords=json.loads(row['keywords']) if row['keywords'] else [],
            found_at=datetime.fromisoformat(row['found_at']),
            pitch_sent=bool(row['pitch_sent']),
            pitch_sent_at=datetime.fromisoformat(row['pitch_sent_at']) if row['pitch_sent_at'] else None,
            response_received=bool(row['response_received']),
            response_received_at=datetime.fromisoformat(row['response_received_at']) if row['response_received_at'] else None,
            notes=row['notes']
        )
