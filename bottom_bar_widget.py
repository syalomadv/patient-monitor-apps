import sys
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon
from nibp_trend_widget import NibpTrendWidget
from nibp_main_widget import NibpMainWidget
from temp_widget import TempWidget
from vital_sign_widget import VitalSignWidget

class BottomBarWidget(QWidget):
    """
    Bottom bar widget with two-row layout: Row 1 for trend data, Row 2 for numeric vitals.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #000000; color: #FFFFFF; border-top: 1px solid #333333;")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 5, 10, 5)
        main_layout.setSpacing(10)

        # Row 1: Trend/List Row - merged Temp and NIBP Trend with zero spacing, full width to waveform edge
        row1_layout = QHBoxLayout()
        row1_layout.setSpacing(0)  # Zero spacing for consolidation
        row1_layout.setContentsMargins(0, 0, 0, 0)  # No margins for container

        # Temperature Block (far left) - eliminate left/right margins
        self.temp_widget = TempWidget()
        self.temp_widget.setStyleSheet("margin-right: 0 !important; padding-right: 0 !important; margin-left: 0 !important; padding-left: 0 !important;")
        row1_layout.addWidget(self.temp_widget, stretch=1)  # Allow expansion

        # NIBP Trend Table (adjacent right to Temperature, no spacing) - eliminate left/right margins
        self.nibp_trend_widget = NibpTrendWidget()
        self.nibp_trend_widget.setStyleSheet("position: relative; left: -5px !important; margin-left: 0 !important;")
        row1_layout.addWidget(self.nibp_trend_widget, stretch=3)  # More stretch for trend table

        main_layout.addLayout(row1_layout)

        # Row 2: Numeric Vitals Row - CO2 below NIBP for hierarchy
        row2_layout = QVBoxLayout()
        row2_layout.setSpacing(12)  # Consistent vertical spacing

        # NIBP Main Reading (top)
        self.nibp_main_widget = NibpMainWidget()
        row2_layout.addWidget(self.nibp_main_widget, alignment=Qt.AlignCenter)

        # CO2 Widget (below NIBP, smaller font)
        self.co2_widget = VitalSignWidget("CO2", "35", "mmHg", "#FFFFFF")
        row2_layout.addWidget(self.co2_widget, alignment=Qt.AlignCenter)

        # Add stretch to push control buttons to the right
        row2_layout.addStretch()

        # Control buttons (flush with bottom-right corner, tightly grouped, min 44x44px)
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(0)  # Tightly grouped

        # Alarm Reset button
        self.alarm_reset_button = QPushButton()
        self.alarm_reset_button.setText("🔕")  # Icon for Alarm Reset
        self.alarm_reset_button.setFont(QFont("Arial", 10))
        self.alarm_reset_button.setMinimumSize(44, 44)  # Min 44x44px
        self.alarm_reset_button.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: #FFFFFF;
                border: 1px solid #666666;
            }
            QPushButton:hover {
                border: 2px solid #FFFFFF;  /* Hover effect: border highlight */
            }
        """)
        buttons_layout.addWidget(self.alarm_reset_button)

        # Freeze button
        self.freeze_button = QPushButton()
        self.freeze_button.setText("❄️")  # Icon for Freeze
        self.freeze_button.setFont(QFont("Arial", 10))
        self.freeze_button.setMinimumSize(44, 44)  # Min 44x44px
        self.freeze_button.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: #FFFFFF;
                border: 1px solid #666666;
            }
            QPushButton:hover {
                border: 2px solid #FFFFFF;  /* Hover effect: border highlight */
            }
        """)
        buttons_layout.addWidget(self.freeze_button)

        # Setup button
        self.setup_button = QPushButton()
        self.setup_button.setText("⚙️")  # Icon for Setup
        self.setup_button.setFont(QFont("Arial", 10))
        self.setup_button.setMinimumSize(44, 44)  # Min 44x44px
        self.setup_button.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: #FFFFFF;
                border: 1px solid #666666;
            }
            QPushButton:hover {
                border: 2px solid #FFFFFF;  /* Hover effect: border highlight */
            }
        """)
        buttons_layout.addWidget(self.setup_button)

        # Display Mode button
        self.display_mode_button = QPushButton()
        self.display_mode_button.setText("📺")  # Icon for Display Mode
        self.display_mode_button.setFont(QFont("Arial", 10))
        self.display_mode_button.setMinimumSize(44, 44)  # Min 44x44px
        self.display_mode_button.setStyleSheet("""
            QPushButton {
                background-color: #333333;
                color: #FFFFFF;
                border: 1px solid #666666;
            }
            QPushButton:hover {
                border: 2px solid #FFFFFF;  /* Hover effect: border highlight */
            }
        """)
        buttons_layout.addWidget(self.display_mode_button)

        # Add buttons layout to a container for alignment
        buttons_container = QWidget()
        buttons_container.setLayout(buttons_layout)
        row2_layout.addWidget(buttons_container, alignment=Qt.AlignBottom | Qt.AlignRight)  # Flush bottom-right

        main_layout.addLayout(row2_layout)

    def update_nibp(self, data):
        # Update trend with historical data (for now, just current as single entry)
        trend_data = [{
            'time': data.get('time', '16:54'),
            'nibp': f"{data.get('systolic', '120')}/{data.get('diastolic', '80')} ({data.get('map', '93')})",
            'pr': data.get('pr', '60'),
            'status': 'Normal'
        }]
        self.nibp_trend_widget.update_trend(trend_data)
        self.nibp_main_widget.update_data(data)

    def update_temp(self, data):
        self.temp_widget.update_data(data)

    def update_co2(self, value, unit):
        self.co2_widget.update_value(value, unit)
