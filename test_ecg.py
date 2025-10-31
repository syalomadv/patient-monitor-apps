import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from ecg_widget import ECGWidget

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ECG Widget Test")
        self.setGeometry(100, 100, 800, 600)
        self.ecg_widget = ECGWidget()
        self.setCentralWidget(self.ecg_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    sys.exit(app.exec())
