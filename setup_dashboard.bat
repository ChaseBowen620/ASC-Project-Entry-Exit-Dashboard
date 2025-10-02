@echo off
echo Setting up ASC Survey Dashboard with uv virtual environment...
echo.

echo Creating virtual environment with uv...
uv venv

echo.
echo Activating virtual environment and installing dependencies...
call .venv\Scripts\activate.bat
uv pip install -r requirements.txt

echo.
echo Setting up Django database...
python manage.py makemigrations
python manage.py makemigrations surveys
python manage.py migrate

echo.
echo Installing React dependencies...
cd frontend
npm install
cd ..

echo.
echo Importing survey data...
python manage.py import_survey_data "ASC Project Survey_September 19, 2025_15.07.csv"

echo.
echo Setup complete! Run start_dashboard.bat to start the application.
echo.
pause
