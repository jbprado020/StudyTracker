"""Sessions management tab component for Study Tracker."""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QFormLayout, QLabel, QFrame, QMessageBox, QHeaderView, QSizePolicy,
    QDateEdit, QTimeEdit, QAbstractItemView, QShortcut, QFileDialog,
    QDoubleSpinBox, QCheckBox
)
from PyQt5.QtGui import QIcon, QColor, QKeySequence
from PyQt5.QtCore import Qt, QSize, QDate, QTime
from datetime import datetime
import pandas as pd

from utils.styles import Styles
from utils.time_utils import (
    calculate_duration
)
from config.database import Database
from services.session_service import SessionService


class SessionsTab(QWidget):
    """Sessions management tab for adding, editing, and deleting study sessions."""

    def __init__(self, db: Database):
        """Initialize sessions tab.
        
        Args:
            db: Database instance
        """
        super().__init__()
        self.db = db
        self.session_service = SessionService(db)
        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)
        self.layout.setContentsMargins(8, 6, 8, 8)
        self.setLayout(self.layout)
        self.setAccessibleName("Sessions tab")
        self.setAccessibleDescription("Manage study sessions with add, edit, delete, and export actions")

        # Form section
        self._create_form_section()

        # Buttons section
        self._create_buttons_section()

        # Filter section
        self._create_filter_section()

        # Table section
        self._create_table_section()

        self.load_sessions()

    def _create_form_section(self) -> None:
        """Create form section for inputting session data."""
        form_layout = QFormLayout()
        form_frame = QFrame()
        form_frame.setObjectName("surfaceCard")
        form_frame.setStyleSheet(Styles.FORM_FRAME_STYLESHEET)
        form_frame.setLayout(form_layout)
        self.layout.addWidget(form_frame)

        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setFormAlignment(Qt.AlignHCenter | Qt.AlignTop)
        form_layout.setHorizontalSpacing(20)
        form_layout.setVerticalSpacing(18)
        form_layout.setContentsMargins(30, 20, 30, 20)

        # Subject input
        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("e.g., Math, Programming...")
        self.subject_input.setAccessibleName("Subject")
        self.subject_input.setAccessibleDescription("Enter the study subject name")
        form_layout.addRow("Subject:", self.subject_input)

        # Start time input
        self.start_input = QTimeEdit()
        self.start_input.setDisplayFormat("hh:mm AP")
        self.start_input.setTime(QTime.currentTime())
        self.start_input.setAccessibleName("Start Time")
        self.start_input.setAccessibleDescription("Select the session start time")
        form_layout.addRow("Start Time:", self.start_input)

        # End time input
        self.end_input = QTimeEdit()
        self.end_input.setDisplayFormat("hh:mm AP")
        self.end_input.setTime(QTime.currentTime().addSecs(3600))
        self.end_input.setAccessibleName("End Time")
        self.end_input.setAccessibleDescription("Select the session end time")
        form_layout.addRow("End Time:", self.end_input)

        # Date input
        self.date_input = QDateEdit()
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        self.date_input.setAccessibleName("Date")
        self.date_input.setAccessibleDescription("Select the study date")
        form_layout.addRow("Date:", self.date_input)

        # Apply label styling
        for i in range(form_layout.rowCount()):
            label_item = form_layout.itemAt(i, QFormLayout.LabelRole)
            if label_item and label_item.widget():
                label_item.widget().setStyleSheet(Styles.FORM_LABEL_STYLESHEET)

        # Set field minimum size
        for field in [self.subject_input, self.start_input, self.end_input, self.date_input]:
            field.setMinimumHeight(36)
            field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            field.setMinimumWidth(220)

    def _create_buttons_section(self) -> None:
        """Create buttons section for CRUD operations."""
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        buttons_layout.setContentsMargins(20, 10, 20, 10)
        buttons_layout.setAlignment(Qt.AlignCenter)

        # Add button
        self.add_button = QPushButton("Add Session")
        self.add_button.setText("&Save Session")
        self.add_button.setIcon(QIcon("assets/add-time.png"))
        self.add_button.setIconSize(QSize(22, 22))
        self.add_button.setMinimumHeight(45)
        self.add_button.clicked.connect(self.save_session)
        self.add_button.setAccessibleName("Save Session")
        self.add_button.setAccessibleDescription("Save a new study session")

        # Edit button
        self.edit_button = QPushButton("&Edit Session")
        self.edit_button.setIcon(QIcon("assets/pen.png"))
        self.edit_button.setIconSize(QSize(22, 22))
        self.edit_button.setMinimumHeight(45)
        self.edit_button.clicked.connect(self.edit_session)
        self.edit_button.setAccessibleName("Edit Session")
        self.edit_button.setAccessibleDescription("Update the selected study session")

        # Delete button
        self.delete_button = QPushButton("&Delete Session")
        self.delete_button.setIcon(QIcon("assets/delete.png"))
        self.delete_button.setIconSize(QSize(22, 22))
        self.delete_button.setMinimumHeight(45)
        self.delete_button.clicked.connect(self.delete_session)
        self.delete_button.setAccessibleName("Delete Session")
        self.delete_button.setAccessibleDescription("Delete the selected study session")

        # Export button
        self.export_button = QPushButton("E&xport Sessions")
        self.export_button.setIcon(QIcon("assets/share.png"))
        self.export_button.setIconSize(QSize(22, 22))
        self.export_button.setMinimumHeight(45)
        self.export_button.clicked.connect(self.export_sessions)
        self.export_button.setAccessibleName("Export Sessions")
        self.export_button.setAccessibleDescription("Export all study sessions to a CSV file")

        # Configure buttons
        for btn in [self.add_button, self.edit_button, self.delete_button, self.export_button]:
            btn.setMinimumWidth(120)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setCursor(Qt.PointingHandCursor)
            buttons_layout.addWidget(btn)

        buttons_container = QFrame()
        buttons_container.setObjectName("surfaceCard")
        buttons_container.setLayout(buttons_layout)
        buttons_container.setStyleSheet(Styles.BUTTONS_CONTAINER_STYLESHEET)
        self.layout.addSpacing(10)
        self.layout.addWidget(buttons_container)

        self._create_shortcuts()

    def _create_shortcuts(self) -> None:
        """Register keyboard shortcuts for faster keyboard-only workflows."""
        QShortcut(QKeySequence("Ctrl+S"), self, self.save_session)
        QShortcut(QKeySequence("Ctrl+E"), self, self.export_sessions)
        QShortcut(QKeySequence("Delete"), self, self.delete_session)
        QShortcut(QKeySequence("Ctrl+F"), self, lambda: self.search_input.setFocus())

    def _create_filter_section(self) -> None:
        """Create sessions filtering controls."""
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(10)
        filter_layout.setContentsMargins(15, 8, 15, 8)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search subject...")
        self.search_input.setMinimumHeight(34)
        self.search_input.setAccessibleName("Subject search")
        self.search_input.setAccessibleDescription("Filter sessions by subject")
        filter_layout.addWidget(QLabel("Search:"))
        filter_layout.addWidget(self.search_input)

        self.use_date_filter = QCheckBox("Use Date Range")
        self.use_date_filter.setChecked(False)
        self.use_date_filter.setAccessibleName("Date range filter toggle")
        self.use_date_filter.setAccessibleDescription("Enable or disable date range filtering")
        filter_layout.addWidget(self.use_date_filter)

        self.filter_start_date = QDateEdit()
        self.filter_start_date.setDisplayFormat("yyyy-MM-dd")
        self.filter_start_date.setDate(QDate.currentDate().addMonths(-1))
        self.filter_start_date.setCalendarPopup(True)
        self.filter_start_date.setMinimumHeight(34)
        filter_layout.addWidget(QLabel("From:"))
        filter_layout.addWidget(self.filter_start_date)

        self.filter_end_date = QDateEdit()
        self.filter_end_date.setDisplayFormat("yyyy-MM-dd")
        self.filter_end_date.setDate(QDate.currentDate())
        self.filter_end_date.setCalendarPopup(True)
        self.filter_end_date.setMinimumHeight(34)
        filter_layout.addWidget(QLabel("To:"))
        filter_layout.addWidget(self.filter_end_date)

        self.min_duration_input = QDoubleSpinBox()
        self.min_duration_input.setRange(0.0, 24.0)
        self.min_duration_input.setSingleStep(0.25)
        self.min_duration_input.setDecimals(2)
        self.min_duration_input.setSuffix(" h")
        self.min_duration_input.setMinimumHeight(34)
        self.min_duration_input.setAccessibleName("Minimum duration")
        self.min_duration_input.setAccessibleDescription("Filter sessions by minimum duration in hours")
        filter_layout.addWidget(QLabel("Min Duration:"))
        filter_layout.addWidget(self.min_duration_input)

        self.apply_filter_button = QPushButton("Apply Filters")
        self.apply_filter_button.clicked.connect(self.apply_filters)
        filter_layout.addWidget(self.apply_filter_button)

        self.clear_filter_button = QPushButton("Clear Filters")
        self.clear_filter_button.clicked.connect(self.clear_filters)
        filter_layout.addWidget(self.clear_filter_button)

        filter_frame = QFrame()
        filter_frame.setObjectName("surfaceCard")
        filter_frame.setStyleSheet(Styles.FORM_FRAME_STYLESHEET)
        filter_frame.setLayout(filter_layout)
        self.layout.addWidget(filter_frame)

    def _create_table_section(self) -> None:
        """Create table section for displaying sessions."""
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Subject", "Start Time", "End Time", "Date"])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setStyleSheet(Styles.TABLE_STYLESHEET)
        self.table.cellClicked.connect(self.fill_inputs_from_table)
        self.table.setAccessibleName("Sessions table")
        self.table.setAccessibleDescription("Shows all saved study sessions")
        self.layout.addWidget(self.table)

    def save_session(self) -> None:
        """Save a new study session."""
        subject = self.subject_input.text().strip()
        start = self.start_input.time().toString("hh:mm AP")
        end = self.end_input.time().toString("hh:mm AP")
        date = self.date_input.date().toString("yyyy-MM-dd")

        validation_error = self.session_service.validate_session_input(
            self.session_service.normalize_subject(subject),
            start,
            end,
            date,
        )
        if validation_error:
            QMessageBox.warning(self, "Error", validation_error)
            return

        # Confirmation
        clean_subject = self.session_service.normalize_subject(subject)
        duration = calculate_duration(start, end)
        reply = QMessageBox.question(
            self,
            "Confirm Save",
            f"Save session for '{clean_subject}'?\n({duration:.2f} hours)\n\nDate: {date}",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            result = self.session_service.create_session(subject, start, end, date)
            if result.ok:
                QMessageBox.information(self, "Success", f"Session '{clean_subject}' saved!")
                self.apply_filters()
                self.clear_inputs()
            else:
                QMessageBox.critical(self, "Error", result.message)

    def edit_session(self) -> None:
        """Edit selected study session."""
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Error", "Select a session to edit first.")
            return

        session_id = int(self.table.item(selected, 0).text())
        old_subject = self.table.item(selected, 1).text()
        old_start = self.table.item(selected, 2).text()
        old_end = self.table.item(selected, 3).text()
        old_date = self.table.item(selected, 4).text()

        # Get new values or use old ones
        subject = self.subject_input.text().strip() or old_subject
        subject = self.session_service.normalize_subject(subject)
        start = self.start_input.time().toString("hh:mm AP") or old_start
        end = self.end_input.time().toString("hh:mm AP") or old_end
        date = self.date_input.date().toString("yyyy-MM-dd") or old_date

        # Check if changes were made
        if (subject, start, end, date) == (old_subject, old_start, old_end, old_date):
            QMessageBox.information(self, "No Changes", "No changes detected.")
            return

        validation_error = self.session_service.validate_session_input(subject, start, end, date)
        if validation_error:
            QMessageBox.warning(self, "Error", validation_error)
            return

        # Confirmation
        reply = QMessageBox.question(
            self,
            "Confirm Edit",
            f"Update session?\n\n📘 Subject: {old_subject} → {subject}\n"
            f"🕒 Time: {old_start} - {old_end} → {start} - {end}\n"
            f"📅 Date: {old_date} → {date}",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            result = self.session_service.update_session(session_id, subject, start, end, date)
            if result.ok:
                QMessageBox.information(self, "Success", f"Session updated!")
                self.apply_filters()
                # Highlight updated row
                for i in range(self.table.columnCount()):
                    self.table.item(selected, i).setBackground(QColor("#dbeafe"))
                self.clear_inputs()
            else:
                QMessageBox.critical(self, "Error", result.message)

    def delete_session(self) -> None:
        """Delete selected study session."""
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Error", "Select a session to delete.")
            return

        session_id = int(self.table.item(selected, 0).text())
        subject = self.table.item(selected, 1).text()

        reply = QMessageBox.warning(
            self,
            "Confirm Delete",
            f"Delete session for '{subject}' (ID {session_id})?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            if self.db.delete_session(session_id):
                QMessageBox.information(self, "Success", "Session deleted.")
                self.apply_filters()
            else:
                QMessageBox.critical(self, "Error", "Failed to delete session.")

    def export_sessions(self) -> None:
        """Export all sessions to CSV file."""
        rows = self.db.get_all_sessions()
        if not rows:
            QMessageBox.information(self, "No Data", "No sessions available to export.")
            return

        df = pd.DataFrame(rows, columns=["ID", "Subject", "Start Time", "End Time", "Date"])
        default_name = f"study_sessions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Sessions",
            default_name,
            "CSV Files (*.csv);;All Files (*)"
        )

        if not filename:
            return

        try:
            df.to_csv(filename, index=False)
            QMessageBox.information(self, "Success", f"Sessions exported to '{filename}'.")
        except Exception as exc:
            QMessageBox.critical(self, "Export Failed", f"Could not export sessions.\n\nDetails: {exc}")

    def load_sessions(self, rows=None) -> None:
        """Load session rows into table.

        Args:
            rows: Optional pre-filtered rows. If None, loads all sessions.
        """
        if rows is None:
            rows = self.db.get_all_sessions()

        self.table.setRowCount(len(rows))

        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))

    def apply_filters(self) -> None:
        """Apply active filters and refresh the table."""
        subject_query = self.search_input.text().strip()
        min_duration = float(self.min_duration_input.value())

        start_date = None
        end_date = None
        if self.use_date_filter.isChecked():
            start_date = self.filter_start_date.date().toString("yyyy-MM-dd")
            end_date = self.filter_end_date.date().toString("yyyy-MM-dd")

        rows = self.session_service.get_filtered_sessions(
            subject_query=subject_query,
            start_date=start_date,
            end_date=end_date,
            min_duration_hours=min_duration,
        )
        self.load_sessions(rows)

    def clear_filters(self) -> None:
        """Reset filters and load all sessions."""
        self.search_input.clear()
        self.use_date_filter.setChecked(False)
        self.filter_start_date.setDate(QDate.currentDate().addMonths(-1))
        self.filter_end_date.setDate(QDate.currentDate())
        self.min_duration_input.setValue(0.0)
        self.load_sessions()

    def clear_inputs(self) -> None:
        """Clear all input fields."""
        self.subject_input.clear()
        self.start_input.setTime(QTime.currentTime())
        self.end_input.setTime(QTime.currentTime().addSecs(3600))
        self.date_input.setDate(QDate.currentDate())

    def fill_inputs_from_table(self) -> None:
        """Fill input fields from selected table row."""
        selected = self.table.currentRow()
        if selected < 0:
            return

        self.subject_input.setText(self.table.item(selected, 1).text())
        start_time = QTime.fromString(self.table.item(selected, 2).text(), "hh:mm AP")
        if start_time.isValid():
            self.start_input.setTime(start_time)

        end_time = QTime.fromString(self.table.item(selected, 3).text(), "hh:mm AP")
        if end_time.isValid():
            self.end_input.setTime(end_time)

        date_value = QDate.fromString(self.table.item(selected, 4).text(), "yyyy-MM-dd")
        if date_value.isValid():
            self.date_input.setDate(date_value)
