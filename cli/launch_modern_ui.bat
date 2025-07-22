@echo off
title Auto-Dock Modern UI
echo.
echo ========================================
echo      AUTO-DOCK MODERN UI LAUNCHER
echo ========================================
echo.

cd /d "C:\Auto-Dock-"

echo Checking Python environment...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.8+ first.
    pause
    exit /b 1
)

echo Installing required packages...
pip install -q rich prompt_toolkit 2>nul

echo.
echo Starting Auto-Dock Modern UI...
echo.

python cli/modern_ui.py

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to start Modern UI
    echo Please check the error messages above.
    pause
)
