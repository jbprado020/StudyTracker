"""Main application entry point for Study Tracker."""

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget, QFrame, QHBoxLayout, QLabel
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from datetime import datetime

from config.database import Database
from ui.dashboard_tab import DashboardTab
from ui.sessions_tab import SessionsTab
from utils.styles import Styles


class StudyTracker(QWidget):
    """Main application window for Study Tracker."""

    def __init__(self):
        """Initialize the Study Tracker application."""
        super().__init__()

        # Initialize database
        self.db = Database("study_sessions.db")

        # Window configuration
        self.setWindowIcon(QIcon("assets/book.png"))
        self.setWindowTitle("Pradofy - Study Time and Productivity Tracker")
        self.setGeometry(100, 100, 900, 600)

        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Header
        self._create_header(main_layout)

        # Tabs
        tabs = QTabWidget()
        tabs.setStyleSheet("QTabBar { margin-left: 10px; }")

        # Dashboard tab
        self.dashboard = DashboardTab(self.db)
        tabs.addTab(self.dashboard, "Dashboard")

        # Sessions tab
        self.sessions = SessionsTab(self.db)
        tabs.addTab(self.sessions, "Sessions")

        main_layout.addWidget(tabs)

    def _create_header(self, layout: QVBoxLayout) -> None:
        """Create header section with title and date.
        
        Args:
            layout: Parent layout to add header to
        """
        header_frame = QFrame()
        header_frame.setObjectName("appHeader")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(12, 8, 12, 8)
        header_layout.setSpacing(10)

        # Title section
        title_box = QVBoxLayout()
        title_label = QLabel("Pradofy Study - Study Time & Productivity Tracker")
        title_label.setObjectName("appTitle")
        title_label.setFont(Styles.get_title_font())

        subtitle_label = QLabel("Track sessions • Visualize progress")
        subtitle_label.setStyleSheet("color: #6b7280; font-size: 11px;")

        title_box.addWidget(title_label)
        title_box.addWidget(subtitle_label)
        title_box.setSpacing(0)
        header_layout.addLayout(title_box)

        # Stretch in middle
        header_layout.addStretch()

        # Date section
        date_label = QLabel(datetime.today().strftime("%A, %b %d %Y"))
        date_label.setStyleSheet("color: #6b7280; font-size: 12px;")
        header_layout.addWidget(date_label)

        # Apply styling
        header_frame.setStyleSheet(Styles.HEADER_STYLESHEET)
        header_frame.setGraphicsEffect(Styles.get_shadow_effect())

        layout.addWidget(header_frame)

    def closeEvent(self, event):  # noqa: N802
        """Handle application close event.
        
        Args:
            event: Close event
        """
        self.db.close()
        event.accept()


def main():
    """Main entry point for the application."""
    app = QApplication(sys.argv)
    app.setStyleSheet(Styles.GLOBAL_STYLESHEET)

    window = StudyTracker()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
