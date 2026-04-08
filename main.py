import sys
import os

# IMPORTANT CRITICAL FIX: We MUST import onnxruntime before PyQt5, otherwise PyQt5 loads
# conflicting MSVC/OpenMP DLLs, causing onnxruntime to throw WinError 1114 on Windows!
try:
    import onnxruntime
    from rapidocr_onnxruntime import RapidOCR
    # Pre-initialize just to be safe
    _ = RapidOCR()
except ImportError:
    pass

from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QPen, QFont
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from capture import capture_active_screen, pixmap_to_pil
from ocr_engine import OCREngine
from overlay import ScreenOverlay


class HotkeyBridge(QObject):
    activated = pyqtSignal()


def _make_icon():
    px = QPixmap(64, 64)
    px.fill(Qt.transparent)
    p = QPainter(px)
    p.setRenderHint(QPainter.Antialiasing)
    p.setPen(QPen(QColor(233, 69, 96), 5))
    p.setBrush(QColor(233, 69, 96, 45))
    p.drawEllipse(8, 4, 36, 36)
    p.setPen(QPen(QColor(255, 255, 255), 6, cap=Qt.RoundCap))
    p.drawLine(38, 36, 54, 52)
    p.setPen(QColor(255, 255, 255, 200))
    p.setFont(QFont("Segoe UI", 16, QFont.Bold))
    p.drawText(14, 8, 28, 28, Qt.AlignCenter, "S")
    p.end()
    return QIcon(px)


class ScreenLensApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)

        self.ocr = OCREngine()
        self.overlay = None

        # Tray
        self.tray = QSystemTrayIcon(_make_icon(), self.app)
        self.tray.setToolTip("ScreenLens — Ctrl+Shift+S")

        menu = QMenu()
        menu.addAction("🔍  Activate").triggered.connect(self._activate)
        menu.addSeparator()
        menu.addAction("✕  Quit").triggered.connect(self._quit)
        self.tray.setContextMenu(menu)
        self.tray.activated.connect(
            lambda r: self._activate() if r == QSystemTrayIcon.DoubleClick else None
        )
        self.tray.show()

        # Hotkey
        self.bridge = HotkeyBridge()
        self.bridge.activated.connect(self._activate)
        try:
            import keyboard
            keyboard.add_hotkey("ctrl+shift+s", lambda: self.bridge.activated.emit(), suppress=True)
        except Exception as e:
            print(f"[WARN] Hotkey error: {e}")

        self.tray.showMessage("ScreenLens", "Press Ctrl+Shift+S to activate", QSystemTrayIcon.Information, 2500)

    def _activate(self):
        if self.overlay:
            return
        pixmap, geo = capture_active_screen()
        pil_img = pixmap_to_pil(pixmap)
        self.overlay = ScreenOverlay(pixmap, pil_img, geo, self.ocr)
        self.overlay.closed.connect(self._on_closed)
        self.overlay.copied.connect(self._on_copied)

    def _on_copied(self, text):
        snip = text[:50] + "..." if len(text) > 50 else text
        self.tray.showMessage("Text Copied!", snip, QSystemTrayIcon.Information, 2500)

    def _on_closed(self):
        self.overlay = None

    def _quit(self):
        try:
            import keyboard
            keyboard.unhook_all()
        except Exception:
            pass
        self.tray.hide()
        self.app.quit()

    def run(self):
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    ScreenLensApp().run()
