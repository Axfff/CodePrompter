@echo off

REM Check if a virtual environment directory exists, if not, create one
IF NOT EXIST "venv" (
    echo Creating virtual environment...
    python -m venv venv
) ELSE (
    echo Virtual environment already exists.
)

REM Activate the virtual environment
call venv\Scripts\activate.bat

REM Ensure the latest version of pip is installed
python -m pip install --upgrade pip

REM Install dependencies
pip install -r requirements.txt

REM Optional: Install the package globally
pip install .

REM Confirm installation
echo Code Prompter is now installed and ready to use!
pause
