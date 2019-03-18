call server.bat

:START
netstat -o -n -a | findstr 8000
if %ERRORLEVEL% equ 0 goto FIN

goto NOTFOUND

:NOTFOUND

timeout 5
goto START

:FIN

call browser.bat
