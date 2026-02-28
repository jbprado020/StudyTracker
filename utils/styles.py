"""Styling configuration for Study Tracker."""


class Styles:
    """Centralized styling constants and methods."""

    # Global app stylesheet
    GLOBAL_STYLESHEET = """
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
    """

    # Header styling
    HEADER_STYLESHEET = """
        QFrame#appHeader {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #ffffff, stop:1 #f9fafb);
            border-bottom: 1px solid #e2e8f0;
            border-radius: 8px;
        }
        QLabel#appTitle {
            color: #0f1720;
        }
    """

    # Stat cards styling
    STAT_CARD_STYLESHEET = """
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

    # Chart frame styling
    CHART_FRAME_STYLESHEET = """
        QFrame {
            background-color: #ffffff;
            border-radius: 16px;
            border: 1px solid #e2e8f0;
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

    # Form frame styling
    FORM_FRAME_STYLESHEET = """
        QFrame {
            background-color: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 16px 20px;
            margin-bottom: 12px;
        }
    """

    # Label styling
    FORM_LABEL_STYLESHEET = """
        QLabel {
            font-weight: 600;
            color: #1e3a8a;
            padding-right: 8px;
            min-width: 90px;
        }
    """

    # Table styling
    TABLE_STYLESHEET = """
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
    """

    # Buttons container styling
    BUTTONS_CONTAINER_STYLESHEET = """
        QFrame {
            border: none;
            margin-bottom: 10px;
        }
    """

    @staticmethod
    def get_title_font():
        """Get title font configuration."""
        from PyQt5.QtGui import QFont
        return QFont("Segoe UI", 16, QFont.Bold)

    @staticmethod
    def get_shadow_effect():
        """Get drop shadow effect."""
        from PyQt5.QtWidgets import QGraphicsDropShadowEffect
        from PyQt5.QtCore import Qt
        from PyQt5.QtGui import QColor
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setOffset(0, 2)
        shadow.setColor(Qt.gray)
        return shadow

    @staticmethod
    def get_card_shadow_effect():
        """Get shadow effect for stat cards."""
        from PyQt5.QtWidgets import QGraphicsDropShadowEffect
        from PyQt5.QtGui import QColor
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setOffset(0, 8)
        shadow.setColor(QColor(37, 99, 235, 60))
        return shadow

    @staticmethod
    def get_chart_shadow_effect():
        """Get shadow effect for chart frames."""
        from PyQt5.QtWidgets import QGraphicsDropShadowEffect
        from PyQt5.QtGui import QColor
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(24)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(37, 99, 235, 40))
        return shadow
