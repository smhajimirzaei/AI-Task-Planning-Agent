@echo off
REM AI Task Planning Agent - Installation Script for Windows

echo ==================================
echo AI Task Planning Agent Installer
echo ==================================
echo.

REM Check Python version
echo Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.9 or higher from https://www.python.org/
    pause
    exit /b 1
)

python -c "import sys; exit(0 if sys.version_info >= (3,9) else 1)" 2>nul
if errorlevel 1 (
    echo Error: Python 3.9 or higher is required
    python --version
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo. Python %PYTHON_VERSION% detected
echo.

REM Create virtual environment
echo Creating virtual environment...
if exist venv (
    echo Virtual environment already exists
    set /p RECREATE="Do you want to recreate it? (y/N): "
    if /i "%RECREATE%"=="y" (
        rmdir /s /q venv
        python -m venv venv
        echo. Virtual environment recreated
    )
) else (
    python -m venv venv
    echo. Virtual environment created
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo. Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1
echo. pip upgraded
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo. Dependencies installed
echo.

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env >nul
    echo. .env file created
    echo.
    echo WARNING: Edit .env and add your Anthropic API key
    echo    Get your key from: https://console.anthropic.com/
) else (
    echo .env file already exists
)
echo.

REM Installation complete
echo ==================================
echo Installation Complete!
echo ==================================
echo.
echo Next steps:
echo 1. Activate the virtual environment:
echo    venv\Scripts\activate
echo.
echo 2. Add your Anthropic API key to .env file
echo.
echo 3. Run the setup wizard:
echo    python main.py setup
echo.
echo 4. Add your first task:
echo    python main.py add-task "Your task" --priority high --duration 2
echo.
echo 5. Generate your first plan:
echo    python main.py plan
echo.
echo For more information, see:
echo - QUICKSTART.md (5-minute guide)
echo - USAGE_GUIDE.md (comprehensive documentation)
echo - example_usage.py (code examples)
echo.
echo Happy planning!
echo.
pause
