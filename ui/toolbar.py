"""Floating mode toolbar for ScreenLens overlay."""

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QPushButton
from ui.styles import TOOLBAR_FRAME_QSS, MODE_BTN_QSS


class ModeToolbar(QFrame):
    """Bottom toolbar with Circle / Select / Search mode buttons."""

    mode_changed = pyqtSignal(str)  # 'circle', 'select', 'search'

    MODES = [
        ("circle",  "⭕  Circle"),
        ("select",  "▢  Select"),
        ("search",  "🔍  Search"),
    ]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(TOOLBAR_FRAME_QSS)
        self.setFixedHeight(56)
        self._current = "circle"

        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 6, 8, 6)
        layout.setSpacing(6)

        self.buttons = {}
        for mode_id, label in self.MODES:
            btn = QPushButton(label)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setProperty("mode", mode_id)
            btn.clicked.connect(lambda checked, m=mode_id: self._select(m))
            layout.addWidget(btn)
            self.buttons[mode_id] = btn

        self._refresh_styles()

    # ── API ──────────────────────────────────────────────

    def current_mode(self):
        return self._current

    # ── internals ────────────────────────────────────────

    def _select(self, mode_id):
        if mode_id == self._current:
            return
        self._current = mode_id
        self._refresh_styles()
        self.mode_changed.emit(mode_id)

    def _refresh_styles(self):
        for mid, btn in self.buttons.items():
            active = mid == self._current
            btn.setStyleSheet(MODE_BTN_QSS.format(
                bg="rgba(233,69,96,0.75)" if active else "rgba(255,255,255,0.06)",
                fg="white",
                border="rgba(233,69,96,0.8)" if active else "rgba(255,255,255,0.08)",
                hover_bg="rgba(233,69,96,0.9)" if active else "rgba(255,255,255,0.12)",
            ))
