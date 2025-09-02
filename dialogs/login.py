from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from utils.models import validate_user
from utils.config_manager import load_config

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.showFullScreen()

        layout = QVBoxLayout()

        config = load_config()
        pc_number = config.get("pc_number") if config else "0"
        self.label_pc = QLabel(f"PC {pc_number}")
        self.label_pc.setAlignment(Qt.AlignRight)
        self.label_pc.setStyleSheet("font-size: 26px; font-weight: bold; color: white;")
        layout.addWidget(self.label_pc)

        self.label = QLabel("Ingrese sus credenciales")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 22px; font-weight: bold; color: #00ffea;")
        layout.addWidget(self.label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuario")
        self.username_input.setFixedHeight(40)
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(40)
        layout.addWidget(self.password_input)

        self.btn_login = QPushButton("Iniciar Sesión")
        self.btn_login.setStyleSheet("""
            QPushButton {
                background-color: #00ffea;
                color: black;
                font-weight: bold;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #ffaa00;
                color: black;
            }
        """)
        self.btn_login.clicked.connect(self.login)
        layout.addWidget(self.btn_login)

        self.setStyleSheet("background-color: #121212; color: white; font-family: Consolas;")
        self.setLayout(layout)
        self.user_data = None

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        user = validate_user(username, password)
        if user:
            self.user_data = user
            self.accept()
        else:
            self.label.setText("❌ Usuario o contraseña incorrectos")
            self.label.setStyleSheet("font-size: 22px; font-weight: bold; color: red;")
