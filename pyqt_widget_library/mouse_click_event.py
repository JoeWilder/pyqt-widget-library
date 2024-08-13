from enum import Enum


class MouseClickEvent:
    class MouseButton(Enum):
        LEFT_CLICK = ...
        MIDDLE_CLICK = ...
        RIGHT_CLICK = ...

    def __init__(self, button_type: MouseButton, coordinates: tuple[float, float]):
        self._button_type: self.MouseButton = button_type
        self._coordinates = coordinates

    def __str__(self):
        return f"{{type: {self.button_type}, coordinates: {self.coordinates}}}"

    @property
    def button_type(self):
        return self._button_type

    @button_type.setter
    def button_type(self, button_type: MouseButton):
        self._button_type = button_type

    @property
    def coordinates(self):
        return self._coordinates

    @coordinates.setter
    def coordinates(self, coordinates: tuple[float, float]):
        self._coordinates = coordinates
