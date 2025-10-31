import sys
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class NibpTrendWidget(QWidget):
    """
    Widget for displaying NIBP trend data as a table of historical readings.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #000000; color: #FFFFFF; border: none;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # Label
        self.label = QLabel("NIBP Trend")
        self.label.setFont(QFont("Arial", 10))
        self.label.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        layout.addWidget(self.label, alignment=Qt.AlignLeft)

        # Table for trend data
        self.table = QTableWidget()
        self.table.setRowCount(5)  # Show last 5 readings
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Time", "NIBP", "PR", "Status"])
        self.table.horizontalHeader().setFont(QFont("Arial", 8))
        self.table.verticalHeader().setVisible(False)
        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #000000;
                color: #FFFFFF;
                gridline-color: #333333;
                border: none;
            }
            QHeaderView::section {
                background-color: #333333;
                color: #FFFFFF;
                border: 1px solid #666666;
                font-size: 8px;
            }
            QTableWidget::item {
                border: 1px solid #333333;
                font-size: 8px;
            }
        """)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        # Initialize with dummy data
        self.history = []
        self.update_trend([])

    def update_trend(self, data_list):
        """
        Update the trend table with list of historical data.

        Args:
            data_list (list): List of dicts with 'time', 'nibp', 'pr', 'status'
        """
        self.history = data_list[-5:]  # Keep last 5
        self.table.setRowCount(len(self.history))
        for row, data in enumerate(self.history):
            self.table.setItem(row, 0, QTableWidgetItem(data.get('time', '')))
            self.table.setItem(row, 1, QTableWidgetItem(data.get('nibp', '')))
            self.table.setItem(row, 2, QTableWidgetItem(data.get('pr', '')))
            self.table.setItem(row, 3, QTableWidgetItem(data.get('status', 'Normal')))
