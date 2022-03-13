from PyQt5 import QtWidgets, uic, QtCore
import os
import subprocess

class InferenceSettings(QtWidgets.QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        uic.loadUi('ui/predictions-settings.ui', self)
        
        self.settings = QtCore.QSettings("TIFR", "Cms-App")
    
        try:
            self.darknetField.setText(self.settings.value("inferenceDarknet"))
            self.configField.setText(self.settings.value("inferenceConfig"))
            self.weightsField.setText(self.settings.value("inferenceWeights"))
            self.dataFileField.setText(self.settings.value("inferenceData"))
            self.darknetField.setStyleSheet("color: black;border-bottom: 2px solid black;")
            self.configField.setStyleSheet("color: black;border-bottom: 2px solid black;")
            self.weightsField.setStyleSheet("color: black;border-bottom: 2px solid black;")
            self.dataFileField.setStyleSheet("color: black;border-bottom: 2px solid black;")
            
        except:
            self.parentWidget().statusbar.showMessage("Settings could not be loaded. Please use the button above to set paths", 10000)
            
        
        self.msgBox = QtWidgets.QMessageBox(self)

        self.darknetBtn.clicked.connect(self.setDarknetPath)
        self.configBtn.clicked.connect(self.setCfgPath)
        self.weightsBtn.clicked.connect(self.setWeightsPath)
        self.dataFileBtn.clicked.connect(self.setDataFilePath)
        # self.radioButton.clicked.connect(self.radio)
        # self.radioButton_2.clicked.connect(self.radio)
        self.darknetBtn.setStyleSheet("color: white;border-style: none;border-width: none;border-radius: 0px;border-color: black;font:bold 14px;min-width: 7em;padding: 6px;background-color: grey;")
        self.configBtn.setStyleSheet("color: white;border-style: none;border-width: none;border-radius: 0px;border-color: black;font:bold 14px;min-width: 7em;padding: 6px;background-color: grey;")
        self.weightsBtn.setStyleSheet("color: white;border-style: none;border-width: none;border-radius: 0px;border-color: black;font:bold 14px;min-width: 7em;padding: 6px;background-color: grey;")
        self.dataFileBtn.setStyleSheet("color: white;border-style: none;border-width: none;border-radius: 0px;border-color: black;font:bold 14px;min-width: 7em;padding: 6px;background-color: grey;")
    # def radio(self):
    #     if self.radioButton.isChecked():
    #         prevDir = os.getcwd()
    #         os.chdir(self.darknetField.text())
    #         print(prevDir)
    #         a_file = open("Makefile", "r")
    #         list_of_lines = a_file.readlines()
    #         list_of_lines[0] = "GPU=1\n"
    #         list_of_lines[1] = "CUDNN=1\n"
    #         list_of_lines[2] = "CUDNN_HALF=1\n"
    #         a_file = open("Makefile", "w")
    #         a_file.writelines(list_of_lines)
    #         a_file.close()
    #         os.system("make")
    #         os.chdir(prevDir)
        # elif self.radioButton_2.isChecked():
        #     prevDir = os.getcwd()
        #     os.chdir(self.darknetField.text())
        #     print(prevDir)
        #     a_file = open("Makefile", "r")
        #     list_of_lines = a_file.readlines()
        #     list_of_lines[0] = "GPU=0\n"
        #     list_of_lines[1] = "CUDNN=0\n"
        #     list_of_lines[2] = "CUDNN_HALF=0\n"
        #     a_file = open("Makefile", "w")
        #     a_file.writelines(list_of_lines)
        #     a_file.close()
        #     subprocess.call("make",shell=True)
        #     os.chdir(prevDir)
        # else:
        #     prevDir = os.getcwd()
        #     os.chdir(self.darknetField.text())
        #     print(prevDir)
        #     a_file = open("Makefile", "r")
        #     list_of_lines = a_file.readlines()
        #     list_of_lines[0] = "GPU=0\n"
        #     list_of_lines[1] = "CUDNN=0\n"
        #     list_of_lines[2] = "CUDNN_HALF=0\n"
        #     a_file = open("Makefile", "w")
        #     a_file.writelines(list_of_lines)
        #     a_file.close()
        #     os.system("make")
        #     os.chdir(prevDir)
    def getValues(self):
        return (self.darknetField.text(), 
            self.configField.text(), 
            self.weightsField.text(), 
            self.dataFileField.text())
       
    @staticmethod
    def launch(parent):
        dlg = InferenceSettings(parent)
        r = dlg.exec_()
        if r:
            return dlg.getValues()
        return None
    @staticmethod
    def getValuetry(parent):
        dlg = InferenceSettings(parent)
        # r = dlg.exec_()
        # if r:
        return dlg.getValues()
        # return None

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