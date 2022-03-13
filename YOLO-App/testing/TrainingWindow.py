from PyQt5 import QtWidgets, uic, QtCore, QtSql
from PyQt5.QtGui import QIcon
import os, subprocess
import time, datetime, signal
import platform, psutil, dateutil

from src.TrainingSettings import TrainingSettings

class AlignDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(AlignDelegate, self).initStyleOption(option, index)
        option.displayAlignment = QtCore.Qt.AlignCenter

class TrainingWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(TrainingWindow, self).__init__(parent)
        uic.loadUi('ui/training.ui', self)
        
        
        #### RESTORE WINDOW DIMENSIONS ####
        self.settings = QtCore.QSettings("TIFR", "GSR-App")
        geometry = self.settings.value('TestingWindowGeometry', bytes('', 'utf-8'))
        self.restoreGeometry(geometry)
        
        self.currentUser = self.settings.value("loggedUser")
        
        #### GUI HELPERS ####
        self._createToolBarActions()
        self._createToolBar()
        self._createStatusBar()
        self._setTableProperties()
        
        self.statusMessages = ['Not Started/Stopped', 'Running', 'Error']
        self.tableData = []
        self.tableSelections = {}
        
        # Database Connection
        self.con3 = QtSql.QSqlDatabase.database("con3", open=True)
           
        self._createTable()
        self._queryTable()
        
        #### DEBUG STATEMENTS ####
        # self._deleteTableData() 
        # self._deleteTable()

    def onCellChanged(self, item):
        """
        Add selected row to tableSelections List
        
        Arguments:
            Item - Checked row in the table
          
        Returns: None  
        """
        
        # If Checkbox selected
        if item.checkState() == QtCore.Qt.Checked:
            
            # Get row index
            index = self.trainingTable.currentIndex()
            # print('{} Checked'.format(item.text()))
            self.tableSelections[item.text()] = item.row()
            
            # Display message on status bar
            self.statusbar.showMessage("Selected {}".format(item.text()), 5000)
            # print(self.tableSelections)
            
            # row = self.trainingTable.currentRow()
            # # print('{} Checked'.format(item.text()))
            # self.tableSelections[item.text()] = int(self.trainingTable.verticalHeaderItem(row).text()
            # print(self.tableSelections)
            
        # On checkbox unselect    
        else:
            
            # for d in self.tableSelections:
            #     if d['name'] == item.text():
            #         self.tableSelections.remove(d)
            
            if item.text() in self.tableSelections:
                self.tableSelections.pop(item.text()) # Remove from selections
                
                # Display message on status bar
                self.statusbar.showMessage("Unselected {}".format(item.text()), 5000)
            
            # print('{} Unchecked'.format(item.row()))
            # print(self.tableSelections)
            
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

    def displayTableData(self):
        """
        Loop over database rows and display data in table
        
        Arguments: None
        Returns: None
        """
        
        # Required Parameters for QTableWidget
        n_col = 9
        n_row = len(self.tableData)
        self.trainingTable.setColumnCount(n_col)
        self.trainingTable.setRowCount(n_row)
        
        # verticalLabels = []
        
        # Displaying data 
        for i, row in enumerate(self.tableData):
            
            # Create a checkbox with trainingName as the title
            item = QtWidgets.QTableWidgetItem(row['name'])
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Unchecked)  

            # Adding items to table
            self.trainingTable.setItem(i, 0, item)
            self.trainingTable.setItem(i, 1, QtWidgets.QTableWidgetItem(row['startDT']))
            self.trainingTable.setItem(i, 2, QtWidgets.QTableWidgetItem(row['startTime']))
            self.trainingTable.setItem(i, 3, QtWidgets.QTableWidgetItem(row['endDT']))
            self.trainingTable.setItem(i, 4, QtWidgets.QTableWidgetItem(row['endTime']))
            self.trainingTable.setItem(i, 5, QtWidgets.QTableWidgetItem(row['hours']))
            self.trainingTable.setItem(i, 6, QtWidgets.QTableWidgetItem(str(row['pid'])))
            self.trainingTable.setItem(i, 7, QtWidgets.QTableWidgetItem(row['status']))
            self.trainingTable.setItem(i, 8, QtWidgets.QTableWidgetItem(row['createdBy']))

        # self.trainingTable.setVerticalHeaderLabels(verticalLabels)
        
        # Sort rows according to startTime
        self.trainingTable.sortItems(2, QtCore.Qt.DescendingOrder)

    def closeEvent(self, event):
        """
        Save window geometry i.e size and pos
        
        Arguments: 
            event - close signal sent by Qt
            
        Returns: None
        """
        
        geometry = self.saveGeometry() # Get window geometry
        self.settings.setValue('TrainingWindowGeometry', geometry) # Save to settings
        super(TrainingWindow, self).closeEvent(event)

    ######## GUI HELPERS ########
    def _createToolBarActions(self):
        """
        Create tool bar actions
        
        Arguments: None
        Returns: None
        """

        self.backAction = QtWidgets.QAction(QIcon(":back.png"), "Back", self)
        self.newTrainingAction = QtWidgets.QAction(QIcon(":new-training.png"), "New Training", self)
        self.startTrainingAction = QtWidgets.QAction(QIcon(":start-training.png"), "Start Training", self)
        self.cancelTrainingAction = QtWidgets.QAction(QIcon(":delete-training.png"), "Cancel Training", self)
        # self.deleteTrainingAction = QtWidgets.QAction(QIcon(":delete-training.png"), "Delete Training", self)
        # self.trainingHelpAction = QtWidgets.QAction(QIcon(":help-training.png"), "Help", self)
       
    def _createToolBar(self):
        """
        Create toolbar
        
        Arguments: None
        Returns: None
        """
            
        fileToolBar = QtWidgets.QToolBar("File") # Create toolbar
        fileToolBar.setMovable(False) # Don't allow moving
        self.addToolBar(fileToolBar) # Set to window
        
        # Adding buttons i.e actions
        fileToolBar.addAction(self.backAction)
        fileToolBar.addSeparator()
        fileToolBar.addAction(self.newTrainingAction)
        fileToolBar.addAction(self.startTrainingAction)
        fileToolBar.addAction(self.cancelTrainingAction)
        # fileToolBar.addAction(self.deleteTrainingAction)
        # fileToolBar.addAction(self.trainingHelpAction)
        
        # Connecting slots for actions
        self.backAction.triggered.connect(self.backButton)
        self.newTrainingAction.triggered.connect(self.newTraining)
        self.startTrainingAction.triggered.connect(self.startTraining)
        self.cancelTrainingAction.triggered.connect(self.cancelTraining)
        # self.deleteTrainingAction.triggered.connect(self.deleteTraining)
        
    def _createStatusBar(self):
        """
        Create status bar to display messages
        
        Arguments: None
        Returns: None
        """
        self.statusbar = self.statusBar()
        # Adding a temporary message
        self.statusbar.showMessage("Ready", 5000)
        
    ######### DB METHODS ##########               
    def _createTable(self):
        """
        Create 'trainings' table if doesn't exist
        
        Arguments: None
        Returns: None
        """
        
        query = QtSql.QSqlQuery(self.con3)
        query.exec("""CREATE TABLE IF NOT EXISTS trainings (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, 
                name TEXT NOT NULL UNIQUE, 
                startDT INTEGER NOT NULL,
                endDT INTEGER,
                weightPath TEXT NOT NULL,
                cfgPath TEXT NOT NULL, 
                dataPath TEXT NOT NULL,
                darknetPath TEXT NOT NULL,
                pid INTEGER,
                status INTEGER,
                createdBy TEXT NOT NULL); 
                """)
   
    def _queryTable(self):
        """
        Get rows from DB table
        
        Arguments: None
        Returns: None
        """
        
        query = QtSql.QSqlQuery(self.con3)
        query.exec("SELECT * from trainings")
        
        # Looping over rows
        while query.next():
            record = query.record()

            # Storing data in a dictionary
            data = {}
            data['id'] = record.value("id")
            data['name'] = record.value("name")
            data['weightPath'] = record.value('weightPath')
            data['cfgPath'] = record.value('cfgPath')
            data['dataPath'] = record.value('dataPath')
            data['darknetPath'] = record.value('darknetPath')
            data['createdBy'] = record.value('createdBy')
            
            # If startDT is set, convert unixTime to normal time
            # else set to null for the table
            startDT = record.value("startDT")
            if startDT == 0:
                data['startDT'] = "--"
                data['startTime'] = "--"
            
            else:
                convertedStartDate, convertedStartTime = self._unixTimeToTime(startDT)
                
                data['startDT'] = convertedStartDate
                data['startTime'] = convertedStartTime
            
            # If endDT is set, convert unixTime to normal time
            # else set to null for the table
            endDT = record.value("endDT")
            if endDT == 0:
                
                data['endDT'] = "--"
                data['endTime'] = "--"
                data['hours'] = "0"
                
            else:
                convertedEndDate, convertedEndTime = self._unixTimeToTime(endDT)
                
                data['endDT'] = convertedEndDate
                data['endTime'] = convertedEndTime
                
                # Calculate hours difference between startDT and endDT
                hours = dateutil.relativedelta.relativedelta(datetime.datetime.fromtimestamp(endDT),\
                    datetime.datetime.fromtimestamp(startDT))
                data['hours'] = "{}:{}".format(hours.hours, hours.minutes)
            
            # Process ID    
            pid = record.value('pid')
            
            # Status
            status = record.value("status")
            
            # If process is running, keep as is
            if self._checkProcess(pid):
                data['pid'] = pid
                data['status'] = self.statusMessages[status]
            
            # else change value of PID and update status
            else:
                data['pid'] = "--"
                data['status'] = self.statusMessages[0]
                self._updateStatusChange(0, 0, data['name'])
            
            self.tableData.append(data)
        
        # Displaying data
        self.displayTableData()
   
    def _insertData(self, name, weightPath, cfgPath, dataPath, darknetPath):
        """
        Insert new training into the table
        
        Arguments:
            name - Name of the training
            weightPath - Location of weight file (Full Path)
            cfgPath - Location of configuration file (Full Path)
            dataPath - Location of data file (Full Path)
            darknetPath - Location of darknet on system (Full Path)
            
        Returns:
            bool - True/False
        """
        
        query = QtSql.QSqlQuery(self.con3)
        query.prepare("""INSERT INTO trainings (name, startDT, endDT, weightPath, cfgPath, dataPath, darknetPath, pid, status, createdBy)
              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""")

        query.addBindValue(name)
        query.addBindValue(0)
        query.addBindValue(0)
        query.addBindValue(weightPath)
        query.addBindValue(cfgPath)
        query.addBindValue(dataPath)
        query.addBindValue(darknetPath)
        query.addBindValue(0)
        query.addBindValue(0)
        query.addBindValue(self.currentUser)
        
        # If insertion is successful
        if query.exec():
            self.statusbar.showMessage("Created Training. Select to peform actions", 5000)
            return True
        
        return False
    
    def _updateStatusChange(self, pid, status, name):
        """
        Update status of training if its not running on application startup
        
        Arguments:
            pid - Process ID
            status - Process Status
            name - Name of training
            
        Returns: None
        """
        
        query = QtSql.QSqlQuery(self.con3)
        
        query.prepare("""UPDATE trainings SET \
                pid = ?, \
                status = ? \
                WHERE name = ?""")
                
        query.addBindValue(pid)
        query.addBindValue(status)
        query.addBindValue(name)
        
        query.exec()
    
    def _updateTrainingStart(self, pid, name):
        """
        Update training information after starting
        
        Arguments:
            pid - Process ID
            name - Name of training
            
        Returns:
            bool - True on successful update
        """
        
        query = QtSql.QSqlQuery(self.con3)
    
        query.prepare("""UPDATE trainings SET \
                startDT = ?, \
                pid = ?, \
                status = ? \
                WHERE name = ?""")
                
        query.addBindValue(int(time.time())) # Get current time
        query.addBindValue(pid)
        query.addBindValue(1)
        query.addBindValue(name)
        
        return query.exec()
    
    def _updateAfterStopping(self, endTime, name):
        """
        Update training information after stopping
        
        Arguments:
            endTime - Time when process has stopped
            name - Name of training
            
        Returns:
            bool - True on successful update
        """
        
        query = QtSql.QSqlQuery(self.con3)
        
        query.prepare("""UPDATE trainings SET \
                endDT = ?,
                pid = ?, \
                status = ? \
                WHERE name = ?""")
                
        query.addBindValue(endTime)
        query.addBindValue(0)
        query.addBindValue(1)
        query.addBindValue(name)
        
        return query.exec()
        
    def _deleteTableData(self, *args):
        """
        Delete row(s) from table
        
        Arguments:
            args - Name of training
            
        Returns: 
            bool - True on successful delete
    
        """
        
        query = QtSql.QSqlQuery(self.con3)
        
        # Delete single row
        if args:
            
            query.prepare("""DELETE FROM trainings WHERE name = ?""")
            query.addBindValue(args[0])
        
        # Delete all rows
        else:
            query.prepare("""DELETE FROM trainings""")
            
        return query.exec()
         
    def _deleteTable(self):
        
        query = QtSql.QSqlQuery(self.con3)
        query.prepare("""DROP TABLE trainings""")
        query.exec()
         
    ######### SLOTS ###########
    def newTraining(self):
        """
        Launch dialog to create new training
        
        Arguments: None
        Returns: None
        """
        
        # Get values from dialog
        values = TrainingSettings.launch(self)
        
        if values:
            
            # Insert into database
            if self._insertData(values[0], values[1], values[2], values[3], values[4]):
                self.tableData.clear()
                self.trainingTable.setRowCount(0)
                self._queryTable() # Refresh Table
                
            else:
                self.statusbar.showMessage("Could Not Create Training. Please make sure the name is unique", 10000)
            
        else:
            self.statusbar.showMessage("Cancelled creation of new training", 10000)
        
    def startTraining(self):
        """
        Start training of selected sessions
        
        Arguments: None
        Returns: None
        """
        
        # If no rows selected
        if not self.tableSelections:
            self.errorBox("Please select the name of the training session that is to be started")
        
        else:
            
            # Loop over selections    
            for training_name, row in self.tableSelections.items():
                
                # Get Paths of selected session
                weightPath, cfgPath, dataPath, darknetPath = self._getPaths(training_name)
                
                # File to store iteration and other information
                trainingDetailsText = dataPath.rpartition("/")[0] + "/" + training_name  + "_trainingInfo.txt"
                
                prevDir = os.getcwd()
                os.chdir(darknetPath) # Change to darknets directory
            
                with open(trainingDetailsText, 'w') as outfile:
                        
                    # For windows platform
                    if platform.system() == "Windows":
                    
                        # pid = subprocess.Popen(['dir']).pid
                        pid = subprocess.Popen(["start", "/b", "darknet.exe", "detector", "train", \
                            "{}".format(dataPath), \
                            "{}".format(cfgPath), \
                            "{}".format(weightPath),\
                            "-dont_show"],\
                            stdout=outfile).pid
                    
                    # For windows platform
                    else:
                        
                        # pid = subprocess.Popen(['ls']).pid
                        pid = subprocess.Popen(["nohup", "./darknet", "detector", "train", \
                            "{}".format(dataPath), \
                            "{}".format(cfgPath), \
                            "{}".format(weightPath),\
                            "-dont_show","&"],\
                            stdout=outfile).pid
                
                os.chdir(prevDir)
                
                # Update session information in table
                if self._updateTrainingStart(pid, training_name):
                    self.statusbar.showMessage("{} training started".format(training_name), 10000)
                
            # Refresh Table
            self.tableSelections.clear()
            self.tableData.clear()
            self._queryTable()
        
    def cancelTraining(self):
        """
        Stop training of selected sessions
        
        Arguments: None
        Returns: None
        """
        
        # If no rows selected
        if not self.tableSelections:
            self.errorBox("Please select the name of the training session that is to be cancelled")
        
        else:
            
            # Loop over selections
            for training_name, row in self.tableSelections.items():
                
                # Get process ID and status of training
                pid, status = self._getProcessDetails(training_name)
                
                # If running
                if status == 1:
                    os.kill(pid, signal.SIGTERM) # Terminate
                    
                    endTime = time.time() # Get end time
                    
                    # Update data in database table
                    if self._updateAfterStopping(endTime, training_name):
                        self.statusbar.showMessage("Training stopped", 10000)
                        self.tableData.clear()
                        self._queryTable() # Refresh table
                    
                else:
                    self.statusbar.showMessage("Process not running, cannot kill", 10000)
            
            self.tableSelections.clear()
        
    
    # def deleteTraining(self):
    #     """
    #     Delete selected sessions
        
    #     Arguments: None
    #     Returns: None
    #     """
    #     # If no rows selected
    #     if not self.tableSelections:
    #         self.errorBox("Please select the name of the training session that is to be deleted")
        
    #     else:
            
    #         # Loop over selections
    #         for training_name, row in self.tableSelections.items():
                
    #             # Delete row from database table and QTableWidget
    #             if self._deleteTableData(training_name):
    #                 self.trainingTable.removeRow(row)
    #                 self.statusbar.showMessage("Deleted Training", 5000)
    #                 print("Successfully Deleted")
                
    #             else:
    #                 self.statusbar.showMessage("Error Deleting", 5000)
    #                 print("Error Deleting")
                
    #         self.tableSelections.clear()
        
    def backButton(self):
        """
        Go back to main page
        
        Arguments: None
        Returns: None
        """
        self.close()
        self.parentWidget().show()
        
    ######## HELPERS ########
    
    def _setTableProperties(self):
        """
        Set QTableWidget Properties
        
        Arguments: None
        Returns: None
        """
        
        ###### Table Widget Settings ######
        # Set cells to be non editable but allow COPY
        self.trainingTable.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        
        # Allow stretching of columns
        header = self.trainingTable.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(7, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(8, QtWidgets.QHeaderView.Stretch)
        
        # Connect slot
        self.trainingTable.itemClicked.connect(self.onCellChanged)
        
        # Align centre
        delegate = AlignDelegate(self.trainingTable)
        self.trainingTable.setItemDelegateForColumn(1, delegate)
        self.trainingTable.setItemDelegateForColumn(2, delegate)
        self.trainingTable.setItemDelegateForColumn(3, delegate)
        self.trainingTable.setItemDelegateForColumn(4, delegate)
        self.trainingTable.setItemDelegateForColumn(5, delegate)
        self.trainingTable.setItemDelegateForColumn(6, delegate)
        self.trainingTable.setItemDelegateForColumn(7, delegate)
        self.trainingTable.setItemDelegateForColumn(8, delegate)
    
    def _getPaths(self, name):
        """
        Get file paths from name
        
        Arguments:
            name - Training name
            
        Returns:
            weightPath - .weight file path
            cfgPath - .cfg file path
            dataPath - .data file path
            darknetPath - Darknet location on system
        """
        
        for data in self.tableData:
            if data['name'] == name:
                return data['weightPath'], data['cfgPath'], data['dataPath'], data['darknetPath']
    
    def _getProcessDetails(self, name):
        """
        Get process details from name
        
        Arguments:
            name - Training name
            
        Returns:
            pid - Process ID
            status - Process status
        """
        
        for data in self.tableData:
            if data['name'] == name:
                return data['pid'], self.statusMessages.index(data['status'])
    
    def _unixTimeToTime(self, timestamp):
        """
        Convert unix time to 24 hour time
        
        Arguments:
            timestamp - Time in UNIX format
            
        Returns:
            convertedDate - Date in DD/MM/YYYY format
            convertedTime - Time in HH:MM format
        """
        
        convertedTime = datetime.datetime.fromtimestamp(timestamp)
        convertedDate = "{}/{}/{}".format(convertedTime.day, convertedTime.month, convertedTime.year)
        convertedTime = "{}:{}".format(convertedTime.hour, convertedTime.minute)
    
        return convertedDate, convertedTime
    
    def _checkProcess(self, processID):
        """
        Check if process is running
        
        Arguments:
            processID - PID of process that is to be checked
            
        Returns:
            bool - True/False
        """
        
        if psutil.pid_exists(processID):
            return True
        
        return False
        
    # def _createModel(self):    
    #     self.tableModel = QtGui.QStandardItemModel(self)
    #     self.tableModel.itemChanged.connect(self.itemChanged)
    #     # self.tableModel.setHorizontalHeaderLabels(['Name', 'Start Time', 'End Time', 'Hours Elapsed', 'Status'])
    #     # self.tableModel.setDefaultAlignment(Qt.AlignHCenter)
    #     # self.tableModel.itemChanged.connect(self.itemChanged)
        
    #     self.tableModel.setHeaderData(0, QtCore.Qt.Horizontal, "Name")
    #     self.tableModel.setHeaderData(1, QtCore.Qt.Horizontal, "Start Time")
    #     self.tableModel.setHeaderData(2, QtCore.Qt.Horizontal, "End Time")
    #     self.tableModel.setHeaderData(3, QtCore.Qt.Horizontal, "Hours Elapsed")
    #     self.tableModel.setHeaderData(3, QtCore.Qt.Horizontal, "Status")
    
    # def itemChanged(self, item):
    #     print("Item {!r} checkState: {}".format(item.text(), item.checkState()))
    