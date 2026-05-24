@echo off
title TikTok Threads Mobile Tool
echo Installing required modules...
python -m pip install -r requirements.txt
echo.
echo Starting server...
echo PC: http://127.0.0.1:5000
echo Phone: use your PC IP with :5000 on same Wi-Fi
echo.
python app.py
pause
