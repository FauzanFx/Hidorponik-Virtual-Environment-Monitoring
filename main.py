# main.py

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from model import Model
from view_pyqt import View
from controller_pyqt import Controller
from environment import HydroponicEnvironment
from ui_config import STYLE_SHEET

class App(QMainWindow):
    # Inisialisasi Aplikasi Utama
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hydroponic Monitoring and Automation")
        self.setGeometry(100, 100, 1100, 650)

        self.environment = HydroponicEnvironment()
        self.model = Model()
        self.controller = Controller(self.model, self.environment)
        self.view = View(self.controller)
        
        self.controller.view = self.view
        self.controller.start_update_loop()

        self.setCentralWidget(self.view)

# Titik Masuk Eksekusi Program
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE_SHEET)
    win = App()
    win.show()
    sys.exit(app.exec())