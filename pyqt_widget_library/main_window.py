from PyQt6.QtWidgets import QWidget, QVBoxLayout, QMainWindow
from pyqt_widget_library.simple_display import SimpleDisplay
from pyqt_widget_library.interactive_display import InteractiveDisplay
from enum import Enum


class MainWindow(QMainWindow):

    class Type(Enum):
        SIMPLE = "simple"
        INTERACTIVE = "interactive"

    def __init__(self, title: str = "Image Display", maximized: bool = False, type: Type | None = None):
        super().__init__()
        self._title = title
        self.setWindowTitle(self._title)
        self.setGeometry(100, 100, 800, 600)
        self.setMinimumSize(100, 100)
        if maximized:
            self.showMaximized()
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        if type is not None:
            self.create_ui(type)

    def create_ui(self, type: Type):
        if type == self.Type.SIMPLE:
            self.simple_display = SimpleDisplay()
            layout = QVBoxLayout(self.central_widget)
            layout.addWidget(self.simple_display)
            self.simple_display.open_image()
        elif type == self.Type.INTERACTIVE:
            self.interactive_display = InteractiveDisplay()
            layout = QVBoxLayout(self.central_widget)
            layout.addWidget(self.interactive_display)
            self.interactive_display.click_event.connect(lambda event: print(event))

    def display(self):
        self.show()
