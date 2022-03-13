from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap

class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        uic.loadUi('ui/main_widget.ui', self)
        
        self.annotationIcon = QPixmap('icons/annotation_tool.png')
        self.annotationIconLabel = self.findChild(QtWidgets.QLabel, 'annotationIconLabel')
        self.annotationIconLabel.setScaledContents(False)
        self.annotationIconLabel.setPixmap(self.annotationIcon)
        self.annotationIconLabel.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed) 
        
        self.trainingIcon = QPixmap('icons/training.png')
        self.trainingIconLabel = self.findChild(QtWidgets.QLabel, 'trainingIcon')
        self.trainingIconLabel.setScaledContents(False)
        self.trainingIconLabel.setPixmap(self.trainingIcon)
        self.trainingIconLabel.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed) 
        
        # self.testingIcon = QPixmap('icons/testing.png')
        # self.testingIconLabel = self.findChild(QtWidgets.QLabel, 'testingIcon')
        # self.testingIconLabel.setScaledContents(False)
        # self.testingIconLabel.setPixmap(self.testingIcon)
        # self.testingIconLabel.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed) 