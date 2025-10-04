@echo off
echo Starting ASC Survey Dashboard...
echo.

echo Activating virtual environment and starting Django Backend...
start "Django Backend" cmd /k "call .venv\Scripts\activate.bat && cd backend && python manage.py runserver"

echo Waiting 5 seconds for Django to start...
timeout /t 5 /nobreak > nul

echo Starting React Frontend...
start "React Frontend" cmd /k "cd frontend && npm start"

echo.
echo Dashboard is starting up!
echo Django Backend: http://localhost:8000
echo React Frontend: http://localhost:3000
echo.
echo Press any key to exit this window...
pause > nul
