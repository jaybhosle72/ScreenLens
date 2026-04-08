import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal

class OCRWorker(QThread):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, image, engine):
        super().__init__()
        self.image = image
        self.engine = engine

    def run(self):
        try:
            results = self.engine._do_ocr(self.image)
            self.finished.emit(results)
        except Exception as e:
            self.error.emit(str(e))

class OCREngine:
    def __init__(self):
        try:
            from rapidocr_onnxruntime import RapidOCR
            self._ocr = RapidOCR()
            self.is_ready = True
        except ImportError:
            self._ocr = None
            self.is_ready = False

    @property
    def available(self):
        return self.is_ready

    def _get_ocr(self):
        return self._ocr

    def extract_text_async(self, pil_image):
        return OCRWorker(pil_image, self)

    def _do_ocr(self, pil_image):
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')
            
        ocr = self._get_ocr()
        arr = np.array(pil_image)
        # Convert RGB to BGR for RapidOCR (standard cv2 format)
        arr_bgr = arr[:, :, ::-1]
        
        result, _ = ocr(arr_bgr)
        if not result:
            return []
        items = []
        for bbox, text, conf in result:
            if not text.strip():
                continue
            xs = [p[0] for p in bbox]
            ys = [p[1] for p in bbox]
            x, y = int(min(xs)), int(min(ys))
            w, h = int(max(xs)) - x, int(max(ys)) - y
            items.append(((x, y, w, h), text, conf))
        return items

    @staticmethod
    def get_plain_text(results):
        return " ".join(r[1] for r in results if r[1].strip())
