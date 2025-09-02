import sys
from PyQt5.QtWidgets import QApplication
from dialogs.login import LoginDialog
from dialogs.session import SessionWindow
from dialogs.config_dialog import ConfigDialog
from utils.config_manager import load_config
import os
from PyQt5.QtGui import QIcon

class MainApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.session = None
        self.ensure_config()
        self.show_login()
        icon_path = os.path.join(os.path.dirname(__file__), "assets", "icons8-controlar-64.ico")
        self.app.setWindowIcon(QIcon(icon_path))

    def ensure_config(self):
        config = load_config()
        if not config:
            config_dialog = ConfigDialog()
            if config_dialog.exec_() != ConfigDialog.Accepted or not config_dialog.success:
                sys.exit(0)

    def show_login(self):
        login = LoginDialog()
        if login.exec_():
            user = login.user_data
            self.start_session(user)
        else:
            sys.exit(0)

    def start_session(self, user):
        self.session = SessionWindow(user)
        self.session.session_closed.connect(self.show_login)
        self.session.show()

    def run(self):
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    app = MainApp()
    app.run()
