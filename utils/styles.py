"""Styling configuration for Study Tracker."""


class Styles:
    """Centralized styling constants and methods."""

    # Global app stylesheet
    GLOBAL_STYLESHEET = """
        QWidget {
            background-color: #f4f7f4;
            font-family: 'Segoe UI';
            font-size: 13px;
            color: #1f2937;
        }

        QFrame#surfaceCard {
            background-color: #ffffff;
            border: 1px solid #dce6df;
            border-radius: 16px;
        }

        QLineEdit, QDateEdit, QTimeEdit, QDoubleSpinBox {
            background: #f7faf7;
            border: 1px solid #cbd8ce;
            border-radius: 10px;
            padding: 8px 10px;
            color: #1f2937;
            selection-background-color: #0f766e;
            selection-color: #ffffff;
        }

        QLineEdit:focus, QDateEdit:focus, QTimeEdit:focus, QDoubleSpinBox:focus {
            border: 2px solid #0f766e;
            background: #ffffff;
        }

        QLineEdit::placeholder {
            color: #8b9b8f;
        }

        QCheckBox {
            color: #32443a;
            spacing: 8px;
        }

        QCheckBox::indicator {
            width: 16px;
            height: 16px;
            border-radius: 4px;
            border: 1px solid #9db4a2;
            background: #ffffff;
        }

        QCheckBox::indicator:checked {
            background: #0f766e;
            border: 1px solid #0f766e;
        }

        QPushButton {
            background-color: #0f766e;
            color: white;
            font-weight: 600;
            border: 1px solid #0d5f58;
            border-radius: 10px;
            padding: 9px 15px;
        }

        QPushButton:hover {
            background-color: #0d5f58;
        }

        QPushButton:pressed {
            background-color: #0a4b45;
        }

        QPushButton:focus {
            border: 2px solid #f59e0b;
        }

        QFrame#appHeader {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #0f766e,
                stop:1 #115e59
            );
            border: 1px solid #0b4a45;
            border-radius: 16px;
        }

        QLabel#appTitle {
            color: #f0fdf4;
            font-size: 19px;
            font-weight: 700;
            letter-spacing: 0.3px;
        }

        QLabel#appSubtitle {
            color: #d1fae5;
            font-size: 11px;
        }

        QLabel#appBadge {
            background: rgba(255, 255, 255, 0.14);
            color: #ecfeff;
            border: 1px solid rgba(255, 255, 255, 0.35);
            border-radius: 10px;
            padding: 6px 10px;
            font-weight: 600;
        }

        QLabel#headerDate {
            color: #ccfbf1;
            font-size: 12px;
        }

        QTabWidget::pane {
            border: none;
            background: transparent;
        }

        QTabBar::tab {
            background-color: #dcece2;
            color: #1f4d46;
            font-weight: 600;
            padding: 10px 18px;
            border-radius: 14px;
            margin-right: 8px;
            margin-top: 6px;
            border: 1px solid #c4d8cb;
        }

        QTabBar::tab:selected {
            background-color: #0f766e;
            color: #ffffff;
            border: 1px solid #0d5f58;
        }

        QTabBar::tab:hover {
            background-color: #1f8a80;
            color: #ffffff;
        }

        QLabel {
            color: #283941;
        }

        QTableWidget {
            background: #ffffff;
            border: 1px solid #d6e3d9;
            border-radius: 14px;
            gridline-color: #edf2ed;
            alternate-background-color: #f6faf7;
            selection-background-color: #d1fae5;
            selection-color: #14532d;
            padding: 4px;
        }

        QTableWidget:focus {
            border: 2px solid #0f766e;
            background: #ffffff;
        }

        QHeaderView::section {
            background-color: #ecf8f1;
            color: #14532d;
            font-weight: 700;
            border: none;
            border-bottom: 1px solid #d6e3d9;
            padding: 10px;
        }
    """

    HIGH_CONTRAST_STYLESHEET = """
        QWidget {
            background-color: #ffffff;
            color: #111111;
            font-family: 'Segoe UI';
        }

        QLineEdit, QDateEdit, QTimeEdit {
            background: #ffffff;
            border: 2px solid #111111;
            border-radius: 6px;
            padding: 8px;
            color: #111111;
        }

        QLineEdit:focus, QDateEdit:focus, QTimeEdit:focus, QTableWidget:focus {
            border: 3px solid #0b57d0;
        }

        QPushButton {
            background-color: #0b57d0;
            color: #ffffff;
            border: 2px solid #111111;
            border-radius: 8px;
            padding: 8px 14px;
            font-weight: 700;
        }
        QPushButton:hover {
            background-color: #0842a3;
        }
        QPushButton:focus {
            border: 3px solid #111111;
        }

        QTableWidget {
            background: #ffffff;
            border: 2px solid #111111;
            selection-background-color: #0b57d0;
            selection-color: #ffffff;
        }

        QHeaderView::section {
            background-color: #111111;
            color: #ffffff;
            font-weight: 700;
            border: none;
            padding: 8px;
        }

        QTabWidget::pane {
            border: none;
            background: transparent;
        }
        QTabBar::tab {
            background-color: #e5e7eb;
            color: #111111;
            font-weight: 700;
            padding: 8px 16px;
            border-radius: 14px;
            margin-right: 6px;
            margin-top: 4px;
            border: 1px solid #111111;
        }
        QTabBar::tab:selected {
            background-color: #111111;
            color: #ffffff;
        }
    """

    # Header styling
    HEADER_STYLESHEET = """
        QFrame#appHeader { padding: 2px; }
    """

    # Stat cards styling
    STAT_CARD_STYLESHEET = """
        QLabel {
            color: #ffffff;
            border-radius: 18px;
            padding: 20px 24px;
            font-weight: 600;
            font-size: 15px;
            letter-spacing: 0.2px;
            min-height: 66px;
        }

        QLabel#hoursCard {
            background-color: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #0f766e,
                stop:1 #115e59
            );
        }

        QLabel#subjectsCard {
            background-color: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #0ea5a2,
                stop:1 #0f766e
            );
        }

        QLabel#topSubjectCard {
            background-color: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 #f59e0b,
                stop:1 #d97706
            );
        }

        QLabel:hover {
            border: 1px solid rgba(255, 255, 255, 0.42);
        }
    """

    # Chart frame styling
    CHART_FRAME_STYLESHEET = """
        QFrame {
            background-color: #ffffff;
            border-radius: 16px;
            border: 1px solid #dce6df;
            padding: 20px 22px 24px 22px;
            margin: 8px 6px;
        }

        QLabel#chartTitle {
            font-weight: 700;
            font-size: 14px;
            color: #0f5132;
            margin-bottom: 12px;
            letter-spacing: 0.3px;
            border-left: 4px solid #0f766e;
            padding-left: 10px;
        }
    """

    # Form frame styling
    FORM_FRAME_STYLESHEET = """
        QFrame {
            background-color: #ffffff;
            border: 1px solid #dce6df;
            border-radius: 14px;
            padding: 18px 20px;
            margin-bottom: 12px;
        }
    """

    # Label styling
    FORM_LABEL_STYLESHEET = """
        QLabel {
            font-weight: 600;
            color: #14532d;
            padding-right: 8px;
            min-width: 90px;
        }
    """

    # Table styling
    TABLE_STYLESHEET = """
        QTableWidget {
            background: #ffffff;
            border: 1px solid #d6e3d9;
            border-radius: 14px;
            gridline-color: #edf2ed;
            alternate-background-color: #f6faf7;
            selection-background-color: #d1fae5;
            selection-color: #14532d;
        }
        QHeaderView::section {
            background-color: #ecf8f1;
            font-weight: 700;
            border: none;
            padding: 10px;
            font-size: 13px;
            color: #14532d;
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
    def build_global_stylesheet(font_size: int = 13, high_contrast: bool = False) -> str:
        """Build global stylesheet with accessibility options.

        Args:
            font_size: Base font size in pixels
            high_contrast: Whether to apply high-contrast theme

        Returns:
            Complete stylesheet string
        """
        base = Styles.HIGH_CONTRAST_STYLESHEET if high_contrast else Styles.GLOBAL_STYLESHEET
        return f"QWidget {{ font-size: {font_size}px; }}\n" + base

    @staticmethod
    def get_title_font():
        """Get title font configuration."""
        from PyQt5.QtGui import QFont
        return QFont("Segoe UI", 17, QFont.Bold)

    @staticmethod
    def get_shadow_effect():
        """Get drop shadow effect."""
        from PyQt5.QtWidgets import QGraphicsDropShadowEffect
        from PyQt5.QtCore import Qt
        from PyQt5.QtGui import QColor
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(24)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(15, 118, 110, 80))
        return shadow

    @staticmethod
    def get_card_shadow_effect():
        """Get shadow effect for stat cards."""
        from PyQt5.QtWidgets import QGraphicsDropShadowEffect
        from PyQt5.QtGui import QColor
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(24)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(17, 94, 89, 70))
        return shadow

    @staticmethod
    def get_chart_shadow_effect():
        """Get shadow effect for chart frames."""
        from PyQt5.QtWidgets import QGraphicsDropShadowEffect
        from PyQt5.QtGui import QColor
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(18)
        shadow.setOffset(0, 4)
        shadow.setColor(QColor(17, 94, 89, 45))
        return shadow
