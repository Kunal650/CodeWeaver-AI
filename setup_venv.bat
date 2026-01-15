@echo off
REM CodeWeaver AI - Virtual Environment Setup Script
REM Run this script to create and activate the virtual environment

echo ========================================
echo   CodeWeaver AI - Environment Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.9+ and try again.
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo [1/3] Creating virtual environment...
    python -m venv venv
    echo       Virtual environment created successfully!
) else (
    echo [1/3] Virtual environment already exists.
)

echo.
echo [2/3] Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo [3/3] Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo To activate the environment manually, run:
echo   venv\Scripts\activate
echo.
echo To start the application, run:
echo   streamlit run main.py
echo.
pause
