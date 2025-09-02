import sys
from PyQt5.QtWidgets import QApplication
from dialogs.login import LoginDialog
from dialogs.session import SessionWindow


class MainApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.session = None
        self.show_login()

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
