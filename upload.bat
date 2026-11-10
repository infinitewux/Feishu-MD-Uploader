@echo off
cd /d "%~dp0"
chcp 65001 >nul
set "PYTHONIOENCODING=utf-8"
if not exist "%~dp0venv\Scripts\python.exe" (
    echo Python virtual environment not found. See README.md for setup.
    pause
    exit /b 1
)
"%~dp0venv\Scripts\python.exe" "%~dp0src\upload_dialog.py"
pause
