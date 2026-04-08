"""Design system for ScreenLens — inspired by Google Circle to Search."""

from PyQt5.QtGui import QColor

# ── Overlay ──────────────────────────────────────────────
DIM_COLOR = QColor(0, 0, 0, 110)

# ── Stroke glow layers (width, r, g, b, a) ──────────────
# Drawn outer→inner so the bloom builds up naturally
GLOW_LAYERS = [
    (34, 233, 69,  96,  18),
    (24, 233, 69,  96,  35),
    (16, 233, 69,  96,  60),
    (9,  255, 140, 170, 85),
]
STROKE_WIDTH = 3.5
STROKE_COLOR = QColor(255, 255, 255, 240)

# ── Accent palette ───────────────────────────────────────
ACCENT      = QColor(233, 69, 96)
ACCENT_LIGHT = QColor(255, 140, 170)
SUCCESS     = QColor(78, 204, 163)
BG_CARD     = QColor(28, 28, 48, 220)
BG_GLASS    = QColor(255, 255, 255, 18)
BORDER      = QColor(255, 255, 255, 30)
TEXT_PRIMARY = QColor(255, 255, 255)
TEXT_SECONDARY = QColor(255, 255, 255, 178)
TEXT_MUTED   = QColor(255, 255, 255, 100)

FONT_FAMILY = "Segoe UI"

# ── QSS Stylesheets ─────────────────────────────────────

CLOSE_BTN_QSS = """
QPushButton {
    background: rgba(255,255,255,0.08);
    color: white;
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 20px;
    font-size: 18px;
    font-family: Segoe UI;
}
QPushButton:hover {
    background: rgba(233,69,96,0.5);
    border-color: rgba(233,69,96,0.6);
}
"""

BRAND_LABEL_QSS = """
QLabel {
    color: rgba(255,255,255,0.92);
    font-size: 17px;
    font-weight: 600;
    font-family: Segoe UI;
    background: transparent;
}
"""

TOOLBAR_FRAME_QSS = """
QFrame {
    background: rgba(20,20,35,0.88);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 28px;
}
"""

MODE_BTN_QSS = """
QPushButton {{
    background: {bg};
    color: {fg};
    border: 1px solid {border};
    border-radius: 22px;
    padding: 8px 20px;
    font-size: 13px;
    font-weight: 500;
    font-family: Segoe UI;
    min-width: 90px;
}}
QPushButton:hover {{
    background: {hover_bg};
}}
"""

SEARCH_INPUT_QSS = """
QLineEdit {
    background: rgba(255,255,255,0.06);
    color: white;
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 22px;
    padding: 10px 20px;
    font-size: 14px;
    font-family: Segoe UI;
    selection-background-color: rgba(233,69,96,0.4);
}
QLineEdit:focus {
    border-color: rgba(233,69,96,0.6);
    background: rgba(255,255,255,0.09);
}
"""

POPUP_FRAME_QSS = """
QFrame {
    background: rgba(22,22,40,0.94);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 16px;
}
"""

POPUP_TEXT_QSS = """
QTextEdit {
    background: rgba(255,255,255,0.04);
    color: white;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding: 10px;
    font-size: 14px;
    font-family: Segoe UI;
    selection-background-color: rgba(233,69,96,0.4);
}
"""

POPUP_BTN_PRIMARY_QSS = """
QPushButton {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 rgba(233,69,96,0.85), stop:1 rgba(200,50,80,0.85));
    color: white;
    border: none;
    border-radius: 12px;
    padding: 9px 22px;
    font-size: 13px;
    font-weight: 600;
    font-family: Segoe UI;
}
QPushButton:hover {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 rgba(233,69,96,1.0), stop:1 rgba(220,60,90,1.0));
}
"""

POPUP_BTN_SECONDARY_QSS = """
QPushButton {
    background: rgba(255,255,255,0.07);
    color: rgba(255,255,255,0.88);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 12px;
    padding: 9px 18px;
    font-size: 13px;
    font-family: Segoe UI;
}
QPushButton:hover {
    background: rgba(255,255,255,0.14);
    border-color: rgba(255,255,255,0.20);
}
"""

TOAST_QSS = """
QLabel {
    background: rgba(78,204,163,0.92);
    color: white;
    border-radius: 18px;
    padding: 10px 24px;
    font-size: 13px;
    font-weight: 600;
    font-family: Segoe UI;
}
"""

HINT_LABEL_QSS = """
QLabel {
    color: rgba(255,255,255,0.45);
    font-size: 12px;
    font-family: Segoe UI;
    background: transparent;
}
"""
