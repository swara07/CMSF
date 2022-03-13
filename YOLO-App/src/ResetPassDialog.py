from PyQt5 import QtWidgets, uic

class ResetPasswordDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi('ui/passReset.ui', self)
        
        
    def getValues(self):
        return (self.usernameField.text(), \
                    self.passwordField.text(),\
                        self.newPassField.text(),\
                            self.cnfPassField.text())
       
    @staticmethod
    def launch(parent):
        dlg = ResetPasswordDialog(parent)
        r = dlg.exec_()
        # print(r)
        if r == QtWidgets.QDialog.Accepted:
            return dlg.getValues()
        return None
