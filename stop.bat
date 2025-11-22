@echo off
echo ========================================
echo   Crypto Radar - Stopping Services
echo ========================================
echo.

REM Kill Python processes (Bot and Web App)
taskkill /F /IM python.exe /T >nul 2>&1

echo All services stopped!
echo ========================================
pause
