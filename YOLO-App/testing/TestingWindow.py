from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import QPixmap, QIcon

from src.InferenceSettings import InferenceSettings
from src.Inference import Inference

class Worker(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    dataSent = QtCore.pyqtSignal(str)
    
    def __init__(self, imgPath,darknetPath, configPath, weightPath, dataPath, autoCorrectFlag, parent=None):
        super(Worker, self).__init__(parent)

        self.imgPath = imgPath
        self.autoCorrectFlag = autoCorrectFlag
        self.inferencer = Inference(darknetPath, 
                                    configPath,
                                    weightPath,
                                    dataPath)  
        
    def run(self):
        """Long-running task."""
        outputText = self.inferencer.getInferences(self.imgPath, self.autoCorrectFlag)
        self.dataSent.emit(outputText)
        self.finished.emit()

class TestingWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(TestingWindow, self).__init__(parent)
        uic.loadUi('ui/testing.ui', self)
        
        self.settings = QtCore.QSettings("TIFR", "GSR-App")
        geometry = self.settings.value('TestingWindowGeometry', bytes('', 'utf-8'))
        self.restoreGeometry(geometry)
        
        self.outputField.setStyleSheet("QTextEdit"
                                       "{"
                                       "background: white;"
                                       "color: black;"
                                       "}")
        
        self.testingImagePath = None
        self.autoCorrectFlag = False
        
        self._createToolBarActions()
        self._createToolBar()
        self._createStatusBar()
        self.restoreSettings()
        
        # Connecting slots
        self.clearBtn.clicked.connect(self.clearSetImage)
        self.imageBtn_2.clicked.connect(self.setImagePath)
        self.predictBtn.clicked.connect(self.predict)
        self.saveButton.clicked.connect(self.saveAsText)
        
        self.autoCorrectChkBox.setChecked(False)
        self.autoCorrectChkBox.stateChanged.connect(lambda:self.btnstate(self.autoCorrectChkBox))
                
    def btnstate(self,b):
        
        if b.isChecked() == True:
            self.autoCorrectFlag = True
        else:
            self.autoCorrectFlag = False
                
    def _createToolBarActions(self):
        self.backAction = QtWidgets.QAction(QIcon(":back.png"), "Back", self)
        self.testingSettingsAction = QtWidgets.QAction(QIcon(":settings.png"), "Inference Settings", self)
        
    def _createToolBar(self):
        """
        Create toolbar
        
        Arguments: None
        Returns: None
        """
        
        fileToolBar = QtWidgets.QToolBar("File")
        fileToolBar.setMovable(False)
        self.addToolBar(fileToolBar)
        
        # Adding buttons i.e actions
        fileToolBar.addAction(self.backAction)
        fileToolBar.addSeparator()
        fileToolBar.addAction(self.testingSettingsAction)
        
        # Connecting slots for actions
        self.backAction.triggered.connect(self.backButton)
        self.testingSettingsAction.triggered.connect(self.settingsWindow)
        
    def _createStatusBar(self):
        """
        Create status bar to display messages
        
        Arguments: None
        Returns: None
        """
        self.statusbar = self.statusBar()
        # Adding a temporary message
        self.statusBar().showMessage("Ready", 10000)
        
    def settingsWindow(self):
        # Get values from dialog
        values = InferenceSettings.launch(self)
        
        if values:
    
            self.darknetPath = values[0]
            self.configPath = values[1]
            self.weightPath = values[2]
            self.dataPath = values[3]
            
            self.settings.setValue("inferenceDarknet", self.darknetPath)
            self.settings.setValue("inferenceConfig", self.configPath)
            self.settings.setValue("inferenceWeights", self.weightPath)
            self.settings.setValue("inferenceData", self.dataPath)
            
            self.statusBar().showMessage("New Settings Saved", 10000)
            
        else:
            self.statusBar().showMessage("New settings not saved. Press OK after making changes to save", 10000)
                 
    def backButton(self):
        self.close()
        self.parentWidget().show()
    
    def closeEvent(self, event):
        geometry = self.saveGeometry()
        self.settings.setValue('TestingWindowGeometry', geometry)
        super(TestingWindow, self).closeEvent(event)
    
    def restoreSettings(self):
        
        self.darknetPath = self.settings.value("inferenceDarknet")
        self.configPath = self.settings.value("inferenceConfig")
        self.weightPath = self.settings.value("inferenceWeights")
        self.dataPath = self.settings.value("inferenceData")
            
        if not self.checkPaths():
                         
            self.statusBar().showMessage("Paths not set. Use the settings button above", 10000)
        
    def setImagePath(self):
        
        self.inputImagePlaceholder_2.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.testingImagePath = QtWidgets.QFileDialog.getOpenFileName(self, 
                                                                  'Select Data File',
                                                                  "", 
                                                                  "Image files (*.jpg *.png)")
        # print(self.configurationFilePath)
        self.image = QPixmap(self.testingImagePath[0])
        # self.inputImagePlaceholder_2.setScaledContents(True)
        # self.inputImagePlaceholder_2.resize(self.image.width(), self.image.height())
        self.inputImagePlaceholder_2.setPixmap(self.image.scaled(\
                self.inputImagePlaceholder_2.width(),\
                self.inputImagePlaceholder_2.height(),\
                QtCore.Qt.KeepAspectRatio
            ))
        
    def clearSetImage(self):
        """
        Clear Image Window
        Input: None
        Returns: None
        """
        self.inputImagePlaceholder_2.clear()
        
    def handleThreadStarted(self):
        self.predictBtn.setText("Processing")
        self.predictBtn.setEnabled(False)

    def handleThreadFinished(self):
        self.button.setText('Predict')
        self.predictBtn.setEnabled(True)
        
    def setOutputText(self, data):
        self.outputField.setText(data)
        
    def predict(self):
        
        def disableButtons(stylesheet):
            
            self.clearBtn.setEnabled(False)
            self.clearBtn.setStyleSheet(stylesheet)
            
            self.imageBtn_2.setEnabled(False)
            self.imageBtn_2.setStyleSheet(stylesheet)
            
            self.saveButton.setEnabled(False)
            self.saveButton.setStyleSheet(stylesheet)
            
            self.predictBtn.setEnabled(False)
            self.predictBtn.setText("Processing")
            self.predictBtn.setStyleSheet(stylesheet)
            
            self.statusBar().showMessage("Getting Results...Please wait")
        
        def enableButtons(stylesheet):
            self.predictBtn.setEnabled(True)
            self.predictBtn.setStyleSheet(stylesheet)
            self.predictBtn.setText("Predict")
                
            self.clearBtn.setEnabled(True)    
            self.clearBtn.setStyleSheet(stylesheet)

            self.imageBtn_2.setEnabled(True)
            self.imageBtn_2.setStyleSheet(stylesheet)
            
            self.saveButton.setStyleSheet(stylesheet)
            self.saveButton.setEnabled(True)
            
            self.statusBar().showMessage("Processing Complete", 10000)

        if self.checkPaths():
            
            if self.testingImagePath:
                
                ogStylesheet = self.imageBtn_2.styleSheet() 
                
                ### INFERENCE THREAD ###
                # QThread Object
                self.thread = QtCore.QThread()
                
                # Worker Object
                self.worker = Worker(self.testingImagePath[0], self.darknetPath, \
                    self.configPath, self.weightPath, self.dataPath, self.autoCorrectFlag)
                
                # Moving worker to the thread
                self.worker.moveToThread(self.thread)
                
                # Connecting signals and slots
                self.thread.started.connect(self.worker.run)
                self.worker.finished.connect(self.thread.quit)
                self.worker.finished.connect(self.worker.deleteLater)
                self.thread.finished.connect(self.thread.deleteLater)
                self.worker.dataSent.connect(self.setOutputText)
                
                # Starting the thread
                self.thread.start()

                btnDisableStylesheet = """QPushButton{
                                        color: #848c86;
                                        border-style: none;
                                        border-width: 3px;
                                        border-radius: 8px;
                                        border-color: #3b403c;
                                        border-bottom: 4px solid #3b403c;
                                        background-color: rgb(59, 64, 60);
                                        font: bold 14px;
                                        min-width: 10em;
                                        padding: 6px;
                                    } """
                
                disableButtons(btnDisableStylesheet)
                
                self.thread.finished.connect(lambda: enableButtons(stylesheet=ogStylesheet))
                
            else:
                
                self.errorBox("Please open an image")
                
        else:
            
            self.errorBox("Path(s) Not Set")
            
    def checkPaths(self):
        
        if all(v is not None for v in [self.darknetPath, self.configPath, self.weightPath, self.dataPath]):
            return True
            
        return False
            
    def saveAsText(self):
        text = self.outputField.toPlainText()
        fname = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', "", ".txt")[0]
        
        with open(fname, 'w') as f:
            f.write(text)
            
    def errorBox(self, text):
        """
        Display message/error box 
        
        Arguments:
            text - Text that is to be displayed in the box
            
        Returns: None
        """
        msgBox = QtWidgets.QMessageBox(self)
        msgBox.setIcon(QtWidgets.QMessageBox.Critical)
        msgBox.setText(text)
        msgBox.setWindowTitle("Error")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec()