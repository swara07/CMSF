# TIFR YOLO Training & Testing App

PyQt5 based YOLO Training and Testing App. Features tool to create datasets.

## Requirements

 1. PyQt5
 2. lxml
 3. bcrypt
 4. psutil
 5. python-dateutil
 6. qt-material
 7. qtwidgets
 
 ## Installation
 1. Open a terminal
 2. Install Python Virtual Environments 

		sudo apt install -y python3-venv
    
3. Create a virtual environment

	    python3 -m venv my_env

	where my_env is the environment name

4. Activate the virtual environment

	    source my_env/bin/activate

	Your command prompt will now be prefixed with the name of your environment, in this case it is called `my_env`.

	    (my_env) user@ubuntu:~/TIFR$

5. Navigate to the directory where application has been cloned.
6. Run the following command to install all requirements:

	    pip install -r requirements.txt

7. Launch the application by executing the following command in the application's root directory:

	    python3 app.py

## How to use

### Creating an account

 1. Launch the application.
 2. Click on `Register` button.
 3. This will open the `User Registraion` window.
 4. Enter the required details. (`Username`, `Email` and `Phone Number` must be unique)
 5. Click `OK`.
 
 ### Training
| Icons | Meaning |
|---|---|
|![New Training](https://cdn0.iconfinder.com/data/icons/very-basic-2-android-l-lollipop-icon-pack/24/plus-64.png) |Create new training session |
| ![Start Training](https://cdn4.iconfinder.com/data/icons/ionicons/512/icon-play-64.png) | Start Selected Training(s) |
| ![Stop/Pause Training](https://cdn0.iconfinder.com/data/icons/zondicons/20/hand-stop-64.png) | Stop/Pause Selected Training(s) |
| ![Delete Training](https://cdn3.iconfinder.com/data/icons/user-interface-169/32/trash-64.png) | Delete Selected Training(s) |

#### Create Training Session
 1. Click on `New Training` button in the toolbar at the top.
 2. Fill out the following details:
     * Training Name (Must be unique)
     * Compiled Darknet Path
     * Weight Path
     * Configuration File Path
     * Data Path
3. A new training session will be created and added to the table. 

Note: `Training Name` must be unique. Failure to do so will result in the session not being created.

#### Start Training
1. Select the session that is to be started by clicking on the checkbox in the first column i.e the `Name` column.
2. Click on `Start Training` button in the toolbar.

#### Stop Training
1. Select the session that is to be stopped by clicking on the checkbox in the first column i.e the `Name` column. (Note: Training has to be running inorder to be stopped)
2. Click on `Stop Training` button in the toolbar.

#### Delete Training
1. Select the session that is to be deleted by clicking on the checkbox in the first column i.e the `Name` column. 
2. Click on `Delete Training` button in the toolbar.

### Testing
| Icons | Meaning |
|--|--|
| ![Training Settings](https://cdn3.iconfinder.com/data/icons/linecons-free-vector-icons-pack/32/settings-64.png)| Set Various Paths required for Inference|

 1. Click on the `Inference Settings` button in the toolbar.
 2. Set the following paths:
	* Darknet Path
	* Weight File Path
	* Configuration File Path
	* Data File Path
3. Open image on which inference is to be made using the `Open` button located at the bottom.
4. Click `Predict` button and wait for output to be displayed in the `Output Panel`.

Note: This settings has to be done only once unless changes are to be made to the paths. Settings are stored for future startups. 

## Database Tables

### User Table
| Column Name | Type | Constraints
|--|--|--|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
|employeeID | TEXT | NOT NULL |
|username | TEXT | UNIQUE NOT NULL |
|password | TEXT | NOT NULL |
|fullName | TEXT | NOT NULL |
|email | TEXT | UNIQUE NOT NULL |
|phoneNumber | TEXT | UNIQUE NOT NULL |

### Training Sessions Table
| Column Name | Type | Constraints
|--|--|--|
| id | INTEGER | PRIMARY KEY AUTOINCREMENT |
|name | TEXT | NOT NULL |
|startDT | INTEGER | NOT NULL |
|endDT | INTEGER | -- |
|weightPath | TEXT | NOT NULL |
|cfgPath | TEXT | NOT NULL |
|dataPath | TEXT | NOT NULL |
|darknetPath | TEXT | NOT NULL |
|pid | INTEGER | -- |
|status | INTEGER | -- |
|createdBy | TEXT | NOT NULL |
