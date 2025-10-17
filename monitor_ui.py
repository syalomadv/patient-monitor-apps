import sys
import random
from PySide6.QtWidgets import (QApplication, QMainWindow, QHBoxLayout, QVBoxLayout,
                               QWidget, QLabel, QFrame, QMenu, QPushButton, QSpacerItem)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QAction
from PySide6.QtWidgets import QGraphicsDropShadowEffect
import pyqtgraph as pg
from datetime import datetime


class MonitorUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Patient Monitor - Mindray uMEC 120 Style")
        self.setGeometry(100, 100, 2400, 1600)
        self.resize(2400, 1600)

        self.audio_paused = False
        self.current_mode = "monitoring"
        self.simulation_timer = None

        self.setStyleSheet("""
            QMainWindow {
                background-color: #000000;
                color: #FFFFFF;
            }
            QLabel {
                color: #FFFFFF;
                font-family: 'Segoe UI Light', 'Roboto Light', sans-serif;
                font-weight: normal;
            }
            QFrame {
                background-color: #000000;
                border: none;
            }
            QPushButton#menuBtn {
                background-color: #000000;
                color: #FFFFFF;
                border: none;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
                font-size: 12pt;
                font-weight: bold;
                padding: 5px 15px;
                min-width: 100px;
                min-height: 30px;
                border-radius: 0;
            }
            QPushButton#menuBtn:hover {
                background-color: #00AEEF;
                border: 1px solid #00AEEF;
            }
            QPushButton#menuBtn:pressed {
                background-color: #004A77;
            }
            QLabel#timeLabel {
                color: #FFD700;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12pt;
                font-weight: bold;
                background-color: #000000;
                padding: 5px 10px;
                border: none;
            }
            QLabel#modeIndicator {
                font-family: 'Segoe UI Semibold', 'Roboto Medium', sans-serif;
                font-size: 12pt;
                font-weight: bold;
                text-transform: uppercase;
                padding: 5px 10px;
                background-color: transparent;
                border: none;
            }
            QLabel#standbyLabel {
                color: #FF4444;
                font-family: 'Segoe UI', sans-serif;
                font-size: 48pt;
                font-weight: bold;
                background-color: rgba(0, 0, 0, 0.8);
            }
            QMenu {
                background-color: #000000;
                color: #FFFFFF;
                border: 1px solid #333333;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
                font-size: 12pt;
            }
            QMenu::item {
                padding: 5px 20px;
                background-color: transparent;
            }
            QMenu::item:selected {
                background-color: #00AEEF;
            }
            QPushButton {
                color: #FFFFFF;
                border: 1px solid #333333;
                border-radius: 8px;
                font-weight: bold;
                font-family: 'Segoe UI', sans-serif;
                font-size: 11px;
                padding: 10px;
                min-width: 120px;
                min-height: 45px;
            }
            QPushButton:hover {
                border: 1px solid #00AEEF;
            }
            QPushButton:pressed {
                background-color: #002244;
            }
            #nibpBtn { background-color: #111111; }
            #alarmResetBtn { background-color: #CC4444; }
            #audioPauseBtn { background-color: #111111; }
            #audioPauseBtn.active { background-color: #FF6600; }
            #freezeBtn { background-color: #111111; }
            #manualEventBtn { background-color: #111111; }
            #stopAllBtn { background-color: #AA2222; }
            #standbyBtn { background-color: #111111; }
            #moreBtn { background-color: #003366; }
        """)

        self.digital_font = QFont("Courier New", 12)
        self.vital_font = QFont("Courier New", 24, QFont.Bold)
        self.menu_font = QFont("Segoe UI", 12, QFont.Bold)
        self.time_font = QFont("Consolas", 12, QFont.Bold)
        self.mode_font = QFont("Segoe UI Semibold", 12, QFont.Bold)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)

        self.create_custom_top_bar(main_layout)

        self.create_header(main_layout)

        split_layout = QHBoxLayout()
        split_layout.setSpacing(10)

        left_widget = QFrame()
        self.left_layout = QVBoxLayout(left_widget)
        self.left_layout.setSpacing(5)
        self.create_waveforms(self.left_layout)
        split_layout.addWidget(left_widget, 7)

        right_widget = QFrame()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setSpacing(20)
        self.create_vital_panel(right_layout)
        split_layout.addWidget(right_widget, 3)

        main_layout.addLayout(split_layout)

        self.create_quick_access_bar(main_layout)

        pg.setConfigOption('background', '#000000')
        pg.setConfigOption('foreground', '#FFFFFF')
        pg.setConfigOptions(antialias=True)

        self.set_mode("monitoring")
        default_vitals = {
            'hr': '75',
            'spo2': '98%',
            'rr': '18',
            'nibp': '120/80 (93)',
            'temp': '37.0°C',
            'co2': '35 mmHg'
        }
        self.update_vitals_ui(default_vitals)

    def create_waveforms(self, layout):
        # Create waveform plots
        self.ecg_plot = pg.PlotWidget()
        self.ecg_plot.setBackground('#000000')
        self.ecg_plot.showGrid(x=True, y=True, alpha=0.2)
        self.ecg_plot.getPlotItem().getAxis('bottom').setPen('#222222')
        self.ecg_plot.getPlotItem().getAxis('left').setPen('#222222')
        layout.addWidget(self.ecg_plot)

        self.pleth_plot = pg.PlotWidget()
        self.pleth_plot.setBackground('#000000')
        self.pleth_plot.showGrid(x=True, y=True, alpha=0.2)
        self.pleth_plot.getPlotItem().getAxis('bottom').setPen('#222222')
        self.pleth_plot.getPlotItem().getAxis('left').setPen('#222222')
        layout.addWidget(self.pleth_plot)

        self.resp_plot = pg.PlotWidget()
        self.resp_plot.setBackground('#000000')
        self.resp_plot.showGrid(x=True, y=True, alpha=0.2)
        self.resp_plot.getPlotItem().getAxis('bottom').setPen('#222222')
        self.resp_plot.getPlotItem().getAxis('left').setPen('#222222')
        layout.addWidget(self.resp_plot)

        self.art_plot = pg.PlotWidget()
        self.art_plot.setBackground('#000000')
        self.art_plot.showGrid(x=True, y=True, alpha=0.2)
        self.art_plot.getPlotItem().getAxis('bottom').setPen('#222222')
        self.art_plot.getPlotItem().getAxis('left').setPen('#222222')
        layout.addWidget(self.art_plot)

        self.co2_plot = pg.PlotWidget()
        self.co2_plot.setBackground('#000000')
        self.co2_plot.showGrid(x=True, y=True, alpha=0.2)
        self.co2_plot.getPlotItem().getAxis('bottom').setPen('#222222')
        self.co2_plot.getPlotItem().getAxis('left').setPen('#222222')
        layout.addWidget(self.co2_plot)

    def create_vital_panel(self, layout):
        # Create vitals labels with colors and effects
        self.hr_label = QLabel("HR\n75")
        self.hr_label.setFont(self.vital_font)
        self.hr_label.setStyleSheet("color: #00FF00;")  # Green
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(Qt.white)
        self.hr_label.setGraphicsEffect(shadow)
        layout.addWidget(self.hr_label)

        self.spo2_label = QLabel("SpO2\n98%")
        self.spo2_label.setFont(self.vital_font)
        self.spo2_label.setStyleSheet("color: #00FFFF;")  # Cyan
        shadow2 = QGraphicsDropShadowEffect()
        shadow2.setBlurRadius(10)
        shadow2.setColor(Qt.white)
        self.spo2_label.setGraphicsEffect(shadow2)
        layout.addWidget(self.spo2_label)

        self.rr_label = QLabel("RR\n18")
        self.rr_label.setFont(self.vital_font)
        self.rr_label.setStyleSheet("color: #FFFF00;")  # Yellow
        shadow3 = QGraphicsDropShadowEffect()
        shadow3.setBlurRadius(10)
        shadow3.setColor(Qt.white)
        self.rr_label.setGraphicsEffect(shadow3)
        layout.addWidget(self.rr_label)

        self.nibp_label = QLabel("NIBP\n120/80 (93)")
        self.nibp_label.setFont(self.vital_font)
        self.nibp_label.setStyleSheet("color: #FF0000;")  # Red
        shadow4 = QGraphicsDropShadowEffect()
        shadow4.setBlurRadius(10)
        shadow4.setColor(Qt.white)
        self.nibp_label.setGraphicsEffect(shadow4)
        layout.addWidget(self.nibp_label)

        self.temp_label = QLabel("TEMP\n37.0°C")
        self.temp_label.setFont(self.vital_font)
        self.temp_label.setStyleSheet("color: #FFFFFF;")  # White
        shadow5 = QGraphicsDropShadowEffect()
        shadow5.setBlurRadius(10)
        shadow5.setColor(Qt.white)
        self.temp_label.setGraphicsEffect(shadow5)
        layout.addWidget(self.temp_label)

        self.co2_label = QLabel("CO2\n35 mmHg")
        self.co2_label.setFont(self.vital_font)
        self.co2_label.setStyleSheet("color: #FFA500;")  # Orange
        shadow6 = QGraphicsDropShadowEffect()
        shadow6.setBlurRadius(10)
        shadow6.setColor(Qt.white)
        self.co2_label.setGraphicsEffect(shadow6)
        layout.addWidget(self.co2_label)

    def create_quick_access_bar(self, layout):
        # Create quick access buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.nibp_btn = QPushButton("NIBP")
        self.nibp_btn.setObjectName("nibpBtn")
        button_layout.addWidget(self.nibp_btn)

        self.alarm_reset_btn = QPushButton("Alarm Reset")
        self.alarm_reset_btn.setObjectName("alarmResetBtn")
        button_layout.addWidget(self.alarm_reset_btn)

        self.audio_pause_btn = QPushButton("Audio Pause")
        self.audio_pause_btn.setObjectName("audioPauseBtn")
        button_layout.addWidget(self.audio_pause_btn)

        self.freeze_btn = QPushButton("Freeze")
        self.freeze_btn.setObjectName("freezeBtn")
        button_layout.addWidget(self.freeze_btn)

        self.manual_event_btn = QPushButton("Manual Event")
        self.manual_event_btn.setObjectName("manualEventBtn")
        button_layout.addWidget(self.manual_event_btn)

        self.stop_all_btn = QPushButton("Stop All")
        self.stop_all_btn.setObjectName("stopAllBtn")
        button_layout.addWidget(self.stop_all_btn)

        self.standby_btn = QPushButton("Standby")
        self.standby_btn.setObjectName("standbyBtn")
        button_layout.addWidget(self.standby_btn)

        self.more_btn = QPushButton("More")
        self.more_btn.setObjectName("moreBtn")
        button_layout.addWidget(self.more_btn)

        # Add Save Screenshot button
        self.save_screenshot_btn = QPushButton("Save Screenshot")
        self.save_screenshot_btn.clicked.connect(self.save_screenshot)
        button_layout.addWidget(self.save_screenshot_btn)

        layout.addLayout(button_layout)

    def update_vitals_ui(self, vitals):
        self.hr_label.setText(f"HR\n{vitals['hr']}")
        self.spo2_label.setText(f"SpO2\n{vitals['spo2']}")
        self.rr_label.setText(f"RR\n{vitals['rr']}")
        self.nibp_label.setText(f"NIBP\n{vitals['nibp']}")
        self.temp_label.setText(f"TEMP\n{vitals['temp']}")
        self.co2_label.setText(f"CO2\n{vitals['co2']}")

    def save_screenshot(self):
        from PySide6.QtGui import QPixmap
        pixmap = self.grab()
        pixmap.setDevicePixelRatio(3)  # For high DPI
        pixmap.save("screenshot.png", "PNG", 100)

    def set_mode(self, mode):
        self.current_mode = mode
        if mode == "monitoring":
            self.mode_indicator.setText("MODE: MONITORING")
            self.mode_indicator.setStyleSheet("color: #00FF00;")  # Green
        elif mode == "standby":
            self.mode_indicator.setText("STANDBY")
            self.mode_indicator.setStyleSheet("color: #FF4444;")  # Red
        elif mode == "demo":
            self.mode_indicator.setText("DEMO")
            self.mode_indicator.setStyleSheet("color: #FFFF00;")  # Yellow

    def create_custom_top_bar(self, parent_layout):
        top_frame = QFrame()
        top_frame.setFixedHeight(40)
        top_layout = QHBoxLayout(top_frame)
        top_layout.setContentsMargins(8, 0, 8, 0)
        top_layout.setSpacing(5)

        menu_items = [
            ("Patient", self.create_patient_menu),
            ("Display", self.create_display_menu),
            ("Parameter", self.create_parameter_menu),
            ("Alarm", self.create_alarm_menu),
            ("Review", self.create_review_menu),
            ("Settings", self.create_settings_menu),
            ("Mode", self.create_mode_menu),
            ("Help", self.create_help_menu)
        ]

        for text, menu_func in menu_items:
            btn = QPushButton(text)
            btn.setObjectName("menuBtn")
            btn.setFont(self.menu_font)
            btn.clicked.connect(lambda checked, f=menu_func: f().exec(btn.mapToGlobal(btn.rect().topRight())))
            top_layout.addWidget(btn)

        top_layout.addStretch(1)

        self.time_label = QLabel(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.time_label.setObjectName("timeLabel")
        self.time_label.setFont(self.time_font)
        self.time_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        top_layout.addWidget(self.time_label)

        self.time_timer = QTimer(self)
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(1000)

        parent_layout.addWidget(top_frame)

    def update_time(self):
        self.time_label.setText("2023-10-27 16:30:00")

    def create_mode_menu(self):
        menu = QMenu(self)
        demo_action = QAction("Start Demo Mode", self)
        demo_action.triggered.connect(lambda: self.set_mode("demo"))
        menu.addAction(demo_action)

        monitoring_action = QAction("Start Monitoring Mode", self)
        monitoring_action.triggered.connect(lambda: self.set_mode("monitoring"))
        menu.addAction(monitoring_action)

        standby_action = QAction("Standby Mode", self)
        standby_action.triggered.connect(lambda: self.set_mode("standby"))
        menu.addAction(standby_action)

        return menu

    def create_patient_menu(self):
        menu = QMenu(self)
        menu.addAction(QAction("New Patient", self, triggered=lambda: print("Patient: New Patient")))
        menu.addAction(QAction("Edit Info", self, triggered=lambda: print("Patient: Edit Info")))
        menu.addAction(QAction("Discharge", self, triggered=lambda: print("Patient: Discharge")))

        category_menu = QMenu("Category", self)
        category_menu.addAction(QAction("Adult", self, triggered=lambda: print("Category: Adult")))

    def create_display_menu(self):
        menu = QMenu(self)
        menu.addAction(QAction("Waveforms", self, triggered=lambda: print("Display: Waveforms")))
        menu.addAction(QAction("Vitals", self, triggered=lambda: print("Display: Vitals")))
        return menu

    def create_parameter_menu(self):
        menu = QMenu(self)
        menu.addAction(QAction("HR", self, triggered=lambda: print("Parameter: HR")))
        menu.addAction(QAction("SPO2", self, triggered=lambda: print("Parameter: SPO2")))
        return menu

    def create_alarm_menu(self):
        menu = QMenu(self)
        menu.addAction(QAction("Reset Alarms", self, triggered=lambda: print("Alarm: Reset")))
        menu.addAction(QAction("Silence", self, triggered=lambda: print("Alarm: Silence")))
        return menu

    def create_review_menu(self):
        menu = QMenu(self)
        menu.addAction(QAction("Trends", self, triggered=lambda: print("Review: Trends")))
        menu.addAction(QAction("Events", self, triggered=lambda: print("Review: Events")))
        return menu

    def create_settings_menu(self):
        menu = QMenu(self)
        menu.addAction(QAction("General", self, triggered=lambda: print("Settings: General")))
        menu.addAction(QAction("Network", self, triggered=lambda: print("Settings: Network")))
        return menu

    def create_help_menu(self):
        menu = QMenu(self)
        menu.addAction(QAction("About", self, triggered=lambda: print("Help: About")))
        menu.addAction(QAction("Manual", self, triggered=lambda: print("Help: Manual")))
        return menu

    def create_header(self, parent_layout):
        header_frame = QFrame()
        header_layout = QHBoxLayout(header_frame)
        patient_label = QLabel("Patient: Unknown")
        patient_label.setFont(self.menu_font)
        header_layout.addWidget(patient_label)
        header_layout.addStretch()
        self.mode_indicator = QLabel("MONITORING")
        self.mode_indicator.setObjectName("modeIndicator")
        self.mode_indicator.setFont(self.mode_font)
        header_layout.addWidget(self.mode_indicator)
        parent_layout.addWidget(header_frame)

    def closeEvent(self, event):
        if hasattr(self, 'app') and hasattr(self.app, 'worker'):
            self.app.worker.stop()
            self.app.worker.wait()
        event.accept()
