IF EXIST "C:Users\Club\Documents\Horse-Show-Administration\src\newenv\horseshow-proj"(
cd C:Users\Club\Documents\Horse-Show-Administration\src\newenv\horseshow-proj
git pull
ECHO "Successfully Updated!"
pause
)ELSE(
ECHO "Directory not found"
pause
)
