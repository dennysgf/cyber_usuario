from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QLabel, QPushButton,
    QApplication, QSystemTrayIcon, QMenu, QAction
)
from PyQt5.QtCore import QTimer, Qt, pyqtSignal
from PyQt5.QtGui import QIcon
import os
from utils.models import get_time_remaining
from utils.db import get_connection


class SessionWindow(QMainWindow):
    session_closed = pyqtSignal()

    def __init__(self, user):
        super().__init__()
        self.user = user

        # Configuración ventana tipo barra
        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.WindowStaysOnTopHint
            | Qt.WindowMinimizeButtonHint
        )

        screen_geometry = QApplication.primaryScreen().geometry()
        ancho_barra = 400
        alto_barra = 50
        x = screen_geometry.width() - ancho_barra
        self.setGeometry(x, 0, ancho_barra, alto_barra)
        self.setStyleSheet("background-color: rgba(30, 30, 30, 180);")

        # Layout
        container = QWidget()
        bar = QHBoxLayout(container)
        bar.setContentsMargins(10, 5, 10, 5)
        bar.setSpacing(10)

        # Usuario
        self.label_user = QLabel(f"👤 {self.user['username']}")
        self.label_user.setStyleSheet("font-size: 14px; font-weight: bold; color: #00ffea;")
        bar.addWidget(self.label_user)

        # Botón minimizar
        self.btn_minimize = QPushButton("—")
        self.btn_minimize.setFixedWidth(30)
        self.btn_minimize.setStyleSheet("background-color:#444; color:white; font-size:14px;")
        self.btn_minimize.clicked.connect(self.hide_to_tray)
        bar.addWidget(self.btn_minimize)

        # Botón finalizar
        self.btn_logout = QPushButton("Finalizar")
        self.btn_logout.setFixedWidth(80)
        self.btn_logout.setStyleSheet("background-color:#ff0044; color:white; font-weight:bold;")
        self.btn_logout.clicked.connect(self.close_session)
        bar.addWidget(self.btn_logout)

        # Tiempo
        self.label_timer = QLabel()
        self.label_timer.setStyleSheet("font-size: 14px; font-weight: bold; color: #00ff00;")
        bar.addWidget(self.label_timer)

        container.setLayout(bar)
        self.setCentralWidget(container)

        # Tiempo
        self.remaining_time = int(self.user["tiempo"])
        self.update_timer_label()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.countdown)
        self.timer.start(1000)

        # Ruta del ícono
        ICON_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "icons8-controlar-64.png")

        # System Tray
        self.tray_icon = QSystemTrayIcon(QIcon(ICON_PATH), self)
        tray_menu = QMenu()

        restore_action = QAction("Restaurar", self)
        restore_action.triggered.connect(self.showNormal)
        tray_menu.addAction(restore_action)

        logout_action = QAction("Finalizar sesión", self)
        logout_action.triggered.connect(self.close_session)
        tray_menu.addAction(logout_action)

        exit_action = QAction("Salir", self)
        exit_action.triggered.connect(QApplication.quit)
        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.setToolTip("Cyber Control - Barra de Sesión")

        # Restaurar con doble clic
        self.tray_icon.activated.connect(self.on_tray_activated)

        self.tray_icon.show()
        self.show()

    def hide_to_tray(self):
        self.hide()
        self.tray_icon.showMessage("Cyber Control", "La barra se ocultó en el área de notificación.")

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.showNormal()
            self.activateWindow()

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
        tiempo_guardado = int(self.remaining_time)
        conn = get_connection()
        if conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE usuarios SET tiempo_restante = %s WHERE id = %s",
                (tiempo_guardado, self.user["id"])
            )
            conn.commit()
            cur.close()
            conn.close()

        self.timer.stop()
        self.tray_icon.hide()
        self.close()

        # 🔑 dispara la señal para que main_user abra el login de nuevo
        self.session_closed.emit()

