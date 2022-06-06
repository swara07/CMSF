from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import QPixmap, QIcon
import qrc_resources
import sys, os

from src.Settings import SettingsDialog
from src.TrainingWindow import TrainingWindow
# from src.TestingWindow import TestingWindow

from labelImg.labelImg import MainWindow

class AppWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(AppWindow, self).__init__(parent)
        uic.loadUi('ui/main2.ui', self)
                
        self.settings = QtCore.QSettings("TIFR", "CMS-App")
        geometry = self.settings.value('MainWindowGeometry', bytes('', 'utf-8'))
        self.restoreGeometry(geometry)
        
        self.welcomePlaceholder.setText('Welcome {}'.format(self.settings.value("loggedUser")))
        
        self.annotationIcon = QPixmap('icons/annotation_tool6.png.jpg')
        self.annotationIconLabel = self.findChild(QtWidgets.QLabel, 'annotationIcon')
        self.annotationIconLabel.setScaledContents(False)
        self.annotationIconLabel.setPixmap(self.annotationIcon)
        # self.annotationIconLabel.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed) 
        self.annotationIconLabel.setMinimumSize(1, 1)
        # get resize events for the label
        self.annotationIconLabel.installEventFilter(self)
        
        self.trainingIcon = QPixmap('icons/training6.png')
        self.trainingIconLabel = self.findChild(QtWidgets.QLabel, 'trainingIcon')
        self.trainingIconLabel.setScaledContents(False)
        self.trainingIconLabel.setPixmap(self.trainingIcon)
        # self.trainingIconLabel.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed) 
        self.trainingIconLabel.setMinimumSize(1, 1)
        # get resize events for the label
        self.trainingIconLabel.installEventFilter(self)
        
        # self.testingIcon = QPixmap('icons/testing.png')
        # self.testingIconLabel = self.findChild(QtWidgets.QLabel, 'testingIcon')
        # self.testingIconLabel.setScaledContents(False)
        # self.testingIconLabel.setPixmap(self.testingIcon)
        # # self.testingIconLabel.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed) 
        # self.testingIconLabel.setMinimumSize(1, 1)
        # # get resize events for the label
        # self.testingIconLabel.installEventFilter(self)
        
        self.launchAnnotation.clicked.connect(self.launchAnnotationTool)
        self.launchTraining.clicked.connect(self.trainingWindow)
        # self.launchTesting.clicked.connect(self.testingWindow)
        
        self._createActions()
        self._connectActions()
        self._createMenuBar()
        
    def eventFilter(self, source, event):
        if (source is self.annotationIconLabel and event.type() == QtCore.QEvent.Resize):
        # re-scale the pixmap when the label resizes
            self.annotationIconLabel.setPixmap(self.annotationIcon.scaled(
            self.annotationIconLabel.size(), QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation))
            
        elif (source is self.trainingIconLabel and event.type() == QtCore.QEvent.Resize):
        # re-scale the pixmap when the label resizes
            self.trainingIconLabel.setPixmap(self.trainingIcon.scaled(
            self.trainingIconLabel.size(), QtCore.Qt.KeepAspectRatio,
            QtCore.Qt.SmoothTransformation))
            
        # elif (source is self.testingIconLabel and event.type() == QtCore.QEvent.Resize):
        # # re-scale the pixmap when the label resizes
        #     self.testingIconLabel.setPixmap(self.testingIcon.scaled(
        #     self.testingIconLabel.size(), QtCore.Qt.KeepAspectRatio,
        #     QtCore.Qt.SmoothTransformation))
            
        return super(AppWindow, self).eventFilter(source, event)
        
    def launchAnnotationTool(self):
        classFile = os.path.join(os.path.dirname(__file__), "labelImg/data", "predefined_classes.txt")
        #print(classFile)
        win = MainWindow(default_prefdef_class_file=classFile, parent = self)
        win.show()
    
    def trainingWindow(self):        
        self.hide()
        training = TrainingWindow(self)
        training.show()
        
    # def testingWindow(self):        
    #     self.hide()
    #     testing = TestingWindow(self)
    #     testing.show()
        
    def _createActions(self):
        # Creating actions using the second constructor
        self.settingsAction = QtWidgets.QAction(QIcon(":settings.png"), "&Settings", self)
        self.logoutAction = QtWidgets.QAction(QIcon(":logout.png"), "&Logout", self)
        self.exitAction = QtWidgets.QAction(QIcon(":exit.png"), "&Exit", self)
        self.helpContentAction = QtWidgets.QAction("&Help", self)
        
    def _connectActions(self):
        # Connecting actions
        self.settingsAction.triggered.connect(self.launchSettingsPanel)
        
        self.logoutAction.triggered.connect(self.logout)
        
        self.exitAction.triggered.connect(self.close)
        self.exitAction.setShortcut("Ctrl+W")
        
        self.helpContentAction.triggered.connect(self.helpWindow)
        
    def _createMenuBar(self):
        
        stylesheet = """

            QMenuBar{
                background-color: #00207f;
                color: white;
            }
            
            QMenuBar:item {
                background-color: #00207f;
                color: white;
            }

            QMenuBar:item:selected {
                background-color: #082459;
            }
        
        """
        
        menuBar = self.menuBar()
        # menuBar.setStyleSheet(stylesheet)
        fileMenu =  menuBar.addMenu("&File")
        # fileMenu.addAction(self.settingsAction)
        fileMenu.addAction(self.logoutAction)
        fileMenu.addAction(self.exitAction)
        
        helpMenu = menuBar.addMenu("&Help")
        helpMenu.addAction(self.helpContentAction)
        
    def logout(self):
        self.settings.setValue("loggedUser", "")
        self.close()
        self.parentWidget().show()
        
    def helpWindow(self):
        print("Help")
        
    def hideEvent(self, event):   
        self.settings.setValue("appWindowSize", self.size())
        self.settings.setValue("appWindowPosition", self.pos())
        
    def closeEvent(self, event):
        geometry = self.saveGeometry()
        self.settings.setValue('MainWindowGeometry', geometry)
        super(AppWindow, self).closeEvent(event)
        
    def launchSettingsPanel(self):
        settingsDialog = SettingsDialog(self)
        # apply_stylesheet(register_page, theme='dark_lightgreen.xml')
        # settingsDialog.setFixedSize(int(self.frameGeometry().height()* 0.4), int(self.frameGeometry().width() * 0.8))
        settingsDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        settingsDialog.show()
