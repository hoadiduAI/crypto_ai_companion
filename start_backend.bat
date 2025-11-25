@echo off
chcp 65001 >nul
echo ========================================
echo   Crypto AI Chat - Startup Script
echo ========================================
echo.

REM Check if .env exists
if not exist .env (
    echo [ERROR] File .env chua ton tai!
    echo.
    echo Hay tao file .env voi noi dung:
    echo GEMINI_API_KEY=your-api-key-here
    echo.
    pause
    exit /b 1
)

REM Load .env and set environment variable
for /f "tokens=1,2 delims==" %%a in (.env) do (
    if "%%a"=="GEMINI_API_KEY" set GEMINI_API_KEY=%%b
)

REM Check if API key is set
if "%GEMINI_API_KEY%"=="" (
    echo [ERROR] GEMINI_API_KEY chua duoc set trong file .env
    echo.
    echo Mo file .env va dien API key cua ban
    echo.
    pause
    exit /b 1
)

echo [OK] API Key loaded: %GEMINI_API_KEY:~0,20%...
echo.
echo Starting backend server...
echo.

python ai_chat_api.py

pause
