# AI Crypto Radar (React/Vite Edition)

## Overview
**AI Crypto Radar** is a professional-grade crypto trading assistant powered by **Google Gemini 2.5 Flash**. It provides real-time market analysis, trade setups, and risk detection in a Cyberpunk-themed interface.

## Features
- **AI Signal Analysis:** Long/Short/Neutral signals with confidence scores.
- **Trade Setups:** Entry, Target (TP), and Stop Loss levels.
- **Risk Radar:** Whale concentration, volume anomalies, and order book health.
- **Liquidation Heatmap:** Visual simulation of liquidity clusters.
- **Cyberpunk UI:** Glassmorphism, Neon Glows, and animated Radar scanning.

## Tech Stack
- **Frontend:** React 18, Vite, TypeScript
- **Styling:** Tailwind CSS
- **AI:** Google Gemini SDK
- **Icons:** Lucide React

## Setup & Run

### 1. Install Dependencies
```bash
npm install
```

### 2. Configure Environment
Create a `.env` file in the root directory:
```env
VITE_GEMINI_API_KEY=your_google_api_key_here
```

### 3. Start Development Server
```bash
npm run dev
```

## Project Structure
```
/src
  /components    # UI Components (Header, SearchBar, Heatmap...)
  /services      # API Integration (Gemini)
  App.tsx        # Main Logic
  types.ts       # TypeScript Interfaces
```

---
*Migrated from Python/Streamlit by Antigravity.*
