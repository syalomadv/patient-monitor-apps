import sys
from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout, QGraphicsDropShadowEffect
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class VitalSignWidget(QWidget):
    """
    A reusable widget for displaying vital signs in a patient monitor UI,
    with hierarchical layout: small label, large value+unit, supplementary data.
    """
    def __init__(self, label, value, unit="", color="#FFFFFF", supplementary="", parent=None):
        """
        Initialize the VitalSignWidget.

        Args:
            label (str): The label for the vital sign (e.g., "HR", "SpO2").
            value (str): The current value (e.g., "75", "98").
            unit (str): The unit for the value (e.g., "bpm", "%").
            color (str): Hex color code for the value text.
            supplementary (str): Supplementary data below value.
            parent (QWidget): Parent widget.
        """
        super().__init__(parent)
        self.label = label
        self.value = value
        self.unit = unit
        self.color = color
        self.supplementary = supplementary

        self.setStyleSheet("background-color: #000000; border: none;")

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(2)

        # Small label
        self.label_label = QLabel(self.label)
        self.label_label.setAlignment(Qt.AlignCenter)
        self.label_label.setFont(QFont("Arial", 10))
        self.label_label.setStyleSheet("color: #888888; background-color: transparent;")
        layout.addWidget(self.label_label)

        # Large value + unit
        self.value_label = QLabel(f"{self.value} {self.unit}")
        self.value_label.setAlignment(Qt.AlignCenter)
        if self.label == "CO2":
            self.value_label.setFont(QFont("Monospace", 12, QFont.Bold))  # Smaller font for CO2 hierarchy
            self.value_label.setStyleSheet(f"color: {self.color}; background-color: transparent;")
        else:
            self.value_label.setFont(QFont("Monospace", 48, QFont.Bold))  # Monospace for others
            self.value_label.setStyleSheet(f"color: {self.color}; background-color: transparent;")
        layout.addWidget(self.value_label)

        # Supplementary label
        self.supplementary_label = QLabel(self.supplementary)
        self.supplementary_label.setAlignment(Qt.AlignCenter)
        self.supplementary_label.setFont(QFont("Arial", 10))
        self.supplementary_label.setStyleSheet("color: #CCCCCC; background-color: transparent;")
        layout.addWidget(self.supplementary_label)

    def update_value(self, new_value, new_unit=None):
        """
        Update the displayed value and optionally the unit.

        Args:
            new_value (str): The new value.
            new_unit (str): The new unit (optional).
        """
        if new_unit is not None:
            self.unit = new_unit
        self.value = new_value
        self.value_label.setText(f"{self.value} {self.unit}")

    def update_supplementary(self, new_supplementary):
        """
        Update the supplementary data.

        Args:
            new_supplementary (str): New supplementary text.
        """
        self.supplementary = new_supplementary
        self.supplementary_label.setText(self.supplementary)

    def set_color(self, new_color):
        """
        Update the value text color.

        Args:
            new_color (str): New hex color code.
        """
        self.color = new_color
        self.value_label.setStyleSheet(f"color: {self.color}; background-color: transparent;")
