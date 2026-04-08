from PyQt5.QtWidgets import QApplication
from mss.windows import MSS as mss
from PIL import Image

def capture_active_screen():
    screen = QApplication.primaryScreen()
    pixmap = screen.grabWindow(QApplication.desktop().winId())
    return pixmap, QApplication.desktop().screenGeometry()

def pixmap_to_pil(pixmap):
    image = pixmap.toImage()
    size = image.size()
    s = image.bits().asstring(size.width() * size.height() * image.depth() // 8)
    return Image.frombytes('RGBA', (size.width(), size.height()), s, 'raw', 'BGRA')

def crop_pil_region(pil_img, x, y, w, h):
    try:
        return pil_img.crop((x, y, x + w, y + h))
    except Exception as e:
        print("Crop error:", e)
        return None
