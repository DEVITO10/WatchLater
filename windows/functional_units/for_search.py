import time
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QLineEdit
from PySide6.QtCore import Qt, QTimer, QThread, Signal
from font_loader import load_fonts
from fetch_search_results import start_search
from functional_units.loading_screen import LoadingScreen

class SearchThread(QThread):
    def __init__(self, query):
        super().__init__()
        self.query = query

    def run(self):
        start_search(self.query)
        self.finished.emit()

class SearchPopup(QWidget):
    def __init__(self, parent=None, width=0, height=0):
        super().__init__(parent)

        load_fonts()
        self.width = width
        self.height = height
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

        main_conatiner = QVBoxLayout()
        main_conatiner.setAlignment(Qt.AlignCenter)

        # Row for Search Label and Close button
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

        self.close_btn = QPushButton()
        self.close_btn.setFixedSize(height*0.05, height*0.05)
        self.close_btn.setIcon(QIcon("icons/close.svg"))
        self.close_btn.setIconSize(self.close_btn.sizeHint())
        self.close_btn.setStyleSheet("background-color: rgba(0,0,0,0);")
        self.close_btn.clicked.connect(lambda: SearchPopup.close(self))

        row_1.addWidget(label)
        row_1.addWidget(self.close_btn)

        # Row for Search Input Box
        row_2 = QHBoxLayout()
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Enter 3 or more char...")
        self.input_field.setStyleSheet(f"""
                                  font-family: Lora;
                                  font-weight: bold;
                                  font-size: {size/1.5}px;
                                  color: black;
                                  background-color: white;
                                  border: 2px solid #FFD369""")
        self.input_field.textChanged.connect(self.toggle_button)

        row_2.addWidget(self.input_field)

        # Row for Search Button
        row_3 = QHBoxLayout()
        self.submit_button = QPushButton("Search", self)
        self.submit_button.setStyleSheet(f"""
                                  font-family: Lora;
                                  font-weight: bold;
                                  font-size: {size/1.5}px;
                                  color: black;
                                  background-color: #FFD369;
                                  border: 2px solid #FFD369;""")
        self.submit_button.setEnabled(False)
        self.submit_button.setIcon(QIcon("icons/search_black.svg"))
        self.submit_button.setIconSize(self.submit_button.sizeHint())
        self.submit_button.clicked.connect(self.search_clicked)

        row_3.addWidget(self.submit_button)

        main_conatiner.addLayout(row_1)
        main_conatiner.addLayout(row_2)
        main_conatiner.addLayout(row_3)

        search_dialog.setLayout(main_conatiner)

        layout.addWidget(search_dialog)

        self.setLayout(layout)

    def toggle_button(self):
        if(len(self.input_field.text()) >= 3):
            self.submit_button.setEnabled(True)
        else:
            self.submit_button.setEnabled(False)
    
    def search_clicked(self):
        SearchPopup.close(self)
        self.loading_screen = LoadingScreen(self.parent(), width=self.width, height=self.height)
        self.loading_screen.show()

        self.search_thread = SearchThread(self.input_field.text())
        self.search_thread.start()
        self.search_thread.finished.connect(self.show_results)

    def show_results(self):
        self.loading_screen.close()
