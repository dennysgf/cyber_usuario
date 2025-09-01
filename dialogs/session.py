from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLabel, QPushButton, QApplication
from PyQt5.QtCore import QTimer, Qt, pyqtSignal
from utils.models import logout_user, get_time_remaining

class SessionWindow(QMainWindow):
    session_closed = pyqtSignal()

    def __init__(self, user):
        super().__init__()
        self.user = user
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.show()
        screen_geometry = QApplication.primaryScreen().geometry()
        self.setGeometry(0, 0, screen_geometry.width(), 80)

        container = QWidget()
        bar = QHBoxLayout(container)

        self.label_user = QLabel(f"👤 {self.user['username']}")
        self.label_user.setStyleSheet("font-size: 16px; font-weight: bold; color: #00ffea;")
        bar.addWidget(self.label_user)

        self.label_timer = QLabel()
        self.label_timer.setStyleSheet("font-size: 16px; font-weight: bold; color: #00ff00;")
        bar.addWidget(self.label_timer)

        self.btn_logout = QPushButton("Finalizar")
        self.btn_logout.setStyleSheet("""
            QPushButton {
                background-color: #ff0044;
                color: white;
                font-weight: bold;
                padding: 4px 10px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #ffaa00;
                color: black;
            }
        """)
        self.btn_logout.clicked.connect(self.close_session)
        bar.addWidget(self.btn_logout)

        container.setLayout(bar)
        self.setCentralWidget(container)

        self.remaining_time = float(self.user["tiempo"]) * 3600
        self.update_timer_label()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.countdown)
        self.timer.start(1000)

    def update_timer_label(self):
        horas = int(self.remaining_time) // 3600
        minutos = (int(self.remaining_time) % 3600) // 60
        segundos = int(self.remaining_time) % 60
        self.label_timer.setText(f"⏳ {horas:02d}:{minutos:02d}:{segundos:02d}")

    def countdown(self):
        db_time = get_time_remaining(self.user["id"])
        if db_time <= 0:
            self.close_session()
            return
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.update_timer_label()
        else:
            self.close_session()

    def close_session(self):
        logout_user(self.user["id"])
        self.timer.stop()
        self.close()
        self.session_closed.emit()
