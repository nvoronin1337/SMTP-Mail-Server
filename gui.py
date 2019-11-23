import sys
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QObject, pyqtSlot

from python_ui.Ui_login_dialog import Ui_Dialog
from python_ui.Ui_inbox import Ui_MainWindow

from client import MAILClient

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.accepted.connect(self.ok_clicked)
    
    @pyqtSlot()
    def ok_clicked(self):
        email = str(self.ui.email_le.text())
        password = str(self.ui.pass_le.text())
        HOST, PORT = '::1', 8025
        try:
            client = MAILClient(HOST, PORT, email, password,1)
            #pass client to inbox window and close dialog
            
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Incorrect credentials!")
            msg.setInformativeText('Please try again!')
            msg.setWindowTitle('Can\'t sign in')
            msg.setStandardButtons(QMessageBox.Ok)
            def close_msg():
                msg.close()
            msg.buttonClicked.connect(close_msg)
            msg.exec_()
            self.show()
            #print('Error: Invalid Credentials')

    @pyqtSlot()
    def cancel_clicked(self):
        self.close()


class InboxWindow(QMainWindow):
    def __init__(self):
        super(InboxWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #setup handlers here


def main():
    app = QApplication(sys.argv)
    dialog = LoginDialog()
    dialog.show()
    #window = InboxWindow()
    #window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
