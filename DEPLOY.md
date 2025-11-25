# 🚀 Deployment Guide for Crypto AI Companion

This guide will help you deploy your Crypto AI Companion to the web so you can access it from anywhere.

## Option 1: Deploy to Render (Recommended - Free & Easy)

1.  **Push your code to GitHub:**
    *   Create a new repository on GitHub.
    *   Push all files in this folder to that repository.

2.  **Create a New Web Service on Render:**
    *   Go to [dashboard.render.com](https://dashboard.render.com/).
    *   Click **New +** and select **Web Service**.
    *   Connect your GitHub account and select the repository you just created.

3.  **Configure the Service:**
    *   **Name:** `crypto-ai-companion` (or any name you like)
    *   **Region:** Singapore (or closest to you)
    *   **Branch:** `main` (or `master`)
    *   **Runtime:** `Python 3`
    *   **Build Command:** `pip install -r requirements.txt`
    *   **Start Command:** `uvicorn ai_chat_api:app --host 0.0.0.0 --port $PORT`
    *   **Plan:** Free

4.  **Set Environment Variables:**
    *   Scroll down to **Environment Variables**.
    *   Click **Add Environment Variable**.
    *   **Key:** `GEMINI_API_KEY`
    *   **Value:** `Your_Actual_Gemini_API_Key_Here` (Copy from your `.env` file)

5.  **Deploy:**
    *   Click **Create Web Service**.
    *   Wait for the deployment to finish (it might take a few minutes).
    *   Once done, Render will give you a URL (e.g., `https://crypto-ai-companion.onrender.com`). Click it to use your app!

---

## Option 2: Deploy to Railway

1.  **Push your code to GitHub.**

2.  **Create a New Project on Railway:**
    *   Go to [railway.app](https://railway.app/).
    *   Click **New Project** -> **Deploy from GitHub repo**.
    *   Select your repository.

3.  **Configure Variables:**
    *   Click on the project card.
    *   Go to the **Variables** tab.
    *   Add `GEMINI_API_KEY` with your API key value.

4.  **Deploy:**
    *   Railway usually auto-detects the `Procfile` and deploys automatically.
    *   Go to **Settings** -> **Domains** to get your public URL.

## ⚠️ Important Notes

*   **API Key:** Never commit your `.env` file to GitHub. Always set the `GEMINI_API_KEY` in the hosting provider's dashboard.
*   **Cost:** Both Render and Railway have free tiers that are sufficient for this app.
*   **Wake Up Time:** On the free tier of Render, the app might "sleep" after inactivity. The first request might take 30-60 seconds to load. This is normal.
