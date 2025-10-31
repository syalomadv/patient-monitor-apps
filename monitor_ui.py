import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QHBoxLayout, QVBoxLayout,
                               QWidget, QLabel, QGridLayout)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, QTimer
from datetime import datetime
from data_worker import DataWorker
from waveform_widget import WaveformWidget
from imped_widget import ImpedWidget
from nibp_widget import NibpWidget
from temp_widget import TempWidget
from vital_sign_widget import VitalSignWidget
from status_bar_widget import StatusBarWidget
from bottom_bar_widget import BottomBarWidget


class MonitorUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Patient Monitor")
        self.setGeometry(100, 100, 1400, 900)
        self.setStyleSheet("background-color: #000000; color: #FFFFFF;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout: Vertical
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Status bar at top
        self.status_bar = StatusBarWidget()
        main_layout.addWidget(self.status_bar)

        # Middle section: Horizontal split (70% left, 30% right) - adjusted for balance
        middle_layout = QHBoxLayout()
        middle_layout.setContentsMargins(10, 10, 10, 10)
        middle_layout.setSpacing(10)

        # Left side: Four stacked waveforms (70% width) - ensure grid alignment
        left_layout = QVBoxLayout()
        left_layout.setSpacing(0)  # No spacing for perfect grid alignment
        self.ecg_ii_widget = WaveformWidget("II", "1mV")
        self.ecg_ii_widget.set_pen_color("#00FF00")  # Bright green for ECG
        left_layout.addWidget(self.ecg_ii_widget)
        self.ecg_i_widget = WaveformWidget("I", "1mV")
        self.ecg_i_widget.set_pen_color("#00FF00")
        left_layout.addWidget(self.ecg_i_widget)
        self.pleth_widget = WaveformWidget("Pleth", "1V")
        self.pleth_widget.set_pen_color("#00FFFF")  # Cyan for Pleth
        left_layout.addWidget(self.pleth_widget)
        # Restore imped_widget for respiration
        self.imped_widget = ImpedWidget()
        left_layout.addWidget(self.imped_widget)
        left_container = QWidget()
        left_container.setLayout(left_layout)
        middle_layout.addWidget(left_container, 7)  # Stretch factor for 70%

        # Right side: Primary vitals (30% width)
        right_layout = QVBoxLayout()
        right_layout.setSpacing(30)  # Vertical spacing between blocks

        # ECG/HR section - ensure high contrast for secondary texts
        ecg_layout = QVBoxLayout()
        ecg_layout.setSpacing(2)
        ecg_top = QHBoxLayout()
        ecg_top.setSpacing(10)
        self.ecg_label = QLabel("ECG")
        self.ecg_label.setFont(QFont("Arial", 10))
        self.ecg_label.setStyleSheet("color: #CCCCCC; background-color: transparent;")  # High contrast gray
        ecg_top.addWidget(self.ecg_label)
        ecg_top.addStretch()
        self.pvcs_label = QLabel("PVCs 0")
        self.pvcs_label.setFont(QFont("Arial", 10))
        self.pvcs_label.setStyleSheet("color: #CCCCCC; background-color: transparent;")
        ecg_top.addWidget(self.pvcs_label)
        self.st_ii_label = QLabel("ST-II 0.10")
        self.st_ii_label.setFont(QFont("Arial", 10))
        self.st_ii_label.setStyleSheet("color: #CCCCCC; background-color: transparent;")
        ecg_top.addWidget(self.st_ii_label)
        ecg_layout.addLayout(ecg_top)

        # HR and ST grid side by side for alignment
        hr_st_layout = QHBoxLayout()
        hr_st_layout.setSpacing(10)

        self.hr_value = QLabel("75")
        self.hr_value.setFont(QFont("Monospace", 72, QFont.Bold))  # Monospace, 72pt, green
        self.hr_value.setStyleSheet("color: #00FF00; background-color: transparent;")
        hr_st_layout.addWidget(self.hr_value, alignment=Qt.AlignCenter)

        # ST grid aligned with HR baseline
        st_grid = QGridLayout()
        st_grid.setSpacing(5)
        leads = ["V1", "V2", "V3", "V4", "V5", "V6", "II", "III", "aVR", "aVL", "aVF"]
        values = ["0.04", "0.05", "0.03", "0.02", "0.01", "0.00", "0.10", "0.08", "-0.02", "-0.01", "0.03"]
        for i, lead in enumerate(leads):
            lead_label = QLabel(lead)
            lead_label.setFont(QFont("Arial", 10))
            lead_label.setStyleSheet("color: #CCCCCC; background-color: transparent;")
            st_grid.addWidget(lead_label, i // 3, (i % 3) * 2)
            value_label = QLabel(values[i])
            value_label.setFont(QFont("Arial", 10))
            value_label.setStyleSheet("color: #CCCCCC; background-color: transparent;")
            st_grid.addWidget(value_label, i // 3, (i % 3) * 2 + 1)
        # Add vertical spacer to lower ST grid baseline to align with HR baseline
        st_container = QWidget()
        st_container.setLayout(st_grid)
        hr_st_layout.addWidget(st_container, alignment=Qt.AlignBottom)

        ecg_layout.addLayout(hr_st_layout)
        right_layout.addLayout(ecg_layout)

        # SpO2 section - high contrast labels
        spo2_layout = QVBoxLayout()
        self.spo2_label = QLabel("SpO2")
        self.spo2_label.setFont(QFont("Arial", 10))
        self.spo2_label.setStyleSheet("color: #CCCCCC; background-color: transparent;")
        spo2_layout.addWidget(self.spo2_label)
        self.spo2_value = QLabel("98")
        self.spo2_value.setFont(QFont("Monospace", 72, QFont.Bold))  # Monospace, 72pt, cyan
        self.spo2_value.setStyleSheet("color: #00FFFF; background-color: transparent;")
        spo2_layout.addWidget(self.spo2_value)
        # Integrate PR with SpO2 block beneath main number
        self.pr_label = QLabel("PR 75")
        self.pr_label.setFont(QFont("Arial", 10))
        self.pr_label.setStyleSheet("color: #CCCCCC; background-color: transparent;")
        spo2_layout.addWidget(self.pr_label, alignment=Qt.AlignCenter)
        self.pi_label = QLabel("PI 1.2")
        self.pi_label.setFont(QFont("Arial", 10))
        self.pi_label.setStyleSheet("color: #CCCCCC; background-color: transparent;")
        spo2_layout.addWidget(self.pi_label, alignment=Qt.AlignCenter)
        right_layout.addLayout(spo2_layout)

        # Resp section - high contrast labels
        resp_layout = QVBoxLayout()
        self.resp_label = QLabel("Resp")
        self.resp_label.setFont(QFont("Arial", 10))
        self.resp_label.setStyleSheet("color: #CCCCCC; background-color: transparent;")
        resp_layout.addWidget(self.resp_label)
        self.resp_value = QLabel("18")
        self.resp_value.setFont(QFont("Monospace", 72, QFont.Bold))  # Monospace, 72pt, yellow
        self.resp_value.setStyleSheet("color: #FFFF00; background-color: transparent;")
        resp_layout.addWidget(self.resp_value)
        self.resp_suppl = QLabel("Imped")
        self.resp_suppl.setFont(QFont("Arial", 10))
        self.resp_suppl.setStyleSheet("color: #CCCCCC; background-color: transparent;")
        resp_layout.addWidget(self.resp_suppl)
        right_layout.addLayout(resp_layout)

        right_container = QWidget()
        right_container.setLayout(right_layout)
        middle_layout.addWidget(right_container, 3)  # Stretch factor for 30%

        middle_container = QWidget()
        middle_container.setLayout(middle_layout)
        main_layout.addWidget(middle_container, 1)  # Stretch for middle

        # Bottom bar
        self.bottom_bar = BottomBarWidget()
        main_layout.addWidget(self.bottom_bar)

        central_widget.setLayout(main_layout)

        # Timer for updating time
        self.timer = QTimer()
        self.timer.timeout.connect(self.status_bar.update_time)
        self.timer.start(1000)  # Update every second

        # Data Worker for real-time updates
        self.data_worker = DataWorker()
        self.data_worker.data_ready.connect(self.update_data)
        self.data_worker.start()

    def update_data(self, data):
        waveforms = data.get('waveforms', {})
        vitals = data.get('vitals', {})

        # Update ECG waveforms with scrolling
        if 'ecg' in waveforms:
            ecg_data = waveforms['ecg']
            # Generate time data based on sample rate
            time_data = [i / 200.0 for i in range(len(ecg_data))]  # Assuming 200 Hz
            self.ecg_ii_widget.update_data(time_data, ecg_data)
            self.ecg_i_widget.update_data(time_data, ecg_data)  # Use same for I and II for now
            self.ecg_ii_widget.set_y_limits(-1.5, 1.5)
            self.ecg_i_widget.set_y_limits(-1.5, 1.5)

        # Update HR
        if 'hr' in vitals:
            hr = vitals['hr'].replace(' bpm', '')
            self.hr_value.setText(hr)

        # Update Pleth waveform with scrolling
        if 'pleth' in waveforms:
            pleth_data = waveforms['pleth']
            time_data = [i / 200.0 for i in range(len(pleth_data))]
            self.pleth_widget.update_data(time_data, pleth_data)
            self.pleth_widget.set_y_limits(90, 100)

        # Update SpO2
        if 'spo2' in vitals:
            spo2 = vitals['spo2'].replace('%', '')
            self.spo2_value.setText(spo2)
            self.pr_label.setText(f"PR {hr}")

        # Update Resp impedance waveform
        if 'resp' in waveforms:
            resp_data = waveforms['resp']
            time_data_resp = [i / 200.0 for i in range(len(resp_data))]
            self.imped_widget.update_data(time_data_resp, resp_data)



        # Update RR
        if 'rr' in vitals:
            rr = vitals['rr'].replace(' bpm', '')
            self.resp_value.setText(rr)

        # Update NIBP bottom bar
        if 'nibp' in vitals:
            nibp_str = vitals['nibp']  # e.g., "120/80 (93)"
            parts = nibp_str.replace('(', '').replace(')', '').split('/')
            if len(parts) >= 2:
                systolic = parts[0].strip()
                diastolic_map = parts[1].split()
                diastolic = diastolic_map[0]
                map_val = diastolic_map[1] if len(diastolic_map) > 1 else '93'
                current_time = datetime.now().strftime("%H:%M")
                self.bottom_bar.update_nibp({'systolic': systolic, 'diastolic': diastolic, 'map': map_val, 'pr': hr, 'time': current_time})

        # Update bottom bar Temp
        if 'temp' in vitals:
            temp = vitals['temp'].replace('°C', '')
            self.bottom_bar.update_temp({'t1': temp, 't2': temp})

        # Update bottom bar CO2
        if 'co2' in vitals:
            co2 = vitals['co2'].replace(' mmHg', '')
            self.bottom_bar.update_co2(co2, "mmHg")

    def closeEvent(self, event):
        self.data_worker.stop()
        self.data_worker.wait()
        super().closeEvent(event)


