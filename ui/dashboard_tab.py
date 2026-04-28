"""Dashboard tab component for Study Tracker."""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGridLayout, QSizePolicy
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import seaborn as sns
import pandas as pd

from utils.styles import Styles
from config.database import Database
from utils import chart_styles


class DashboardTab(QWidget):
    """Dashboard tab showing study statistics and charts."""

    def __init__(self, db: Database):
        """Initialize dashboard tab.
        
        Args:
            db: Database instance
        """
        super().__init__()
        self.db = db
        self.setObjectName("DashboardTab")
        self.setAccessibleName("Dashboard tab")
        self.setAccessibleDescription("Overview of study statistics and visual progress charts")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Grid layout for responsive design
        self.grid = QGridLayout()
        self.grid.setSpacing(18)
        self.layout.addLayout(self.grid)
        self.layout.setContentsMargins(10, 6, 10, 10)
        self.layout.setAlignment(Qt.AlignTop)
        self.grid.setColumnStretch(0, 1)
        self.grid.setColumnStretch(1, 1)

        # Initialize stat cards
        self.total_hours_card = QLabel("🕒 Total Hours: 0.00")
        self.subjects_card = QLabel("📘 Subjects Today: 0")
        self.top_subject_card = QLabel("🏆 Top Subject: None")
        self.total_hours_card.setObjectName("hoursCard")
        self.subjects_card.setObjectName("subjectsCard")
        self.top_subject_card.setObjectName("topSubjectCard")

        self.total_hours_card.setAccessibleName("Total study hours")
        self.total_hours_card.setAccessibleDescription("Displays total accumulated study hours")
        self.subjects_card.setAccessibleName("Subjects studied today")
        self.subjects_card.setAccessibleDescription("Displays number of subjects studied today")
        self.top_subject_card.setAccessibleName("Top subject")
        self.top_subject_card.setAccessibleDescription("Displays the subject with highest total study hours")

        self._setup_stat_cards()

        # Apply chart style for consistent aesthetics
        try:
            chart_styles.apply_chart_style()
        except Exception:
            # fallback: ignore styling failure to avoid crashing UI
            pass

        # Create chart figures
        self.figure_bar = plt.Figure(figsize=(6, 4))
        self.canvas_bar = FigureCanvas(self.figure_bar)
        self.canvas_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas_bar.setAccessibleName("Daily study hours chart")
        self.canvas_bar.setAccessibleDescription("Bar chart showing daily study hours")

        self.figure_pie = plt.Figure(figsize=(6, 4))
        self.canvas_pie = FigureCanvas(self.figure_pie)
        self.canvas_pie.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas_pie.setAccessibleName("Study time by subject chart")
        self.canvas_pie.setAccessibleDescription("Pie chart showing study time distribution by subject")

        self.figure_line = plt.Figure(figsize=(6, 4))
        self.canvas_line = FigureCanvas(self.figure_line)
        self.canvas_line.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvas_line.setAccessibleName("Weekly trend chart")
        self.canvas_line.setAccessibleDescription("Line chart showing study hours over the last 7 days")

        # Create chart frames
        self.bar_frame = self._create_chart_frame("📊 Daily Study Hours", self.canvas_bar)
        self.pie_frame = self._create_chart_frame("📘 Study Time by Subject", self.canvas_pie)
        self.line_frame = self._create_chart_frame("📈 Weekly Trend (Last 7 Days)", self.canvas_line)

        # Add to grid
        self.grid.addWidget(self.pie_frame, 2, 0)
        self.grid.addWidget(self.line_frame, 2, 1)
        self.grid.addWidget(self.bar_frame, 1, 0, 1, 2)

        for frame in [self.pie_frame, self.line_frame, self.bar_frame]:
            frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.update_all()

    def _setup_stat_cards(self) -> None:
        """Setup and style stat cards."""
        self.total_hours_card.setStyleSheet(Styles.STAT_CARD_STYLESHEET)
        self.subjects_card.setStyleSheet(Styles.STAT_CARD_STYLESHEET)
        self.top_subject_card.setStyleSheet(Styles.STAT_CARD_STYLESHEET)

        for card in [self.total_hours_card, self.subjects_card, self.top_subject_card]:
            card.setGraphicsEffect(Styles.get_card_shadow_effect())

        card_container = QHBoxLayout()
        card_container.setSpacing(14)
        card_container.addWidget(self.total_hours_card)
        card_container.addWidget(self.subjects_card)
        card_container.addWidget(self.top_subject_card)
        card_container.setAlignment(Qt.AlignCenter)

        card_frame = QFrame()
        card_frame.setObjectName("surfaceCard")
        card_frame.setLayout(card_container)
        card_frame.setStyleSheet("QFrame#surfaceCard { border: none; background: transparent; }")
        self.layout.addWidget(card_frame)

    def _create_chart_frame(self, title: str, canvas: FigureCanvas) -> QFrame:
        """Create a styled chart frame.
        
        Args:
            title: Chart title
            canvas: Matplotlib canvas
            
        Returns:
            Configured QFrame
        """
        frame = QFrame()
        frame_layout = QVBoxLayout()
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setAlignment(Qt.AlignTop)

        title_label = QLabel(title)
        title_label.setObjectName("chartTitle")
        frame_layout.addWidget(title_label)
        frame_layout.addWidget(canvas)

        frame.setLayout(frame_layout)
        frame.setStyleSheet(Styles.CHART_FRAME_STYLESHEET)
        frame.setGraphicsEffect(Styles.get_chart_shadow_effect())

        return frame

    def update_all(self) -> None:
        """Update all dashboard elements."""
        self.update_stat_cards()
        self.update_bar_chart()
        self.update_pie_chart()
        self.update_line_chart()

    def update_stat_cards(self) -> None:
        """Update statistics cards."""
        # Total hours
        total_hours = self.db.get_total_hours()
        self.total_hours_card.setText(f"🕒 Total Hours: {total_hours:.2f}")

        # Subjects today
        today = datetime.today().strftime("%Y-%m-%d")
        sessions_today = self.db.get_sessions_by_date(today)
        unique_subjects_today = {session[1].strip().lower() for session in sessions_today if session[1].strip()}
        self.subjects_card.setText(f"📘 Subjects Today: {len(unique_subjects_today)}")

        # Top subject
        subject_hours = self.db.get_subject_hours()
        if subject_hours:
            top_subject = max(subject_hours, key=subject_hours.get)
            self.top_subject_card.setText(f"🏆 Top Subject: {top_subject}")
        else:
            self.top_subject_card.setText("🏆 Top Subject: None")

    def update_bar_chart(self) -> None:
        """Update daily study hours bar chart."""
        daily_hours = self.db.get_daily_hours()
        if not daily_hours:
            return

        df = pd.DataFrame(list(daily_hours.items()), columns=["date", "hours"])
        df = df.sort_values("date")

        self.figure_bar.clear()
        ax = self.figure_bar.add_subplot(111)
        try:
            palette = chart_styles.get_palette(len(df))
        except Exception:
            palette = "Blues"

        sns.barplot(x="date", y="hours", data=df, ax=ax, palette=palette)
        ax.set_title("Daily Study Hours", color=chart_styles.TEXT)
        ax.set_ylabel("Hours")
        ax.set_xlabel("Date")
        ax.tick_params(axis='x', rotation=30)
        self.figure_bar.subplots_adjust(top=0.88, bottom=0.2)
        self.canvas_bar.draw()

    def update_pie_chart(self) -> None:
        """Update subject distribution pie chart."""
        subject_hours = self.db.get_subject_hours()
        if not subject_hours:
            return

        self.figure_pie.clear()
        ax = self.figure_pie.add_subplot(111)
        try:
            colors = chart_styles.get_palette(len(subject_hours))
        except Exception:
            colors = sns.color_palette("pastel")[0:len(subject_hours)]

        wedges, texts, autotexts = ax.pie(
            subject_hours.values(),
            labels=subject_hours.keys(),
            autopct='%1.1f%%',
            startangle=140,
            colors=colors,
            textprops={'color': chart_styles.TEXT, 'fontsize': 9, 'weight': 'bold'}
        )
        for autotext in autotexts:
            autotext.set_color("white")
            autotext.set_fontsize(8)

        ax.set_title("Study Time by Subject", fontsize=12, fontweight='bold', pad=40, color=chart_styles.TEXT)
        ax.axis('equal')
        self.figure_pie.subplots_adjust(top=0.85)
        self.canvas_pie.draw()

    def update_line_chart(self) -> None:
        """Update weekly trend line chart."""
        all_sessions = self.db.get_all_sessions()
        if not all_sessions:
            return

        data = []
        for _, subject, start, end, date in all_sessions:
            try:
                from utils.time_utils import calculate_duration
                hours = calculate_duration(start, end)
                data.append({"date": date, "hours": hours})
            except Exception:
                pass

        if not data:
            return

        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"])
        
        # Get last 7 days
        today = datetime.today()
        last_week = today - pd.Timedelta(days=7)
        df = df[df["date"] >= last_week]

        if df.empty:
            return

        daily_totals = df.groupby("date")["hours"].sum().reset_index()

        self.figure_line.clear()
        ax = self.figure_line.add_subplot(111)
        try:
            line_color = chart_styles.PRIMARY
        except Exception:
            line_color = "green"

        sns.lineplot(x="date", y="hours", data=daily_totals, marker="o", ax=ax, color=line_color)
        ax.set_title("Weekly Trend (Last 7 Days)", color=chart_styles.TEXT)
        ax.set_ylabel("Hours")
        ax.set_xlabel("Date")
        ax.tick_params(axis='x', rotation=30)
        self.figure_line.subplots_adjust(top=0.88, bottom=0.2)
        self.canvas_line.draw()
