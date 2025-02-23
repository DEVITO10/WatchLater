from PySide6.QtGui import QFontDatabase
import os

def load_fonts(font_dir="fonts"):
    """Loads all TTF font files from the given directory."""
    font_db = QFontDatabase()
    if not os.path.exists(font_dir):
        print(f"Font directory '{font_dir}' not found!")
        return

    for font_file in os.listdir(font_dir):
        if font_file.endswith(".ttf"):
            font_path = os.path.join(font_dir, font_file)
            font_id = font_db.addApplicationFont(font_path)
            if font_id == -1:
                print(f"Failed to load font: {font_file}")
            else:
                pass
