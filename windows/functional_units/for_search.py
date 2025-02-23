from PySide6.QtGui import QIcon, QPixmap, QFont
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtCore import Qt
from font_loader import load_fonts

class SearchPopup(QWidget):
    def __init__(self, parent=None, width=0, height=0):
        super().__init__(parent)

        load_fonts()
        
        size = height*0.04

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)  # Always on top, no frame
        self.setFixedSize(width, height)
        self.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("background-color: rgba(0,0,0,0.9); color: white;")

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        search_dialog = QWidget()
        search_dialog.setContentsMargins(20, 0, 20, 0)
        search_dialog.setStyleSheet("""
            background-color: rgba(0,0,0,0.9);
        """)

        row_1 = QHBoxLayout()
        label = QLabel("Search")
        label.setStyleSheet(f"""
            background-color: rgba(0,0,0,0);
            border:0px;
            font-family: Lora;
            font-weight: bold;
            font-size: {size}px;
        """)
        label.setAlignment(Qt.AlignCenter)

        close_btn = QPushButton()
        close_btn.setFixedSize(height*0.05, height*0.05)
        close_btn.setIcon(QIcon("icons/close.svg"))
        close_btn.setIconSize(close_btn.sizeHint())
        close_btn.setStyleSheet("background-color: rgba(0,0,0,0);")
        close_btn.clicked.connect(self.close)

        row_1.addWidget(label)
        row_1.addWidget(close_btn)

        search_dialog.setLayout(row_1)

        layout.addWidget(search_dialog)

        self.setLayout(layout)
