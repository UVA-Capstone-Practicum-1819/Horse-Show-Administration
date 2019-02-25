### Installation Instructions

This is the Installation Instruction for the Horse Show Administration program developed by the Capstone Horse Show Administration Team. There are three main parts to this installation:

1) Set up the computer with the required dependencies
2) Clone the repo onto the computer
3) Download and launch the packaged app to start the server

These instructions assume you are using a Windows 10 OS. You can’t successfully test/implement these installation instructions without a Windows computer.

We also assume you’ve set up the path, but do provide some instruction if you do not have them set up.

This program is deployed on a server that can run locally without internet connection.

### Assumptions
- User has Windows 10 OS
- Path has previously been created
- Scripts and dependencies handle database setup and some other installations for you


### Set up the computer with the required dependencies
1) Manually install dependencies
  
  a) Download Python from here: https://www.python.org/downloads/
      
      i) On the main page, under “Download the latest version for Windows”, click “Download Python 3.7.2”
      ii) open the file once it’s fully downloaded, and follow the instructions
  
  b)Download Git from here: https://git-scm.com/downloads 
     
     i) Click the Windows button and once the package is fully downloaded, open it and follow the instructions

2) Add the dependencies to the environment variables (python, pip, git) 
  
  a) Control Panel > System & Security > System > Advanced System Settings > Environment Variables 
  
  b) Click on “Path” under user variables and select “Edit”
  
  c) Browse for ….

 3) Open the Windows control panel and run the following commands: 
  - pip3 install Django==2.1
  - pip3 install django-autocomplete-light
  - pip3 install pdfrw
  - pip3 install django-crispy-forms
  - pip3 install django-localflavor

### Clone the repo onto the computer
1) Go to the search tab on the start menu, and type in “cmd” to search for the command prompt
2) On the command line, type “cd C:\Users\Club\Documents” and run “git clone https://github.com/UVA-Capstone-Practicum-1819/Horse-Show-Administration.git” in order to pull code
   
   a) MUST BE CLONED UNDER “C:\Users\Club\Documents” FOR WINDOWS APP TO WORK
   
   b) If a folder does not exist, cd into the existing folders and type “mkdir “ + folder name
3) Type “dir” into the command line, and if you see a folder called “Horse-Show-Administration”, cloning the repo was successful.

 

### Download and launch the packaged app
1) Download the packaged app from https://drive.google.com/drive/folders/1wo0C-UtjqCUqoELMxYyKEP26PtDLNXdg?usp=sharing 
2) Open the file explorer and go into the Downloads folder
3) Find the downloaded package, right click, and click on “Properties”
4) Click on “Digital Signatures”, click on the signature on the list, and click “Details”
5) Click on “View Certificate”, then “Install Certificate”
6) Select “Local Machine” for Store Location, then click “Next”.
7) Choose the “Place all certificates in the following store” option, click Browse and select the “Trusted Root Certification Authorities” folder. Click “Next”, then “Finish”
8) Now install and launch the downloaded application. 
9) Clicking “Launch Horse Show” should start the server on the browser and allow you to use the app. After finishing a session, click “End Horse Show” to stop the server from running.


