@echo off
cls

REM Detect the system type
ver | find "Windows" > nul
if %errorlevel% == 0 (
    echo System: Windows
) else (
    echo Unknown system type!
    exit /b
)

REM Check if Python is installed
where python > nul
if %errorlevel% neq 0 (
    echo Python is not installed! Please install Python and try again.
    exit /b
)

REM Create and activate virtual environment
echo Setting up virtual environment...
python -m venv venv
if exist venv\Scripts\activate (
    call venv\Scripts\activate
) else (
    echo Failed to create virtual environment!
    exit /b
)

REM Install requirements
if exist requirements.txt (
    echo Installing requirements...
    pip install -r requirements.txt > nul 2>&1
    if %errorlevel% neq 0 (
        echo Failed to install requirements!
        exit /b
    )
) else (
    echo requirements.txt not found!
    exit /b
)

REM Set permissions (Simulated for Windows)
echo Setting permissions...
for %%f in (server\index.html server\styles.css server\script.js) do (
    if exist %%f (
        echo Setting permissions for %%f
        attrib +r %%f
    )
)

echo Setup complete!
pause
