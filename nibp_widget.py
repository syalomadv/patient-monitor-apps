import sys
from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QProgressBar
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class NibpWidget(QWidget):
    """
    A compact widget for displaying NIBP (Non-Invasive Blood Pressure) parameters
    in a patient monitor UI, mimicking the Mindray style with black background,
    sans-serif fonts, white text, and a vertical bar graph for alarm limits.
    """
    def __init__(self, parent=None):
        """
        Initialize the NibpWidget.

        Args:
            parent (QWidget): Parent widget. Defaults to None.
        """
        super().__init__(parent)

        self.setStyleSheet("background-color: #000000; border: none;")

        # Main layout: Vertical for main reading and bar graph
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(10)

        # Top part: Main reading and time/mode
        top_layout = QHBoxLayout()
        top_layout.setSpacing(10)

        # Main reading: Systolic/Diastolic (MAP)
        self.main_reading = QLabel("120/80 (93)")
        self.main_reading.setFont(QFont("Courier New", 24, QFont.Bold))
        self.main_reading.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        top_layout.addWidget(self.main_reading)

        # Time and mode to the right
        time_mode_layout = QVBoxLayout()
        time_mode_layout.setSpacing(0)

        self.time_label = QLabel("16:54")
        self.time_label.setFont(QFont("Segoe UI", 10))
        self.time_label.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        time_mode_layout.addWidget(self.time_label, alignment=Qt.AlignLeft)

        self.mode_label = QLabel("Manual")
        self.mode_label.setFont(QFont("Segoe UI", 10))
        self.mode_label.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        time_mode_layout.addWidget(self.mode_label, alignment=Qt.AlignLeft)

        top_layout.addLayout(time_mode_layout)
        top_layout.addStretch()

        main_layout.addLayout(top_layout)

        # Bottom part: Vertical bar graph for alarm limits
        bar_layout = QVBoxLayout()
        bar_layout.setSpacing(5)

        # High limit at top
        self.high_limit_label = QLabel("160")
        self.high_limit_label.setFont(QFont("Segoe UI", 10))
        self.high_limit_label.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        bar_layout.addWidget(self.high_limit_label, alignment=Qt.AlignCenter)

        # Vertical progress bar representing the alarm limits range
        self.limit_bar = QProgressBar()
        self.limit_bar.setOrientation(Qt.Vertical)
        self.limit_bar.setMinimum(0)  # Will be set dynamically
        self.limit_bar.setMaximum(100)  # Will be set dynamically
        self.limit_bar.setValue(100)  # Full bar to represent the range
        self.limit_bar.setStyleSheet("""
            QProgressBar {
                background-color: #222222;
                border: none;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #FFFFFF;
            }
        """)
        self.limit_bar.setFixedWidth(20)  # Narrow bar
        bar_layout.addWidget(self.limit_bar, alignment=Qt.AlignCenter)

        # Low limit at bottom
        self.low_limit_label = QLabel("90")
        self.low_limit_label.setFont(QFont("Segoe UI", 10))
        self.low_limit_label.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        bar_layout.addWidget(self.low_limit_label, alignment=Qt.AlignCenter)

        main_layout.addLayout(bar_layout)

    def update_data(self, data):
        """
        Update the widget with new data.

        Args:
            data (dict): Data object with keys like 'systolic', 'diastolic', 'map', 'lastMeasuredTime', 'mode', 'highLimit', 'lowLimit'.
        """
        if 'systolic' in data and 'diastolic' in data and 'map' in data:
            self.main_reading.setText(f"{data['systolic']}/{data['diastolic']} ({data['map']})")
        if 'lastMeasuredTime' in data:
            self.time_label.setText(str(data['lastMeasuredTime']))
        if 'mode' in data:
            self.mode_label.setText(str(data['mode']))
        if 'highLimit' in data:
            self.high_limit_label.setText(str(data['highLimit']))
            self.limit_bar.setMaximum(data['highLimit'])
        if 'lowLimit' in data:
            self.low_limit_label.setText(str(data['lowLimit']))
            self.limit_bar.setMinimum(data['lowLimit'])
