@echo off
REM Set up environment and launch Flask app
echo ================================
echo Launching EY Resume–JD Parser...
echo ================================

REM Optional: activate your conda environment (replace 'your_env_name' below)
REM call conda activate your_env_name

REM Start Flask app on a free port
python app.py

pause
