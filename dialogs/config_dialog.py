from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from utils.config_manager import save_config
from utils.db import get_connection

class ConfigDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuración CyberUsuario")

        layout = QVBoxLayout()

        self.label_pc = QLabel("Número de PC:")
        layout.addWidget(self.label_pc)
        self.input_pc = QLineEdit()
        layout.addWidget(self.input_pc)

        self.label_ip = QLabel("IP del Servidor:")
        layout.addWidget(self.label_ip)
        self.input_ip = QLineEdit()
        layout.addWidget(self.input_ip)

        self.btn_test = QPushButton("Probar conexión")
        self.btn_test.clicked.connect(self.test_connection)
        layout.addWidget(self.btn_test)

        self.setLayout(layout)
        self.success = False

    def test_connection(self):
        pc_number = self.input_pc.text().strip()
        server_ip = self.input_ip.text().strip()

        conn = get_connection(host=server_ip)
        if conn:
            conn.close()
            save_config(pc_number, server_ip)
            QMessageBox.information(self, "Éxito", "Conexión exitosa, configuración guardada.")
            self.success = True
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "No se pudo conectar al servidor.")
