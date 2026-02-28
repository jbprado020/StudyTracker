"""Sessions management tab component for Study Tracker."""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTableWidget,
    QTableWidgetItem, QFormLayout, QLabel, QFrame, QMessageBox, QHeaderView, QSizePolicy
)
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import Qt, QSize
from datetime import datetime
import pandas as pd

from utils.styles import Styles
from utils.time_utils import (
    validate_time_format, validate_date_format, is_end_after_start, calculate_duration
)
from config.database import Database


class SessionsTab(QWidget):
    """Sessions management tab for adding, editing, and deleting study sessions."""

    def __init__(self, db: Database):
        """Initialize sessions tab.
        
        Args:
            db: Database instance
        """
        super().__init__()
        self.db = db
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Form section
        self._create_form_section()

        # Buttons section
        self._create_buttons_section()

        # Table section
        self._create_table_section()

        self.load_sessions()

    def _create_form_section(self) -> None:
        """Create form section for inputting session data."""
        form_layout = QFormLayout()
        form_frame = QFrame()
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
        form_layout.addRow("Subject:", self.subject_input)

        # Start time input
        self.start_input = QLineEdit()
        self.start_input.setPlaceholderText("hh:mm AM/PM (e.g., 02:30 PM)")
        form_layout.addRow("Start Time:", self.start_input)

        # End time input
        self.end_input = QLineEdit()
        self.end_input.setPlaceholderText("hh:mm AM/PM (e.g., 04:00 PM)")
        form_layout.addRow("End Time:", self.end_input)

        # Date input
        self.date_input = QLineEdit()
        today = datetime.today().strftime("%Y-%m-%d")
        self.date_input.setText(today)
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
            field.setMinimumWidth(600)

    def _create_buttons_section(self) -> None:
        """Create buttons section for CRUD operations."""
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        buttons_layout.setContentsMargins(20, 10, 20, 10)
        buttons_layout.setAlignment(Qt.AlignCenter)

        # Add button
        self.add_button = QPushButton("Add Session")
        self.add_button.setIcon(QIcon("assets/add-time.png"))
        self.add_button.setIconSize(QSize(22, 22))
        self.add_button.setMinimumHeight(45)
        self.add_button.clicked.connect(self.save_session)

        # Edit button
        self.edit_button = QPushButton("Edit Session")
        self.edit_button.setIcon(QIcon("assets/pen.png"))
        self.edit_button.setIconSize(QSize(22, 22))
        self.edit_button.setMinimumHeight(45)
        self.edit_button.clicked.connect(self.edit_session)

        # Delete button
        self.delete_button = QPushButton("Delete Session")
        self.delete_button.setIcon(QIcon("assets/delete.png"))
        self.delete_button.setIconSize(QSize(22, 22))
        self.delete_button.setMinimumHeight(45)
        self.delete_button.clicked.connect(self.delete_session)

        # Export button
        self.export_button = QPushButton("Export Sessions")
        self.export_button.setIcon(QIcon("assets/share.png"))
        self.export_button.setIconSize(QSize(22, 22))
        self.export_button.setMinimumHeight(45)
        self.export_button.clicked.connect(self.export_sessions)

        # Configure buttons
        for btn in [self.add_button, self.edit_button, self.delete_button, self.export_button]:
            btn.setMinimumWidth(120)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setCursor(Qt.PointingHandCursor)
            buttons_layout.addWidget(btn)

        buttons_container = QFrame()
        buttons_container.setLayout(buttons_layout)
        buttons_container.setStyleSheet(Styles.BUTTONS_CONTAINER_STYLESHEET)
        self.layout.addSpacing(10)
        self.layout.addWidget(buttons_container)

    def _create_table_section(self) -> None:
        """Create table section for displaying sessions."""
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Subject", "Start Time", "End Time", "Date"])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet(Styles.TABLE_STYLESHEET)
        self.table.cellClicked.connect(self.fill_inputs_from_table)
        self.layout.addWidget(self.table)

    def save_session(self) -> None:
        """Save a new study session."""
        subject = self.subject_input.text().strip()
        start = self.start_input.text().strip()
        end = self.end_input.text().strip()
        date = self.date_input.text().strip()

        # Validation
        if not subject or not start or not end or not date:
            QMessageBox.warning(self, "Error", "Please fill in all fields!")
            return

        if not validate_time_format(start):
            QMessageBox.warning(self, "Error", "Start time format invalid. Use: hh:mm AM/PM")
            return

        if not validate_time_format(end):
            QMessageBox.warning(self, "Error", "End time format invalid. Use: hh:mm AM/PM")
            return

        if not validate_date_format(date):
            QMessageBox.warning(self, "Error", "Date format invalid. Use: YYYY-MM-DD")
            return

        if not is_end_after_start(start, end):
            QMessageBox.warning(self, "Error", "End time must be after start time.")
            return

        # Confirmation
        duration = calculate_duration(start, end)
        reply = QMessageBox.question(
            self,
            "Confirm Save",
            f"Save session for '{subject}'?\n({duration:.2f} hours)\n\nDate: {date}",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            if self.db.add_session(subject, start, end, date):
                QMessageBox.information(self, "Success", f"Session '{subject}' saved!")
                self.load_sessions()
                self.clear_inputs()
            else:
                QMessageBox.critical(self, "Error", "Failed to save session.")

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
        start = self.start_input.text().strip() or old_start
        end = self.end_input.text().strip() or old_end
        date = self.date_input.text().strip() or old_date

        # Check if changes were made
        if (subject, start, end, date) == (old_subject, old_start, old_end, old_date):
            QMessageBox.information(self, "No Changes", "No changes detected.")
            return

        # Validation
        if not validate_time_format(start):
            QMessageBox.warning(self, "Error", "Start time format invalid. Use: hh:mm AM/PM")
            return

        if not validate_time_format(end):
            QMessageBox.warning(self, "Error", "End time format invalid. Use: hh:mm AM/PM")
            return

        if not validate_date_format(date):
            QMessageBox.warning(self, "Error", "Date format invalid. Use: YYYY-MM-DD")
            return

        if not is_end_after_start(start, end):
            QMessageBox.warning(self, "Error", "End time must be after start time.")
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
            if self.db.update_session(session_id, subject, start, end, date):
                QMessageBox.information(self, "Success", f"Session updated!")
                self.load_sessions()
                # Highlight updated row
                for i in range(self.table.columnCount()):
                    self.table.item(selected, i).setBackground(QColor("#dbeafe"))
                self.clear_inputs()
            else:
                QMessageBox.critical(self, "Error", "Failed to update session.")

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
                self.load_sessions()
            else:
                QMessageBox.critical(self, "Error", "Failed to delete session.")

    def export_sessions(self) -> None:
        """Export all sessions to CSV file."""
        rows = self.db.get_all_sessions()
        if not rows:
            QMessageBox.information(self, "No Data", "No sessions available to export.")
            return

        df = pd.DataFrame(rows, columns=["ID", "Subject", "Start Time", "End Time", "Date"])
        filename = f"study_sessions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False)
        QMessageBox.information(self, "Success", f"Sessions exported to '{filename}'.")

    def load_sessions(self) -> None:
        """Load all sessions into table."""
        rows = self.db.get_all_sessions()
        self.table.setRowCount(len(rows))

        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))

    def clear_inputs(self) -> None:
        """Clear all input fields."""
        self.subject_input.clear()
        self.start_input.clear()
        self.end_input.clear()
        today = datetime.today().strftime("%Y-%m-%d")
        self.date_input.setText(today)

    def fill_inputs_from_table(self) -> None:
        """Fill input fields from selected table row."""
        selected = self.table.currentRow()
        if selected < 0:
            return

        self.subject_input.setText(self.table.item(selected, 1).text())
        self.start_input.setText(self.table.item(selected, 2).text())
        self.end_input.setText(self.table.item(selected, 3).text())
        self.date_input.setText(self.table.item(selected, 4).text())
