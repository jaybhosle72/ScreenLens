# ScreenLens 🔍

**By Jay Bhosle**

ScreenLens is a ridiculously fast, offline "Live Text" desktop tool for Windows. It lets you instantly copy unselectable text from images, PDFs, protected websites, or even code from YouTube video tutorials.

It runs quietly in your background. Whenever you see something you want to copy, press the hotkey, draw a rectangle, and swipe the text. Done.

## Features
- ⚡ **Instant Capture:** Scans only the specific area you draw, making extraction near-instant.
- 🎯 **"Live Text" Selection:** Puts transparent blue selection bubbles over detected words so you can highlight exactly what you need.
- 🔒 **100% Offline & Private:** Uses an embedded `ONNXRuntime` AI engine. No cloud APIs, no internet needed, and no rate limits.
- 💻 **Frictionless UI:** Doesn't clutter your screen with toolbars. Press `Ctrl+Shift+S`, grab what you need, and the overlay disappears completely.

## Installation

You do not need to know Python or how to use a terminal to use ScreenLens.

1. Go to the **Releases** tab on the right side of this GitHub page.
2. Download `ScreenLens-Installer.exe`.
3. Double-click the installer to install it.
4. (*Optional*) Keep "Run on Startup" checked so the tool is always ready whenever you turn on your PC.

## How to Use

1. Press **`Ctrl+Shift+S`**. Your screen will slightly dim.
2. Drag a rectangle over any image or YouTube video. Let go of the mouse.
3. The AI will instantly scan the rectangle. "Live Text" bubbles will appear over any words it finds.
4. Drag your cursor (I-beam) over the blue text bubbles you want to copy.
5. Let go of your mouse. The text is perfectly copied to your clipboard and ScreenLens gracefully closes.

## Built With

- **Python** & **PyQt5** for the heavily customized transparent overlay engine.
- **RapidOCR (ONNXRuntime)** for lightweight, blistering-fast text recognition.

## License
MIT License. Feel free to fork and improve!
