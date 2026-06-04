@echo off
setlocal
cd /d "%~dp0"

echo ========================================
echo Starting Restaurant Recommendation System
echo ========================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in your PATH.
    echo Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

:: Run the unified runner
python run_all.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Application failed to start.
    echo Please check the error messages above.
    pause
)

endlocal
