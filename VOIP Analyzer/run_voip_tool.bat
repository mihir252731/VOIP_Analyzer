@echo off
SETLOCAL

REM Navigate to the project directory
cd /d "%~dp0"

REM Activate virtual environment
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat
IF %ERRORLEVEL% NEQ 0 (
    echo [!] Failed to activate virtual environment. Ensure it exists.
    pause
    exit /b
)

REM Install required packages
echo [*] Installing Python dependencies...
pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    echo [!] Package installation failed.
    pause
    exit /b
)

REM Run main capture and decode process
echo [*] Starting packet capture (main.py)...
python main.py
IF %ERRORLEVEL% NEQ 0 (
    echo [!] main.py encountered an error.
    pause
    exit /b
)

REM Run analysis and report generation
IF EXIST run_analysis.py (
    echo [*] Running threat analysis (run_analysis.py)...
    python run_analysis.py
    IF %ERRORLEVEL% NEQ 0 (
        echo [!] run_analysis.py failed.
        pause
        exit /b
    )
) ELSE (
    echo [!] run_analysis.py not found. Skipping analysis step.
)

REM Run the dashboard
IF EXIST ui\dashboard.py (
    echo [*] Launching dashboard...
    start "" python ui\dashboard.py
) ELSE (
    echo [!] Dashboard file not found. Skipping UI step.
)

echo [✔] All steps completed. Press any key to exit.
pause
ENDLOCAL
