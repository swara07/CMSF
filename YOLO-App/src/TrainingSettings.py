from PyQt5 import QtWidgets, uic, QtCore
import os

class TrainingSettings(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi('ui/training-settings.ui', self)
        
        self.darknetBtn.clicked.connect(self.setDarknetPath)
        self.configBtn.clicked.connect(self.setConfigPath)
        self.weightBtn.clicked.connect(self.setWeightsPath)
        self.dataBtn.clicked.connect(self.setDataPath)
        
    def getValues(self):
        return (self.trainingNameInput.text(), self.weightFilePath, self.configurationFilePath, \
            self.dataFilePath, self.darknetFilePath)
       
    @staticmethod
    def launch(parent):
        dlg = TrainingSettings(parent)
        r = dlg.exec_()
        if r:
            return dlg.getValues()
        return None
       
    def setDarknetPath(self):
        self.darknetFilePath = str(QtWidgets.QFileDialog.getExistingDirectory(self,"Select Darknet Directory"))
        
        self.darknetPathInput.setText(self.darknetFilePath)
    
    def setConfigPath(self):
        self.configurationFilePath = QtWidgets.QFileDialog.getOpenFileName(self, 
                                                                           'Select Configuration File', 
                                                                           "", 
                                                                           "Configuration files (*.cfg)")[0]
        # print(self.configurationFilePath)
        self.configPathInput.setText(self.configurationFilePath)
        
    def setWeightsPath(self):
        self.weightFilePath = QtWidgets.QFileDialog.getOpenFileName(self, 
                                                                    'Select Weights',
                                                                    "", 
                                                                    "Weight files (*.weights *.74 *.137)")[0]
        # print(self.configurationFilePath)
        self.weightPathInput.setText(self.weightFilePath)
        
    def setDataPath(self):
        self.dataFilePath = QtWidgets.QFileDialog.getOpenFileName(self, 
                                                                  'Select Data File',
                                                                  "", 
                                                                  "Data files (*.data)")[0]
        # print(self.configurationFilePath)
        self.dataPathInput.setText(self.dataFilePath)
        