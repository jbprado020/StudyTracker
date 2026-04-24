"""Main application entry point for Study Tracker."""

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTabWidget, QFrame, QHBoxLayout,
    QLabel, QCheckBox
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from datetime import datetime

from config.database import Database
from config.settings import Config
from ui.dashboard_tab import DashboardTab
from ui.sessions_tab import SessionsTab
from utils.styles import Styles


class StudyTracker(QWidget):
    """Main application window for Study Tracker."""

    def __init__(self):
        """Initialize the Study Tracker application."""
        super().__init__()

        # Initialize configuration
        self.config = Config()

        # Initialize database
        db_path = self.config.get("database_path", "study_sessions.db")
        self.db = Database(db_path)

        # Window configuration
        self.setWindowIcon(QIcon("assets/book.png"))
        self.setWindowTitle("Pradofy - Study Time and Productivity Tracker")
        self.setGeometry(
            self.config.get("window_x", 100),
            self.config.get("window_y", 100),
            self.config.get("window_width", 900),
            self.config.get("window_height", 600),
        )

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

        self._apply_accessibility_styles()

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

        # Accessibility controls
        self.large_text_checkbox = QCheckBox("Large Text")
        self.large_text_checkbox.setChecked(self.config.get("accessibility.large_text", False))
        self.large_text_checkbox.toggled.connect(self._on_accessibility_changed)
        self.large_text_checkbox.setAccessibleName("Large text toggle")
        self.large_text_checkbox.setAccessibleDescription("Enable larger text across the app")
        header_layout.addWidget(self.large_text_checkbox)

        self.high_contrast_checkbox = QCheckBox("High Contrast")
        self.high_contrast_checkbox.setChecked(self.config.get("accessibility.high_contrast", False))
        self.high_contrast_checkbox.toggled.connect(self._on_accessibility_changed)
        self.high_contrast_checkbox.setAccessibleName("High contrast toggle")
        self.high_contrast_checkbox.setAccessibleDescription("Enable high contrast colors for better readability")
        header_layout.addWidget(self.high_contrast_checkbox)

        # Date section
        date_label = QLabel(datetime.today().strftime("%A, %b %d %Y"))
        date_label.setStyleSheet("color: #6b7280; font-size: 12px;")
        header_layout.addWidget(date_label)

        # Apply styling
        header_frame.setStyleSheet(Styles.HEADER_STYLESHEET)
        header_frame.setGraphicsEffect(Styles.get_shadow_effect())

        layout.addWidget(header_frame)

    def _apply_accessibility_styles(self) -> None:
        """Apply user-selected accessibility styling options."""
        app = QApplication.instance()
        if not app:
            return

        base_font_size = int(self.config.get("accessibility.base_font_size", 13))
        use_large_text = bool(self.config.get("accessibility.large_text", False))
        high_contrast = bool(self.config.get("accessibility.high_contrast", False))

        effective_font_size = base_font_size + 2 if use_large_text else base_font_size
        app.setStyleSheet(Styles.build_global_stylesheet(effective_font_size, high_contrast))

    def _on_accessibility_changed(self) -> None:
        """Persist and apply accessibility toggle changes."""
        self.config.set("accessibility.large_text", self.large_text_checkbox.isChecked())
        self.config.set("accessibility.high_contrast", self.high_contrast_checkbox.isChecked())
        self._apply_accessibility_styles()

    def closeEvent(self, event):  # noqa: N802
        """Handle application close event.
        
        Args:
            event: Close event
        """
        self.db.close()
        geometry = self.geometry()
        self.config.set("window_x", geometry.x())
        self.config.set("window_y", geometry.y())
        self.config.set("window_width", geometry.width())
        self.config.set("window_height", geometry.height())
        event.accept()


def main():
    """Main entry point for the application."""
    app = QApplication(sys.argv)
    app.setStyleSheet(Styles.build_global_stylesheet())

    window = StudyTracker()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
