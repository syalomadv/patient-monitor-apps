import sys
from PySide6.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
from datetime import datetime

class StatusBarWidget(QWidget):
    """
    Status bar widget for patient monitor, displaying patient info, date/time, and alarm status with icons.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #000000; color: #FFFFFF; border-bottom: 1px solid #333333;")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(20)

        # Patient info (left)
        self.patient_label = QLabel("John Doe | ID: 12345")
        self.patient_label.setFont(QFont("Arial", 12))
        self.patient_label.setStyleSheet("color: #CCCCCC;")
        layout.addWidget(self.patient_label)

        layout.addStretch()

        # Date/Time (center)
        self.date_time_label = QLabel(datetime.now().strftime("%m/%d/%Y\n%H:%M:%S"))
        self.date_time_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.date_time_label.setStyleSheet("color: #FFFFFF;")
        self.date_time_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.date_time_label)

        layout.addStretch()

        # Alarm status (right) with icons
        alarm_layout = QHBoxLayout()
        alarm_layout.setSpacing(10)

        # Battery icon (placeholder, assume icon exists or use text)
        self.battery_label = QLabel("🔋")  # Use emoji or load pixmap
        self.battery_label.setFont(QFont("Arial", 12))
        alarm_layout.addWidget(self.battery_label)

        # Network icon
        self.network_label = QLabel("📶")
        self.network_label.setFont(QFont("Arial", 12))
        alarm_layout.addWidget(self.network_label)

        # Alarm status text - orange background for PWR interrupted
        self.alarm_label = QLabel("PWR interrupted")
        self.alarm_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.alarm_label.setStyleSheet("color: #FFFFFF; background-color: #FFA500; padding: 2px 5px; border-radius: 3px;")  # Orange background for PWR interrupted
        alarm_layout.addWidget(self.alarm_label)

        layout.addLayout(alarm_layout)

    def update_time(self):
        self.date_time_label.setText(datetime.now().strftime("%m/%d/%Y\n%H:%M:%S"))

    def update_alarm(self, status):
        self.alarm_label.setText(status)
        if "Critical" in status or "interrupted" in status:
            self.alarm_label.setStyleSheet("color: #FFFFFF; background-color: #FF0000; padding: 2px 5px; border-radius: 3px;")
        elif "Warning" in status or "Pause" in status:
            self.alarm_label.setStyleSheet("color: #FFFFFF; background-color: #FFAA00; padding: 2px 5px; border-radius: 3px;")
        else:
            self.alarm_label.setStyleSheet("color: #FFFFFF; background-color: #00AA00; padding: 2px 5px; border-radius: 3px;")
