import sys
import pyqtgraph as pg
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer, QThread, Signal
from monitor_ui import MonitorUI
from data_worker import DataWorker

class MainApp(QApplication):
    def __init__(self):
        super().__init__(sys.argv)
        self.ui = MonitorUI()
        self.ui.show()

        self.worker = DataWorker()
        self.worker.data_ready.connect(self.update_displays)
        self.worker.start()

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.on_update)
        self.update_timer.start(50)

        self.time_timer = QTimer()
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(1000)

    def on_update(self):
        if hasattr(self, 'current_data'):
            self.update_waveforms(self.current_data['waveforms'])
            self.update_vitals(self.current_data['vitals'])

    def update_displays(self, data):
        self.current_data = data

    def update_waveforms(self, waveforms):
        self.ui.ecg_plot.getPlotItem().clear()
        curve = self.ui.ecg_plot.plot(waveforms['ecg'], pen=pg.mkPen('#00FF00', width=3))
        self.ui.ecg_plot.setYRange(-1.5, 1.5)

        self.ui.pleth_plot.getPlotItem().clear()
        self.ui.pleth_plot.plot(waveforms['pleth'], pen=pg.mkPen('#00FFFF', width=3))
        self.ui.pleth_plot.setYRange(0, 100)

        self.ui.resp_plot.getPlotItem().clear()
        self.ui.resp_plot.plot(waveforms['resp'], pen=pg.mkPen('#FFFF00', width=3))
        self.ui.resp_plot.setYRange(-1, 1)

        self.ui.art_plot.getPlotItem().clear()
        self.ui.art_plot.plot(waveforms['art'], pen=pg.mkPen('#FF0000', width=3))
        self.ui.art_plot.setYRange(0, 150)

        self.ui.co2_plot.getPlotItem().clear()
        self.ui.co2_plot.plot(waveforms['co2'], pen=pg.mkPen('#FFA500', width=3))
        self.ui.co2_plot.setYRange(0, 50)

    def update_vitals(self, vitals):

        self.ui.update_vitals_ui(vitals)

    def update_time(self):
        from datetime import datetime
        self.ui.time_label.setText(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))



if __name__ == "__main__":
    app = MainApp()
    try:
        sys.exit(app.exec())
    except KeyboardInterrupt:
        app.worker.stop()
        app.worker.wait()
        sys.exit(0)
