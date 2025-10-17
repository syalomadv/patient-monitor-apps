import sys
from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class TempWidget(QWidget):
    """
    A horizontal widget for displaying Temperature parameters in a patient monitor UI,
    mimicking the Mindray style with black background, sans-serif fonts, white text.
    Displays Temp °C label, T1 and T2 readings vertically stacked, and TD difference.
    """
    def __init__(self, parent=None):
        """
        Initialize the TempWidget.

        Args:
            parent (QWidget): Parent widget. Defaults to None.
        """
        super().__init__(parent)

        self.setStyleSheet("background-color: #000000; border: none;")

        # Main layout: Horizontal
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(10)

        # Left: Temp °C label
        temp_label_layout = QVBoxLayout()
        temp_label_layout.setSpacing(0)

        self.temp_label = QLabel("Temp")
        self.temp_label.setFont(QFont("Segoe UI", 10))
        self.temp_label.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        temp_label_layout.addWidget(self.temp_label, alignment=Qt.AlignCenter)

        self.temp_unit = QLabel("°C")
        self.temp_unit.setFont(QFont("Segoe UI", 10))
        self.temp_unit.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        temp_label_layout.addWidget(self.temp_unit, alignment=Qt.AlignCenter)

        main_layout.addLayout(temp_label_layout)

        # Middle: T1 and T2 vertically stacked
        readings_layout = QVBoxLayout()
        readings_layout.setSpacing(5)

        # T1
        t1_layout = QVBoxLayout()
        t1_layout.setSpacing(0)

        self.t1_label = QLabel("T1")
        self.t1_label.setFont(QFont("Segoe UI", 10))
        self.t1_label.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        t1_layout.addWidget(self.t1_label, alignment=Qt.AlignCenter)

        self.t1_value = QLabel("37.0")
        self.t1_value.setFont(QFont("Courier New", 24, QFont.Bold))
        self.t1_value.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        t1_layout.addWidget(self.t1_value, alignment=Qt.AlignCenter)

        readings_layout.addLayout(t1_layout)

        # T2
        t2_layout = QVBoxLayout()
        t2_layout.setSpacing(0)

        self.t2_label = QLabel("T2")
        self.t2_label.setFont(QFont("Segoe UI", 10))
        self.t2_label.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        t2_layout.addWidget(self.t2_label, alignment=Qt.AlignCenter)

        self.t2_value = QLabel("37.2")
        self.t2_value.setFont(QFont("Courier New", 24, QFont.Bold))
        self.t2_value.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        t2_layout.addWidget(self.t2_value, alignment=Qt.AlignCenter)

        readings_layout.addLayout(t2_layout)

        main_layout.addLayout(readings_layout)

        # Right: TD difference
        td_layout = QVBoxLayout()
        td_layout.setSpacing(0)

        self.td_label = QLabel("TD")
        self.td_label.setFont(QFont("Segoe UI", 10))
        self.td_label.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        td_layout.addWidget(self.td_label, alignment=Qt.AlignCenter)

        self.td_value = QLabel("0.2")
        self.td_value.setFont(QFont("Courier New", 24, QFont.Bold))
        self.td_value.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        td_layout.addWidget(self.td_value, alignment=Qt.AlignCenter)

        main_layout.addLayout(td_layout)

        main_layout.addStretch()

    def update_data(self, data):
        """
        Update the widget with new data.

        Args:
            data (dict): Data object with keys 't1', 't2', 'td'.
        """
        if 't1' in data:
            self.t1_value.setText(str(data['t1']))
        if 't2' in data:
            self.t2_value.setText(str(data['t2']))
        if 'td' in data:
            self.td_value.setText(str(data['td']))
