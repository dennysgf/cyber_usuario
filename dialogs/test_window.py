from PyQt5.QtWidgets import QMainWindow, QLabel, QApplication
from PyQt5.QtCore import Qt

class TestWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.setWindowTitle("Ventana de Prueba")
        self.setGeometry(200, 200, 600, 200)

        label = QLabel(f"✅ Logeado como: {user['username']}", self)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 22px; font-weight: bold; color: #00ff00;")
        self.setCentralWidget(label)
        self.show()
