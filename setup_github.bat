@echo off
echo ========================================
echo   HUONG DAN PUSH CODE LEN GITHUB
echo ========================================
echo.
echo Buoc 1: Mo Git Bash
echo - Nhan chuot phai vao thu muc nay
echo - Chon "Git Bash Here"
echo.
echo Buoc 2: Chay cac lenh sau trong Git Bash:
echo.
echo # Cau hinh Git (thay YOUR_NAME va YOUR_EMAIL)
echo git config --global user.name "YOUR_NAME"
echo git config --global user.email "YOUR_EMAIL"
echo.
echo # Khoi tao Git repository
echo git init
echo.
echo # Them tat ca files
echo git add .
echo.
echo # Commit
echo git commit -m "Initial commit - Crypto Radar Bot"
echo.
echo # Ket noi voi GitHub (thay YOUR_USERNAME)
echo git remote add origin https://github.com/YOUR_USERNAME/crypto-radar-bot.git
echo.
echo # Push len GitHub
echo git branch -M main
echo git push -u origin main
echo.
echo ========================================
pause
