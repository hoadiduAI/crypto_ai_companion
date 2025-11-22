@echo off
REM Quick deployment script for Google Cloud Run
REM Run this after setting up gcloud CLI and project

echo ============================================
echo Crypto Radar - Google Cloud Run Deployment
echo ============================================
echo.

REM Check if gcloud is installed
where gcloud >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: gcloud CLI not found!
    echo Please install from: https://cloud.google.com/sdk/docs/install
    pause
    exit /b 1
)

REM Check if TELEGRAM_BOT_TOKEN is set
if "%TELEGRAM_BOT_TOKEN%"=="" (
    echo ERROR: TELEGRAM_BOT_TOKEN environment variable not set!
    echo.
    echo Please set it first:
    echo   set TELEGRAM_BOT_TOKEN=your_bot_token_here
    echo.
    pause
    exit /b 1
)

echo [1/4] Checking Google Cloud authentication...
gcloud auth list
if %ERRORLEVEL% NEQ 0 (
    echo Please login first: gcloud auth login
    pause
    exit /b 1
)

echo.
echo [2/4] Current project:
gcloud config get-value project
echo.

set /p CONFIRM="Continue with deployment? (y/n): "
if /i not "%CONFIRM%"=="y" (
    echo Deployment cancelled.
    exit /b 0
)

echo.
echo [3/4] Submitting build to Cloud Build...
echo This may take 5-10 minutes...
echo.

gcloud builds submit --config cloudbuild.yaml ^
  --substitutions=_TELEGRAM_BOT_TOKEN=%TELEGRAM_BOT_TOKEN%

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Deployment failed!
    echo Check logs above for details.
    pause
    exit /b 1
)

echo.
echo [4/4] Getting service URL...
echo.

for /f "delims=" %%i in ('gcloud run services describe crypto-radar --region asia-southeast1 --format="value(status.url)"') do set SERVICE_URL=%%i

echo ============================================
echo Deployment Successful!
echo ============================================
echo.
echo Service URL: %SERVICE_URL%
echo.
echo Next steps:
echo 1. Open the URL above to access Streamlit web app
echo 2. Test your Telegram bot with /start command
echo 3. Monitor logs: gcloud run services logs tail crypto-radar
echo.
echo To view logs now, press any key...
pause >nul

gcloud run services logs tail crypto-radar --region asia-southeast1
