import sys
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import pyqtgraph as pg

class ECGWidget(QWidget):
    """
    A PyQt6 widget for displaying ECG parameters in a patient monitor style,
    with black background, bright green text and waveforms, mimicking Mindray or Philips monitors.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #000000; color: #00FF00;")

        # Main horizontal layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(20)

        # Left side: Waveforms
        self.create_left_side(main_layout)

        # Right side: Numeric display
        self.create_right_side(main_layout)

        # Configure pyqtgraph
        pg.setConfigOption('background', '#000000')
        pg.setConfigOption('foreground', '#00FF00')
        pg.setConfigOptions(antialias=True)

    def create_left_side(self, parent_layout):
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(5)

        # Top indicators
        indicators_label = QLabel("X1    Diagnostic    Notch Off")
        indicators_label.setFont(QFont("Segoe UI", 10))
        indicators_label.setStyleSheet("color: #00FF00; background-color: transparent;")
        indicators_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(indicators_label)

        # ECG II waveform
        ii_label = QLabel("II")
        ii_label.setFont(QFont("Courier New", 12, QFont.Weight.Bold))
        ii_label.setStyleSheet("color: #00FF00; background-color: transparent;")
        ii_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(ii_label)

        self.ii_plot = pg.PlotWidget()
        self.ii_plot.setBackground('#000000')
        self.ii_plot.showGrid(x=True, y=True, alpha=0.2)
        self.ii_plot.getPlotItem().getAxis('bottom').setPen('#222222')
        self.ii_plot.getPlotItem().getAxis('left').setPen('#222222')
        self.ii_plot.getPlotItem().getAxis('bottom').setStyle(showValues=False)
        self.ii_plot.getPlotItem().getAxis('left').setStyle(showValues=False)
        self.ii_plot.setMouseEnabled(x=False, y=False)
        self.ii_plot.hideButtons()
        self.ii_curve = self.ii_plot.plot(pen=pg.mkPen('#00FF00', width=2))
        left_layout.addWidget(self.ii_plot)

        scale_label_ii = QLabel("1 mV")
        scale_label_ii.setFont(QFont("Courier New", 10))
        scale_label_ii.setStyleSheet("color: #00FF00; background-color: transparent;")
        scale_label_ii.setAlignment(Qt.AlignmentFlag.AlignRight)
        left_layout.addWidget(scale_label_ii)

        # ECG I waveform
        i_label = QLabel("I")
        i_label.setFont(QFont("Courier New", 12, QFont.Weight.Bold))
        i_label.setStyleSheet("color: #00FF00; background-color: transparent;")
        i_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        left_layout.addWidget(i_label)

        self.i_plot = pg.PlotWidget()
        self.i_plot.setBackground('#000000')
        self.i_plot.showGrid(x=True, y=True, alpha=0.2)
        self.i_plot.getPlotItem().getAxis('bottom').setPen('#222222')
        self.i_plot.getPlotItem().getAxis('left').setPen('#222222')
        self.i_plot.getPlotItem().getAxis('bottom').setStyle(showValues=False)
        self.i_plot.getPlotItem().getAxis('left').setStyle(showValues=False)
        self.i_plot.setMouseEnabled(x=False, y=False)
        self.i_plot.hideButtons()
        self.i_curve = self.i_plot.plot(pen=pg.mkPen('#00FF00', width=2))
        left_layout.addWidget(self.i_plot)

        scale_label_i = QLabel("1 mV")
        scale_label_i.setFont(QFont("Courier New", 10))
        scale_label_i.setStyleSheet("color: #00FF00; background-color: transparent;")
        scale_label_i.setAlignment(Qt.AlignmentFlag.AlignRight)
        left_layout.addWidget(scale_label_i)

        parent_layout.addWidget(left_widget, 7)

    def create_right_side(self, parent_layout):
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(10)

        # ECG label
        ecg_label = QLabel("ECG")
        ecg_label.setFont(QFont("Courier New", 14, QFont.Weight.Bold))
        ecg_label.setStyleSheet("color: #00FF00; background-color: transparent;")
        ecg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(ecg_label)

        # Heart rate
        self.hr_label = QLabel("60")
        self.hr_label.setFont(QFont("Courier New", 48, QFont.Weight.Bold))
        self.hr_label.setStyleSheet("color: #00FF00; background-color: transparent;")
        self.hr_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(self.hr_label)

        # PVCs
        pvcs_label = QLabel("PVCs 0")
        pvcs_label.setFont(QFont("Courier New", 12))
        pvcs_label.setStyleSheet("color: #00FF00; background-color: transparent;")
        pvcs_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(pvcs_label)

        # ST-II
        st_ii_label = QLabel("ST-II 0.10")
        st_ii_label.setFont(QFont("Courier New", 12))
        st_ii_label.setStyleSheet("color: #00FF00; background-color: transparent;")
        st_ii_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(st_ii_label)

        # ST segment grid - aligned baseline with HR
        st_container = QWidget()
        st_container.setStyleSheet("margin-top: 10px;")  # Adjust to align baseline
        st_layout = QVBoxLayout(st_container)
        st_layout.setContentsMargins(0, 0, 0, 0)
        st_layout.setSpacing(5)

        st_label = QLabel("ST-Segment")
        st_label.setFont(QFont("Courier New", 12))
        st_label.setStyleSheet("color: #00FF00; background-color: transparent;")
        st_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        st_layout.addWidget(st_label)

        st_grid = QGridLayout()
        st_grid.setSpacing(5)

        leads = ["V1", "V2", "V3", "V4", "V5", "V6", "II", "III", "aVR", "aVL", "aVF"]
        values = ["0.04", "0.05", "0.03", "0.02", "0.01", "0.00", "0.10", "0.08", "-0.02", "-0.01", "0.03"]

        for i, lead in enumerate(leads):
            lead_label = QLabel(lead)
            lead_label.setFont(QFont("Courier New", 10))
            lead_label.setStyleSheet("color: #00FF00; background-color: transparent;")
            lead_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            st_grid.addWidget(lead_label, i // 3, (i % 3) * 2)

            value_label = QLabel(values[i])
            value_label.setFont(QFont("Courier New", 10))
            value_label.setStyleSheet("color: #00FF00; background-color: transparent;")
            value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            st_grid.addWidget(value_label, i // 3, (i % 3) * 2 + 1)

        st_layout.addLayout(st_grid)
        right_layout.addWidget(st_container)
        right_layout.addStretch()

        parent_layout.addWidget(right_widget, 3)

    def update_waveforms(self, ii_data, i_data):
        """
        Update the ECG waveforms.

        Args:
            ii_data (list): Data for lead II.
            i_data (list): Data for lead I.
        """
        self.ii_curve.setData(ii_data)
        self.i_curve.setData(i_data)

    def update_hr(self, hr):
        """
        Update the heart rate display.

        Args:
            hr (str): Heart rate value.
        """
        self.hr_label.setText(hr)

    def update_st_values(self, st_dict):
        """
        Update the ST segment values.

        Args:
            st_dict (dict): Dictionary with lead names as keys and values as strings.
        """
        # For dynamic updates, implement if needed
        pass
