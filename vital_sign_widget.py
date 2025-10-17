import sys
from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class VitalSignWidget(QWidget):
    """
    A reusable widget for displaying vital signs in a patient monitor UI,
    mimicking the Mindray style with black background, sans-serif fonts,
    specific colors, and glow effects.
    """
    def __init__(self, label, value, unit="", color="#FFFFFF", parent=None):
        """
        Initialize the VitalSignWidget.

        Args:
            label (str): The label for the vital sign (e.g., "HR", "SpO2").
            value (str): The current value (e.g., "75", "98%").
            unit (str): The unit for the value (e.g., "", "%", "bpm"). Defaults to "".
            color (str): Hex color code for the text (e.g., "#00FF00" for green). Defaults to white.
            parent (QWidget): Parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.label = label
        self.value = value
        self.unit = unit
        self.color = color

        self.setStyleSheet("background-color: #000000; border: none;")

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Label
        self.display_label = QLabel(f"{self.label}\n{self.value} {self.unit}")
        self.display_label.setAlignment(Qt.AlignCenter)
        self.display_label.setFont(QFont("Courier New", 24, QFont.Bold))
        self.display_label.setStyleSheet(f"color: {self.color}; background-color: transparent;")

        # Glow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(Qt.white)
        self.display_label.setGraphicsEffect(shadow)

        layout.addWidget(self.display_label)

    def update_value(self, new_value, new_unit=None):
        """
        Update the displayed value and optionally the unit.

        Args:
            new_value (str): The new value to display.
            new_unit (str): The new unit (optional, defaults to current unit).
        """
        if new_unit is not None:
            self.unit = new_unit
        self.value = new_value
        self.display_label.setText(f"{self.label}\n{self.value} {self.unit}")

    def set_color(self, new_color):
        """
        Update the text color.

        Args:
            new_color (str): New hex color code.
        """
        self.color = new_color
        self.display_label.setStyleSheet(f"color: {self.color}; background-color: transparent;")
