# Crypto AI Chat - API Integration Guide

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install fastapi uvicorn google-generativeai requests pillow python-multipart
```

### 2. Set Gemini API Key

```bash
# Windows PowerShell
$env:GEMINI_API_KEY="your-api-key-here"

# Windows CMD
set GEMINI_API_KEY=your-api-key-here

# Linux/Mac
export GEMINI_API_KEY="your-api-key-here"
```

### 3. Start Backend Server

```bash
python ai_chat_api.py
```

Server will run at: `http://localhost:8000`

### 4. Open Frontend

Open `ai-chat-interface.html` in your browser.

**Note**: Due to CORS, you need to either:
- Use a local server (recommended)
- Or enable CORS in your browser (for testing only)

**Recommended**: Use Python's built-in server:
```bash
python -m http.server 8080
```

Then open: `http://localhost:8080/ai-chat-interface.html`

## 📡 API Endpoints

### POST /analyze
Analyze crypto market with text query and optional image

**Form Data:**
- `text` (required): User query
- `image` (optional): Chart image file

**Response:**
```json
{
  "success": true,
  "query": "Phân tích BTC",
  "symbol": "BTCUSDT",
  "market_data": {
    "price": 43250.50,
    "change_24h": 2.3,
    "volume": 28500000000,
    ...
  },
  "analysis": "AI generated analysis..."
}
```

### GET /health
Check API health status

## 🔧 How It Works

1. **User sends query** → Frontend captures text/image
2. **Frontend calls API** → POST to `/analyze`
3. **Backend processes**:
   - Extracts coin symbol from query
   - Fetches real-time data from Binance
   - Sends to Gemini AI for analysis
4. **AI analyzes** → Returns structured response
5. **Frontend displays** → Shows analysis in chat

## 💡 Features

- ✅ Real-time Binance data fetching
- ✅ Gemini AI analysis
- ✅ Image upload support (Gemini Vision)
- ✅ Auto symbol detection
- ✅ Order book analysis
- ✅ Funding rate & OI tracking
- ✅ Vietnamese language support

## 🎯 Example Queries

- "Phân tích BTC hiện tại"
- "ETH có đáng mua không?"
- "Giải thích Funding Rate"
- Upload chart image for technical analysis

## 🐛 Troubleshooting

### API not connecting
- Check if backend server is running
- Verify GEMINI_API_KEY is set
- Check browser console for CORS errors

### No data returned
- Ensure coin symbol is recognized (BTC, ETH, etc.)
- Check Binance API is accessible
- Verify API key is valid

### Slow responses
- Gemini API might be rate-limited
- Network latency to Binance
- Consider caching responses

## 📊 Cost Estimation

**Gemini 2.0 Flash:**
- ~$0.0006 per text analysis
- ~$0.002 per image analysis
- Very affordable for testing!

## 🔐 Security Notes

- Never commit API keys to git
- Use environment variables
- Consider rate limiting for production
- Add authentication for public deployment
