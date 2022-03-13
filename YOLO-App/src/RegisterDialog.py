from PyQt5 import QtWidgets, uic

class RegisterDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi('ui/register.ui', self)

    def getValues(self):
        return (self.usernameField.text(), \
                    self.passwordField.text(),\
                        self.nameField.text(),\
                            self.emailField.text(),\
                                self.phoneField.text(),\
                                    self.employeeIDField.text())
       
    @staticmethod
    def launch(parent):
        dlg = RegisterDialog(parent)
        r = dlg.exec_()
        # print(r)
        if r == QtWidgets.QDialog.Accepted:
            return dlg.getValues()
        return None
        