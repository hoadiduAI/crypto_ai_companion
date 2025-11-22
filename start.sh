#!/bin/bash
# Startup script for Cloud Run
# Runs both Streamlit web app and Telegram bot

set -e

echo "Starting Crypto Radar AI..."

# Create data directory if it doesn't exist
mkdir -p /app/data

# Start Telegram bot in background
echo "Starting Telegram bot..."
python alert_bot.py &
BOT_PID=$!

# Start Streamlit web app on port 8080 (Cloud Run default)
echo "Starting Streamlit web app on port ${PORT:-8080}..."
streamlit run app.py \
  --server.port=${PORT:-8080} \
  --server.address=0.0.0.0 \
  --server.headless=true \
  --server.runOnSave=false \
  --server.fileWatcherType=none \
  --browser.gatherUsageStats=false &
STREAMLIT_PID=$!

# Function to handle shutdown
shutdown() {
  echo "Shutting down gracefully..."
  kill -TERM $BOT_PID 2>/dev/null || true
  kill -TERM $STREAMLIT_PID 2>/dev/null || true
  wait $BOT_PID 2>/dev/null || true
  wait $STREAMLIT_PID 2>/dev/null || true
  echo "Shutdown complete"
  exit 0
}

# Trap signals for graceful shutdown
trap shutdown SIGTERM SIGINT

echo "All services started successfully!"
echo "Telegram Bot PID: $BOT_PID"
echo "Streamlit PID: $STREAMLIT_PID"
echo "Waiting for services..."

# Wait for both processes
wait -n

# If one process exits, shutdown everything
shutdown
