from PyQt5 import QtWidgets, uic, QtCore, QtSql
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QIcon
import sys, time, os
import bcrypt
import qrc_resources
from qtwidgets import AnimatedToggle, PasswordEdit
from qt_material import apply_stylesheet
import re

from src.buttons.LoginButton import LoginButton
from src.buttons.ForgotPassButton import ForgotPassButton
from src.buttons.RegisterButton import RegisterButton
from src.RegisterDialog import RegisterDialog 
from src.ResetPassDialog import ResetPasswordDialog
from src.AppWindow import AppWindow
from PyQt5.QtWidgets import QVBoxLayout
from testing.guii import Ui_MainWindow

class ThreadProgress(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(int)
    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
    def run(self):
        i = 0
        while i<101:
            time.sleep(0.02)
            # time.sleep(0.01)
            self.mysignal.emit(i)
            i += 1
       
class LoginWindow(QtWidgets.QMainWindow):

    name_of=''
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QIcon("tifr-logo.png"))
    
    # Set DB Path
    current_dir = os.path.dirname(os.path.realpath(__file__))
    dbPath = os.path.join(current_dir, "cmsDB.db")
    
    # Setting App Details
    app.setOrganizationName("TIFR")
    app.setApplicationName("YOLO App") 

    # Storing App Settings
    global appSettings  
    appSettings = QtCore.QSettings("TIFR", "CMS-App")
    # print(appSettings.fileName())
    # Applying material design
    # apply_stylesheet(app, theme='dark_blue.xml')
    apply_stylesheet(app, theme='light_blue.xml')
    
    # Setting size of app to 70% of screen size
    dw = QtWidgets.QDesktopWidget()
    x = int(dw.width() * 0.7)
    y = int(dw.height() * 0.7)


     
    
    
        
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        uic.loadUi('ui/login2.ui', self) # Loading UI
        
        oImage = QtGui.QImage("login.png")
        # sImage = oImage.scaled(QtCore.QSize(300,200))                   # resize Image to widgets size
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Window, QtGui.QBrush(oImage))                        
        self.setPalette(palette)
        dw = QtWidgets.QDesktopWidget()

        x = int(dw.width() * 0.7)
        y = int(dw.height() * 0.7)



        try:
            self.resize(appSettings.value("loginWindowSize"))
            self.move(appSettings.value("loginWindowPosition"))
            
        except:
            pass
        
        # Setting TIFR Logo
        self.tifr = QPixmap('tifr-logo.png')
        self.tifrLogo = self.findChild(QtWidgets.QLabel, 'tifrLogo')
        self.tifrLogo.setScaledContents(True)
        self.tifrLogo.setPixmap(self.tifr.scaled(int(x * 0.3), int(y * 0.3)))
        self.tifrLogo.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed) 
        # self.combobox = QtWidgets.QComboBox()
        
        self.vesit = QPixmap('vesit.png')
        self.vesitLogo = self.findChild(QtWidgets.QLabel, 'vesitLogo')
        self.vesitLogo.setScaledContents(True)
        self.vesitLogo.setPixmap(self.vesit.scaled(int(x * 0.5), int(y * 0.5)))
        self.vesitLogo.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed) 

        self.loginBtn.clicked.connect(self.startAppPage)
        self.registerBtn.clicked.connect(self.launchRegisterDialog)
        self.resetPasswordBtn.clicked.connect(self.launchForgotPassDialog) 
        self.comboBox.setStyleSheet("width:400px;")
        self.comboBox.currentTextChanged.connect(self.current_text_changed)
        # self.docButton.clicked.connect(self.documentationWindow)

        self.usernameInput.setStyleSheet("""
                                         QLineEdit{
                                            color: black;
                                            border-bottom: 2px solid black;
                                        } 
                                         
                                        QLineEdit:hover{
                                            color: black;
                                            border: 2px solid black;
                                        }""")
        
        self.passwordInput.setStyleSheet("""
                                         QLineEdit{
                                            color: black;
                                            border-bottom: 2px solid black;
                                        } 
                                         
                                        QLineEdit:hover{
                                            color: black;
                                            border: 2px solid black;
                                        }""")
        
        self.con2 = QtSql.QSqlDatabase.database("con2", open=True)
         
    #### DIALOGS ####
    def current_text_changed(self, s):
        global name_of
        name_of=str(s)
       

        print(name_of)
        # if(d=="Training"):
        #     print(0)
        #     return 0;
        # else:
        #     print(1)
        #     return(1)



    def launchRegisterDialog(self):
        """
        Launch Registration Dialog
        Arguments: None
        Returns: None
        """
        
        values = RegisterDialog.launch(self)
        
        if values:
            if all(v != "" for v in values):
                
                regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

                username = values[0]
                s=values[1]
                password = bcrypt.hashpw(values[1].encode('utf-8'), bcrypt.gensalt())
                password = password.decode("utf-8")

                name = values[2]
                email = values[3]
                phone = values[4]
                eid = values[5]

                l, u, p, d = 0, 0, 0, 0

                if(not re.fullmatch(regex, email)):
                    print("Invalid Email")
                    self._messageBox("Invalid Email", error = True)    
                elif(len(phone)!=10):
                    print("Invalid Phone Number")
                    self._messageBox("Invalid Phone Number", error = True) 
                elif(len(s)<8):
                    print("Invalid Password")
                    self._messageBox("Invalid Password", error = True)
                elif(len(s)>=8):
                    for i in s:
                        if (i.islower()):
                            l+=1            
                        if (i.isupper()):
                            u+=1         
                        if (i.isdigit()):
                            d+=1            
                        if(i=='@'or i=='$' or i=='_'):
                            p+=1   
                    if (not(l>=1 and u>=1 and p>=1 and d>=1 and l+p+u+d==len(s))):
                        print("Invalid Password")
                        self._messageBox("Invalid Password", error = True)
                    else:    
                        query = QtSql.QSqlQuery(self.con2)
                        query.prepare(
                        """INSERT INTO users (employeeID, username, password, fullName, email, phoneNumber)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """)
                        
                        query.addBindValue(eid)
                        query.addBindValue(username)
                        query.addBindValue(password)
                        query.addBindValue(name)
                        query.addBindValue(email)
                        query.addBindValue(phone)
                        
                        if query.exec():
                            self._messageBox("Registered Successfully. You may now login", error = False)
                        else:
                            self._messageBox("Could not register", error = True)            
                
    def launchForgotPassDialog(self,s):
        """
        Launch Password Reset Dialog
        Arguments: None
        Returns: None
        """
        values = ResetPasswordDialog.launch(self)
        
        if values:
            if all(v != "" for v in values):
                
                uname = values[0]
                oldPass = values[1].encode("utf-8")
                newPass = values[2]
                cnfPassNew = values[3]
                
                # Check if user exists and passwords match
                if self._checkCredentials(uname, oldPass, passReset=True):
                        
                    if newPass == cnfPassNew:
                        newPass = bcrypt.hashpw(newPass.encode('utf-8'), bcrypt.gensalt())
                        newPass = newPass.decode("utf-8")
                        
                        if self._updatePassword(uname, newPass):
                            
                            self._messageBox("Password Successfully Updated", error = False)
                            
                        else:
                            
                            self._messageBox("Password not updated", error = True)
                            
                    else:
                        
                        self._messageBox("Passwords do not match", error = True)
                        
                else:
                    
                    self._messageBox("User not found/Old passwords do no match", error = True)
                        
        
        # if values:
    
        #     uname = values[0]
        #     oldPass = values[1]
        #     newPass = values[2]
        #     confirmPass = values[3]
            
        #     fname, verified = self._checkCredentials(uname, oldPass)
        
    def startAppPage(self):
        global name_of

        """
        Check for credentials in database and log in the user
        Arguments: None
        Returns: None
        """
        uname = self.usernameInput.text()
        pword = self.passwordInput.text()
        
        pword = pword.encode("utf-8")
        
        if self._checkCredentials(uname, pword):
            self.hide()
        
            if(name_of=="Testing"):
                self.MainWindow = QtWidgets.QMainWindow()
                self.appWindow = Ui_MainWindow()
                self.appWindow.setupUi(self.MainWindow)
                self.MainWindow.show()

            else:
                appWindow = AppWindow(self)
                appWindow.show()
            
        else:
            self._messageBox("Invalid Username or Password", error = True)    
        
    def documentationWindow(self):
        pass
        
    #### EVENTS ####
    def hideEvent(self, event):   
        appSettings.setValue("loginWindowSize", self.size())
        appSettings.setValue("loginWindowPosition", self.pos())
        
    def closeEvent(self, event):
        appSettings.setValue("loginWindowSize", self.size())
        appSettings.setValue("loginWindowPosition", self.pos())
            
    #### HELPERS ####
    def _updatePassword(self, uname, newPass):
        
        query = QtSql.QSqlQuery(self.con2)
        query.prepare(
            """
            UPDATE users SET password = ? WHERE username = ?
            """)
        
        # Add value to query
        query.addBindValue(newPass)
        query.addBindValue(uname)
        
        # Execute query
        return query.exec()
        
    def _checkCredentials(self, uname, pword, passReset = False):
        """
        Check if user exists
        Arguments: 
            uname {string} - Username from input field
            uname {password} - Password from input field
        Returns:
            True - For successful authentication
            False - For unsuccessful authentication
        """
        
        # Prepare query
        query = QtSql.QSqlQuery(self.con2)
        query.prepare(
            """
            SELECT fullName, password FROM users where username = ?
            """)
        
        # Add value to query
        query.addBindValue(uname)
        # print(query.exec())
        
        # Execute query
        query.exec()
            
        # If user exists
        if query.first():
            
            fname = query.value(0)
            password = query.value(1)
            password = password.encode("utf-8")
            
            # Check if passwords match
            if bcrypt.checkpw(pword, password):
                # print("Successful")
                
                if not passReset:
                    appSettings.setValue("loggedUser", fname)
                    
                return True
                
            else:
                # print("Invalid password")
                return False
                
        # print("Account not found")
        return False
    
    def _messageBox(self, text, error = True):
        """
        Display message/error box 
        
        Arguments:
            text - Text that is to be displayed in the box
            
        Returns: None
        """
        msgBox = QtWidgets.QMessageBox(self)
        
        if error:
        
            msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            msgBox.setWindowTitle("Error")
            
        else:
            
            msgBox.setIcon(QtWidgets.QMessageBox.Information)
            msgBox.setWindowIcon(QIcon(":green-check.png"))
            msgBox.setWindowTitle("Success")
            
        msgBox.setText(text)
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec()
    
