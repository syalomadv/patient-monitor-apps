import sys
import pyqtgraph as pg
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QPixmap, QPainter

class ImpedWidget(QWidget):
    """
    A widget for displaying Impedance (Imped) waveform for respiration monitoring,
    using pyqtgraph with yellow color, black background, and clean plotting.
    """
    def __init__(self, parent=None):
        """
        Initialize the ImpedWidget.

        Args:
            parent (QWidget): Parent widget. Defaults to None.
        """
        super().__init__(parent)

        self.setStyleSheet("background-color: #000000; border: none;")

        # Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Top row: title and scale
        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(0)

        self.title_label = QLabel("Imped")
        self.title_label.setAlignment(Qt.AlignLeft)
        self.title_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.title_label.setStyleSheet("color: #CCCCCC; background-color: transparent;")
        top_layout.addWidget(self.title_label)

        top_layout.addStretch()

        self.scale_label = QLabel("1Ω")
        self.scale_label.setAlignment(Qt.AlignRight)
        self.scale_label.setFont(QFont("Arial", 10))
        self.scale_label.setStyleSheet("color: #CCCCCC; background-color: transparent;")
        top_layout.addWidget(self.scale_label, alignment=Qt.AlignRight)  # Ensure right alignment

        layout.addLayout(top_layout)

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

        # Plot curve with yellow color
        self.curve = self.plot_widget.plot(pen=pg.mkPen('#FFFF00', width=2))  # Bright yellow for Resp

        # Double buffering with QPixmap for flicker-free rendering
        self.pixmap = QPixmap(self.plot_widget.size())
        self.pixmap.fill(Qt.black)
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_plot)
        self.update_timer.start(40)  # 40ms interval for smooth updates

    def update_data(self, x_data, y_data):
        """
        Update the waveform data.

        Args:
            x_data (list or array): X-axis data points.
            y_data (list or array): Y-axis data points.
        """
        self.curve.setData(x_data, y_data)

    def update_plot(self):
        """
        Update the plot display using double buffering to prevent flicker.
        """
        # Resize pixmap if needed
        if self.pixmap.size() != self.plot_widget.size():
            self.pixmap = QPixmap(self.plot_widget.size())
            self.pixmap.fill(Qt.black)

        # Paint to pixmap
        painter = QPainter(self.pixmap)
        self.plot_widget.render(painter)
        painter.end()

        # Update display
        self.update()

    def clear_data(self):
        """
        Clear the waveform data.
        """
        self.curve.setData([], [])

    def paintEvent(self, event):
        """
        Custom paint event for double buffering.
        """
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.pixmap)
        painter.end()
