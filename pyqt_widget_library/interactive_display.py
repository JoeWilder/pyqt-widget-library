from PyQt6.QtWidgets import QLabel, QFileDialog, QPushButton, QGridLayout, QMessageBox, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QFrame
from PyQt6.QtGui import QPixmap, QColor, QBrush, QCursor
from PyQt6.QtCore import Qt, QPoint, pyqtSignal, QStandardPaths, QRectF
from .base_display import BaseDisplay
from .mouse_click_event import MouseClickEvent

SCALE_FACTOR = 1.1
DRAG_SENSITIVITY = 1.25


class InteractiveDisplay(BaseDisplay):
    # coordinates_changed_event = pyqtSignal(QPoint)
    click_event = pyqtSignal(MouseClickEvent)

    def __init__(self):
        super().__init__()

    def init_gui(self):
        self.viewer = self.ImageGraphicsView(self, self.click_event)
        # self.viewer.coordinates_changed.connect(self.handle_coords)
        # self.labelCoords = QLabel(self)
        # self.labelCoords.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignCenter)
        # self.buttonOpen = QPushButton(self)
        # self.buttonOpen.setText("Open Image")
        # self.buttonOpen.clicked.connect(self.handle_open)
        layout = QGridLayout(self)
        layout.addWidget(self.viewer, 0, 0, 1, 3)
        # layout.addWidget(self.buttonOpen, 1, 0, 1, 1)
        # layout.addWidget(self.labelCoords, 1, 2, 1, 1)
        layout.setColumnStretch(2, 2)
        self._path = None

    def handle_coords(self, point):
        if not point.isNull():
            self.labelCoords.setText(f"{point.x()}, {point.y()}")
        else:
            self.labelCoords.clear()

    def handle_open(self):
        if (start := self._path) is None:
            start = QStandardPaths.standardLocations(QStandardPaths.StandardLocation.PicturesLocation)[0]
        if path := QFileDialog.getOpenFileName(self, "Open Image", start)[0]:
            # self.labelCoords.clear()
            if not (pixmap := QPixmap(path)).isNull():
                self.viewer.set_photo(pixmap)
                self._path = path
            else:
                QMessageBox.warning(self, "Error", f"<br>Could not load image file:<br>" f"<br><b>{path}</b><br>")

    class ImageGraphicsView(QGraphicsView):
        coordinates_changed = pyqtSignal(QPoint)

        def __init__(self, parent, click_event):
            super().__init__(parent)
            self._click_event = click_event
            self._expected_button_types = [Qt.MouseButton.LeftButton, Qt.MouseButton.MiddleButton, Qt.MouseButton.RightButton]
            self._zoom = 0
            self._empty = True
            self._scene = QGraphicsScene(self)
            self._photo = QGraphicsPixmapItem()
            self._photo.setShapeMode(QGraphicsPixmapItem.ShapeMode.BoundingRectShape)
            self._scene.addItem(self._photo)
            self.setScene(self._scene)
            self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
            self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
            self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.setBackgroundBrush(QBrush(QColor(30, 30, 30)))
            self.setFrameShape(QFrame.Shape.NoFrame)

            self.is_dragging = False
            self.last_mouse_position = None

        def has_photo(self):
            return not self._empty

        def reset_view(self, scale=1):
            rect = QRectF(self._photo.pixmap().rect())
            if not rect.isNull():
                self.setSceneRect(rect)
                if (scale := max(1, scale)) == 1:
                    self._zoom = 0
                if self.has_photo():
                    unity = self.transform().mapRect(QRectF(0, 0, 1, 1))
                    self.scale(1 / unity.width(), 1 / unity.height())
                    viewrect = self.viewport().rect()
                    scenerect = self.transform().mapRect(rect)
                    factor = min(viewrect.width() / scenerect.width(), viewrect.height() / scenerect.height()) * scale
                    self.scale(factor, factor)
                    self.centerOn(self._photo)
                    self.updateCoordinates()

        def set_photo(self, pixmap=None):
            if pixmap and not pixmap.isNull():
                self._empty = False
                self.setDragMode(QGraphicsView.DragMode.NoDrag)
                self._photo.setPixmap(pixmap)
            else:
                self._empty = True
                self.setDragMode(QGraphicsView.DragMode.NoDrag)
                self._photo.setPixmap(QPixmap())
            self._zoom = 0
            self.reset_view(SCALE_FACTOR**self._zoom)

        def zoom_level(self):
            return self._zoom

        def zoom(self, step):
            zoom = max(0, self._zoom + (step := int(step)))
            if zoom != self._zoom:
                self._zoom = zoom
                if self._zoom > 0:
                    if step > 0:
                        factor = SCALE_FACTOR**step
                    else:
                        factor = 1 / SCALE_FACTOR ** abs(step)
                    self.scale(factor, factor)
                else:
                    self.reset_view()

        def wheelEvent(self, event):
            delta = event.angleDelta().y()
            self.zoom(delta and delta // abs(delta))

        def resizeEvent(self, event):
            super().resizeEvent(event)
            self.reset_view()

        def toggleDragMode(self):
            if self.dragMode() == QGraphicsView.DragMode.ScrollHandDrag:
                self.setDragMode(QGraphicsView.DragMode.NoDrag)
            elif not self._photo.pixmap().isNull():
                self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)

        def updateCoordinates(self, pos=None):
            if self._photo.isUnderMouse():
                if pos is None:
                    pos = self.mapFromGlobal(QCursor.pos())
                point = self.mapToScene(pos).toPoint()
            else:
                point = QPoint()
            self.coordinates_changed.emit(point)

        def mouseMoveEvent(self, event):
            if self.is_dragging:
                delta = event.position().toPoint() - self.last_mouse_position
                # Invert the direction and apply drag sensitivity
                self.horizontalScrollBar().setValue(int(self.horizontalScrollBar().value() - delta.x() * DRAG_SENSITIVITY))
                self.verticalScrollBar().setValue(int(self.verticalScrollBar().value() - delta.y() * DRAG_SENSITIVITY))
                self.last_mouse_position = event.position().toPoint()

            else:
                self.updateCoordinates(event.position().toPoint())

            super().mouseMoveEvent(event)

        def mousePressEvent(self, event):

            if event.button() == Qt.MouseButton.MiddleButton:
                self.is_dragging = True
                self.last_mouse_position = event.position().toPoint()
                self.setCursor(Qt.CursorShape.ClosedHandCursor)

            if event.button() in self._expected_button_types:
                unscaled_x = int(event.pos().x())
                unscaled_y = int(event.pos().y())
                position = self.mapToScene(unscaled_x, unscaled_y)
                coordinates = (position.x(), position.y())

                click_event = MouseClickEvent(event.button(), coordinates)
                self._click_event.emit(click_event)

            super().mousePressEvent(event)

        def mouseReleaseEvent(self, event):
            if event.button() == Qt.MouseButton.MiddleButton:
                self.is_dragging = False
                self.setCursor(Qt.CursorShape.ArrowCursor)

            super().mouseReleaseEvent(event)

        def leaveEvent(self, event):
            self.coordinates_changed.emit(QPoint())
            super().leaveEvent(event)
