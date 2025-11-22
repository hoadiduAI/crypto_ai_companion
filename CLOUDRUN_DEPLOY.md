# 🚀 Google Cloud Run Deployment Guide

## Crypto Radar: AI Pilot Companion

This guide will walk you through deploying the Crypto Radar application to Google Cloud Run.

---

## 📋 Prerequisites

### 1. Google Cloud Account
- Create account at [cloud.google.com](https://cloud.google.com)
- **Free tier includes**: $300 credit for 90 days + Always Free tier
- **Billing must be enabled** (but won't be charged within free tier limits)

### 2. Install Google Cloud CLI

**Windows:**
```powershell
# Download and install from:
# https://cloud.google.com/sdk/docs/install

# Or use PowerShell:
(New-Object Net.WebClient).DownloadFile("https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe", "$env:Temp\GoogleCloudSDKInstaller.exe")
& $env:Temp\GoogleCloudSDKInstaller.exe
```

**Verify installation:**
```bash
gcloud --version
```

### 3. Telegram Bot Token
- Get your bot token from [@BotFather](https://t.me/BotFather)
- Save it securely (you'll need it for deployment)

---

## 🔧 Setup Google Cloud Project

### Step 1: Login to Google Cloud
```bash
gcloud auth login
```

### Step 2: Create New Project
```bash
# Create project
gcloud projects create crypto-radar-prod --name="Crypto Radar Production"

# Set as active project
gcloud config set project crypto-radar-prod
```

### Step 3: Enable Required APIs
```bash
# Enable Cloud Run API
gcloud services enable run.googleapis.com

# Enable Container Registry API
gcloud services enable containerregistry.googleapis.com

# Enable Cloud Build API (for automated builds)
gcloud services enable cloudbuild.googleapis.com
```

### Step 4: Set Default Region
```bash
# Use Asia Southeast (Singapore) for lower latency
gcloud config set run/region asia-southeast1

# Or choose your preferred region:
# us-central1, europe-west1, asia-northeast1, etc.
```

---

## 🚢 Deployment Methods

### Method 1: Automated Deployment (Recommended)

**Using Cloud Build with cloudbuild.yaml**

#### Step 1: Set Environment Variables
```bash
# Navigate to project directory
cd c:\Users\nguye\.gemini\antigravity\scratch\crypto_ai_companion

# Create environment variable for bot token
$env:TELEGRAM_BOT_TOKEN="your_actual_bot_token_here"
```

#### Step 2: Submit Build to Cloud Build
```bash
gcloud builds submit --config cloudbuild.yaml `
  --substitutions=_TELEGRAM_BOT_TOKEN=$env:TELEGRAM_BOT_TOKEN
```

**What this does:**
1. ✅ Builds Docker image
2. ✅ Pushes to Google Container Registry
3. ✅ Deploys to Cloud Run
4. ✅ Sets environment variables
5. ✅ Configures auto-scaling

#### Step 3: Get Service URL
```bash
gcloud run services describe crypto-radar --region asia-southeast1 --format="value(status.url)"
```

---

### Method 2: Manual Deployment

**Using gcloud CLI commands step-by-step**

#### Step 1: Build Docker Image Locally
```bash
cd c:\Users\nguye\.gemini\antigravity\scratch\crypto_ai_companion

# Build image
docker build -t gcr.io/crypto-radar-prod/crypto-radar:latest .
```

#### Step 2: Push to Container Registry
```bash
# Configure Docker to use gcloud credentials
gcloud auth configure-docker

# Push image
docker push gcr.io/crypto-radar-prod/crypto-radar:latest
```

#### Step 3: Deploy to Cloud Run
```bash
gcloud run deploy crypto-radar `
  --image gcr.io/crypto-radar-prod/crypto-radar:latest `
  --platform managed `
  --region asia-southeast1 `
  --allow-unauthenticated `
  --port 8080 `
  --memory 512Mi `
  --cpu 1 `
  --min-instances 1 `
  --max-instances 3 `
  --timeout 300 `
  --set-env-vars TELEGRAM_BOT_TOKEN=$env:TELEGRAM_BOT_TOKEN
```

---

### Method 3: Web Console Deployment

#### Step 1: Build and Push Image
```bash
cd c:\Users\nguye\.gemini\antigravity\scratch\crypto_ai_companion

# Build and push
gcloud builds submit --tag gcr.io/crypto-radar-prod/crypto-radar
```

#### Step 2: Deploy via Console
1. Go to [Cloud Run Console](https://console.cloud.google.com/run)
2. Click **"Create Service"**
3. Select **"Deploy one revision from an existing container image"**
4. Click **"Select"** and choose: `gcr.io/crypto-radar-prod/crypto-radar`
5. **Service name**: `crypto-radar`
6. **Region**: `asia-southeast1`
7. **Authentication**: Allow unauthenticated invocations
8. Click **"Container, Networking, Security"**:
   - **Container port**: `8080`
   - **Memory**: `512 MiB`
   - **CPU**: `1`
   - **Min instances**: `1`
   - **Max instances**: `3`
   - **Request timeout**: `300 seconds`
9. Click **"Variables & Secrets"** → **"Add Variable"**:
   - **Name**: `TELEGRAM_BOT_TOKEN`
   - **Value**: `your_bot_token_here`
10. Click **"Create"**

---

## 🗄️ Database Persistence (Important!)

Cloud Run containers are **stateless** by default. Your SQLite database will reset on each deployment unless you configure persistence.

### Option 1: Cloud Storage Bucket (Free Tier Available)

#### Step 1: Create Storage Bucket
```bash
# Create bucket
gsutil mb -l asia-southeast1 gs://crypto-radar-data

# Set lifecycle (optional - auto-delete old backups)
echo '[{"action": {"type": "Delete"}, "condition": {"age": 30}}]' > lifecycle.json
gsutil lifecycle set lifecycle.json gs://crypto-radar-data
```

#### Step 2: Update Deployment with Volume Mount
```bash
gcloud run deploy crypto-radar `
  --image gcr.io/crypto-radar-prod/crypto-radar:latest `
  --platform managed `
  --region asia-southeast1 `
  --allow-unauthenticated `
  --port 8080 `
  --memory 512Mi `
  --cpu 1 `
  --min-instances 1 `
  --max-instances 3 `
  --timeout 300 `
  --set-env-vars TELEGRAM_BOT_TOKEN=$env:TELEGRAM_BOT_TOKEN,DB_PATH=/data/users.db `
  --execution-environment gen2 `
  --add-volume name=data,type=cloud-storage,bucket=crypto-radar-data `
  --add-volume-mount volume=data,mount-path=/data
```

### Option 2: Cloud SQL (Recommended for Production)

**Cost**: ~$7/month for smallest instance

#### Step 1: Create Cloud SQL Instance
```bash
gcloud sql instances create crypto-radar-db `
  --database-version=POSTGRES_14 `
  --tier=db-f1-micro `
  --region=asia-southeast1
```

#### Step 2: Create Database
```bash
gcloud sql databases create cryptoradar --instance=crypto-radar-db
```

#### Step 3: Update Application
- Modify `user_db.py` to use PostgreSQL instead of SQLite
- Add `psycopg2-binary` to `requirements.txt`
- Update connection string in environment variables

---

## ✅ Verification

### 1. Check Deployment Status
```bash
gcloud run services describe crypto-radar --region asia-southeast1
```

### 2. View Logs
```bash
# Stream logs in real-time
gcloud run services logs tail crypto-radar --region asia-southeast1

# View recent logs
gcloud run services logs read crypto-radar --region asia-southeast1 --limit 50
```

### 3. Test Web App
```bash
# Get service URL
$SERVICE_URL = gcloud run services describe crypto-radar --region asia-southeast1 --format="value(status.url)"

# Open in browser
Start-Process $SERVICE_URL
```

### 4. Test Telegram Bot
- Open Telegram
- Send `/start` to your bot
- Verify bot responds
- Test `/login` command
- Check if login code works with web app

### 5. Test Alert System
```bash
# Check logs for scanning activity
gcloud run services logs tail crypto-radar --region asia-southeast1 | Select-String "SCAN"
```

---

## 📊 Monitoring & Management

### View Metrics
```bash
# Open Cloud Run dashboard
Start-Process "https://console.cloud.google.com/run/detail/asia-southeast1/crypto-radar/metrics"
```

### Set Up Alerts
1. Go to [Cloud Monitoring](https://console.cloud.google.com/monitoring)
2. Create alert for:
   - High error rate
   - High latency
   - Container crashes

### Cost Monitoring
```bash
# View current month costs
Start-Process "https://console.cloud.google.com/billing"
```

**Set Budget Alert:**
1. Go to [Billing Budgets](https://console.cloud.google.com/billing/budgets)
2. Create budget: $10/month
3. Set alert at 50%, 90%, 100%

---

## 🔄 Updates & Redeployment

### Quick Redeploy (Same Code)
```bash
cd c:\Users\nguye\.gemini\antigravity\scratch\crypto_ai_companion

# Build and deploy in one command
gcloud builds submit --config cloudbuild.yaml `
  --substitutions=_TELEGRAM_BOT_TOKEN=$env:TELEGRAM_BOT_TOKEN
```

### Rollback to Previous Version
```bash
# List revisions
gcloud run revisions list --service crypto-radar --region asia-southeast1

# Rollback to specific revision
gcloud run services update-traffic crypto-radar `
  --to-revisions=crypto-radar-00001-abc=100 `
  --region asia-southeast1
```

---

## 🔧 Troubleshooting

### Issue: Container Fails to Start

**Check logs:**
```bash
gcloud run services logs read crypto-radar --region asia-southeast1 --limit 100
```

**Common causes:**
- Missing `TELEGRAM_BOT_TOKEN` environment variable
- Port mismatch (ensure app listens on `$PORT`)
- Insufficient memory/CPU

**Solution:**
```bash
# Update with more resources
gcloud run services update crypto-radar `
  --memory 1Gi `
  --cpu 2 `
  --region asia-southeast1
```

### Issue: Bot Not Responding

**Check if bot process is running:**
```bash
gcloud run services logs read crypto-radar --region asia-southeast1 | Select-String "bot"
```

**Verify token:**
```bash
# Check environment variables
gcloud run services describe crypto-radar --region asia-southeast1 --format="value(spec.template.spec.containers[0].env)"
```

### Issue: Database Resets on Deployment

**Solution:** Implement Cloud Storage volume mount (see Database Persistence section)

### Issue: High Costs

**Check resource usage:**
```bash
Start-Process "https://console.cloud.google.com/run/detail/asia-southeast1/crypto-radar/metrics"
```

**Optimize:**
```bash
# Reduce min instances to 0 (cold starts acceptable)
gcloud run services update crypto-radar `
  --min-instances 0 `
  --region asia-southeast1

# Reduce max instances
gcloud run services update crypto-radar `
  --max-instances 2 `
  --region asia-southeast1
```

---

## 🌐 Custom Domain (Optional)

### Step 1: Verify Domain Ownership
```bash
gcloud domains verify yourdomain.com
```

### Step 2: Map Domain to Service
```bash
gcloud run domain-mappings create `
  --service crypto-radar `
  --domain app.yourdomain.com `
  --region asia-southeast1
```

### Step 3: Update DNS Records
- Add DNS records as shown in Cloud Run console
- Wait for SSL certificate provisioning (automatic)

---

## 💰 Cost Estimation

### Free Tier Limits (Always Free)
- **Requests**: 2 million/month
- **Compute**: 360,000 GB-seconds/month
- **Bandwidth**: 1 GB/month (North America)

### Estimated Costs (Beyond Free Tier)
- **Cloud Run**: $0.00002400/GB-second, $0.00000400/request
- **Container Registry**: $0.026/GB/month storage
- **Cloud Storage** (for DB): $0.020/GB/month
- **Cloud SQL** (optional): ~$7/month (db-f1-micro)

**Expected Monthly Cost**: $0-5 (within free tier for moderate usage)

---

## 🎯 Next Steps

1. ✅ **Monitor for 24 hours**: Check logs, errors, performance
2. ✅ **Setup alerts**: Cloud Monitoring for downtime/errors
3. ✅ **Optimize costs**: Adjust min/max instances based on usage
4. ✅ **Custom domain**: Setup if needed
5. ✅ **CI/CD**: Setup GitHub Actions for auto-deployment
6. ✅ **Backup**: Regular database backups to Cloud Storage

---

## 📚 Additional Resources

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Cloud Run Pricing](https://cloud.google.com/run/pricing)
- [Best Practices](https://cloud.google.com/run/docs/best-practices)
- [Troubleshooting Guide](https://cloud.google.com/run/docs/troubleshooting)

---

## 🆘 Support

**Issues with deployment?**
1. Check logs: `gcloud run services logs tail crypto-radar`
2. Review [troubleshooting section](#-troubleshooting)
3. Check [Cloud Run Status](https://status.cloud.google.com/)

**Need help?**
- [Google Cloud Support](https://cloud.google.com/support)
- [Stack Overflow](https://stackoverflow.com/questions/tagged/google-cloud-run)

---

**Last Updated**: 22/11/2025
**Version**: 1.0
