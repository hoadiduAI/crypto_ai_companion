@echo off
echo ========================================
echo   Crypto Radar - Starting Services
echo ========================================
echo.

REM Start Telegram Bot in background
echo [1/2] Starting Telegram Bot...
start "Crypto Radar Bot" cmd /k "python alert_bot.py"
timeout /t 2 /nobreak >nul

REM Start Streamlit Web App
echo [2/2] Starting Web App...
echo.
echo ========================================
echo   Services Started!
echo ========================================
echo.
echo   Bot: Running in separate window
echo   Web App: http://localhost:8501
echo.
echo Press Ctrl+C to stop Web App
echo Close Bot window to stop Bot
echo ========================================
echo.

streamlit run app.py
