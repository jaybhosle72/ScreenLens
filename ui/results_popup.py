"""Results popup shown after OCR completes."""

from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTextEdit, QGraphicsOpacityEffect,
)
from ui.styles import (
    POPUP_FRAME_QSS, POPUP_TEXT_QSS,
    POPUP_BTN_PRIMARY_QSS, POPUP_BTN_SECONDARY_QSS,
)


class ResultsPopup(QFrame):
    """Glassmorphism popup displaying OCR results with action buttons."""

    search_clicked = pyqtSignal(str)
    copy_text_clicked = pyqtSignal(str)
    copy_image_clicked = pyqtSignal()
    close_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(POPUP_FRAME_QSS)
        self.setFixedWidth(380)
        self.setMaximumHeight(320)

        self._build_ui()

        # Fade-in effect
        self._opacity = QGraphicsOpacityEffect(self)
        self._opacity.setOpacity(0.0)
        self.setGraphicsEffect(self._opacity)

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 14, 16, 14)
        root.setSpacing(12)

        # Header
        header = QHBoxLayout()
        title = QLabel("Extracted Text")
        title.setStyleSheet("color:white; font-size:14px; font-weight:600; font-family:Segoe UI; background:transparent;")
        header.addWidget(title)
        header.addStretch()

        close_btn = QPushButton("✕")
        close_btn.setFixedSize(28, 28)
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet(
            "QPushButton{background:rgba(255,255,255,0.08);color:white;border:none;"
            "border-radius:14px;font-size:14px;font-family:Segoe UI;}"
            "QPushButton:hover{background:rgba(233,69,96,0.5);}"
        )
        close_btn.clicked.connect(self._on_close)
        header.addWidget(close_btn)
        root.addLayout(header)

        # Text area
        self.text_edit = QTextEdit()
        self.text_edit.setStyleSheet(POPUP_TEXT_QSS)
        self.text_edit.setMaximumHeight(140)
        self.text_edit.setPlaceholderText("No text detected")
        root.addWidget(self.text_edit)

        # Action buttons
        btns = QHBoxLayout()
        btns.setSpacing(8)

        self.search_btn = QPushButton("🔍 Search")
        self.search_btn.setCursor(Qt.PointingHandCursor)
        self.search_btn.setStyleSheet(POPUP_BTN_PRIMARY_QSS)
        self.search_btn.clicked.connect(lambda: self.search_clicked.emit(self.text_edit.toPlainText()))
        btns.addWidget(self.search_btn)

        self.copy_txt_btn = QPushButton("📋 Copy Text")
        self.copy_txt_btn.setCursor(Qt.PointingHandCursor)
        self.copy_txt_btn.setStyleSheet(POPUP_BTN_SECONDARY_QSS)
        self.copy_txt_btn.clicked.connect(lambda: self.copy_text_clicked.emit(self.text_edit.toPlainText()))
        btns.addWidget(self.copy_txt_btn)

        self.copy_img_btn = QPushButton("🖼 Copy Image")
        self.copy_img_btn.setCursor(Qt.PointingHandCursor)
        self.copy_img_btn.setStyleSheet(POPUP_BTN_SECONDARY_QSS)
        self.copy_img_btn.clicked.connect(lambda: self.copy_image_clicked.emit())
        btns.addWidget(self.copy_img_btn)

        root.addLayout(btns)

    # ── public API ───────────────────────────────────────

    def show_results(self, text, x, y):
        """Display the popup near the given screen coordinates."""
        self.text_edit.setPlainText(text)

        # Position: prefer below-right; clamp to parent bounds
        parent = self.parent()
        if parent:
            px = min(x, parent.width() - self.width() - 20)
            py = min(y + 16, parent.height() - self.height() - 20)
            px = max(20, px)
            py = max(20, py)
            self.move(int(px), int(py))

        self.show()
        self.raise_()
        self._animate_in()

    def _animate_in(self):
        anim = QPropertyAnimation(self._opacity, b"opacity", self)
        anim.setDuration(250)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.start()
        self._fade_anim = anim  # prevent GC

    def _on_close(self):
        self.hide()
        self.close_clicked.emit()