class Splash(QtWidgets.QMainWindow):
    def __init__(self, parent = None):
        super(Splash, self).__init__(parent)
        QtWidgets.QMainWindow.__init__(self)
        
        uic.loadUi('ui/splash.ui', self) # Loading UI File
        
        # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        progressBarStyleSheet = """
                                QProgressBar {
                                background-color: #363636;
                                color: white;
                                border-style: inset;
                                border-radius: 6px;
                                text-align: center;
                                }

                                QProgressBar::chunk {
                                    border-radius: 6px;
                                    background-color: qlineargradient(spread:pad x1:0, x2:1, y1:0.511364, y2:0.523, stop:0 #5219e3, stop:1 #e31919);
                                }
        """
        
        self.progressBar.setStyleSheet(progressBarStyleSheet)
        
        # Setting image on placeholder
        pixmap = QPixmap("Certificate.png")
        self.certificatePlaceholder.setScaledContents(True)
        self.certificatePlaceholder.setPixmap(pixmap)
        
        # ProgressBar Thread
        progress = ThreadProgress(self)
        progress.mysignal.connect(self.progress)
        progress.start()
        
    @QtCore.pyqtSlot(int)
    def progress(self, i):
        self.progressBar.setValue(i) #Increase value of ProgressBar
        if i == 100:
            self.close()
            # Launch App after loading is complete
            main = LoginWindow(self)
            main.show()

def dbCreator(dbPath):
    """
    Create DB and Tables on application startup
    Arguments:
        dbPath {string} - Path where DB is stored
    
    Returns:
        True - on successful DB and Table creation
        False - If connection to DB could not be created
    """
    
    db = QtSql.QSqlDatabase.addDatabase("QSQLITE", "con1")
    db.setDatabaseName(dbPath)
    if not db.open():
        msgBox = QtWidgets.QMessageBox(None)
        msgBox.setIcon(QtWidgets.QMessageBox.Critical)
        msgBox.setText("Unable to open database")
        msgBox.setWindowTitle("Error")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Cancel)
        msgBox.exec()
        return False
    
    # query = QtSql.QSqlQuery(db)
    # query.prepare("""DROP TABLE users""")
    # query.exec()
    
    query = QtSql.QSqlQuery(db)
    query.exec("""CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, 
                employeeID TEXT, 
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                fullName TEXT NOT NULL, 
                email TEXT UNIQUE NOT NULL,
                phoneNumber TEXT UNIQUE NOT NULL); 
                """)
    
    # query.exec("""CREATE TABLE IF NOT EXISTS training_sessions (
    #             id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, 
    #             session_name VARCHAR(20) NOT NULL, 
    #             started_at VARCHAR(20) NOT NULL,
    #             stopped_at VARCHAR(20) NOT NULL,
    #             hours_elapsed VARCHAR(40) NOT NULL, 
    #             status VARCHAR(40) UNIQUE NOT NULL); 
    #             """)
    
    # print(db.tables())
    # query.prepare("""INSERT INTO users (employeeID, username, password, fullName, email, phoneNumber)
    #          VALUES (?, ?, ?, ?, ?, ?)""")

    # query.addBindValue("1")
    # query.addBindValue("username")
    # query.addBindValue("password")
    # query.addBindValue("name")
    # query.addBindValue("email")
    # query.addBindValue(123)
    # print(query.exec())
             
    # query.exec("""SELECT * FROM users""")
    
    # while query.next():
    
    #     print(query.value(0), query.value(1), query.value(2), query.value(3), query.value(4), query.value(5), query.value(6))
    
    # # print(db.tables())
    
    # Extra Connections
    con2 = QtSql.QSqlDatabase.addDatabase("QSQLITE", "con2")
    con2.setDatabaseName(dbPath)
    
    con3 = QtSql.QSqlDatabase.addDatabase("QSQLITE", "con3")
    con3.setDatabaseName(dbPath)
    
    return True

if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)
    # app.setWindowIcon(QIcon("tifr-logo.png"))
    
    # Set DB Path
    current_dir = os.path.dirname(os.path.realpath(__file__))
    dbPath = os.path.join(current_dir, "cmsDB.db")
    
    # Setting App Details
    app.setOrganizationName("TIFR")
    app.setApplicationName("YOLO App")
    
    # Quit app if DB could not be created
    if not dbCreator(dbPath):
        sys.exit(-1)    

    # Storing App Settings
    global appSettings  
    appSettings = QtCore.QSettings("TIFR", "CMS-App")
    # print(appSettings.fileName())
    
    # Applying material design
    # apply_stylesheet(app, theme='dark_blue.xml')
    apply_stylesheet(app, theme='light_blue.xml')
    
    # Setting size of app to 70% of screen size
    dw = QtWidgets.QDesktopWidget()
    x = int(dw.width() * 0.7)
    y = int(dw.height() * 0.7)
    
    # Launching certificate splash screen
    window = Splash()
    # Fixing size to 70%
    # window.setFixedSize(x, y)
    window.show()

    sys.exit(app.exec_())