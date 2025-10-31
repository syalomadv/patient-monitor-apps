import sys
import pyqtgraph as pg
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class WaveformWidget(QWidget):
    """
    A reusable widget for displaying waveforms in a patient monitor UI,
    using pyqtgraph to mimic the Mindray style with black background,
    white foreground, subtle grids, and clean plotting.
    """
    def __init__(self, title="", scale="", parent=None):
        """
        Initialize the WaveformWidget.

        Args:
            title (str): Optional title for the waveform (e.g., "ECG", "Pleth"). Defaults to "".
            scale (str): Optional scale for the waveform (e.g., "1mV", "1V"). Defaults to "".
            parent (QWidget): Parent widget. Defaults to None.
        """
        super().__init__(parent)
        self.title = title
        self.scale = scale

        self.setStyleSheet("background-color: #000000; border: none;")

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Optional title label
        if self.title:
            self.title_label = QLabel(self.title)
            self.title_label.setAlignment(Qt.AlignCenter)
            self.title_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
            self.title_label.setStyleSheet("color: #FFFFFF; background-color: transparent;")
            layout.addWidget(self.title_label)

        # Optional scale label
        if self.scale:
            self.scale_label = QLabel(self.scale)
            self.scale_label.setAlignment(Qt.AlignCenter)
            self.scale_label.setFont(QFont("Segoe UI", 8))
            self.scale_label.setStyleSheet("color: #CCCCCC; background-color: transparent;")
            layout.addWidget(self.scale_label)

        # Plot widget
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setBackground('#000000')
        self.plot_widget.showGrid(x=True, y=True, alpha=0.2)
        self.plot_widget.getPlotItem().getAxis('bottom').setPen('#222222')
        self.plot_widget.getPlotItem().getAxis('left').setPen('#222222')
        self.plot_widget.getPlotItem().getAxis('bottom').setStyle(showValues=False)
        self.plot_widget.getPlotItem().getAxis('left').setStyle(showValues=False)
        self.plot_widget.setMouseEnabled(x=False, y=False)
        self.plot_widget.hideButtons()

        layout.addWidget(self.plot_widget)

        # Configure pyqtgraph options
        pg.setConfigOption('background', '#000000')
        pg.setConfigOption('foreground', '#FFFFFF')
        pg.setConfigOptions(antialias=True)

        # Plot curve
        self.curve = self.plot_widget.plot(pen=pg.mkPen('#FFFFFF', width=2))

    def update_data(self, x_data, y_data):
        """
        Update the waveform data.

        Args:
            x_data (list or array): X-axis data points.
            y_data (list or array): Y-axis data points.
        """
        self.curve.setData(x_data, y_data)

    def set_pen_color(self, color):
        """
        Set the color of the waveform line.

        Args:
            color (str): Hex color code (e.g., "#00FF00").
        """
        self.curve.setPen(pg.mkPen(color, width=2))

    def clear_data(self):
        """
        Clear the waveform data.
        """
        self.curve.setData([], [])

    def set_y_limits(self, min_val, max_val):
        """
        Set the Y-axis limits for the plot.

        Args:
            min_val (float): Minimum Y value.
            max_val (float): Maximum Y value.
        """
        self.plot_widget.setYRange(min_val, max_val)
