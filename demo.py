import sys
from PyQt6.QtWidgets import QApplication
from pyqt_widget_library.main_window import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create our custom window here. See 'main_window' to see custom displays
    window = MainWindow(type=MainWindow.Type.INTERACTIVE)
    window.display()
    sys.exit(app.exec())
