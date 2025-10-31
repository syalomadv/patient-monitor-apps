import sys
from PySide6.QtWidgets import QApplication
import pyqtgraph
pyqtgraph.Qt.lib = 'PySide6'
pg = pyqtgraph
from monitor_ui import MonitorUI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MonitorUI()
    ui.show()
    sys.exit(app.exec())
