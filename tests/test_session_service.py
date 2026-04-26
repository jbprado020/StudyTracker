"""Unit tests for session service business rules."""

import unittest
from datetime import date, timedelta

from config.database import Database
from services.session_service import SessionService


class SessionServiceTests(unittest.TestCase):
    """Validate SessionService behavior and invariants."""

    def setUp(self):
        """Create an isolated in-memory database for each test."""
        self.db = Database(":memory:")
        self.service = SessionService(self.db)

    def tearDown(self):
        """Close database connection after each test."""
        self.db.close()

    def test_normalize_subject_collapses_spaces(self):
        """Subject normalization should remove duplicate spaces."""
        normalized = self.service.normalize_subject("  Data   Structures  ")
        self.assertEqual(normalized, "Data Structures")

    def test_validate_rejects_future_date(self):
        """Future study dates are not valid."""
        future_date = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")

        result = self.service.create_session("Math", "09:00 AM", "10:00 AM", future_date)

        self.assertFalse(result.ok)
        self.assertIn("future", result.message.lower())

    def test_validate_rejects_end_before_start(self):
        """End time must be strictly after start time."""
        today = date.today().strftime("%Y-%m-%d")

        result = self.service.create_session("Science", "03:00 PM", "01:00 PM", today)

        self.assertFalse(result.ok)
        self.assertIn("after start", result.message.lower())

    def test_create_session_saves_normalized_subject(self):
        """Successful creation should persist cleaned subject text."""
        today = date.today().strftime("%Y-%m-%d")

        result = self.service.create_session("  Web   Development ", "01:00 PM", "02:30 PM", today)

        self.assertTrue(result.ok)
        rows = self.db.get_all_sessions()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][1], "Web Development")

    def test_update_missing_session_returns_error(self):
        """Updating a non-existent session should return a clear error."""
        today = date.today().strftime("%Y-%m-%d")

        result = self.service.update_session(999, "Math", "10:00 AM", "11:00 AM", today)

        self.assertFalse(result.ok)
        self.assertIn("not found", result.message.lower())

    def test_get_filtered_sessions_by_subject_query(self):
        """Filtering by subject should return only matching sessions."""
        today = date.today().strftime("%Y-%m-%d")
        self.db.add_session("Mathematics", "09:00 AM", "10:00 AM", today)
        self.db.add_session("Science", "10:00 AM", "11:00 AM", today)

        rows = self.service.get_filtered_sessions(subject_query="math")

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][1], "Mathematics")

    def test_get_filtered_sessions_by_min_duration(self):
        """Minimum duration filter should drop shorter sessions."""
        today = date.today().strftime("%Y-%m-%d")
        self.db.add_session("Quick Review", "09:00 AM", "09:30 AM", today)
        self.db.add_session("Deep Work", "10:00 AM", "12:00 PM", today)

        rows = self.service.get_filtered_sessions(min_duration_hours=1.0)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0][1], "Deep Work")


if __name__ == "__main__":
    unittest.main()
