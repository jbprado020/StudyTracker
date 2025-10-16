import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton,
    QMessageBox, QTableWidget, QTableWidgetItem, QFormLayout, QLabel,
    QTabWidget, QFrame, QHBoxLayout, QHeaderView, QSizePolicy, QGraphicsDropShadowEffect, QGridLayout
)
from PyQt5.QtGui import QFont, QIcon, QColor
from PyQt5.QtCore import Qt, QSize
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import seaborn as sns
import pandas as pd


class StudyTracker(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon("book.png"))

        self.setWindowTitle("Pradofy - Study Time and Productivity Tracker")
        self.setGeometry(100, 100, 900, 600)
 
        self.conn = sqlite3.connect("study_sessions.db")
        self.create_table()

        main_layout = QVBoxLayout()
        tabs = QTabWidget()
        tabs.setStyleSheet("QTabBar { margin-left: 10px; }")
        header_frame = QFrame()
        header_frame.setObjectName("appHeader")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(12, 8, 12, 8)
        header_layout.setSpacing(10)

        title_box = QVBoxLayout()
        title_label = QLabel("Pradofy Study - Study Time & Productivity Tracker")
        title_label.setObjectName("appTitle")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        subtitle_label = QLabel("Track sessions • Visualize progress")
        subtitle_label.setStyleSheet("color: #6b7280; font-size: 11px;")
        title_box.addWidget(title_label)
        title_box.addWidget(subtitle_label)
        title_box.setSpacing(0)
        header_layout.addLayout(title_box)

        header_layout.addStretch()

        date_label = QLabel(datetime.today().strftime("%A, %b %d %Y"))
        date_label.setStyleSheet("color: #6b7280; font-size: 12px;")
        header_layout.addWidget(date_label)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setOffset(0, 2)
        shadow.setColor(Qt.gray)
        header_frame.setGraphicsEffect(shadow)

        header_frame.setStyleSheet("""
            QFrame#appHeader {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ffffff, stop:1 #f9fafb);
                border-bottom: 1px solid #e2e8f0;
                border-radius: 8px;
            }
            QLabel#appTitle {
                color: #0f1720;
            }
        """)
        main_layout.addWidget(header_frame)
        main_layout.addWidget(tabs)
        self.setLayout(main_layout)

        # --- Dashboard tab ---
        self.dashboard_tab = QWidget()
        self.dashboard_tab.setObjectName("DashboardTab")
        self.dashboard_layout = QVBoxLayout()
        self.dashboard_tab.setLayout(self.dashboard_layout)

        self.dashboard_grid = QGridLayout()
        self.dashboard_grid.setSpacing(20)
        self.dashboard_layout.addLayout(self.dashboard_grid)
        self.dashboard_layout.setContentsMargins(20, 10, 20, 10)
        self.dashboard_layout.setAlignment(Qt.AlignTop)
        self.dashboard_grid.setColumnStretch(0, 1)
        self.dashboard_grid.setColumnStretch(1, 1)

        # --- Stat Cards ---
        self.total_hours_card = QLabel("🕒 Total Hours: 0.00")
        self.subjects_card = QLabel("📘 Subjects Today: 0")
        self.top_subject_card = QLabel("🏆 Top Subject: None")

        card_style = """
            QLabel {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #60a5fa, stop:1 #2563eb
                );
                color: white;
                border-radius: 16px;
                padding: 18px 22px;
                font-weight: 600;
                font-size: 15px;
                letter-spacing: 0.3;
            }
            QLabel:hover {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #93c5fd, stop:1 #3b82f6
                );
                border: 1px solid #60a5fa;
            }
        """
        self.total_hours_card.setStyleSheet(card_style)
        self.subjects_card.setStyleSheet(card_style)
        self.top_subject_card.setStyleSheet(card_style)


        for card in [self.total_hours_card, self.subjects_card, self.top_subject_card]:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(30)
            shadow.setOffset(0, 8)
            shadow.setColor(QColor(37, 99, 235, 60))
            card.setGraphicsEffect(shadow)

        card_container = QHBoxLayout()
        card_container.setSpacing(18)
        card_container.addWidget(self.total_hours_card)
        card_container.addWidget(self.subjects_card)
        card_container.addWidget(self.top_subject_card)
        card_container.setAlignment(Qt.AlignCenter)

        card_frame = QFrame()
        card_frame.setLayout(card_container)
        card_frame.setStyleSheet("QFrame { border: none; }")
        self.dashboard_layout.addWidget(card_frame)


        # --- Dashboard Chart (Daily Study Hours) ---
        self.figure = plt.Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        bar_frame = QFrame()
        bar_layout = QVBoxLayout()
        bar_layout.setContentsMargins(0, 0, 0, 0)
        bar_layout.setAlignment(Qt.AlignTop)
        bar_title = QLabel("📊 Daily Study Hours")
        bar_title.setProperty("class", "chartTitle")
        bar_title.setObjectName("barTitle")
        bar_layout.addWidget(bar_title)
        bar_layout.addWidget(self.canvas)
        bar_frame.setLayout(bar_layout)

        # --- Dashboard Chart (Subject Distribution Pie) ---
        self.figure2 = plt.Figure(figsize=(6, 4))
        self.canvas2 = FigureCanvas(self.figure2)
        self.canvas2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        pie_frame = QFrame()
        pie_layout = QVBoxLayout()
        pie_layout.setContentsMargins(0, 0, 0, 0)
        pie_layout.setAlignment(Qt.AlignTop)
        pie_title = QLabel("📘 Study Time by Subject")
        pie_title.setProperty("class", "chartTitle")
        pie_layout.addWidget(pie_title)
        pie_layout.addWidget(self.canvas2)
        pie_frame.setLayout(pie_layout)
    
        # --- Dashboard Chart (Weekly Trend Line) ---
        self.figure3 = plt.Figure(figsize=(6, 4))
        self.canvas3 = FigureCanvas(self.figure3)
        self.canvas3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        line_frame = QFrame()
        line_layout = QVBoxLayout()
        line_layout.setContentsMargins(0, 0, 0, 0)
        line_layout.setAlignment(Qt.AlignTop)
        line_title = QLabel("📈 Weekly Trend (Last 7 Days)")
        line_title.setProperty("class", "chartTitle")
        line_layout.addWidget(line_title)
        line_layout.addWidget(self.canvas3)
        line_frame.setLayout(line_layout)

        chart_style = """
            QFrame {
                background-color: #ffffff;
                border-radius: 16px;
                border: 1px solid #e2e8f0; /* Light blue border */
                padding: 22px 24px 26px 24px;
                margin: 8px;
            }

            QLabel.chartTitle {
                font-weight: 700;
                font-size: 14px;
                color: #1e40af;
                margin-bottom: 10px;
                padding-left: 6px;
                letter-spacing: 0.4px;
                border-left: 4px solid #2563eb;
                padding-left: 10px;
            }
        """
        
        for frame in (bar_frame, pie_frame, line_frame):
            frame.setStyleSheet(chart_style)
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(24)          # tweak for stronger/softer shadow
            shadow.setOffset(0, 6)           # vertical offset
            shadow.setColor(QColor(37, 99, 235, 40))  # subtle alpha
            frame.setGraphicsEffect(shadow)

        self.dashboard_grid.addWidget(pie_frame, 2, 0)
        self.dashboard_grid.addWidget(line_frame, 2, 1)
        self.dashboard_grid.addWidget(bar_frame, 1, 0, 1, 2)

        pie_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        line_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        bar_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        tabs.addTab(self.dashboard_tab, "Dashboard")

        # --- Sessions tab ---
        self.sessions_tab = QWidget()
        tabs.addTab(self.sessions_tab, "Sessions")
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 16px 20px;
                margin-bottom: 12px;
            }
        """)
        form_frame.setLayout(form_layout)
        layout.addWidget(form_frame)

        # Set form layout alignment and spacing
        form_layout.setLabelAlignment(Qt.AlignRight)
        form_layout.setFormAlignment(Qt.AlignHCenter | Qt.AlignTop)
        form_layout.setHorizontalSpacing(20)
        form_layout.setVerticalSpacing(18)
        form_layout.setContentsMargins(30, 20, 30, 20)

        label_style =   """
            QLabel {
                font-weight: 600;
                color: #1e3a8a;
                padding-right: 8px;
                min-width: 90px;  /* ensures all labels same width */
            }
        """

        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("e.g., Math, Programming...")
        form_layout.addRow("Subject:", self.subject_input)

        self.start_input = QLineEdit()
        self.start_input.setPlaceholderText("hh:mm AM/PM (e.g., 02:30 PM)")
        form_layout.addRow("Start Time:", self.start_input)

        self.end_input = QLineEdit()
        self.end_input.setPlaceholderText("hh:mm AM/PM (e.g., 04:00 PM)")
        form_layout.addRow("End Time:", self.end_input)

        self.date_input = QLineEdit()
        today = datetime.today().strftime("%Y-%m-%d")
        self.date_input.setText(today)
        form_layout.addRow("Date:", self.date_input)

        for i in range(form_layout.rowCount()):
            label_item = form_layout.itemAt(i, QFormLayout.LabelRole)
            if label_item and label_item.widget():
                label_item.widget().setStyleSheet(label_style)

        for field in [self.subject_input, self.start_input, self.end_input, self.date_input]:
            field.setMinimumHeight(36)
            field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            field.setMinimumWidth(600)


        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(15)
        buttons_layout.setContentsMargins(20, 10, 20, 10)
        buttons_layout.setAlignment(Qt.AlignCenter)

        self.add_button = QPushButton("Add Session")
        self.add_button.setIcon(QIcon("add-time.png"))
        self.add_button.setIconSize(QSize(22,22))
        self.add_button.setMinimumHeight(45)
        self.add_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.add_button.clicked.connect(self.save_session)

        self.edit_button = QPushButton("Edit Session")
        self.edit_button.setIcon(QIcon("pen.png"))
        self.edit_button.setIconSize(QSize(22,22))
        self.edit_button.setMinimumHeight(45)
        self.edit_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.edit_button.clicked.connect(self.edit_session)

        self.delete_button = QPushButton("Delete Session")
        self.delete_button.setIcon(QIcon("delete.png"))
        self.delete_button.setIconSize(QSize(22, 22))
        self.delete_button.setMinimumHeight(45)
        self.delete_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.delete_button.clicked.connect(self.delete_session)

        self.export_button = QPushButton("Export Sessions")
        self.export_button.setIcon(QIcon("share.png"))
        self.export_button.setIconSize(QSize(22, 22))
        self.export_button.setMinimumHeight(45)
        self.export_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.export_button.clicked.connect(self.export_sessions)

        for btn in [self.add_button, self.edit_button, self.delete_button, self.export_button]:
            btn.setMinimumWidth(120)
            btn.setCursor(Qt.PointingHandCursor)
            buttons_layout.addWidget(btn)

        buttons_container = QFrame()
        buttons_container.setLayout(buttons_layout)
        buttons_container.setStyleSheet("QFrame { border: none; margin-bottom: 10px; }")
        layout.addSpacing(10)
        layout.addWidget(buttons_container)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Subject", "Start Time", "End Time", "Date"]
        )
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget {
                background: #ffffff;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                gridline-color: #f1f5f9;
                alternate-background-color: #f9fafb;
                selection-background-color: #93c5fd;
                selection-color: #1e3a8a;
            }
            QHeaderView::section {
                background-color: #eff6ff;
                font-weight: 600;
                border: none;
                padding: 8px;
                font-size: 13px;
                color: #1e3a8a;
            }
        """)

        self.table.cellClicked.connect(self.fill_inputs_from_table)
        layout.addWidget(self.table)
        self.sessions_tab.setLayout(layout)

        self.load_sessions()

        self.update_dashboard_cards()
        self.update_dashboard_chart()
        self.update_subject_pie_chart()
        self.update_weekly_trend_chart()

    # --- Database setup ---
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject TEXT,
                start_time TEXT,
                end_time TEXT,
                date TEXT
            )
        """)
        self.conn.commit()

    # --- Save new session ---
    def save_session(self):
        subject = self.subject_input.text().strip()
        start = self.start_input.text().strip()
        end = self.end_input.text().strip()
        date = self.date_input.text().strip()

        if not subject or not start or not end or not date:
            QMessageBox.warning(self, "Error", "Please fill in all fields!")
            return

        try:
            start_dt = datetime.strptime(start, "%I:%M %p")
            end_dt = datetime.strptime(end, "%I:%M %p")
        except ValueError:
            QMessageBox.warning(self, "Error", "Use hh:mm AM/PM format.")
            return

        if end_dt <= start_dt:
            QMessageBox.warning(self, "Error", "End time must be after start time.")
            return

        reply = QMessageBox.question(
            self,
            "Confirm Save",
            f"Do you want to save the session for '{subject}'?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            cursor = self.conn.cursor()
            cursor.execute(
                "INSERT INTO sessions (subject, start_time, end_time, date) VALUES (?, ?, ?, ?)",
                (subject, start, end, date),
            )
            self.conn.commit()
            QMessageBox.information(self, "Saved", f"Session '{subject}' saved!")
            self.load_sessions()
            self.clear_inputs()
        else:
            QMessageBox.information(self, "Cancelled", "Session not saved.")

    def load_sessions(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM sessions")
        rows = cursor.fetchall()

        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))

        self.update_dashboard_cards()
        self.update_dashboard_chart()
        self.update_subject_pie_chart()
        self.update_weekly_trend_chart()

    def edit_session(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Error", "Select a session to edit first.")
            return

        session_id = self.table.item(selected, 0).text()
        old_subject = self.table.item(selected, 1).text()
        old_start = self.table.item(selected, 2).text()
        old_end = self.table.item(selected, 3).text()
        old_date = self.table.item(selected, 4).text()

        subject = self.subject_input.text().strip() or old_subject
        start = self.start_input.text().strip() or old_start
        end = self.end_input.text().strip() or old_end
        date = self.date_input.text().strip() or old_date

        # Check if any changes were made
        if (subject, start, end, date) == (old_subject, old_start, old_end, old_date):
            QMessageBox.information(self, "No Changes", "No changes detected to update.")
            return

        # Validate time format
        try:
            start_dt = datetime.strptime(start, "%I:%M %p")
            end_dt = datetime.strptime(end, "%I:%M %p")
        except ValueError:
            QMessageBox.warning(self, "Error", "Use hh:mm AM/PM format (e.g., 02:30 PM).")
            return

        if end_dt <= start_dt:
            QMessageBox.warning(self, "Error", "End time must be after start time.")
            return

        reply = QMessageBox.question(
            self,
            "Confirm Edit",
            f"Are you sure you want to update the session:\n\n"
            f"📘 Subject: {old_subject} → {subject}\n"
            f"🕒 Time: {old_start} - {old_end} → {start} - {end}\n"
            f"📅 Date: {old_date} → {date}",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE sessions SET subject=?, start_time=?, end_time=?, date=? WHERE id=?",
                (subject, start, end, date, session_id),
            )
            self.conn.commit()
            QMessageBox.information(self, "Updated", f"Session '{subject}' successfully updated!")

            self.load_sessions()

            # Highlight the updated row
            for i in range(self.table.columnCount()):
                self.table.item(selected, i).setBackground(QColor("#dbeafe"))

            self.clear_inputs()
        else:
            QMessageBox.information(self, "Cancelled", "Session update cancelled.")

    def delete_session(self):
        selected = self.table.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Error", "Select a session to delete.")
            return

        session_id = self.table.item(selected, 0).text()
        subject = self.table.item(selected, 1).text()

        reply = QMessageBox.warning(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete the session for '{subject}' (ID {session_id})?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM sessions WHERE id=?", (session_id,))
            self.conn.commit()
            QMessageBox.information(self, "Deleted", "Session deleted.")
            self.load_sessions()
        else:
            QMessageBox.information(self, "Cancelled", "Session not deleted.")

    def export_sessions(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM sessions")
        rows = cursor.fetchall()
        if not rows:
            QMessageBox.information(self, "No Data", "No sessions available to export.")
            return

        df = pd.DataFrame(rows, columns=["ID", "Subject", "Start Time", "End Time", "Date"])
        df.to_csv("study_sessions_export.csv", index=False)
        QMessageBox.information(self, "Exported", "Sessions exported to 'study_sessions_export.csv'.")

    def update_dashboard_cards(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT start_time, end_time FROM sessions")
        rows = cursor.fetchall()

        total_hours = 0
        for start, end in rows:
            try:
                start_dt = datetime.strptime(start, "%I:%M %p")
                end_dt = datetime.strptime(end, "%I:%M %p")
                total_hours += (end_dt - start_dt).seconds / 3600
            except Exception:
                pass

        self.total_hours_card.setText(f"🕒 Total Hours: {total_hours:.2f}")

        today = datetime.today().strftime("%Y-%m-%d")
        cursor.execute("SELECT COUNT(*) FROM sessions WHERE date=?", (today,))
        subjects_today = cursor.fetchone()[0]
        self.subjects_card.setText(f"📘 Subjects Today: {subjects_today}")
       
        cursor.execute("SELECT subject, start_time, end_time FROM sessions")
        rows = cursor.fetchall()

        subject_hours = {}
        for subject, start, end in rows:
            try:
                start_dt = datetime.strptime(start, "%I:%M %p")
                end_dt = datetime.strptime(end, "%I:%M %p")
                hours = (end_dt - start_dt).seconds / 3600
                subject_hours[subject] = subject_hours.get(subject, 0) + hours
            except Exception:
                pass

        if subject_hours:
            top_subject = max(subject_hours, key=subject_hours.get)
            self.top_subject_card.setText(f"🏆 Top Subject: {top_subject}")
        else:
            self.top_subject_card.setText("🏆 Top Subject: None")

    def update_dashboard_chart(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT date, start_time, end_time FROM sessions")
        rows = cursor.fetchall()

        if not rows:
            return

        data = []
        for date, start, end in rows:
            try:
                start_dt = datetime.strptime(start, "%I:%M %p")
                end_dt = datetime.strptime(end, "%I:%M %p")
                hours = (end_dt - start_dt).seconds / 3600
                data.append({"date": date, "hours": hours})
            except Exception:
                pass

        df = pd.DataFrame(data)
        if df.empty:
            return

        daily_totals = df.groupby("date")["hours"].sum().reset_index()

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        sns.barplot(x="date", y="hours", data=daily_totals, ax=ax, palette="Blues")
        ax.set_title("Daily Study Hours")
        self.figure.subplots_adjust(top=0.88, bottom=0.25)
        ax.set_ylabel("Hours")
        ax.set_xlabel("Date")
        ax.tick_params(axis='x', rotation=30)
        self.figure.subplots_adjust(top=0.88, bottom=0.2)
        self.canvas.draw()

    def update_subject_pie_chart(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT subject, start_time, end_time FROM sessions")
        rows = cursor.fetchall()

        if not rows:
            return

        data = {}
        for subject, start, end in rows:
            try:
                start_dt = datetime.strptime(start, "%I:%M %p")
                end_dt = datetime.strptime(end, "%I:%M %p")
                hours = (end_dt - start_dt).seconds / 3600
                data[subject] = data.get(subject, 0) + hours
            except Exception:
                pass

        if not data:
            return

        self.figure2.clear()
        ax = self.figure2.add_subplot(111)
        colors = sns.color_palette("pastel")[0:len(data)]
        wedges, texts, autotexts = ax.pie(
            data.values(),
            labels=data.keys(),
            autopct='%1.1f%%',
            startangle=140,
            colors=colors,
            textprops={'color': 'black', 'fontsize': 9, 'weight': 'bold'}
        )
        for autotext in autotexts:
            autotext.set_color("white")
            autotext.set_fontsize(8)

        ax.set_title("Study Time by Subject", fontsize=12, fontweight='bold', pad=40)
        self.figure2.subplots_adjust(top=0.88, bottom=0.25)
        ax.axis('equal')
        self.figure2.subplots_adjust(top=0.85)
        self.canvas2.draw()

    def update_weekly_trend_chart(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT date, start_time, end_time FROM sessions")
        rows = cursor.fetchall()

        if not rows:
            return

        data = []
        for date, start, end in rows:
            try:
                start_dt = datetime.strptime(start, "%I:%M %p")
                end_dt = datetime.strptime(end, "%I:%M %p")
                hours = (end_dt - start_dt).seconds / 3600
                data.append({"date": date, "hours": hours})
            except Exception:
                pass

        df = pd.DataFrame(data)
        if df.empty:
            return

        df["date"] = pd.to_datetime(df["date"])
        today = datetime.today()
        last_week = today - pd.Timedelta(days=7)
        df = df[df["date"] >= last_week]

        if df.empty:
            return

        daily_totals = df.groupby("date")["hours"].sum().reset_index()

        self.figure3.clear()
        ax = self.figure3.add_subplot(111)
        sns.lineplot(x="date", y="hours", data=daily_totals, marker="o", ax=ax, color="green")
        ax.set_title("Weekly Trend (Last 7 Days)")
        self.figure3.subplots_adjust(top=0.88, bottom=0.25)
        ax.set_ylabel("Hours")
        ax.set_xlabel("Date")
        ax.tick_params(axis='x', rotation=30)
        self.canvas3.draw()

    def clear_inputs(self):
        self.subject_input.clear()
        self.start_input.clear()
        self.end_input.clear()
        today = datetime.today().strftime("%Y-%m-%d")
        self.date_input.setText(today)
    
    def fill_inputs_from_table(self):
        selected = self.table.currentRow()
        if selected < 0:
            return

        self.subject_input.setText(self.table.item(selected, 1).text())
        self.start_input.setText(self.table.item(selected, 2).text())
        self.end_input.setText(self.table.item(selected, 3).text())
        self.date_input.setText(self.table.item(selected, 4).text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudyTracker()

    # Global modern light theme
    app.setStyleSheet("""
        QWidget {
            background-color: #f5f7fa;
            font-family: 'Segoe UI';
            font-size: 13px;
        }

        QLineEdit {
            background: #f8fafc;
            border: 1px solid #cbd5e1;
            border-radius: 6px;
            padding: 8px;
            color: #1e293b;
        }
        QLineEdit:focus{
            border: 1px solid #3b82f6;
            background: #ffffff;
        }

        QPushButton {
            background-color: #2563eb;
            color: white;
            font-weight: 600;
            border-radius: 8px;
            padding: 8px 14px;
            transition: background-color 0.3s ease;
        }
        QPushButton:hover {
            background-color: #1d4ed8;
        }
        QPushButton:pressed {
            background-color: #1e40af;
        }
        QHeaderView::section {
            background-color: #e1e5ea;
            padding: 4px;
            border: none;
            font-weight: bold;
        }

        QTableWidget {
            gridline-color: #dcdcdc;
        }

        QLabel {
            color: #333;
        }
        QTabWidget::pane {
            border: none;
            background: transparent;
        }
        QTabBar::tab {
            background-color: #e0e7ff;
            color: #1e3a8a;
            font-weight: 600;
            padding: 8px 16px;
            border-radius: 14px;
            margin-right: 6px;
            margin-top: 4px;
            transition: all 0.3s ease;
        }
        QTabBar::tab:selected {
            background-color: #2563eb;
            color: white;
            font-weight: bold;
        }
        QTabBar::tab:hover {
            background-color: #60a5fa;
            color: white;
        }
    """)

    window.show()
    sys.exit(app.exec_())
