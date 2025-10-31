import sys
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class NibpParamsWidget(QWidget):
    """
    Widget for displaying secondary NIBP parameters: PR, Time, Status.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #000000; color: #FFFFFF; border: none;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # PR
        self.pr_label = QLabel("PR 60")
        self.pr_label.setFont(QFont("Arial", 10))
        layout.addWidget(self.pr_label, alignment=Qt.AlignLeft)

        # Time
        self.time_label = QLabel("Time 16:54")
        self.time_label.setFont(QFont("Arial", 10))
        layout.addWidget(self.time_label, alignment=Qt.AlignLeft)

        # Status
        self.status_label = QLabel("Status: Normal")
        self.status_label.setFont(QFont("Arial", 10))
        layout.addWidget(self.status_label, alignment=Qt.AlignLeft)

    def update_data(self, data):
        """
        Update the parameters.

        Args:
            data (dict): With keys 'pr', 'time', 'status'
        """
        if 'pr' in data:
            self.pr_label.setText(f"PR {data['pr']}")
        if 'time' in data:
            self.time_label.setText(f"Time {data['time']}")
        if 'status' in data:
            self.status_label.setText(f"Status: {data['status']}")
