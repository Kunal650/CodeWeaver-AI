@echo off
REM CodeWeaver AI - Run Script (Windows)
REM Activates the virtual environment and starts the Streamlit app

echo.
echo ========================================
echo   🧬 Starting CodeWeaver AI...
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found. Please run setup_venv.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment and run Streamlit
call venv\Scripts\activate.bat

echo 🚀 Launching on http://localhost:8501
echo.
streamlit run main.py
