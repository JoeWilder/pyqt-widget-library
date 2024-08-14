from PyQt6.QtWidgets import QGraphicsPolygonItem


class PolygonItemNode(QGraphicsPolygonItem):
    def __init__(self, polygon_item: QGraphicsPolygonItem, next=None, previous=None):
        self.next = next
        self.previous = previous
        self.points = []
        self.mask = None
        super().__init__(polygon_item)
