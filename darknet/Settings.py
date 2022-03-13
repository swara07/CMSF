from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import QPixmap
from qtwidgets import AnimatedToggle

class SettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi('settings.ui', self)