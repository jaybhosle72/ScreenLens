"""ScreenLens — Draw Region, Then Select Text.

1. Draw a rectangle over an area.
2. It instantly scans only that area.
3. Hover and drag over the detected text blocks to copy them.
"""

from PyQt5.QtCore import Qt, QRect, QPoint, pyqtSignal
from PyQt5.QtGui import QColor, QPainter, QPen, QImage, QFont, QCursor
from PyQt5.QtWidgets import QWidget

from capture import crop_pil_region
from clipboard_utils import copy_text

class ScreenOverlay(QWidget):
    closed = pyqtSignal()
    copied = pyqtSignal(str)

    def __init__(self, screenshot_pixmap, screenshot_pil, geometry, ocr_engine):
        super().__init__()
        self.screenshot_pixmap = screenshot_pixmap
        self.screenshot_pil = screenshot_pil
        self.ocr_engine = ocr_engine

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setGeometry(geometry)
        self.setCursor(Qt.CrossCursor)
        self.setMouseTracking(True)

        self.mode = "draw_region" # "draw_region", "processing", "select_text"
        
        # Region drawing
        self.rect_start = None
        self.rect_end = None
        self.ocr_rect = None
        
        self.text_regions = [] # {'rect': QRect, 'text': str, 'selected': bool, 'hover': bool}
        self.ocr_worker = None

        # Text selecting
        self.select_start = None
        self.select_end = None

        self.show()
        self.activateWindow()

    # ─── PAINTING ────────────────────────────────────────

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.SmoothPixmapTransform)

        # 1. Base Screenshot
        p.drawPixmap(0, 0, self.screenshot_pixmap)

        # 2. Dim overlay
        overlay = QImage(self.size(), QImage.Format_ARGB32_Premultiplied)
        if self.mode == "draw_region":
            overlay.fill(QColor(0, 0, 0, 110))
        else:
            overlay.fill(QColor(0, 0, 0, 150)) # Dim darker outside the finalized bounding box

        # Cut out the drawn region
        draw_r = None
        if self.mode == "draw_region" and self.rect_start and self.rect_end:
            draw_r = QRect(self.rect_start, self.rect_end).normalized()
        elif self.mode in ("processing", "select_text") and self.ocr_rect:
            draw_r = self.ocr_rect

        if draw_r:
            op = QPainter(overlay)
            op.setCompositionMode(QPainter.CompositionMode_DestinationOut)
            op.fillRect(draw_r, QColor(0, 0, 0, 255))
            op.end()

        p.drawImage(0, 0, overlay)

        # Draw the boundary of the region
        if draw_r:
            p.setPen(QPen(QColor(255, 255, 255, 180), 2))
            p.setBrush(Qt.NoBrush)
            p.drawRect(draw_r)

        if self.mode == "draw_region":
            p.setPen(Qt.white)
            p.setFont(QFont("Segoe UI", 12, QFont.Bold))
            p.drawText(self.rect().adjusted(0, 40, 0, 0), Qt.AlignTop | Qt.AlignHCenter, 
                       "1. Draw a rectangle around the text")
                       
        elif self.mode == "processing":
            p.setPen(Qt.white)
            p.setFont(QFont("Segoe UI", 12, QFont.Bold))
            p.drawText(self.ocr_rect, Qt.AlignCenter, "Scanning...")

        elif self.mode == "select_text":
            # Draw text regions (Google Lens style)
            for region in self.text_regions:
                r = region['rect']
                
                # Google lens style: rounded blue backgrounds when selected, faint white when available
                if region['selected']:
                    p.setPen(Qt.NoPen)
                    p.setBrush(QColor(66, 133, 244, 150)) # Google Blue
                elif region['hover']:
                    p.setPen(Qt.NoPen)
                    p.setBrush(QColor(255, 255, 255, 80))
                else:
                    p.setPen(Qt.NoPen)
                    p.setBrush(QColor(255, 255, 255, 30))
                
                pad_rect = r.adjusted(-3, -2, 3, 2)
                p.drawRoundedRect(pad_rect, 6, 6)

            # Draw drag selection box over text
            if self.select_start and self.select_end:
                sel_rect = QRect(self.select_start, self.select_end).normalized()
                p.setPen(QPen(QColor(66, 133, 244, 200), 1))
                p.setBrush(QColor(66, 133, 244, 30))
                p.drawRect(sel_rect)
            
            p.setPen(Qt.white)
            p.setFont(QFont("Segoe UI", 12, QFont.Bold))
            p.drawText(self.rect().adjusted(0, 40, 0, 0), Qt.AlignTop | Qt.AlignHCenter, 
                       "2. Swipe to highlight text (or Right Click to cancel)")

        p.end()

    # ─── MOUSE ───────────────────────────────────────────

    def mousePressEvent(self, e):
        if e.button() == Qt.RightButton:
            self.close_overlay()
            return

        if e.button() == Qt.LeftButton:
            if self.mode == "draw_region":
                self.rect_start = e.pos()
                self.rect_end = e.pos()
                self.update()
            elif self.mode == "select_text":
                self.select_start = e.pos()
                self.select_end = e.pos()
                for region in self.text_regions:
                    region['selected'] = False
                self.update()

    def mouseMoveEvent(self, e):
        if self.mode == "draw_region" and self.rect_start:
            self.rect_end = e.pos()
            self.update()
            
        elif self.mode == "select_text":
            if self.select_start: # Dragging to select
                self.select_end = e.pos()
                sel_rect = QRect(self.select_start, self.select_end).normalized()
                for region in self.text_regions:
                    region['selected'] = region['rect'].intersects(sel_rect)
                self.update()
            else: # Hovering
                hovered = False
                for region in self.text_regions:
                    if region['rect'].adjusted(-3, -2, 3, 2).contains(e.pos()):
                        region['hover'] = True
                        hovered = True
                    else:
                        region['hover'] = False
                        
                if hovered:
                    self.setCursor(Qt.IBeamCursor)
                else:
                    self.setCursor(Qt.ArrowCursor)
                self.update()

    def mouseReleaseEvent(self, e):
        if e.button() != Qt.LeftButton:
            return
            
        if self.mode == "draw_region" and self.rect_start:
            self.rect_end = e.pos()
            self.ocr_rect = QRect(self.rect_start, self.rect_end).normalized()
            
            if self.ocr_rect.width() < 10 or self.ocr_rect.height() < 10:
                self.close_overlay()
                return

            self.mode = "processing"
            self.setCursor(Qt.WaitCursor)
            self.update()
            
            self._start_ocr()

        elif self.mode == "select_text" and self.select_start:
            self.select_end = e.pos()
            self._copy_selected_text()

    def _start_ocr(self):
        if not self.ocr_engine.available:
            self.close_overlay()
            return
            
        x, y, w, h = self.ocr_rect.x(), self.ocr_rect.y(), self.ocr_rect.width(), self.ocr_rect.height()
        cropped = crop_pil_region(self.screenshot_pil, x, y, w, h)
        
        self.ocr_worker = self.ocr_engine.extract_text_async(cropped)
        self.ocr_worker.finished.connect(self._on_ocr_done)
        self.ocr_worker.error.connect(self._on_ocr_error)
        self.ocr_worker.start()
        
    def _on_ocr_error(self, msg):
        print(f"OCR ERROR: {msg}")
        self.close_overlay()

    def _on_ocr_done(self, results):
        self.mode = "select_text"
        self.setCursor(Qt.ArrowCursor)
        
        # Offset coordinates by ocr_rect
        ox, oy = self.ocr_rect.x(), self.ocr_rect.y()
        self.text_regions = []
        for bbox, text, conf in results:
            x, y, w, h = bbox
            self.text_regions.append({
                'rect': QRect(x + ox, y + oy, w, h),
                'text': text,
                'selected': False,
                'hover': False
            })
            
        self.update()

    def _copy_selected_text(self):
        selected_regions = [r for r in self.text_regions if r['selected']]
        if not selected_regions:
            # Maybe they just clicked a single box?
            selected_regions = [r for r in self.text_regions if r['hover']]
            
        if not selected_regions:
            self.select_start = None
            self.select_end = None
            self.update()
            return

        selected_regions.sort(key=lambda r: (r['rect'].y() // 15, r['rect'].x()))
        
        final_text_lines = []
        current_y_group = -1
        current_line = []
        
        for region in selected_regions:
            y_group = region['rect'].y() // 15
            if current_y_group == -1:
                current_y_group = y_group
                
            if abs(y_group - current_y_group) <= 1:
                current_line.append(region['text'])
            else:
                final_text_lines.append(" ".join(current_line))
                current_line = [region['text']]
                current_y_group = y_group
                
        if current_line:
            final_text_lines.append(" ".join(current_line))

        full_text = "\n".join(final_text_lines).strip()
        
        if full_text:
            copy_text(full_text)
            self.copied.emit(full_text)
            
        self.close_overlay()

    # ─── KEYBOARD & WINDOW ──────────────────────────────

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close_overlay()

    def close_overlay(self):
        if self.ocr_worker and self.ocr_worker.isRunning():
            self.ocr_worker.terminate()
        self.closed.emit()
        self.close()
        self.deleteLater()
