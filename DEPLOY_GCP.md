# 🚀 Deploying to Google Cloud Run (Web Console Method)

This is the easiest way to deploy if you don't want to use command-line tools.

## Prerequisites
1.  **GitHub Account:** You need to push your code to a GitHub repository.
2.  **Google Cloud Account:** With billing enabled.

## Step 1: Push Code to GitHub
1.  Create a new repository on [GitHub](https://github.com/new).
2.  Push all the files in this folder to that repository.
    *(If you need help with this, let me know!)*

## Step 2: Create Service on Cloud Run
1.  Go to the [Google Cloud Run Console](https://console.cloud.google.com/run).
2.  Click **CREATE SERVICE**.
3.  **Source:** Select **Continuously deploy new revisions from a source repository**.
4.  **Cloud Build:** Click **SET UP WITH CLOUD BUILD**.
    *   **Repository Provider:** GitHub.
    *   **Repository:** Select the repo you just created.
    *   **Branch:** `^main$` (or master).
    *   **Build Type:** Go with **Dockerfile** (it should auto-detect the one we created).
    *   Click **SAVE**.

## Step 3: Configure Service
1.  **Service Name:** `crypto-ai-companion` (auto-filled).
2.  **Region:** Choose `asia-southeast1` (Singapore) for best speed in Vietnam.
3.  **Authentication:** Select **Allow unauthenticated invocations** (so you can access it publicly).
4.  **CPU allocation:** Select **CPU is only allocated during request processing** (cheaper).

## Step 4: Set API Key (Important!)
1.  Expand the **Container, Networking, Security** section (at the bottom).
2.  Go to the **VARIABLES & SECRETS** tab.
3.  Click **ADD VARIABLE**.
    *   **Name:** `GEMINI_API_KEY`
    *   **Value:** `Your_Actual_Gemini_API_Key_Here` (Copy from your `.env` file)

## Step 5: Deploy
1.  Click **CREATE**.
2.  Wait a few minutes for the build and deployment to finish.
3.  Once done, you will see a **URL** at the top (e.g., `https://crypto-ai-companion-xyz.a.run.app`).
4.  Click it and enjoy your app!
