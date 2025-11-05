import sys
from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from waveform_widget import WaveformWidget

class Spo2RespWidget(QWidget):
    """
    A reusable widget for displaying combined SpO2 and Respiration parameters
    in a patient monitor UI, mimicking the Mindray style with black background,
    sans-serif fonts, specific colors, and structured layout.
    """
    def __init__(self, parent=None):
        """
        Initialize the Spo2RespWidget.

        Args:
            parent (QWidget): Parent widget. Defaults to None.
        """
        super().__init__(parent)

        self.setStyleSheet("background-color: #000000; border: none;")

        # Main layout: Vertical split for SpO2 (top) and Resp (bottom)
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(10)

        # Top half: SpO2 section
        spo2_frame = QFrame()
        spo2_frame.setStyleSheet("background-color: #000000; border: none;")
        spo2_layout = QVBoxLayout(spo2_frame)
        spo2_layout.setContentsMargins(0, 0, 0, 0)
        spo2_layout.setSpacing(5)

        # Pleth waveform at top
        self.pleth_waveform = WaveformWidget()
        self.pleth_waveform.set_pen_color("#0000FF")  # Distinct blue for SpO2
        spo2_layout.addWidget(self.pleth_waveform)

        # SpO2 primary value and limits
        spo2_bottom_layout = QHBoxLayout()
        spo2_bottom_layout.setSpacing(0)  # Tight grouping

        spo2_primary_layout = QVBoxLayout()
        spo2_primary_layout.setSpacing(0)

        self.spo2_label = QLabel("SpO2")
        self.spo2_label.setFont(QFont("Segoe UI", 10))
        self.spo2_label.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        spo2_primary_layout.addWidget(self.spo2_label, alignment=Qt.AlignCenter)

        self.spo2_value = QLabel("98")
        self.spo2_value.setFont(QFont("Courier New", 48, QFont.Bold))
        self.spo2_value.setStyleSheet("color: #00FFFF; background-color: transparent;")
        spo2_primary_layout.addWidget(self.spo2_value, alignment=Qt.AlignCenter)

        self.spo2_unit = QLabel("%")
        self.spo2_unit.setFont(QFont("Segoe UI", 12))
        self.spo2_unit.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        spo2_primary_layout.addWidget(self.spo2_unit, alignment=Qt.AlignCenter)

        spo2_bottom_layout.addLayout(spo2_primary_layout)

        # Secondary parameters (PI, PR) adjacent to value
        secondary_layout = QVBoxLayout()
        secondary_layout.setSpacing(0)

        self.pi_label = QLabel("PI")
        self.pi_label.setFont(QFont("Segoe UI", 10))
        self.pi_label.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        secondary_layout.addWidget(self.pi_label, alignment=Qt.AlignLeft)

        self.pi_value = QLabel("1.2")
        self.pi_value.setFont(QFont("Segoe UI", 10))
        self.pi_value.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        secondary_layout.addWidget(self.pi_value, alignment=Qt.AlignLeft)

        self.pr_label = QLabel("PR")
        self.pr_label.setFont(QFont("Segoe UI", 10))
        self.pr_label.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        secondary_layout.addWidget(self.pr_label, alignment=Qt.AlignLeft)

        self.pr_value = QLabel("75")
        self.pr_value.setFont(QFont("Segoe UI", 10))
        self.pr_value.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        secondary_layout.addWidget(self.pr_value, alignment=Qt.AlignLeft)

        spo2_bottom_layout.addLayout(secondary_layout)

        # SpO2 alarm limits (stacked vertically to the right)
        spo2_limits_layout = QVBoxLayout()
        spo2_limits_layout.setSpacing(5)

        self.spo2_high_limit = QLabel("100")
        self.spo2_high_limit.setFont(QFont("Segoe UI", 10))
        self.spo2_high_limit.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        spo2_limits_layout.addWidget(self.spo2_high_limit, alignment=Qt.AlignCenter)

        self.spo2_low_limit = QLabel("90")
        self.spo2_low_limit.setFont(QFont("Segoe UI", 10))
        self.spo2_low_limit.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        spo2_limits_layout.addWidget(self.spo2_low_limit, alignment=Qt.AlignCenter)

        spo2_bottom_layout.addLayout(spo2_limits_layout)

        # Source to the right
        source_layout = QVBoxLayout()
        source_layout.setSpacing(5)

        self.source_label = QLabel("Source")
        self.source_label.setFont(QFont("Segoe UI", 10))
        self.source_label.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        source_layout.addWidget(self.source_label, alignment=Qt.AlignLeft)

        self.source_value = QLabel("Finger")
        self.source_value.setFont(QFont("Segoe UI", 10))
        self.source_value.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        source_layout.addWidget(self.source_value, alignment=Qt.AlignLeft)

        spo2_bottom_layout.addLayout(source_layout)
        spo2_bottom_layout.addStretch()

        spo2_layout.addLayout(spo2_bottom_layout)

        main_layout.addWidget(spo2_frame)

        # Bottom half: Resp section
        resp_frame = QFrame()
        resp_frame.setStyleSheet("background-color: #000000; border: none;")
        resp_layout = QHBoxLayout(resp_frame)
        resp_layout.setContentsMargins(0, 0, 0, 0)
        resp_layout.setSpacing(10)

        # Resp waveform on the left
        self.resp_waveform = WaveformWidget()
        self.resp_waveform.set_pen_color("#FFFF00")  # Yellow for Resp
        resp_layout.addWidget(self.resp_waveform)

        # Resp primary value and limits on the right
        resp_right_layout = QVBoxLayout()
        resp_right_layout.setSpacing(10)

        # Resp primary value
        resp_primary_layout = QVBoxLayout()
        resp_primary_layout.setSpacing(0)

        self.resp_label = QLabel("Resp")
        self.resp_label.setFont(QFont("Segoe UI", 10))
        self.resp_label.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        resp_primary_layout.addWidget(self.resp_label, alignment=Qt.AlignCenter)

        self.resp_value = QLabel("20")
        self.resp_value.setFont(QFont("Courier New", 48, QFont.Bold))
        self.resp_value.setStyleSheet("color: #FFFF00; background-color: transparent;")
        resp_primary_layout.addWidget(self.resp_value, alignment=Qt.AlignCenter)

        self.resp_unit = QLabel("bpm")
        self.resp_unit.setFont(QFont("Segoe UI", 12))
        self.resp_unit.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        resp_primary_layout.addWidget(self.resp_unit, alignment=Qt.AlignCenter)

        resp_right_layout.addLayout(resp_primary_layout)

        # Resp alarm limits (stacked vertically below primary)
        resp_limits_layout = QVBoxLayout()
        resp_limits_layout.setSpacing(5)

        self.resp_high_limit = QLabel("30")
        self.resp_high_limit.setFont(QFont("Segoe UI", 10))
        self.resp_high_limit.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        resp_limits_layout.addWidget(self.resp_high_limit, alignment=Qt.AlignCenter)

        self.resp_low_limit = QLabel("10")
        self.resp_low_limit.setFont(QFont("Segoe UI", 10))
        self.resp_low_limit.setStyleSheet("color: #FFFFFF; background-color: transparent;")
        resp_limits_layout.addWidget(self.resp_low_limit, alignment=Qt.AlignCenter)

        resp_right_layout.addLayout(resp_limits_layout)
        resp_right_layout.addStretch()

        resp_layout.addLayout(resp_right_layout)

        main_layout.addWidget(resp_frame)

    def update_data(self, data):
        """
        Update the widget with new data.

        Args:
            data (dict): Data object with keys like 'spo2', 'spo2HighLimit', 'pulseRate', 'respirationRate', 'respHighLimit', etc.
        """
        if 'spo2' in data:
            self.spo2_value.setText(str(data['spo2']))
        if 'spo2HighLimit' in data:
            self.spo2_high_limit.setText(str(data['spo2HighLimit']))
        if 'spo2LowLimit' in data:
            self.spo2_low_limit.setText(str(data['spo2LowLimit']))
        if 'pulseRate' in data:
            self.pr_value.setText(str(data['pulseRate']))
        if 'perfusionIndex' in data:
            self.pi_value.setText(str(data['perfusionIndex']))
        if 'source' in data:
            self.source_value.setText(str(data['source']))
        if 'respirationRate' in data:
            self.resp_value.setText(str(data['respirationRate']))
        if 'respHighLimit' in data:
            self.resp_high_limit.setText(str(data['respHighLimit']))
        if 'respLowLimit' in data:
            self.resp_low_limit.setText(str(data['respLowLimit']))

    def update_waveform(self, time_data, waveform_data, resp_time_data=None, resp_waveform_data=None):
        """
        Update the pleth and resp waveforms with scrolling.

        Args:
            time_data (list): Time data for pleth x-axis.
            waveform_data (list): Pleth waveform data.
            resp_time_data (list, optional): Time data for resp x-axis.
            resp_waveform_data (list, optional): Resp waveform data.
        """
        if waveform_data is not None and len(waveform_data) > 0:
            self.pleth_waveform.update_data(time_data, waveform_data)
        if resp_waveform_data is not None and len(resp_waveform_data) > 0:
            self.resp_waveform.update_data(resp_time_data or time_data, resp_waveform_data)
