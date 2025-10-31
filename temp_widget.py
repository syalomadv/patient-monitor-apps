import sys
from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class TempWidget(QWidget):
    """
    A compact widget for displaying temperature parameters in a patient monitor UI,
    designed to look realistic like those used in hospitals. The widget has a black background,
    white text with bold sans-serif fonts, and is sized approximately 200x100 pixels.
    It displays the label "Temp" with unit "°C" at the top-left, two temperature readings
    T1 and T2 below, and the temperature difference TD on the right side.
    """
    def __init__(self, parent=None):
        """
        Initialize the TempWidget with the specified layout and styling.

        Args:
            parent (QWidget): Parent widget. Defaults to None.
        """
        super().__init__(parent)

        # Set black background and no border for realistic hospital monitor look - allow dynamic width
        self.setStyleSheet("background-color: #000000; border: none;")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)  # Allow width expansion

        # Main layout: Vertical to stack top label row and bottom readings row
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)

        # Top row: Horizontal layout for "Temp" and "°C" labels
        top_layout = QHBoxLayout()
        top_layout.setSpacing(2)

        # "Temp" label at top-left
        self.temp_label = QLabel("Temp")
        self.temp_label.setFont(QFont("Arial", 10))
        self.temp_label.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        top_layout.addWidget(self.temp_label, alignment=Qt.AlignLeft)

        # "°C" unit aligned to the right of "Temp"
        self.temp_unit = QLabel("°C")
        self.temp_unit.setFont(QFont("Arial", 10))
        self.temp_unit.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        top_layout.addWidget(self.temp_unit, alignment=Qt.AlignLeft)

        top_layout.addStretch()  # Push elements to the left
        main_layout.addLayout(top_layout)

        # Bottom row: Horizontal layout for T1/T2 on left and TD on right
        bottom_layout = QHBoxLayout()
        bottom_layout.setSpacing(10)

        # Left side: Vertical layout for T1 and T2 readings
        readings_layout = QVBoxLayout()
        readings_layout.setSpacing(5)

        # T1 reading: Label and value vertically stacked
        t1_layout = QVBoxLayout()
        t1_layout.setSpacing(0)

        self.t1_label = QLabel("T1")
        self.t1_label.setFont(QFont("Arial", 10))
        self.t1_label.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        t1_layout.addWidget(self.t1_label, alignment=Qt.AlignCenter)

        self.t1_value = QLabel("37.0")
        self.t1_value.setFont(QFont("Monospace", 36, QFont.Bold))  # 36pt monospace white
        self.t1_value.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        t1_layout.addWidget(self.t1_value, alignment=Qt.AlignCenter)

        readings_layout.addLayout(t1_layout)

        # T2 reading: Label and value vertically stacked
        t2_layout = QVBoxLayout()
        t2_layout.setSpacing(0)

        self.t2_label = QLabel("T2")
        self.t2_label.setFont(QFont("Arial", 10))
        self.t2_label.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        t2_layout.addWidget(self.t2_label, alignment=Qt.AlignCenter)

        self.t2_value = QLabel("37.2")
        self.t2_value.setFont(QFont("Monospace", 36, QFont.Bold))  # 36pt monospace white
        self.t2_value.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        t2_layout.addWidget(self.t2_value, alignment=Qt.AlignCenter)

        readings_layout.addLayout(t2_layout)

        bottom_layout.addLayout(readings_layout)

        # Right side: Vertical layout for TD difference
        td_layout = QVBoxLayout()
        td_layout.setSpacing(0)

        self.td_label = QLabel("TD")
        self.td_label.setFont(QFont("Arial", 10))
        self.td_label.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        td_layout.addWidget(self.td_label, alignment=Qt.AlignCenter)

        self.td_value = QLabel("0.2")
        self.td_value.setFont(QFont("Monospace", 36, QFont.Bold))  # 36pt monospace white
        self.td_value.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        td_layout.addWidget(self.td_value, alignment=Qt.AlignCenter)

        bottom_layout.addLayout(td_layout)

        main_layout.addLayout(bottom_layout)

    def update_data(self, data):
        """
        Update the temperature values dynamically. This method can be called to refresh
        the widget with new data, such as from sensors or real-time monitoring systems.
        The TD (temperature difference) is calculated as the absolute difference between T1 and T2.

        Args:
            data (dict): Dictionary containing temperature data with keys 't1' and 't2'.
                         The 'td' key is optional; if not provided, it will be calculated.
        """
        if 't1' in data:
            self.t1_value.setText(str(data['t1']))
        if 't2' in data:
            self.t2_value.setText(str(data['t2']))
        if 'td' in data:
            self.td_value.setText(str(data['td']))
        elif 't1' in data and 't2' in data:
            # Calculate TD as absolute difference if not provided
            t1 = float(data['t1'])
            t2 = float(data['t2'])
            td = abs(t1 - t2)
            self.td_value.setText(f"{td:.1f}")
