"""Styling configuration for Study Tracker."""

import re


def _make_token_map():
    """Build the default token → value map from Styles class attributes.
    Called lazily after the class is fully defined.
    """
    return {
        "PRIMARY":       Styles.PRIMARY,
        "PRIMARY_DARK":  Styles.PRIMARY_DARK,
        "PRIMARY_DARKEST": Styles.PRIMARY_DARKEST,
        "ACCENT":        Styles.ACCENT,
        "HIGHLIGHT":     Styles.HIGHLIGHT,
        "HEADER_START":  Styles.HEADER_START,
        "HEADER_END":    Styles.HEADER_END,
        "SURFACE":       Styles.SURFACE,
        "CARD_SURFACE":  Styles.CARD_SURFACE,
        "CARD_BORDER":   Styles.CARD_BORDER,
        "TEXT":          Styles.TEXT,
        "MUTED":         Styles.MUTED,
        "TAB_BG":        Styles.TAB_BG,
        "TAB_TEXT":      Styles.TAB_TEXT,
    }


class Styles:
    """Centralized styling constants and methods."""

    # Theme color tokens
    PRIMARY          = "#0f766e"
    PRIMARY_DARK     = "#0d5f58"
    PRIMARY_DARKEST  = "#0a4b45"
    ACCENT           = "#0ea5a2"
    HIGHLIGHT        = "#f59e0b"
    HEADER_START     = "#0f766e"
    HEADER_END       = "#115e59"
    SURFACE          = "#f4f7f4"
    CARD_SURFACE     = "#ffffff"
    CARD_BORDER      = "#dce6df"
    TEXT             = "#1f2937"
    MUTED            = "#8b9b8f"
    TAB_BG           = "#dcece2"
    TAB_TEXT         = "#1f4d46"

    # ------------------------------------------------------------------
    # Safe token resolver
    # ------------------------------------------------------------------

    @staticmethod
    def resolve(template: str, extra: dict = None) -> str:
        """Replace {TOKEN} placeholders in a stylesheet string.

        Unlike str.format(), this only replaces known named tokens so that
        ordinary CSS curly braces (e.g. ``QLabel { color: red; }``) are
        left untouched and never raise a KeyError.

        Args:
            template: Raw stylesheet string containing {TOKEN} markers.
            extra: Optional additional token → value pairs to merge in.

        Returns:
            Stylesheet with all known tokens substituted.
        """
        tokens = _make_token_map()
        if extra:
            tokens.update(extra)

        def replacer(match: re.Match) -> str:
            key = match.group(1)
            return tokens.get(key, match.group(0))   # unknown → leave as-is

        # Match {WORD} where WORD is all-caps/underscores (our token convention)
        return re.sub(r"\{([A-Z_]+)\}", replacer, template)

    # ------------------------------------------------------------------
    # Stylesheets  (tokens use {ALL_CAPS} convention)
    # ------------------------------------------------------------------

    GLOBAL_STYLESHEET_TEMPLATE = """
        QWidget {
            background-color: {SURFACE};
            font-family: 'Segoe UI';
            font-size: 13px;
            color: {TEXT};
        }

        QFrame#surfaceCard {
            background-color: {CARD_SURFACE};
            border: 1px solid {CARD_BORDER};
            border-radius: 16px;
        }

        QLineEdit, QDateEdit, QTimeEdit, QDoubleSpinBox {
            background: #f7faf7;
            border: 1px solid #cbd8ce;
            border-radius: 10px;
            padding: 8px 10px;
            color: {TEXT};
            selection-background-color: {PRIMARY};
            selection-color: #ffffff;
        }

        QLineEdit:focus, QDateEdit:focus, QTimeEdit:focus, QDoubleSpinBox:focus {
            border: 2px solid {PRIMARY};
            background: {CARD_SURFACE};
        }

        QLineEdit::placeholder {
            color: {MUTED};
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
            background: {CARD_SURFACE};
        }

        QCheckBox::indicator:checked {
            background: {PRIMARY};
            border: 1px solid {PRIMARY};
        }

        QPushButton {
            background-color: {PRIMARY};
            color: white;
            font-weight: 600;
            border: 1px solid {PRIMARY_DARK};
            border-radius: 10px;
            padding: 9px 15px;
        }

        QPushButton:hover {
            background-color: {PRIMARY_DARK};
        }

        QPushButton:pressed {
            background-color: {PRIMARY_DARKEST};
        }

        QPushButton:focus {
            border: 2px solid {HIGHLIGHT};
        }

        QFrame#appHeader {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 {HEADER_START},
                stop:1 {HEADER_END}
            );
            border: 1px solid #0b4a45;
            border-radius: 16px;
        }

        QLabel#appTitle {
            color: #0f5132;
            font-size: 19px;
            font-weight: 700;
            letter-spacing: 0.3px;
        }

        QLabel#appSubtitle {
            color: #14532d;
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
            color: #0f5132;
            font-size: 12px;
        }

        QTabWidget::pane {
            border: none;
            background: transparent;
        }

        QTabBar::tab {
            background-color: {TAB_BG};
            color: {TAB_TEXT};
            font-weight: 600;
            padding: 10px 18px;
            border-radius: 14px;
            margin-right: 8px;
            margin-top: 6px;
            border: 1px solid #c4d8cb;
        }

        QTabBar::tab:selected {
            background-color: {PRIMARY};
            color: #ffffff;
            border: 1px solid {PRIMARY_DARK};
        }

        QTabBar::tab:hover {
            background-color: {PRIMARY_DARK};
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
            border: 2px solid {PRIMARY};
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

    HEADER_STYLESHEET = """
        QFrame#appHeader { padding: 2px; }
    """

    # Tokens: {PRIMARY}, {HEADER_END}, {ACCENT}, {HIGHLIGHT}
    # CSS braces like "QLabel {" are safe because resolve() only replaces
    # {ALL_CAPS_TOKENS}, not arbitrary brace content.
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
                stop:0 {PRIMARY},
                stop:1 {HEADER_END}
            );
        }

        QLabel#subjectsCard {
            background-color: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 {ACCENT},
                stop:1 {PRIMARY}
            );
        }

        QLabel#topSubjectCard {
            background-color: qlineargradient(
                x1:0, y1:0, x2:1, y2:1,
                stop:0 {HIGHLIGHT},
                stop:1 #d97706
            );
        }

        QLabel:hover {
            border: 1px solid rgba(255, 255, 255, 0.42);
        }
    """

    # Tokens: {TEXT}, {PRIMARY}
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
            color: {TEXT};
            margin-bottom: 12px;
            letter-spacing: 0.3px;
            border-left: 4px solid {PRIMARY};
            padding-left: 10px;
        }
    """

    FORM_FRAME_STYLESHEET = """
        QFrame {
            background-color: #ffffff;
            border: 1px solid #dce6df;
            border-radius: 14px;
            padding: 18px 20px;
            margin-bottom: 12px;
        }
    """

    FORM_LABEL_STYLESHEET = """
        QLabel {
            font-weight: 600;
            color: #14532d;
            padding-right: 8px;
            min-width: 90px;
        }
    """

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

    BUTTONS_CONTAINER_STYLESHEET = """
        QFrame {
            border: none;
            margin-bottom: 10px;
        }
    """

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @staticmethod
    def build_global_stylesheet(font_size: int = 13, high_contrast: bool = False) -> str:
        """Build global stylesheet with accessibility options.

        Args:
            font_size: Base font size in pixels
            high_contrast: Whether to apply high-contrast theme

        Returns:
            Complete stylesheet string
        """
        template = (
            Styles.HIGH_CONTRAST_STYLESHEET if high_contrast
            else Styles.GLOBAL_STYLESHEET_TEMPLATE
        )
        base = Styles.resolve(template)
        return f"QWidget {{ font-size: {font_size}px; }}\n" + base

    @staticmethod
    def get_title_font():
        """Get title font configuration."""
        from PyQt5.QtGui import QFont
        return QFont("Segoe UI", 17, QFont.Bold)

    @staticmethod
    def get_shadow_effect():
        """Get drop shadow effect for the app header."""
        from PyQt5.QtWidgets import QGraphicsDropShadowEffect
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
