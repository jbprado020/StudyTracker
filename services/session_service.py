"""Business logic service for creating and updating study sessions."""

from dataclasses import dataclass
from typing import Optional, List, Tuple

from config.database import Database
from utils.time_utils import (
    validate_time_format,
    validate_date_format,
    validate_study_date,
    is_end_after_start,
    calculate_duration,
)


@dataclass
class ServiceResult:
    """Standard service operation response."""

    ok: bool
    message: str


class SessionService:
    """Encapsulates study session validation and persistence rules."""

    def __init__(self, db: Database):
        """Initialize service with a database dependency.

        Args:
            db: Database instance
        """
        self.db = db

    @staticmethod
    def normalize_subject(subject: str) -> str:
        """Normalize subject input to prevent duplicated variants.

        Args:
            subject: Raw subject text

        Returns:
            Cleaned subject
        """
        return " ".join(subject.split())

    def validate_session_input(self, subject: str, start: str, end: str, date: str) -> Optional[str]:
        """Validate session fields and return an error message when invalid.

        Args:
            subject: Subject name
            start: Start time in hh:mm AM/PM
            end: End time in hh:mm AM/PM
            date: Date in YYYY-MM-DD

        Returns:
            Error message if invalid, otherwise None
        """
        if not subject or not start or not end or not date:
            return "Please fill in all fields."

        if not validate_time_format(start):
            return "Start time format invalid. Use: hh:mm AM/PM"

        if not validate_time_format(end):
            return "End time format invalid. Use: hh:mm AM/PM"

        if not validate_date_format(date):
            return "Date format invalid. Use: YYYY-MM-DD"

        if not validate_study_date(date):
            return "Date cannot be in the future."

        if not is_end_after_start(start, end):
            return "End time must be after start time."

        return None

    def create_session(self, subject: str, start: str, end: str, date: str) -> ServiceResult:
        """Validate and persist a new session.

        Args:
            subject: Subject name
            start: Start time
            end: End time
            date: Session date

        Returns:
            ServiceResult describing operation outcome
        """
        subject = self.normalize_subject(subject)
        error = self.validate_session_input(subject, start, end, date)
        if error:
            return ServiceResult(False, error)

        if not self.db.add_session(subject, start, end, date):
            return ServiceResult(False, "Failed to save session.")

        return ServiceResult(True, "Session saved successfully.")

    def update_session(
        self,
        session_id: int,
        subject: str,
        start: str,
        end: str,
        date: str,
    ) -> ServiceResult:
        """Validate and persist session updates.

        Args:
            session_id: Session ID to update
            subject: Updated subject
            start: Updated start time
            end: Updated end time
            date: Updated date

        Returns:
            ServiceResult describing operation outcome
        """
        subject = self.normalize_subject(subject)
        error = self.validate_session_input(subject, start, end, date)
        if error:
            return ServiceResult(False, error)

        if not self.db.update_session(session_id, subject, start, end, date):
            return ServiceResult(False, "Session not found or update failed.")

        return ServiceResult(True, "Session updated successfully.")

    def get_filtered_sessions(
        self,
        subject_query: str = "",
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        min_duration_hours: float = 0.0,
    ) -> List[Tuple]:
        """Return sessions filtered by search criteria.

        Args:
            subject_query: Optional subject search query
            start_date: Optional date lower bound
            end_date: Optional date upper bound
            min_duration_hours: Optional minimum session duration filter

        Returns:
            Filtered session rows
        """
        rows = self.db.query_sessions(subject_query, start_date, end_date)
        if min_duration_hours <= 0:
            return rows

        filtered_rows = []
        for row in rows:
            try:
                duration = calculate_duration(row[2], row[3])
                if duration >= min_duration_hours:
                    filtered_rows.append(row)
            except ValueError:
                continue

        return filtered_rows
