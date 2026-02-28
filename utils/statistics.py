"""Statistics and analytics for Study Tracker."""

from typing import Dict, List, Tuple
from datetime import datetime, timedelta
from config.database import Database
from utils.time_utils import calculate_duration


class StudyStatistics:
    """Calculate and provide study statistics."""

    def __init__(self, db: Database):
        """Initialize statistics calculator.
        
        Args:
            db: Database instance
        """
        self.db = db

    def get_total_hours(self) -> float:
        """Get total study hours.
        
        Returns:
            Total hours as float
        """
        return self.db.get_total_hours()

    def get_average_session_duration(self) -> float:
        """Get average session duration in hours.
        
        Returns:
            Average session duration
        """
        sessions = self.db.get_all_sessions()
        if not sessions:
            return 0.0

        total_hours = 0
        for _, _, start, end, _ in sessions:
            try:
                total_hours += calculate_duration(start, end)
            except Exception:
                pass

        return total_hours / len(sessions)

    def get_longest_session(self) -> Tuple[str, float]:
        """Get the longest study session.
        
        Returns:
            Tuple of (subject_name, duration_hours)
        """
        sessions = self.db.get_all_sessions()
        if not sessions:
            return ("None", 0.0)

        longest = ("", 0.0)
        for _, subject, start, end, _ in sessions:
            try:
                duration = calculate_duration(start, end)
                if duration > longest[1]:
                    longest = (subject, duration)
            except Exception:
                pass

        return longest if longest[0] else ("None", 0.0)

    def get_subjects_count(self) -> int:
        """Get number of unique subjects studied.
        
        Returns:
            Count of unique subjects
        """
        subject_hours = self.db.get_subject_hours()
        return len(subject_hours)

    def get_daily_average(self) -> float:
        """Get average study hours per day.
        
        Returns:
            Average hours per day
        """
        daily_hours = self.db.get_daily_hours()
        if not daily_hours:
            return 0.0

        return sum(daily_hours.values()) / len(daily_hours)

    def get_sessions_count(self) -> int:
        """Get total number of sessions.
        
        Returns:
            Total session count
        """
        return len(self.db.get_all_sessions())

    def get_sessions_today(self) -> int:
        """Get number of sessions today.
        
        Returns:
            Session count for today
        """
        today = datetime.today().strftime("%Y-%m-%d")
        return len(self.db.get_sessions_by_date(today))

    def get_today_hours(self) -> float:
        """Get total study hours today.
        
        Returns:
            Total hours today
        """
        today = datetime.today().strftime("%Y-%m-%d")
        sessions = self.db.get_sessions_by_date(today)

        total = 0.0
        for _, _, start, end, _ in sessions:
            try:
                total += calculate_duration(start, end)
            except Exception:
                pass

        return total

    def get_weekly_average(self) -> float:
        """Get average study hours per day in the last 7 days.
        
        Returns:
            Average hours per day in last week
        """
        daily_hours = self.db.get_daily_hours()
        if not daily_hours:
            return 0.0

        # Filter to last 7 days
        today = datetime.today()
        week_ago = today - timedelta(days=7)

        week_hours = {}
        for date_str, hours in daily_hours.items():
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d")
                if date >= week_ago:
                    week_hours[date_str] = hours
            except Exception:
                pass

        if not week_hours:
            return 0.0

        return sum(week_hours.values()) / len(week_hours)

    def get_subject_breakdown(self) -> Dict[str, Dict]:
        """Get detailed breakdown per subject.
        
        Returns:
            Dictionary with subject statistics
        """
        subject_hours = self.db.get_subject_hours()
        sessions = self.db.get_all_sessions()
        
        subject_stats: Dict[str, Dict] = {}
        
        for subject, hours in subject_hours.items():
            # Count sessions for this subject
            subject_sessions = [s for s in sessions if s[1] == subject]
            avg_duration = hours / len(subject_sessions) if subject_sessions else 0
            
            subject_stats[subject] = {
                "total_hours": round(hours, 2),
                "sessions_count": len(subject_sessions),
                "average_duration": round(avg_duration, 2),
                "percentage": round((hours / sum(subject_hours.values()) * 100), 1) if subject_hours else 0
            }
        
        return subject_stats

    def get_streak_info(self) -> Dict:
        """Get current study streak information.
        
        Returns:
            Dictionary with streak information
        """
        daily_hours = self.db.get_daily_hours()
        if not daily_hours:
            return {"current_streak": 0, "longest_streak": 0}

        # Sort dates
        dates = sorted(daily_hours.keys())
        current_streak = 0
        longest_streak = 0
        temp_streak = 0

        today = datetime.today().strftime("%Y-%m-%d")
        yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")

        for i, date in enumerate(dates):
            # Check if consecutive
            is_consecutive = False
            if i == 0:
                is_consecutive = True
            else:
                current_date = datetime.strptime(date, "%Y-%m-%d")
                prev_date = datetime.strptime(dates[i-1], "%Y-%m-%d")
                is_consecutive = (current_date - prev_date).days == 1

            if is_consecutive:
                temp_streak += 1
            else:
                if temp_streak > longest_streak:
                    longest_streak = temp_streak
                temp_streak = 1

            # Check if current streak includes today
            if date == today or date == yesterday:
                current_streak = temp_streak

        if temp_streak > longest_streak:
            longest_streak = temp_streak

        return {
            "current_streak": current_streak,
            "longest_streak": longest_streak
        }
