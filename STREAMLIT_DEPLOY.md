# 🚀 Streamlit Cloud Deployment Guide

## Crypto Radar: AI Pilot Companion (Web App Only)

Deploy your Crypto Radar web app to Streamlit Cloud for **FREE** in minutes!

---

## ✨ Why Streamlit Cloud?

- ✅ **100% Free** for public apps
- ✅ **No Docker needed** - just Python code
- ✅ **Auto-deploy** from GitHub
- ✅ **Built-in SSL** (HTTPS)
- ✅ **Custom subdomain** (yourapp.streamlit.app)
- ✅ **Easy updates** - just push to GitHub

---

## 📋 Prerequisites

1. **GitHub Account** - [Sign up free](https://github.com/signup)
2. **Streamlit Cloud Account** - [Sign up free](https://share.streamlit.io/signup)
3. **Your code** - Already in `c:\Users\nguye\.gemini\antigravity\scratch\crypto_ai_companion`

---

## 🚀 Deployment Steps

### Step 1: Push Code to GitHub

#### Option A: Using GitHub Desktop (Easiest)

1. Download [GitHub Desktop](https://desktop.github.com/)
2. Install and login with your GitHub account
3. Click **"Create New Repository"**
   - **Name**: `crypto-radar`
   - **Local Path**: `c:\Users\nguye\.gemini\antigravity\scratch\crypto_ai_companion`
   - **Keep this code private**: ✅ (if you have private repos)
4. Click **"Create Repository"**
5. Click **"Publish repository"**

#### Option B: Using Git CLI

```powershell
cd c:\Users\nguye\.gemini\antigravity\scratch\crypto_ai_companion

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Crypto Radar Web App"

# Create repo on GitHub and push
# (Follow GitHub instructions to create repo and add remote)
git remote add origin https://github.com/YOUR_USERNAME/crypto-radar.git
git branch -M main
git push -u origin main
```

---

### Step 2: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Fill in the form:
   - **Repository**: Select `YOUR_USERNAME/crypto-radar`
   - **Branch**: `main`
   - **Main file path**: `app_simple.py`
   - **App URL**: Choose your subdomain (e.g., `crypto-radar.streamlit.app`)
4. Click **"Deploy!"**

**That's it!** ✨

Streamlit Cloud will:
- Install dependencies from `requirements.txt`
- Run your app
- Give you a public URL

---

## ⏱️ Deployment Time

- **First deployment**: 3-5 minutes
- **Subsequent updates**: 1-2 minutes (auto-deploy on git push)

---

## 🔄 Updating Your App

After deployment, any changes you push to GitHub will automatically redeploy:

```powershell
cd c:\Users\nguye\.gemini\antigravity\scratch\crypto_ai_companion

# Make changes to app_simple.py or other files

# Commit and push
git add .
git commit -m "Updated analysis features"
git push

# Streamlit Cloud will auto-deploy in 1-2 minutes
```

---

## ⚙️ Advanced Configuration (Optional)

### Custom Domain

1. Go to your app settings on Streamlit Cloud
2. Click **"Custom domain"**
3. Follow instructions to add CNAME record to your DNS

### Secrets Management

If you need API keys or secrets:

1. Go to your app settings
2. Click **"Secrets"**
3. Add secrets in TOML format:
```toml
# .streamlit/secrets.toml format
API_KEY = "your_api_key_here"
```

Access in code:
```python
import streamlit as st
api_key = st.secrets["API_KEY"]
```

### Resource Limits

**Free tier limits:**
- **Memory**: 1 GB RAM
- **CPU**: Shared
- **Storage**: 1 GB
- **Bandwidth**: Unlimited

**For more resources**, upgrade to Streamlit Cloud Pro ($20/month)

---

## 🔍 Monitoring & Logs

### View Logs

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click on your app
3. Click **"Manage app"** → **"Logs"**

### Check Status

- **Green dot**: App is running
- **Red dot**: App has errors (check logs)
- **Gray dot**: App is sleeping (wakes on first visit)

---

## 🐛 Troubleshooting

### Issue: App Won't Deploy

**Check logs for errors:**
1. Go to app management page
2. Click "Logs"
3. Look for error messages

**Common causes:**
- Missing dependencies in `requirements.txt`
- Syntax errors in `app_simple.py`
- Import errors

**Solution:**
```powershell
# Test locally first
cd c:\Users\nguye\.gemini\antigravity\scratch\crypto_ai_companion
streamlit run app_simple.py

# If it works locally, check requirements.txt is complete
```

### Issue: App is Slow

**Causes:**
- Too much data processing
- No caching
- Large dataframes

**Solutions:**
- Use `@st.cache_data` decorator (already implemented)
- Reduce data fetching frequency
- Optimize queries

### Issue: App Keeps Restarting

**Cause:** Exceeding memory limit (1GB)

**Solutions:**
- Reduce data size
- Clear caches more frequently
- Upgrade to Streamlit Cloud Pro

---

## 💰 Cost Comparison

| Platform | Cost | Setup Time | Features |
|----------|------|------------|----------|
| **Streamlit Cloud** | **FREE** | **5 min** | ✅ Easy, Auto-deploy |
| Google Cloud Run | $0-5/mo | 30 min | ✅ More resources |
| Heroku | $7/mo | 20 min | ⚠️ Deprecated free tier |
| AWS | $5-10/mo | 60 min | ⚠️ Complex setup |

**Recommendation**: Start with Streamlit Cloud, migrate to Cloud Run if you need more resources.

---

## 📊 Performance Tips

### 1. Use Caching Effectively

```python
@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_data():
    return mm_detector.fetch_binance_data()
```

### 2. Lazy Loading

Only fetch data when needed:
```python
if selected_coin:
    # Only analyze when coin is selected
    analysis = orchestrator.analyze_coin(selected_coin)
```

### 3. Reduce API Calls

- Cache API responses
- Batch requests when possible
- Use longer TTL for static data

---

## 🎯 Next Steps After Deployment

1. ✅ **Share your app** - Get the URL and share with users
2. ✅ **Monitor usage** - Check analytics in Streamlit Cloud
3. ✅ **Gather feedback** - Add feedback form or contact info
4. ✅ **Iterate** - Improve based on user feedback
5. ✅ **Consider monetization** - Add premium features later

---

## 🔗 Useful Links

- [Streamlit Cloud Dashboard](https://share.streamlit.io)
- [Streamlit Documentation](https://docs.streamlit.io)
- [Streamlit Community Forum](https://discuss.streamlit.io)
- [Streamlit Gallery](https://streamlit.io/gallery) - Inspiration

---

## 📝 Example Apps

Check out these Streamlit apps for inspiration:
- [Streamlit Gallery](https://streamlit.io/gallery)
- [30 Days of Streamlit](https://30days.streamlit.app/)

---

## 🆘 Need Help?

- **Streamlit Docs**: [docs.streamlit.io](https://docs.streamlit.io)
- **Community Forum**: [discuss.streamlit.io](https://discuss.streamlit.io)
- **Discord**: [Streamlit Discord](https://discord.gg/streamlit)

---

**Ready to deploy?** Follow Step 1 to push your code to GitHub, then Step 2 to deploy! 🚀

---

**Last Updated**: 22/11/2025
**Deployment Time**: ~5 minutes
**Cost**: FREE
