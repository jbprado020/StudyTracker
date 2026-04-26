# Pradofy Study Tracker 📚

[![Python Tests](https://github.com/jbprado020/StudyTracker/actions/workflows/tests.yml/badge.svg)](https://github.com/jbprado020/StudyTracker/actions/workflows/tests.yml)

A modern, feature-rich desktop application for tracking study sessions and visualizing productivity metrics. Built with PyQt5 and powered by data analysis libraries.

## Features ✨

### Dashboard
- **Quick Stats Cards**: View total study hours, subjects studied today, and your top subject at a glance
- **Daily Study Hours Chart**: Interactive bar chart showing study hours per day
- **Subject Distribution Pie Chart**: Visualize how study time is distributed across subjects
- **Weekly Trend Line Chart**: Track your study patterns over the last 7 days with a line chart

### Session Management
- **Add Sessions**: Record new study sessions with subject, start time, end time, and date
- **Edit Sessions**: Modify existing sessions with validation
- **Delete Sessions**: Remove sessions with confirmation
- **Session Display**: View all sessions in an organized table format
- **Quick Fill**: Click on a session in the table to auto-fill the input fields
- **Export to CSV**: Export all sessions to a timestamped CSV file for further analysis

### User Interface
- Modern, responsive design with gradient backgrounds
- Smooth animations and hover effects
- Real-time validation and helpful error messages
- Professional styling with Segoe UI font
- Tab-based interface for easy navigation

## Installation 🚀

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone or download the project**
```bash
cd StudyTracker
```

2. **Create a virtual environment** (optional but recommended)
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Run the Application

```bash
python main.py
```

The application window will open, and you can start tracking your study sessions!

## Project Structure 📁

```
StudyTracker/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── study_sessions.db       # SQLite database (auto-created)
│
├── config/
│   ├── __init__.py
│   └── database.py         # Database operations and models
│
├── ui/
│   ├── __init__.py
│   ├── dashboard_tab.py    # Dashboard widget and charts
│   └── sessions_tab.py     # Session management widget
│
└── utils/
    ├── __init__.py
    ├── styles.py           # Centralized styling system
    └── time_utils.py       # Time validation and calculations
```

## Usage Guide 📖

### Adding a Session

1. Navigate to the **Sessions** tab
2. Fill in the required fields:
   - **Subject**: What you studied (e.g., "Math", "Python Programming")
   - **Start Time**: When you started (format: `hh:mm AM/PM`, e.g., `02:30 PM`)
   - **End Time**: When you finished (format: `hh:mm AM/PM`)
   - **Date**: The study date (format: `YYYY-MM-DD`)
3. Click **Add Session**
4. Confirm the session in the popup dialog

### Editing a Session

1. Click on a session in the table to auto-fill the input fields
2. Modify any fields as needed
3. Click **Edit Session**
4. Confirm the changes in the dialog
5. The updated row will be highlighted in light blue

### Deleting a Session

1. Click on a session in the table to select it
2. Click **Delete Session**
3. Confirm deletionin the warning dialog

### Exporting Sessions

1. Click **Export Sessions** to save all your data
2. A CSV file will be created with timestamp: `study_sessions_YYYYMMDD_HHMMSS.csv`
3. Open with Excel, Google Sheets, or any spreadsheet application

### Viewing Statistics

- **Dashboard Tab**: See all your study metrics at a glance
  - Total hours studied across all sessions
  - Number of subjects studied today
  - Your most-studied subject
  - Visual charts showing daily, subject, and weekly trends

## Data Validation ✅

All inputs are validated to ensure data integrity:

- **Subject**: Must not be empty (max 255 characters recommended)
- **Time Format**: Must be `hh:mm AM/PM` (e.g., `02:30 PM`, `09:15 AM`)
- **Date Format**: Must be `YYYY-MM-DD` (e.g., `2024-01-15`)
- **Time Logic**: End time must be after start time
- **Date Logic**: Date must be valid and in the past or today

## Database 🗄️

The application uses **SQLite** for persistent data storage:

- `study_sessions.db` - Automatically created on first run
- Stores: Subject, Start Time, End Time, Date, and Creation Timestamp
- No need for external database setup

## Dependencies 📦

| Package | Version | Purpose |
|---------|---------|---------|
| PyQt5 | 5.15.9 | GUI framework |
| matplotlib | 3.8.0 | Chart rendering |
| seaborn | 0.13.0 | Statistical visualizations |
| pandas | 2.1.3 | Data analysis and manipulation |
| numpy | 1.24.3 | Numerical computations |

## Keyboard Shortcuts ⌨️

- `Tab` - Move to next field in form
- `Shift+Tab` - Move to previous field
- `Click table row` - Auto-fill form with session data

## Tips & Tricks 💡

1. **Time Format**: Use 12-hour format with AM/PM (e.g., `2:30 PM`, not `14:30`)
2. **Consistent Subjects**: Use the same subject name for accurate statistics
3. **Regular Exports**: Export your data regularly as a backup
4. **Review Charts**: Check the Dashboard weekly to identify study patterns
5. **Set Goals**: Track your top subject and try to balance study time

## Troubleshooting 🔧

### "add-time.png not found" Error
- Ensure icon PNG files are in the same directory as `main.py`
- Required icons: `add-time.png`, `pen.png`, `delete.png`, `share.png`, `book.png`

### Charts not displaying
- Ensure matplotlib and seaborn are properly installed
- Try: `pip install --upgrade matplotlib seaborn`

### Database is locked
- Close other instances of the application
- Delete `study_sessions.db` to start fresh (will lose all data)

### Time validation fails
- Check format: Must be `hh:mm AM/PM` with proper spacing
- Examples: ✅ `02:30 PM`, ❌ `2:30pm`, ❌ `14:30`

## Future Enhancements 🚀

- [ ] Goal setting and tracking
- [ ] Weekly/Monthly study plans
- [ ] Subject-specific notifications
- [ ] Data import from CSV
- [ ] Dark mode theme
- [ ] Cloud synchronization
- [ ] Mobile app companion
- [ ] Advanced filtering and search

## License 📄

This project is open source and available under the MIT License.

## Contributing 🤝

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Improve documentation
- Submit pull requests

## Contact & Support 💬

For questions or support, please reach out or open an issue in the repository.

---

**Happy studying! 📚🎓**
