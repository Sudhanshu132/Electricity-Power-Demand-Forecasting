@echo off
setlocal
echo ============================================
echo     Running Power Demand Forecast Pipeline
echo ============================================

REM Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Python is not installed or not in PATH.
    pause
    exit /b
)

REM Run the main Python script
python MainStart.py
IF %ERRORLEVEL% NEQ 0 (
    echo ❌ Script failed to execute.
    pause
    exit /b
)

echo.
echo ✅ Forecast completed successfully.
pause
