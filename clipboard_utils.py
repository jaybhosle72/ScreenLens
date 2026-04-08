import io
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QClipboard
from PIL import Image

def copy_text(text):
    QApplication.clipboard().setText(text, QClipboard.Clipboard)

def copy_pil_image(pil_img):
    # Not used directly in new workflow but helpful
    pass
