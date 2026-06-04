@echo off
echo ========================================
echo Restaurant Recommendation System Setup
echo ========================================
echo.

echo Step 1: Checking prerequisites...
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH.
    pause
    exit /b 1
)

echo Checking MySQL...
python -c "import pymysql; pymysql.connect(host='localhost', user='root', password='root', connect_timeout=2)" > nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Could not connect to local MySQL (root/root).
    echo Please ensure MySQL is running or update credentials in backend/config.py later.
)

echo Checking MongoDB...
python -c "from pymongo import MongoClient; MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000).server_info()" > nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Could not connect to local MongoDB (localhost:27017).
    echo Reviews and analysis will not work without MongoDB.
)
echo.

echo Step 2: Setting up MySQL database schema...
python backend\setup_mysql.py
if %errorlevel% neq 0 (
    echo ERROR: MySQL setup failed.
    pause
    exit /b 1
)
echo MySQL database created successfully!
echo.

echo Step 3: Installing Python dependencies...
cd backend
python -m pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Python dependencies.
    pause
    exit /b 1
)
echo.

echo Step 4: Training ML models and loading sample data...
python setup_data.py
if %errorlevel% neq 0 (
    echo ERROR: Failed to setup data.
    pause
    exit /b 1
)
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the application:
echo 1. Backend: python backend\app.py
echo 2. Frontend: Open frontend\index.html in your browser
echo.
echo Or run: start_app.bat
echo.
pause
