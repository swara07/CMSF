from PyQt5 import QtWidgets, uic, QtCore
import os

class InferenceSettings(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi('inference-settings.ui', self)
        
        self.settings = QtCore.QSettings("TIFR", "Cms-App")
    
        try:
            self.darknetField.setText(self.settings.value("inferenceDarknet"))
            self.configField.setText(self.settings.value("inferenceConfig"))
            self.weightsField.setText(self.settings.value("inferenceWeights"))
            self.dataFileField.setText(self.settings.value("inferenceData"))
         
        except:
            self.parentWidget().statusbar.showMessage("Settings could not be loaded. Please use the button above to set paths", 10000)
            
        
        self.msgBox = QtWidgets.QMessageBox(self)

        self.darknetBtn.clicked.connect(self.setDarknetPath)
        self.configBtn.clicked.connect(self.setCfgPath)
        self.weightsBtn.clicked.connect(self.setWeightsPath)
        self.dataFileBtn.clicked.connect(self.setDataFilePath)

    def getValues(self):
        return (self.darknetField.text(), \
            self.configField.text(), \
            self.weightsField.text(), \
            self.dataFileField.text())
       
    @staticmethod
    def launch(parent):
        dlg = InferenceSettings(parent)
        r = dlg.exec_()
        if r:
            return dlg.getValues()
        return None

    def setDarknetPath(self):
        self.darknetFilePath = str(QtWidgets.QFileDialog.getExistingDirectory(self,"Select Darknet Directory"))
        
        def checkForDarknet(path):
            if os.path.isfile(path + str("/darknet_images.py")):
                return True 
        
        if not checkForDarknet(self.darknetFilePath):
            self.msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            self.msgBox.setText("Darknet Not Found")
            self.msgBox.setInformativeText("Please select directory where darknet_images.py exists")
            self.msgBox.setWindowTitle("Warning")
            self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.msgBox.exec()
            
        else:
            self.darknetField.setText(self.darknetFilePath)
    
    def setCfgPath(self):
        self.configurationFilePath = QtWidgets.QFileDialog.getOpenFileName(self, 
                                                                           'Select Configuration File', 
                                                                           "", 
                                                                           "Configuration files (*.cfg)")[0]
        # print(self.configurationFilePath)
        self.configField.setText(self.configurationFilePath)
        
    def setWeightsPath(self):
        self.weightFilePath = QtWidgets.QFileDialog.getOpenFileName(self, 
                                                                    'Select Weights',
                                                                    "", 
                                                                    "Weight files (*.weights)")[0]
        # print(self.configurationFilePath)
        self.weightsField.setText(self.weightFilePath)
        
    def setDataFilePath(self):
        self.dataFilePath = QtWidgets.QFileDialog.getOpenFileName(self, 
                                                                  'Select Data File',
                                                                  "", 
                                                                  "Data files (*.data)")[0]
        # print(self.configurationFilePath)
        self.dataFileField.setText(self.dataFilePath)