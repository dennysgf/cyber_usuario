import os
from dotenv import load_dotenv
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

load_dotenv()

class ExitDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirmar salida")

        layout = QVBoxLayout()

        self.label = QLabel("Ingrese credenciales de administrador")
        layout.addWidget(self.label)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuario")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.btn_confirm = QPushButton("Confirmar")
        self.btn_confirm.clicked.connect(self.check_credentials)
        layout.addWidget(self.btn_confirm)

        self.setLayout(layout)
        self.accepted = False

    def check_credentials(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        exit_user = os.getenv("EXIT_USER")
        exit_pass = os.getenv("EXIT_PASS")

        if username == exit_user and password == exit_pass:
            self.accepted = True
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "Credenciales incorrectas")
