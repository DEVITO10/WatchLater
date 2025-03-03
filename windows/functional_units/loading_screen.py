from PySide6.QtGui import QIcon, QPixmap, QMovie
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit
from PySide6.QtCore import Qt
from font_loader import load_fonts

class LoadingScreen(QWidget):
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

        load_dialog = QWidget()
        load_dialog.setContentsMargins(20, 0, 20, 0)
        load_dialog.setStyleSheet("""
            background-color: rgba(0,0,0,0.9);
        """)

        main_conatiner = QVBoxLayout()
        main_conatiner.setAlignment(Qt.AlignCenter)

        self.gif_label = QLabel()
        self.gif_label.setFixedSize(size*2, size*2)
        self.gif_label.setAlignment(Qt.AlignCenter)

        self.movie = QMovie("./icons/loading.gif")
        self.gif_label.setMovie(self.movie)
        self.movie.setScaledSize(self.gif_label.size())
        self.movie.start()

        self.text_label = QLabel("Fetching Results...")
        self.text_label.setStyleSheet(f"""
            background-color: rgba(0,0,0,0);
            border:0px;
            font-family: Lora;
            font-weight: bold;
            font-size: {size}px;
            color: #FFD369;
        """)
        self.text_label.setAlignment(Qt.AlignCenter)

        main_conatiner.addWidget(self.gif_label, alignment=Qt.AlignCenter)
        main_conatiner.addWidget(self.text_label, alignment=Qt.AlignCenter)

        load_dialog.setLayout(main_conatiner)

        layout.addWidget(load_dialog)

        self.setLayout(layout)
