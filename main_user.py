import sys
from PyQt5.QtWidgets import QApplication
from dialogs.login import LoginDialog
from dialogs.session import SessionWindow

def start_login():
    login = LoginDialog()
    if login.exec_():
        user = login.user_data
        session = SessionWindow(user)
        session.session_closed.connect(start_login)
        session.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    start_login()
    sys.exit(app.exec_())
