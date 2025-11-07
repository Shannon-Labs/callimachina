"""
CALLIMACHINA Database Backend
SQLite-based storage for fragment corpus and metadata
Enables scale-up to 400+ works with efficient querying
"""

import sqlite3
import json
import pandas as pd
from pathlib import Path
from typing import List, Dict, Optional, Any
import logging
from datetime import datetime


class FragmentDatabase:
    """SQLite database for managing fragment corpus at scale."""
    
    def __init__(self, db_path: str = "callimachina_corpus.db"):
        """Initialize database connection."""
        self.db_path = Path(db_path)
        self.logger = logging.getLogger(__name__)
        self._init_database()
    
    def _init_database(self):
        """Create database tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            # Fragments table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS fragments (
                    id TEXT PRIMARY KEY,
                    text TEXT NOT NULL,
                    source TEXT,
                    source_author TEXT,
                    confidence REAL,
                    position INTEGER,
                    work_id TEXT,
                    language TEXT DEFAULT 'greek',
                    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT  -- JSON string for additional data
                )
            """)
            
            # Citations table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS citations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fragment_id TEXT,
                    cited_author TEXT,
                    cited_work TEXT,
                    pattern TEXT,
                    confidence REAL,
                    FOREIGN KEY (fragment_id) REFERENCES fragments (id)
                )
            """)
            
            # Works table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS works (
                    work_id TEXT PRIMARY KEY,
                    author TEXT,
                    title TEXT,
                    genre TEXT,
                    century INTEGER,
                    status TEXT DEFAULT 'lost',
                    priority_score REAL,
                    recoverability_score REAL,
                    reconstruction_confidence REAL,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT  -- JSON string
                )
            """)
            
            # Translation chains table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS translation_chains (
                    work_id TEXT PRIMARY KEY,
                    greek_original TEXT,
                    syriac_intermediary TEXT,
                    arabic_translation TEXT,
                    latin_translation TEXT,
                    transmission_score REAL,
                    confidence REAL,
                    FOREIGN KEY (work_id) REFERENCES works (work_id)
                )
            """)
            
            # Create indexes for performance
            conn.execute("CREATE INDEX IF NOT EXISTS idx_fragments_work ON fragments(work_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_fragments_source ON fragments(source)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_citations_fragment ON citations(fragment_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_citations_author ON citations(cited_author)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_works_author ON works(author)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_works_genre ON works(genre)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_works_priority ON works(priority_score DESC)")
            
            conn.commit()
        
        self.logger.info(f"Database initialized at {self.db_path}")
    
    def insert_fragment(self, fragment: Dict[str, Any]) -> bool:
        """Insert a fragment into the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                # Insert fragment
                metadata = fragment.get('metadata', {})
                conn.execute("""
                    INSERT OR REPLACE INTO fragments 
                    (id, text, source, source_author, confidence, position, work_id, language, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    fragment['id'],
                    fragment['text'],
                    fragment.get('source'),
                    fragment.get('source_author'),
                    fragment.get('confidence'),
                    fragment.get('position'),
                    fragment.get('work_id'),
                    fragment.get('language', 'greek'),
                    json.dumps(metadata) if metadata else None
                ))
                
                # Insert citations
                for citation in fragment.get('citations', []):
                    conn.execute("""
                        INSERT INTO citations 
                        (fragment_id, cited_author, cited_work, pattern, confidence)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        fragment['id'],
                        citation.get('cited_author'),
                        citation.get('cited_work'),
                        citation.get('pattern'),
                        citation.get('confidence')
                    ))
                
                conn.commit()
            return True
        except Exception as e:
            self.logger.error(f"Failed to insert fragment {fragment.get('id')}: {e}")
            return False
    
    def insert_work(self, work: Dict[str, Any]) -> bool:
        """Insert or update a work in the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                metadata = work.get('metadata', {})
                conn.execute("""
                    INSERT OR REPLACE INTO works 
                    (work_id, author, title, genre, century, status, priority_score, 
                     recoverability_score, reconstruction_confidence, metadata)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    work['work_id'],
                    work.get('author'),
                    work.get('title'),
                    work.get('genre'),
                    work.get('century'),
                    work.get('status', 'lost'),
                    work.get('priority_score'),
                    work.get('recoverability_score'),
                    work.get('reconstruction_confidence'),
                    json.dumps(metadata) if metadata else None
                ))
                conn.commit()
            return True
        except Exception as e:
            self.logger.error(f"Failed to insert work {work.get('work_id')}: {e}")
            return False
    
    def get_fragments_by_work(self, work_id: str) -> List[Dict[str, Any]]:
        """Get all fragments for a specific work."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM fragments WHERE work_id = ?", (work_id,))
            fragments = []
            for row in cursor.fetchall():
                fragment = dict(row)
                if fragment['metadata']:
                    fragment['metadata'] = json.loads(fragment['metadata'])
                
                # Get citations for this fragment
                cit_cursor = conn.execute(
                    "SELECT cited_author, cited_work, pattern, confidence FROM citations WHERE fragment_id = ?",
                    (fragment['id'],)
                )
                fragment['citations'] = [dict(cit) for cit in cit_cursor.fetchall()]
                fragments.append(fragment)
            return fragments
    
    def get_works_by_priority(self, limit: int = 400) -> pd.DataFrame:
        """Get top N works by priority score."""
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query("""
                SELECT work_id, author, title, genre, century, status, 
                       priority_score, recoverability_score, reconstruction_confidence
                FROM works 
                WHERE status = 'lost' 
                ORDER BY priority_score DESC, recoverability_score DESC
                LIMIT ?
            """, conn, params=(limit,))
            return df
    
    def get_network_data(self) -> pd.DataFrame:
        """Get data for building citation network."""
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query("""
                SELECT f.source_author, c.cited_author, c.cited_work, 
                       c.pattern, c.confidence, f.work_id
                FROM citations c
                JOIN fragments f ON c.fragment_id = f.id
                WHERE c.cited_author IS NOT NULL
            """, conn)
            return df
    
    def update_work_confidence(self, work_id: str, confidence: float) -> bool:
        """Update reconstruction confidence for a work."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    UPDATE works 
                    SET reconstruction_confidence = ?, last_updated = CURRENT_TIMESTAMP
                    WHERE work_id = ?
                """, (confidence, work_id))
                conn.commit()
            return True
        except Exception as e:
            self.logger.error(f"Failed to update confidence for {work_id}: {e}")
            return False
    
    def get_reconstruction_stats(self) -> Dict[str, Any]:
        """Get statistics about the corpus."""
        with sqlite3.connect(self.db_path) as conn:
            stats = {}
            
            # Work counts
            cursor = conn.execute("""
                SELECT status, COUNT(*) as count 
                FROM works 
                GROUP BY status
            """)
            stats['work_counts'] = dict(cursor.fetchall())
            
            # Fragment counts
            cursor = conn.execute("SELECT COUNT(*) FROM fragments")
            stats['total_fragments'] = cursor.fetchone()[0]
            
            # Average confidence
            cursor = conn.execute("""
                SELECT AVG(reconstruction_confidence) 
                FROM works 
                WHERE reconstruction_confidence IS NOT NULL
            """)
            stats['avg_confidence'] = cursor.fetchone()[0]
            
            # Top authors
            cursor = conn.execute("""
                SELECT author, COUNT(*) as work_count
                FROM works
                WHERE author IS NOT NULL
                GROUP BY author
                ORDER BY work_count DESC
                LIMIT 10
            """)
            stats['top_authors'] = dict(cursor.fetchall())
            
            return stats
    
    def bulk_insert_fragments(self, fragments: List[Dict[str, Any]]) -> int:
        """Bulk insert fragments for performance."""
        inserted = 0
        try:
            with sqlite3.connect(self.db_path) as conn:
                for fragment in fragments:
                    try:
                        metadata = fragment.get('metadata', {})
                        conn.execute("""
                            INSERT OR REPLACE INTO fragments 
                            (id, text, source, source_author, confidence, position, work_id, language, metadata)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            fragment['id'],
                            fragment['text'],
                            fragment.get('source'),
                            fragment.get('source_author'),
                            fragment.get('confidence'),
                            fragment.get('position'),
                            fragment.get('work_id'),
                            fragment.get('language', 'greek'),
                            json.dumps(metadata) if metadata else None
                        ))
                        inserted += 1
                    except Exception as e:
                        self.logger.warning(f"Failed to insert fragment {fragment.get('id')}: {e}")
                conn.commit()
        except Exception as e:
            self.logger.error(f"Bulk insert failed: {e}")
        
        return inserted
    
    def export_to_dataframe(self) -> pd.DataFrame:
        """Export all works to DataFrame for analysis."""
        return self.get_works_by_priority(limit=10000)  # Large number to get all


# Global database instance
db = FragmentDatabase()