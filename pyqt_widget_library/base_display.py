from PyQt6.QtWidgets import QWidget


class BaseDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.init_gui()

    def init_gui(self):
        raise NotImplementedError("Subclasses should implement this!")
