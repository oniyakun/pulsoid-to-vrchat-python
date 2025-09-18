@echo off
chcp 65001 >nul
title Pulsoid to VRChat OSC Bridge (Python)

echo ========================================
echo  Pulsoid to VRChat OSC Bridge (Python)
echo ========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not found. Please install Python 3.7+
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if in correct directory
if not exist "main.py" (
    echo Error: main.py not found
    echo Please run this script in the correct directory
    pause
    exit /b 1
)

REM Create virtual environment if not exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing/updating dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Warning: Dependencies installation may have issues, but continuing...
)

echo.
echo Starting program...
echo Press Ctrl+C to stop the program
echo.

REM Run main program
python main.py

REM Check exit status
if %errorlevel% neq 0 (
    echo.
    echo Error: Program exited with error code %errorlevel%
    echo Please check the error messages above
) else (
    echo.
    echo Program exited normally
)

echo.
echo Press any key to close window...
pause >nul