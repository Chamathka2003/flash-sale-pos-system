@echo off
REM Setup script for Flash Sale POS System on Windows

echo ==================================
echo Flash Sale POS System - Setup
echo ==================================

REM Backend setup
echo.
echo Setting up Backend...
cd backend

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create database (ensure MySQL is running)
echo Creating database...
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS assignment_db;"

REM Run migrations
echo Running migrations...
python manage.py makemigrations
python manage.py migrate

echo Backend setup complete!
echo To start the backend: python manage.py runserver

REM Frontend setup
echo.
echo Setting up Frontend...
cd ..\frontend

echo Installing npm dependencies...
call npm install

echo Frontend setup complete!
echo To start the frontend: npm start

echo.
echo ==================================
echo Setup Complete!
echo ==================================
echo.
echo Next steps:
echo 1. Start backend: cd backend ^&^& python manage.py runserver
echo 2. Start frontend: cd frontend ^&^& npm start
echo 3. Populate data: cd backend ^&^& python populate_data.py
echo 4. Run tests: cd backend ^&^& python load_test.py
pause
