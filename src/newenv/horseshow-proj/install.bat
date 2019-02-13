if not exist "C:Users\Student\Documents\Horse-Show" (
mkdir C:Users\Student\Documents\Horse-Show
cd C:Users\Student\Documents\Horse-Show
git init
git config --global --unset http.proxy
git clone https://github.com/UVA-Capstone-Practicum-1819/Horse-Show-Administration.git
cd C:Users\Student\Documents\Horse-Show
cd Horse-Show-Administration
cd src
cd newenv
cd horseshow-proj
python manage.py makemigrations
python manage.py migrate
pause
) ELSE (
cd C:Users\Student\Documents\Horse-Show
cd Horse-Show-Administration
cd src
cd newenv
cd horseshow-proj
git pull
pause
)