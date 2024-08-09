import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QFileDialog
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class BaseDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.init_gui()

    def init_gui(self):
        raise NotImplementedError("Subclasses should implement this!")
