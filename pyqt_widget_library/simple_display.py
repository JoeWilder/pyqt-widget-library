from PyQt6.QtWidgets import QLabel, QVBoxLayout, QFileDialog
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from .base_display import BaseDisplay


class SimpleDisplay(BaseDisplay):
    def __init__(self):
        super().__init__()
        self.pixmap = None

    def init_gui(self):
        layout = QVBoxLayout(self)
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setScaledContents(True)
        layout.addWidget(self.image_label)

    def display_image(self, image_path: str):
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            self.pixmap = pixmap
            self.update_image()
        else:
            print("Failed to load image.")

    def update_image(self):
        if self.pixmap:
            scaled_pixmap = self.pixmap.scaled(
                self.image_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.image_label.setPixmap(scaled_pixmap)

    def clear_image(self):
        self.image_label.clear()
        self.pixmap = None

    def open_image(self, file_type: str = "Images", supported_extensions: list[str] = ["png", "jpg", "jpeg"]):
        supported_extensions_str = f"{file_type} ("
        for ext in supported_extensions:
            if ext[0] != ".":
                ext = "." + ext
            supported_extensions_str += "*" + ext + " "
        supported_extensions_str = supported_extensions_str.strip() + ")"

        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", supported_extensions_str)
        if file_name:
            self.display_image(file_name)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_image()
