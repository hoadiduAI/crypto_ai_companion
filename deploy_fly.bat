@echo off
echo ========================================
echo   HUONG DAN DEPLOY LEN FLY.IO
echo ========================================
echo.
echo Buoc 1: Dang ky/Dang nhap Fly.io
echo --------------------------------
echo Chay lenh:
echo   flyctl auth signup
echo hoac (neu da co tai khoan):
echo   flyctl auth login
echo.
echo Buoc 2: Khoi tao Fly app
echo --------------------------------
echo   flyctl launch --no-deploy
echo.
echo Tra loi cac cau hoi:
echo   - App name: crypto-radar-bot
echo   - Region: sin (Singapore)
echo   - Postgres: No
echo   - Redis: No
echo   - Deploy now: No
echo.
echo Buoc 3: Them secrets (Bot Token va Chat ID)
echo --------------------------------
echo   flyctl secrets set TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN
echo   flyctl secrets set TELEGRAM_CHAT_ID=YOUR_CHAT_ID
echo.
echo Buoc 4: Deploy!
echo --------------------------------
echo   flyctl deploy
echo.
echo Buoc 5: Xem logs
echo --------------------------------
echo   flyctl logs
echo.
echo ========================================
echo   CHI TIET XEM FILE: FLY_DEPLOY.md
echo ========================================
pause
