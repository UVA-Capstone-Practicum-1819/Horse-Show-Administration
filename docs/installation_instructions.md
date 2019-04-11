### Installation Instructions

This is the Installation Instruction for the Horse Show Administration program developed by the Capstone Horse Show Administration Team. There are three main parts to this installation:



1. Set up the computer with the required dependencies
2. Clone the repo onto the computer
3. Download and launch the packaged app to start the server

These instructions assume you are using a Windows 10 OS. You can't successfully test/implement these installation instructions without a Windows computer.

We also assume you've set up the folders, but provide some instruction if you do not have them set up.

This program is deployed on a server that can run locally without internet connection.

### Assumptions



*   Windows 10 OS
*   Path has previously been created 
*   Scripts and dependencies handle database setup and some other installations for you

### Create your Club Windows User Account



1. On your machine, go to the search tab on the start menu, and type in "Settings"
2. Click on "Account"
3. Under "Family & Other People", click "Add Someone Else to this PC"
4. Click "I don't have this person's sign-in information"
5. Click "Add a user without a Microsoft account"
6. Create the new account while making sure that the username is "Club"
4. Click on the Club account from the "Family & other people" screen and change the account type to Administrator
5. Log into the new "Club" account

### Set up the computer with the required dependencies (NOTE: This step requires internet connection)



1. Manually install dependencies
    - Download Python from here: [https://www.python.org/downloads/](https://www.python.org/downloads/)
*   On the main page, under "Download the latest version for Windows", click "Download Python 3.7.2", open the file once it's fully downloaded, and follow the instructions by accepting the default options and proceeding through the screens to install
    - Download Git from here: [https://git-scm.com/downloads](https://git-scm.com/downloads) 
*   Click the Windows button and once the package is fully downloaded, open it and follow the instructions by accepting the default options and proceeding through the screens to install
2. Add the dependencies to the environment variables (python, git) 
    - Go to the search tab on the start menu and then type "Edit the system environment variables" 
    - Click "Environment Variables" 
    - Click on the  "Path" row under user variables and select "Edit"
    - Click "New" and type the path name where Python is installed on your computer to add it. It can usually be found at the following path: "C:\Users\Club\AppData\Local\Programs\Python\Python37-32\"
    - Click "New" and type the path name where Python Scripts is installed on your computer to add it. It can usually be found at the following path:"C:\Users\Club\AppData\Local\Programs\Python\Python37-32\Scripts\"
     - Click "New" and type the path name where the Git Bin is installed on your computer to add it. It can usually be found at the following path: "C:\Program Files\Git\bin"
     - Click "New" and type the path name where the Git Cmd is installed on your computer to add it. It can usually be found at the following path: "C:\Program Files\Git\cmd"
     - Then press "OK" to save

### Clone the repo onto the computer (NOTE: This step requires internet connection)



1. Go to the search tab on the start menu, and type in "cmd" to search for the command prompt
2. On the command line, type "cd C:\Users\Club\Documents" and run "git clone [https://github.com/UVA-Capstone-Practicum-1819/Horse-Show-Administration.git](https://github.com/UVA-Capstone-Practicum-1819/Horse-Show-Administration.git)" in order to pull code
    - MUST BE CLONED UNDER "C:\Users\Club\Documents" FOR WINDOWS APP TO WORK
    - If a folder does not exist, cd into the existing folders and type "mkdir " + folder name or use the "File Explorer" to manually create the new folder
3. Type "dir" into the command line, and if you see a folder called "Horse-Show-Administration", cloning the repo was successful.

### Install the project dependencies (NOTE: This step requires internet connection)



1.  Press the Windows Start. Type "Command Prompt" and then click on it. Once open, run the following commands: 

    - pip3 install Django==2.1


    - pip3 install django-autocomplete-light


    - pip3 install pdfrw


    - pip3 install django-crispy-forms


    - pip3 install django-localflavor


    - pip3 install django-bootstrap4


    - pip3 install pylabels


    - pip3 install reportlab
    
    
    - pip3 install xlutils


### Create the database



1. Press the Windows Start. Type "Command Prompt" and then click on it.
2. On the command line, type "cd C:\Users\Club\Documents\Horse-Show-Administration\src\newenv\horseshow-proj"
3. Type "python manage.py makemigrations show" 
4. Type "python manage.py migrate"

     


### Download and launch the packaged app (NOTE: This step requires internet connection)



1. Download the packaged app from [https://drive.google.com/drive/folders/1wo0C-UtjqCUqoELMxYyKEP26PtDLNXdg?usp=sharing](https://drive.google.com/drive/folders/1wo0C-UtjqCUqoELMxYyKEP26PtDLNXdg?usp=sharing) 
2. Open the file explorer and go into the Downloads folder
3. Find the downloaded package, right click, and click on "Properties"
4. Click on "Digital Signatures", click on the signature on the list, and click "Details"
5. Click on "View Certificate", then "Install Certificate"
6. Select "Local Machine" for Store Location, then click "Next".
7. Choose the "Place all certificates in the following store" option, click Browse and select the "Trusted Root Certification Authorities" folder. Click "Next", then "Finish"
8. Now install and launch the downloaded application. 
9. Clicking "Launch Horse Show" should start the server on the browser and allow you to use the app. After finishing a session, click "End Horse Show" to stop the server from running.
