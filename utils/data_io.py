"""Data import/export utilities for Study Tracker."""

import csv
from datetime import datetime
from pathlib import Path
from typing import List, Dict
from config.database import Database


class DataExporter:
    """Handle data export operations."""

    @staticmethod
    def export_to_csv(db: Database, filename: str = None) -> str:
        """Export all sessions to CSV file.
        
        Args:
            db: Database instance
            filename: Optional custom filename (default: timestamped)
            
        Returns:
            Path to exported file
        """
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"study_sessions_{timestamp}.csv"

        sessions = db.get_all_sessions()
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Subject', 'Start Time', 'End Time', 'Date'])
            
            for session in sessions:
                writer.writerow(session)

        return filename

    @staticmethod
    def export_to_json(db: Database, filename: str = None) -> str:
        """Export all sessions to JSON file.
        
        Args:
            db: Database instance
            filename: Optional custom filename (default: timestamped)
            
        Returns:
            Path to exported file
        """
        import json
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"study_sessions_{timestamp}.json"

        sessions = db.get_all_sessions()
        
        data = {
            "exported_at": datetime.now().isoformat(),
            "total_sessions": len(sessions),
            "sessions": [
                {
                    "id": s[0],
                    "subject": s[1],
                    "start_time": s[2],
                    "end_time": s[3],
                    "date": s[4]
                }
                for s in sessions
            ]
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

        return filename

    @staticmethod
    def export_statistics(db: Database, filename: str = None) -> str:
        """Export statistics report.
        
        Args:
            db: Database instance
            filename: Optional custom filename
            
        Returns:
            Path to exported file
        """
        import json
        from utils.statistics import StudyStatistics
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"study_report_{timestamp}.json"

        stats = StudyStatistics(db)
        subject_breakdown = stats.get_subject_breakdown()
        streak_info = stats.get_streak_info()

        report = {
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_hours": round(stats.get_total_hours(), 2),
                "total_sessions": stats.get_sessions_count(),
                "unique_subjects": stats.get_subjects_count(),
                "average_session_duration": round(stats.get_average_session_duration(), 2),
                "daily_average": round(stats.get_daily_average(), 2),
                "weekly_average": round(stats.get_weekly_average(), 2),
                "today_hours": round(stats.get_today_hours(), 2),
                "today_sessions": stats.get_sessions_today()
            },
            "streaks": streak_info,
            "longest_session": {
                "subject": stats.get_longest_session()[0],
                "hours": round(stats.get_longest_session()[1], 2)
            },
            "subject_breakdown": subject_breakdown
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)

        return filename


class DataImporter:
    """Handle data import operations."""

    @staticmethod
    def import_from_csv(db: Database, filename: str) -> int:
        """Import sessions from CSV file.
        
        Args:
            db: Database instance
            filename: Path to CSV file
            
        Returns:
            Number of sessions imported
        """
        imported_count = 0
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)  # Skip header
                
                for row in reader:
                    if len(row) >= 4:
                        _, subject, start_time, end_time, date = row[:5]
                        if db.add_session(subject.strip(), start_time.strip(), 
                                        end_time.strip(), date.strip()):
                            imported_count += 1
        except Exception as e:
            print(f"Error importing CSV: {e}")
            return 0

        return imported_count

    @staticmethod
    def import_from_json(db: Database, filename: str) -> int:
        """Import sessions from JSON file.
        
        Args:
            db: Database instance
            filename: Path to JSON file
            
        Returns:
            Number of sessions imported
        """
        import json
        
        imported_count = 0
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                if isinstance(data, dict) and "sessions" in data:
                    sessions = data["sessions"]
                else:
                    sessions = data if isinstance(data, list) else []
                
                for session in sessions:
                    if all(k in session for k in ['subject', 'start_time', 'end_time', 'date']):
                        if db.add_session(session['subject'], session['start_time'],
                                        session['end_time'], session['date']):
                            imported_count += 1
        except Exception as e:
            print(f"Error importing JSON: {e}")
            return 0

        return imported_count
