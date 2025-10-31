import sys
from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class NibpMainWidget(QWidget):
    """
    Dominant NIBP reading widget with label, main reading, MAP, and vertical scale.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            background-color: #000000;
            color: #FFFFFF;
            font-family: Arial, sans-serif;
            border: none;
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)

        # Label above main reading: "NIBP mmHg"
        self.nibp_label = QLabel("NIBP mmHg")
        self.nibp_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(self.nibp_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Main NIBP reading: "120/80" (larger, bold, monospace)
        self.main_reading = QLabel("120/80")
        self.main_reading.setFont(QFont("Monospace", 48, QFont.Weight.Bold))  # 48pt monospace white
        self.main_reading.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        layout.addWidget(self.main_reading, alignment=Qt.AlignmentFlag.AlignCenter)

        # Mean arterial pressure below: "(93)"
        self.map_label = QLabel("(93)")
        self.map_label.setFont(QFont("Monospace", 36, QFont.Weight.Bold))  # Adjusted for hierarchy, monospace
        self.map_label.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        layout.addWidget(self.map_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Vertical scale indicators: 160 at top, bar in middle, 90 at bottom
        scale_layout = QVBoxLayout()
        scale_layout.setSpacing(5)

        # High scale: "160"
        self.high_scale_label = QLabel("160")
        self.high_scale_label.setFont(QFont("Arial", 10))
        scale_layout.addWidget(self.high_scale_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Vertical bar as a QFrame
        self.scale_bar = QFrame()
        self.scale_bar.setFrameShape(QFrame.Shape.VLine)
        self.scale_bar.setFrameShadow(QFrame.Shadow.Sunken)
        self.scale_bar.setStyleSheet("color: #FFFFFF; background-color: #FFFFFF;")
        self.scale_bar.setFixedWidth(2)
        self.scale_bar.setFixedHeight(50)  # Adjust height as needed
        scale_layout.addWidget(self.scale_bar, alignment=Qt.AlignmentFlag.AlignCenter)

        # Low scale: "90"
        self.low_scale_label = QLabel("90")
        self.low_scale_label.setFont(QFont("Arial", 10))
        scale_layout.addWidget(self.low_scale_label, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(scale_layout)

    def update_data(self, data):
        """
        Update the main reading.

        Args:
            data (dict): With keys 'systolic', 'diastolic', 'map'
        """
        if 'systolic' in data and 'diastolic' in data:
            self.main_reading.setText(f"{data['systolic']}/{data['diastolic']}")
        if 'map' in data:
            self.map_label.setText(f"({data['map']})")
