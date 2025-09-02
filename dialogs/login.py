from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from utils.models import validate_user
from utils.config_manager import load_config
from dialogs.exit_dialog import ExitDialog


class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.showFullScreen()

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # Barra superior con botón X
        top_bar = QHBoxLayout()
        self.btn_exit = QPushButton("X")
        self.btn_exit.setFixedSize(40, 40)
        self.btn_exit.setStyleSheet("""
            QPushButton {
                background-color: #ff0044;
                color: white;
                font-weight: bold;
                font-size: 18px;
                border-radius: 6px;
                border: 2px solid #ff0044;
            }
            QPushButton:hover {
                background-color: #0d0d0d;
                color: #ff0044;
                border: 2px solid #ffaa00;
            }
        """)
        self.btn_exit.clicked.connect(self.try_exit)
        top_bar.addWidget(self.btn_exit, alignment=Qt.AlignLeft)
        main_layout.addLayout(top_bar)

        # Número de PC
        config = load_config()
        pc_number = config.get("pc_number") if config else "0"
        self.label_pc = QLabel(f"PC {pc_number}")
        self.label_pc.setAlignment(Qt.AlignRight)
        self.label_pc.setStyleSheet("font-size: 28px; font-weight: bold; color: #00ffea;")
        main_layout.addWidget(self.label_pc)

        # Título central gamer
        self.label = QLabel("⚡ Ingrese sus credenciales ⚡")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont("Consolas", 22, QFont.Bold))
        self.label.setStyleSheet("color: #00ffea; margin: 25px; text-shadow: 0px 0px 10px #00ffea;")
        main_layout.addWidget(self.label)

        # Input Usuario
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("👤 Usuario")
        self.username_input.setFixedWidth(320)
        self.username_input.setFixedHeight(45)
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: #1a1a1a;
                border: 2px solid #00ffea;
                border-radius: 10px;
                color: white;
                padding: 8px;
                font-size: 16px;
            }
            QLineEdit:focus {
                border: 2px solid #ffaa00;
                box-shadow: 0 0 10px #ffaa00;
            }
        """)
        main_layout.addWidget(self.username_input, alignment=Qt.AlignCenter)

        # Input Contraseña
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("🔒 Contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedWidth(320)
        self.password_input.setFixedHeight(45)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #1a1a1a;
                border: 2px solid #00ffea;
                border-radius: 10px;
                color: white;
                padding: 8px;
                font-size: 16px;
            }
            QLineEdit:focus {
                border: 2px solid #ffaa00;
                box-shadow: 0 0 10px #ffaa00;
            }
        """)
        self.password_input.returnPressed.connect(self.login)  # Enter = login
        main_layout.addWidget(self.password_input, alignment=Qt.AlignCenter)

        # Botón de Login
        self.btn_login = QPushButton("🎮 Iniciar Sesión 🎮")
        self.btn_login.setFixedWidth(320)
        self.btn_login.setFixedHeight(45)
        self.btn_login.setStyleSheet("""
            QPushButton {
                background-color: #00ffea;
                color: black;
                font-weight: bold;
                font-size: 16px;
                border-radius: 10px;
                border: 2px solid #00ffea;
            }
            QPushButton:hover {
                background-color: #0d0d0d;
                color: #ffaa00;
                border: 2px solid #ffaa00;
                box-shadow: 0 0 15px #ffaa00;
            }
        """)
        self.btn_login.clicked.connect(self.login)
        main_layout.addWidget(self.btn_login, alignment=Qt.AlignCenter)

        # Fondo dinámico gamer
        self.setStyleSheet("""
            QDialog {
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0d0d0d, stop:1 #1e1e2e
                );
                color: white;
                font-family: Consolas;
            }
        """)

        self.setLayout(main_layout)
        self.user_data = None

    def try_exit(self):
        dlg = ExitDialog(self)
        if dlg.exec_() == ExitDialog.Accepted and dlg.accepted:
            self.reject()

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        user = validate_user(username, password)
        if user:
            self.user_data = user
            self.accept()
        else:
            self.label.setText("❌ Usuario o contraseña incorrectos ❌")
            self.label.setStyleSheet("color: #ff0044; font-size: 20px; font-weight: bold;")
