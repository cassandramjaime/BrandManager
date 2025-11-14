"""
SQLite database manager for research papers with full-text search
"""
import sqlite3
import json
from datetime import datetime
from typing import List, Optional, Dict
from contextlib import contextmanager
from pathlib import Path

from .paper_models import Paper, PaperSummary, PaperFilter, SearchQuery


class PaperDatabase:
    """SQLite database for storing and searching research papers"""
    
    def __init__(self, db_path: str = "papers.db"):
        """
        Initialize the paper database
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self._initialize_database()
    
    @contextmanager
    def _get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def _initialize_database(self):
        """Create database tables if they don't exist"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Papers table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS papers (
                    paper_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    authors TEXT NOT NULL,
                    abstract TEXT NOT NULL,
                    publication_date TEXT NOT NULL,
                    source TEXT NOT NULL,
                    url TEXT NOT NULL,
                    pdf_url TEXT,
                    citation_count INTEGER DEFAULT 0,
                    categories TEXT,
                    key_findings TEXT,
                    methodology TEXT,
                    practical_applications TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Paper summaries table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS paper_summaries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    paper_id TEXT NOT NULL,
                    concise_summary TEXT NOT NULL,
                    main_contribution TEXT NOT NULL,
                    methodology_summary TEXT NOT NULL,
                    results_summary TEXT NOT NULL,
                    relevance_to_product TEXT NOT NULL,
                    application_area TEXT NOT NULL,
                    technical_difficulty TEXT NOT NULL,
                    production_readiness TEXT NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (paper_id) REFERENCES papers(paper_id)
                )
            """)
            
            # Full-text search virtual table
            cursor.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS papers_fts USING fts5(
                    paper_id,
                    title,
                    authors,
                    abstract,
                    key_findings,
                    content=papers,
                    content_rowid=rowid
                )
            """)
            
            # Triggers to keep FTS table in sync
            cursor.execute("""
                CREATE TRIGGER IF NOT EXISTS papers_ai AFTER INSERT ON papers BEGIN
                    INSERT INTO papers_fts(rowid, paper_id, title, authors, abstract, key_findings)
                    VALUES (new.rowid, new.paper_id, new.title, new.authors, new.abstract, new.key_findings);
                END
            """)
            
            cursor.execute("""
                CREATE TRIGGER IF NOT EXISTS papers_ad AFTER DELETE ON papers BEGIN
                    INSERT INTO papers_fts(papers_fts, rowid, paper_id, title, authors, abstract, key_findings)
                    VALUES('delete', old.rowid, old.paper_id, old.title, old.authors, old.abstract, old.key_findings);
                END
            """)
            
            cursor.execute("""
                CREATE TRIGGER IF NOT EXISTS papers_au AFTER UPDATE ON papers BEGIN
                    INSERT INTO papers_fts(papers_fts, rowid, paper_id, title, authors, abstract, key_findings)
                    VALUES('delete', old.rowid, old.paper_id, old.title, old.authors, old.abstract, old.key_findings);
                    INSERT INTO papers_fts(rowid, paper_id, title, authors, abstract, key_findings)
                    VALUES (new.rowid, new.paper_id, new.title, new.authors, new.abstract, new.key_findings);
                END
            """)
            
            # Create indices for better query performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_papers_publication_date 
                ON papers(publication_date DESC)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_papers_source 
                ON papers(source)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_papers_citation_count 
                ON papers(citation_count DESC)
            """)
    
    def save_paper(self, paper: Paper) -> bool:
        """
        Save a paper to the database
        
        Args:
            paper: Paper object to save
            
        Returns:
            True if saved successfully, False if already exists
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO papers (
                        paper_id, title, authors, abstract, publication_date,
                        source, url, pdf_url, citation_count, categories,
                        key_findings, methodology, practical_applications
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    paper.paper_id,
                    paper.title,
                    json.dumps(paper.authors),
                    paper.abstract,
                    paper.publication_date.isoformat(),
                    paper.source.value,
                    paper.url,
                    paper.pdf_url,
                    paper.citation_count,
                    json.dumps(paper.categories),
                    paper.key_findings,
                    paper.methodology,
                    paper.practical_applications
                ))
                return True
        except sqlite3.IntegrityError:
            return False
    
    def save_summary(self, summary: PaperSummary) -> bool:
        """
        Save a paper summary to the database
        
        Args:
            summary: PaperSummary object to save
            
        Returns:
            True if saved successfully
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO paper_summaries (
                    paper_id, concise_summary, main_contribution,
                    methodology_summary, results_summary, relevance_to_product,
                    application_area, technical_difficulty, production_readiness
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                summary.paper_id,
                summary.concise_summary,
                summary.main_contribution,
                summary.methodology_summary,
                summary.results_summary,
                summary.relevance_to_product,
                summary.application_area.value,
                summary.technical_difficulty.value,
                summary.production_readiness.value
            ))
            return True
    
    def get_paper(self, paper_id: str) -> Optional[Paper]:
        """
        Get a paper by ID
        
        Args:
            paper_id: Unique paper identifier
            
        Returns:
            Paper object or None if not found
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM papers WHERE paper_id = ?", (paper_id,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_paper(row)
            return None
    
    def get_summary(self, paper_id: str) -> Optional[PaperSummary]:
        """
        Get the latest summary for a paper
        
        Args:
            paper_id: Unique paper identifier
            
        Returns:
            PaperSummary object or None if not found
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM paper_summaries 
                WHERE paper_id = ? 
                ORDER BY created_at DESC 
                LIMIT 1
            """, (paper_id,))
            row = cursor.fetchone()
            
            if row:
                return self._row_to_summary(row)
            return None
    
    def search_papers(self, query: SearchQuery) -> List[Paper]:
        """
        Search papers using full-text search
        
        Args:
            query: SearchQuery object
            
        Returns:
            List of matching Paper objects
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Build the query
            if query.query:
                # Full-text search
                sql = """
                    SELECT p.* FROM papers p
                    INNER JOIN papers_fts fts ON p.rowid = fts.rowid
                    WHERE papers_fts MATCH ?
                """
                params = [query.query]
            else:
                # Simple filter query
                sql = "SELECT * FROM papers WHERE 1=1"
                params = []
            
            # Add filters if present
            if query.filters:
                if query.filters.days_back:
                    sql += " AND publication_date >= datetime('now', '-' || ? || ' days')"
                    params.append(query.filters.days_back)
                
                if query.filters.min_citations:
                    sql += " AND citation_count >= ?"
                    params.append(query.filters.min_citations)
                
                if query.filters.sources:
                    placeholders = ','.join('?' * len(query.filters.sources))
                    sql += f" AND source IN ({placeholders})"
                    params.extend([s.value for s in query.filters.sources])
            
            # Add ordering and pagination
            sql += " ORDER BY publication_date DESC LIMIT ? OFFSET ?"
            params.extend([query.limit, query.offset])
            
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            
            return [self._row_to_paper(row) for row in rows]
    
    def get_recent_papers(self, days: int = 30, limit: int = 100) -> List[Paper]:
        """
        Get recent papers from the last N days
        
        Args:
            days: Number of days to look back
            limit: Maximum number of papers to return
            
        Returns:
            List of Paper objects
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM papers 
                WHERE publication_date >= datetime('now', '-' || ? || ' days')
                ORDER BY publication_date DESC
                LIMIT ?
            """, (days, limit))
            rows = cursor.fetchall()
            
            return [self._row_to_paper(row) for row in rows]
    
    def get_top_papers(self, days: int = 7, limit: int = 10) -> List[Paper]:
        """
        Get top papers by citation count from the last N days
        
        Args:
            days: Number of days to look back
            limit: Maximum number of papers to return
            
        Returns:
            List of Paper objects sorted by citation count
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM papers 
                WHERE publication_date >= datetime('now', '-' || ? || ' days')
                ORDER BY citation_count DESC, publication_date DESC
                LIMIT ?
            """, (days, limit))
            rows = cursor.fetchall()
            
            return [self._row_to_paper(row) for row in rows]
    
    def _row_to_paper(self, row: sqlite3.Row) -> Paper:
        """Convert a database row to a Paper object"""
        return Paper(
            paper_id=row['paper_id'],
            title=row['title'],
            authors=json.loads(row['authors']),
            abstract=row['abstract'],
            publication_date=datetime.fromisoformat(row['publication_date']),
            source=row['source'],
            url=row['url'],
            pdf_url=row['pdf_url'],
            citation_count=row['citation_count'],
            categories=json.loads(row['categories']) if row['categories'] else [],
            key_findings=row['key_findings'],
            methodology=row['methodology'],
            practical_applications=row['practical_applications']
        )
    
    def _row_to_summary(self, row: sqlite3.Row) -> PaperSummary:
        """Convert a database row to a PaperSummary object"""
        return PaperSummary(
            paper_id=row['paper_id'],
            concise_summary=row['concise_summary'],
            main_contribution=row['main_contribution'],
            methodology_summary=row['methodology_summary'],
            results_summary=row['results_summary'],
            relevance_to_product=row['relevance_to_product'],
            application_area=row['application_area'],
            technical_difficulty=row['technical_difficulty'],
            production_readiness=row['production_readiness']
        )
    
    def get_stats(self) -> Dict:
        """
        Get database statistics
        
        Returns:
            Dictionary with database stats
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) as count FROM papers")
            total_papers = cursor.fetchone()['count']
            
            cursor.execute("SELECT COUNT(*) as count FROM paper_summaries")
            total_summaries = cursor.fetchone()['count']
            
            cursor.execute("""
                SELECT source, COUNT(*) as count 
                FROM papers 
                GROUP BY source
            """)
            papers_by_source = {row['source']: row['count'] for row in cursor.fetchall()}
            
            return {
                'total_papers': total_papers,
                'total_summaries': total_summaries,
                'papers_by_source': papers_by_source
            }
