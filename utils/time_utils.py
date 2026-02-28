"""Time utilities for Study Tracker."""

from datetime import datetime


def calculate_duration(start_time: str, end_time: str) -> float:
    """Calculate duration in hours between two times.
    
    Args:
        start_time: Time in format "hh:mm AM/PM"
        end_time: Time in format "hh:mm AM/PM"
        
    Returns:
        Duration in hours as float
        
    Raises:
        ValueError: If time format is invalid
    """
    start_dt = datetime.strptime(start_time, "%I:%M %p")
    end_dt = datetime.strptime(end_time, "%I:%M %p")
    duration = (end_dt - start_dt).seconds / 3600
    return duration


def validate_time_format(time_str: str) -> bool:
    """Validate time format (hh:mm AM/PM).
    
    Args:
        time_str: Time string to validate
        
    Returns:
        bool: True if valid format, False otherwise
    """
    try:
        datetime.strptime(time_str, "%I:%M %p")
        return True
    except ValueError:
        return False


def validate_date_format(date_str: str) -> bool:
    """Validate date format (YYYY-MM-DD).
    
    Args:
        date_str: Date string to validate
        
    Returns:
        bool: True if valid format, False otherwise
    """
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def is_end_after_start(start_time: str, end_time: str) -> bool:
    """Check if end time is after start time.
    
    Args:
        start_time: Start time in format "hh:mm AM/PM"
        end_time: End time in format "hh:mm AM/PM"
        
    Returns:
        bool: True if end time is after start time
    """
    try:
        start_dt = datetime.strptime(start_time, "%I:%M %p")
        end_dt = datetime.strptime(end_time, "%I:%M %p")
        return end_dt > start_dt
    except ValueError:
        return False
