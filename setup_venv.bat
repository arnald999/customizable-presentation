@echo off
echo [Step 1] Creating virtual environment...
python -m venv venv

echo [Step 2] Activating virtual environment...
call venv\Scripts\activate

echo [Step 3] Installing requirements...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo [✓] Environment is ready!
echo Run this to activate the venv in future:
echo     call venv\Scripts\activate
