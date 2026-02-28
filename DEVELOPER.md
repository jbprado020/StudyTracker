# Developer Guide

## Architecture Overview

Pradofy Study Tracker follows a modular architecture with clean separation of concerns:

### Layers

1. **Database Layer** (`config/database.py`)
   - Handles all SQLite operations
   - Provides CRUD methods for sessions
   - Manages database connections

2. **UI Layer** (`ui/`)
   - `dashboard_tab.py` - Statistics and charts visualization
   - `sessions_tab.py` - Session management and CRUD operations
   - Built with PyQt5 components

3. **Utilities** (`utils/`)
   - `styles.py` - Centralized styling and theming
   - `time_utils.py` - Time validation and calculations
   - `statistics.py` - Statistical analysis and reporting
   - `data_io.py` - Import/export functionality

4. **Configuration** (`config/`)
   - `settings.py` - Application settings management
   - `database.py` - Database operations

## Key Design Patterns

### Dependency Injection
Database instance is passed to UI components, reducing coupling:
```python
dashboard = DashboardTab(db)
sessions = SessionsTab(db)
```

### Centralized Styling
All CSS-like styles are in `utils/styles.py` for easy theming:
```python
frame.setStyleSheet(Styles.CHART_FRAME_STYLESHEET)
frame.setGraphicsEffect(Styles.get_chart_shadow_effect())
```

### Utility Functions
Reusable functions for common operations:
- `time_utils.py` - Time parsing and validation
- `statistics.py` - Statistical calculations
- `data_io.py` - Import/export operations

## Adding New Features

### Add a New Tab
1. Create new file in `ui/` (e.g., `goals_tab.py`)
2. Inherit from `QWidget`
3. Accept `db` parameter in constructor
4. Add to tabs in `main.py`:
```python
goals_tab = GoalsTab(self.db)
tabs.addTab(goals_tab, "Goals")
```

### Add Database Features
1. Add method to `Database` class in `config/database.py`
2. Follow the pattern of existing CRUD methods
3. Use parameterized queries for security

### Add Statistics
1. Add method to `StudyStatistics` class in `utils/statistics.py`
2. Use existing database methods
3. Return dict or tuple as needed

### Update Styling
1. Add new style string to `Styles` class in `utils/styles.py`
2. Use in UI components:
```python
frame.setStyleSheet(Styles.YOUR_NEW_STYLESHEET)
```

## Testing

Run individual components:
```python
# Test database
from config.database import Database
db = Database("test.db")
db.add_session("Math", "02:00 PM", "03:30 PM", "2024-01-15")
```

## Performance Considerations

- Lazy load charts only on dashboard tab visibility
- Batch database queries when possible
- Use indexing for frequently queried columns
- Cache statistics results if needed

## Code Style

- Follow PEP 8
- Use type hints for function parameters and returns
- Add docstrings to all public methods
- Use descriptive variable names

Example:
```python
def calculate_duration(start_time: str, end_time: str) -> float:
    """Calculate duration in hours between two times.
    
    Args:
        start_time: Time in format "hh:mm AM/PM"
        end_time: Time in format "hh:mm AM/PM"
        
    Returns:
        Duration in hours as float
    """
```

## Dependencies Management

Keep `requirements.txt` updated when adding new packages:
```bash
pip freeze > requirements.txt
```

Optional: Use `pipreqs` for automatic detection:
```bash
pipreqs --force
```
