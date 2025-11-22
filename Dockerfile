# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Expose port for Streamlit (Cloud Run default: 8080)
EXPOSE 8080

# Set environment variable for port
ENV PORT=8080

# Run Streamlit app
CMD streamlit run app_simple.py \
  --server.port=$PORT \
  --server.address=0.0.0.0 \
  --server.headless=true \
  --server.runOnSave=false \
  --server.fileWatcherType=none \
  --browser.gatherUsageStats=false
