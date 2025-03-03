# color palette
#222831
#393E46
#FFD369
#EEEEEE
import sys
from PySide6.QtGui import QFontDatabase, QIcon, QPixmap, QFont
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLineEdit, QLabel, QSizePolicy
from PySide6.QtCore import Qt

from font_loader import load_fonts
from functional_units.for_search import SearchPopup

class SquareButton(QPushButton):
    def resizeEvent(self, event):
        """ Ensure the button remains square by matching width to height """
        size = event.size().height()
        self.setFixedSize(size, size)
        super().resizeEvent(event)

class ToDoApp(QWidget):

    height = None
    width = None

    def __init__(self,height):
        super().__init__()

        height = (height-100)
        width = ((height-100)*9)//16

        load_fonts()

        self.setWindowTitle("WatchLater")
        self.setFixedSize(width, height)
        self.setStyleSheet("""
            background-color: 222831;
        """)
        self.setWindowIcon(QIcon("icons/icon.png"))

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Title
        title = QLabel("WatchLater", self)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            font-size: {height*0.05}px;
            color: #FFD369;
        """)
        title.setFont(QFont('Rye'))
        title.setFixedSize(width, height*0.1)

        # Main Content
        body = QVBoxLayout()

        row_1 = QLabel("Recently Added", self)
        row_1.setAlignment(Qt.AlignCenter)
        row_1.setStyleSheet(f"""
            font-size: {height*0.02}px;
            color: #FFD369
        """)
        row_1.setFixedSize(width, height*0.04)
        row_1.setFont(QFont('Rye'))

        row_2 = QHBoxLayout()
        row_2.setContentsMargins(10, 10, 10, 10)

        first_item = QLabel()
        pixmap = QPixmap("imdb_image.png")
        scaled_pixmap = pixmap.scaled(first_item.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        first_item.setPixmap(scaled_pixmap)
        first_item.setScaledContents(True)
        first_item.setStyleSheet("""
            border: 3px solid #EEEEEE;
        """)

        second_item = QLabel()
        pixmap = QPixmap("wiki_image.png")
        scaled_pixmap = pixmap.scaled(second_item.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        second_item.setPixmap(scaled_pixmap)
        second_item.setScaledContents(True)
        second_item.setStyleSheet("""
            border: 3px solid #EEEEEE;
        """)

        row_2.addWidget(first_item)
        row_2.addWidget(second_item)

        row_3 = QHBoxLayout()
        row_3.setContentsMargins(10, 10, 10, 10)

        third_item = QLabel()
        pixmap = QPixmap("mdl_image.png")
        scaled_pixmap = pixmap.scaled(third_item.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        third_item.setPixmap(scaled_pixmap)
        third_item.setScaledContents(True)
        third_item.setStyleSheet("""
            border: 3px solid #EEEEEE;
        """)

        fourth_item = QLabel()
        pixmap = QPixmap("mal_image.png")
        scaled_pixmap = pixmap.scaled(fourth_item.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        fourth_item.setPixmap(scaled_pixmap)
        fourth_item.setScaledContents(True)
        fourth_item.setStyleSheet("""
            border: 3px solid #EEEEEE;
        """)

        row_3.addWidget(third_item)
        row_3.addWidget(fourth_item)

        body.addWidget(row_1)
        body.addLayout(row_2)
        body.addLayout(row_3)

        # Taskbar
        taskbar = QWidget()
        taskbar.setFixedSize(width, abs(height*0.08))
        taskbar.setContentsMargins(0, 0, 0, 0)
        taskbar.setStyleSheet("""
            background-color: black;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        """)

        # Taskbar Menus
        taskbar_menu = QHBoxLayout()
        taskbar_menu.setContentsMargins(0, 0, 0, 0)

        self.remove_button_1 = SquareButton()
        self.remove_button_1.setIcon(QIcon("icons/menu.svg"))
        self.remove_button_1.setIconSize(self.remove_button_1.sizeHint())

        self.search_btn = SquareButton()
        self.search_btn.setIcon(QIcon("icons/search.svg"))
        self.search_btn.setIconSize(self.search_btn.sizeHint())
        self.search_btn.clicked.connect(lambda: self.show_search(width, height))
        
        self.remove_button_2 = SquareButton()
        self.remove_button_2.setIcon(QIcon("icons/tick.svg"))
        self.remove_button_2.setIconSize(self.remove_button_2.sizeHint())

        taskbar.setLayout(taskbar_menu)

        taskbar_menu.addWidget(self.remove_button_1)
        taskbar_menu.addWidget(self.search_btn)
        taskbar_menu.addWidget(self.remove_button_2)

        layout.addWidget(title)
        layout.addLayout(body)
        layout.addWidget(taskbar)

        self.setLayout(layout)

        self.popup = None

    def show_search(self, width, height):
        if self.popup:
            self.popup.close()

        self.popup = SearchPopup(self, width=width, height=height)
        self.popup.show()
        

    def add_task(self):
        task = self.task_input.text()
        if task:
            self.task_list.addItem(task)
            self.task_input.clear()
            self.show_popup(f'Task "{task}" added!')

    def remove_task(self):
        selected_item = self.task_list.currentItem()
        if selected_item:
            self.task_list.takeItem(self.task_list.row(selected_item))

    def show_popup(self, message):
        popup = QWidget(self)
        popup.setWindowFlags(popup.windowFlags() | Qt.WindowStaysOnTopHint)
        popup.setGeometry(120, 80, 200, 100)
        popup.setStyleSheet("background-color: black; color: white; padding: 10px; border-radius: 10px;")

        layout = QVBoxLayout()
        label = QLabel(message, popup)
        label.setStyleSheet("color: white;")
        layout.addWidget(label)
        popup.setLayout(layout)

        popup.show()

app = QApplication([])
screen = app.primaryScreen()
screen_size = screen.size()
screen_height = screen_size.height()
window = ToDoApp(screen_height)
window.show()
app.exec()
