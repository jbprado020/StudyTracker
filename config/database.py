"""Database configuration and operations for Study Tracker."""

import sqlite3
from typing import List, Dict, Tuple, Optional

from utils.logger import get_logger


logger = get_logger(__name__)


class Database:
    """Handles all database operations for study sessions."""

    def __init__(self, db_path: str = "study_sessions.db"):
        """Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self) -> None:
        """Create sessions table if it doesn't exist."""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                date TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_date ON sessions(date)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sessions_subject ON sessions(subject)")
        self.conn.commit()

    def add_session(self, subject: str, start_time: str, end_time: str, date: str) -> bool:
        """Add a new study session.
        
        Args:
            subject: Subject being studied
            start_time: Start time in format "hh:mm AM/PM"
            end_time: End time in format "hh:mm AM/PM"
            date: Date in format "YYYY-MM-DD"
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO sessions (subject, start_time, end_time, date) VALUES (?, ?, ?, ?)",
                (subject, start_time, end_time, date),
            )
            self.conn.commit()
            return True
        except Exception as e:
            logger.exception("Error adding session")
            return False

    def get_all_sessions(self) -> List[Tuple]:
        """Get all study sessions.
        
        Returns:
            List of tuples containing session data
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, subject, start_time, end_time, date FROM sessions ORDER BY date DESC")
        return cursor.fetchall()

    def query_sessions(
        self,
        subject_query: str = "",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List[Tuple]:
        """Query sessions by optional subject and date filters.

        Args:
            subject_query: Optional subject text search
            start_date: Optional lower bound date (YYYY-MM-DD)
            end_date: Optional upper bound date (YYYY-MM-DD)

        Returns:
            Filtered list of sessions
        """
        query = "SELECT id, subject, start_time, end_time, date FROM sessions WHERE 1=1"
        params = []

        if subject_query:
            query += " AND LOWER(subject) LIKE ?"
            params.append(f"%{subject_query.lower()}%")

        if start_date:
            query += " AND date >= ?"
            params.append(start_date)

        if end_date:
            query += " AND date <= ?"
            params.append(end_date)

        query += " ORDER BY date DESC, id DESC"

        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()

    def update_session(self, session_id: int, subject: str, start_time: str, 
                      end_time: str, date: str) -> bool:
        """Update an existing session.
        
        Args:
            session_id: ID of session to update
            subject: Updated subject
            start_time: Updated start time
            end_time: Updated end time
            date: Updated date
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE sessions SET subject=?, start_time=?, end_time=?, date=? WHERE id=?",
                (subject, start_time, end_time, date, session_id),
            )
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            logger.exception("Error updating session")
            return False

    def delete_session(self, session_id: int) -> bool:
        """Delete a session.
        
        Args:
            session_id: ID of session to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM sessions WHERE id=?", (session_id,))
            self.conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            logger.exception("Error deleting session")
            return False

    def get_sessions_by_date(self, date: str) -> List[Tuple]:
        """Get sessions for a specific date.
        
        Args:
            date: Date in format "YYYY-MM-DD"
            
        Returns:
            List of tuples containing session data for that date
        """
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, subject, start_time, end_time, date FROM sessions WHERE date=? ORDER BY start_time",
            (date,),
        )
        return cursor.fetchall()

    def get_subject_hours(self) -> Dict[str, float]:
        """Calculate total hours per subject.
        
        Returns:
            Dictionary mapping subjects to total hours
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT subject, start_time, end_time FROM sessions")
        rows = cursor.fetchall()

        subject_hours = {}
        for subject, start, end in rows:
            try:
                from utils.time_utils import calculate_duration
                hours = calculate_duration(start, end)
                subject_hours[subject] = subject_hours.get(subject, 0) + hours
            except Exception:
                pass

        return subject_hours

    def get_daily_hours(self) -> Dict[str, float]:
        """Calculate total hours per day.
        
        Returns:
            Dictionary mapping dates to total hours
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT date, start_time, end_time FROM sessions")
        rows = cursor.fetchall()

        daily_hours = {}
        for date, start, end in rows:
            try:
                from utils.time_utils import calculate_duration
                hours = calculate_duration(start, end)
                daily_hours[date] = daily_hours.get(date, 0) + hours
            except Exception:
                pass

        return daily_hours

    def get_total_hours(self) -> float:
        """Calculate total study hours across all sessions.
        
        Returns:
            Total hours as float
        """
        return sum(self.get_daily_hours().values())

    def close(self) -> None:
        """Close database connection."""
        self.conn.close()
