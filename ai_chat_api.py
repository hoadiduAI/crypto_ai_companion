"""
AI Chat API Server
Connects to Gemini API for real crypto analysis
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import google.generativeai as genai
import requests
import os
from typing import Optional
import base64
from PIL import Image
import io

app = FastAPI(title="Crypto AI Chat API")

# Serve frontend
@app.get("/")
async def read_index():
    return FileResponse('crypto-ai-chat.html')

@app.get("/markdown-formatter.js")
async def read_formatter():
    return FileResponse('markdown-formatter.js')

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini - Read from .env file if exists
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Try to read from .env file if not in environment
if not GEMINI_API_KEY and os.path.exists(".env"):
    with open(".env", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("GEMINI_API_KEY="):
                GEMINI_API_KEY = line.split("=", 1)[1].strip()
                break

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
else:
    print("WARNING: GEMINI_API_KEY not found in environment or .env file")

class AnalysisRequest(BaseModel):
    text: str
    image_base64: Optional[str] = None

class BinanceDataFetcher:
    """Fetch real-time data from Binance"""
    
    BASE_URL = "https://api.binance.com/api/v3"
    FUTURES_URL = "https://fapi.binance.com/fapi/v1"
    
    @staticmethod
    def extract_symbol(text: str) -> Optional[str]:
        """Extract coin symbol from user text"""
        text_upper = text.upper()
        common_symbols = ['BTC', 'ETH', 'BNB', 'SOL', 'XRP', 'ADA', 'DOGE', 'MATIC', 'DOT', 'AVAX']
        
        for symbol in common_symbols:
            if symbol in text_upper:
                return f"{symbol}USDT"
        
        return None
    
    @classmethod
    def get_ticker_data(cls, symbol: str) -> dict:
        """Get 24h ticker data"""
        try:
            url = f"{cls.BASE_URL}/ticker/24hr"
            response = requests.get(url, params={"symbol": symbol}, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    "price": float(data["lastPrice"]),
                    "change_24h": float(data["priceChangePercent"]),
                    "volume": float(data["volume"]),
                    "quote_volume": float(data["quoteVolume"]),
                    "high_24h": float(data["highPrice"]),
                    "low_24h": float(data["lowPrice"])
                }
        except Exception as e:
            print(f"Error fetching ticker: {e}")
        return {}
    
    @classmethod
    def get_orderbook(cls, symbol: str, limit: int = 20) -> dict:
        """Get order book data"""
        try:
            url = f"{cls.BASE_URL}/depth"
            response = requests.get(url, params={"symbol": symbol, "limit": limit}, timeout=5)
            if response.status_code == 200:
                data = response.json()
                
                # Calculate buy/sell walls
                bids = [[float(price), float(qty)] for price, qty in data["bids"][:10]]
                asks = [[float(price), float(qty)] for price, qty in data["asks"][:10]]
                
                top_bid = max(bids, key=lambda x: x[1]) if bids else [0, 0]
                top_ask = max(asks, key=lambda x: x[1]) if asks else [0, 0]
                
                return {
                    "top_buy_wall": {"price": top_bid[0], "amount": top_bid[1]},
                    "top_sell_wall": {"price": top_ask[0], "amount": top_ask[1]},
                    "bid_depth": sum([qty for _, qty in bids]),
                    "ask_depth": sum([qty for _, qty in asks])
                }
        except Exception as e:
            print(f"Error fetching orderbook: {e}")
        return {}
    
    @classmethod
    def get_funding_rate(cls, symbol: str) -> dict:
        """Get funding rate from futures"""
        try:
            url = f"{cls.FUTURES_URL}/premiumIndex"
            response = requests.get(url, params={"symbol": symbol}, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    "funding_rate": float(data["lastFundingRate"]) * 100,  # Convert to percentage
                    "mark_price": float(data["markPrice"])
                }
        except Exception as e:
            print(f"Error fetching funding rate: {e}")
        return {}
    
    @classmethod
    def get_open_interest(cls, symbol: str) -> dict:
        """Get open interest from futures"""
        try:
            url = f"{cls.FUTURES_URL}/openInterest"
            response = requests.get(url, params={"symbol": symbol}, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    "open_interest": float(data["openInterest"])
                }
        except Exception as e:
            print(f"Error fetching OI: {e}")
        return {}
    
    @classmethod
    def get_all_data(cls, symbol: str) -> dict:
        """Fetch all market data"""
        ticker = cls.get_ticker_data(symbol)
        orderbook = cls.get_orderbook(symbol)
        funding = cls.get_funding_rate(symbol)
        oi = cls.get_open_interest(symbol)
        
        return {
            "symbol": symbol,
            **ticker,
            **orderbook,
            **funding,
            **oi
        }

class AIAnalyzer:
    """AI-powered crypto analysis using Gemini"""
    
    def __init__(self):
        # Use gemini-flash-latest - always points to latest stable flash model
        self.model = genai.GenerativeModel('gemini-flash-latest')
    
    def build_prompt(self, user_query: str, market_data: dict) -> str:
        """Build analysis prompt"""
        
        # Format market data nicely
        data_summary = ""
        if market_data:
            data_summary = f"""
DATA THỊ TRƯỜNG (tự động thu thập từ Binance):
- Symbol: {market_data.get('symbol', 'N/A')}
- Giá hiện tại: ${market_data.get('price', 0):,.2f}
- Thay đổi 24h: {market_data.get('change_24h', 0):+.2f}%
- Volume 24h: ${market_data.get('quote_volume', 0):,.0f}
- High 24h: ${market_data.get('high_24h', 0):,.2f}
- Low 24h: ${market_data.get('low_24h', 0):,.2f}
"""
            
            if 'funding_rate' in market_data:
                data_summary += f"- Funding Rate: {market_data['funding_rate']:.4f}%\n"
            
            if 'open_interest' in market_data:
                data_summary += f"- Open Interest: {market_data['open_interest']:,.0f}\n"
            
            if 'top_buy_wall' in market_data:
                buy_wall = market_data['top_buy_wall']
                sell_wall = market_data['top_sell_wall']
                data_summary += f"- Top Buy Wall: ${buy_wall['price']:,.2f} ({buy_wall['amount']:,.2f})\n"
                data_summary += f"- Top Sell Wall: ${sell_wall['price']:,.2f} ({sell_wall['amount']:,.2f})\n"
        
        prompt = f"""
Bạn là chuyên gia phân tích thị trường crypto với 10 năm kinh nghiệm, đặc biệt giỏi về:
- Phân tích hành vi Market Maker (MM)
- Đọc hiểu order book, volume, funding rate
- Technical analysis và price action

USER HỎI: {user_query}

{data_summary}

HÃY PHÂN TÍCH THEO CẤU TRÚC SAU:

🎯 **TÌNH HÌNH HIỆN TẠI**
- Tóm tắt ngắn gọn tình trạng coin dựa trên data trên
- Xu hướng hiện tại (uptrend/downtrend/sideways)

🔍 **DẤU HIỆU MARKET MAKER**
- MM đang làm gì? (accumulation/distribution/pump/dump/zombie mode)
- Phân tích order book: Buy walls vs Sell walls
- Volume pattern: Tăng/giảm, có bất thường không?
- Funding rate: Long/Short đang chiếm ưu thế?

📊 **CÁC CHỈ SỐ QUAN TRỌNG**
- Những level giá cần chú ý (support/resistance)
- Volume confirmation
- Các tín hiệu kỹ thuật khác

💡 **GỢI Ý HÀNH ĐỘNG** (nếu user hỏi về trading)
- Nên làm gì tiếp theo? (quan sát/vào lệnh/chờ đợi)
- Entry/Exit points gợi ý
- Stop loss nên đặt ở đâu

⚠️ **RỦI RO CẦN LƯU Ý**
- Các rủi ro tiềm ẩn
- Điều kiện để kịch bản thay đổi

PHONG CÁCH TRẢ LỜI:
- Thân thiện, dễ hiểu, có emoji
- Giải thích "TẠI SAO" chứ không chỉ đưa kết luận
- Dùng ví dụ cụ thể, sinh động (như "Zombie Mode", "MM rút phích")
- Chia thành sections rõ ràng với headers

LƯU Ý QUAN TRỌNG:
- Đây là PHÂN TÍCH THÔNG TIN, KHÔNG phải lời khuyên đầu tư
- Luôn nhắc user tự nghiên cứu và quản lý rủi ro
- Nếu thiếu data, hãy nói rõ và yêu cầu thêm thông tin

Hãy trả lời bằng tiếng Việt, phong cách như đang chat với bạn bè!
"""
        return prompt
    
    def analyze(self, user_query: str, market_data: dict = None, image_bytes: bytes = None) -> str:
        """Perform AI analysis"""
        try:
            prompt = self.build_prompt(user_query, market_data or {})
            
            if image_bytes:
                # Analyze with image
                image = Image.open(io.BytesIO(image_bytes))
                response = self.model.generate_content([prompt, image])
            else:
                # Text only
                response = self.model.generate_content(prompt)
            
            return response.text
        
        except Exception as e:
            return f"❌ Lỗi khi phân tích: {str(e)}\n\nVui lòng thử lại hoặc liên hệ support."

# Initialize analyzer
analyzer = AIAnalyzer()

@app.get("/")
async def root():
    return {
        "message": "Crypto AI Chat API",
        "status": "running",
        "endpoints": ["/analyze", "/health"]
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "gemini_configured": bool(GEMINI_API_KEY)
    }

@app.post("/analyze")
async def analyze_crypto(
    text: str = Form(...),
    image: Optional[UploadFile] = File(None)
):
    """
    Analyze crypto market based on user query and optional chart image
    """
    try:
        # Extract symbol from query
        symbol = BinanceDataFetcher.extract_symbol(text)
        
        # Fetch market data if symbol found
        market_data = {}
        if symbol:
            market_data = BinanceDataFetcher.get_all_data(symbol)
        
        # Process image if provided
        image_bytes = None
        if image:
            image_bytes = await image.read()
        
        # Get AI analysis
        analysis = analyzer.analyze(text, market_data, image_bytes)
        
        return {
            "success": True,
            "query": text,
            "symbol": symbol,
            "market_data": market_data,
            "analysis": analysis
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-json")
async def analyze_json(request: AnalysisRequest):
    """
    Alternative endpoint accepting JSON
    """
    try:
        # Extract symbol
        symbol = BinanceDataFetcher.extract_symbol(request.text)
        
        # Fetch market data
        market_data = {}
        if symbol:
            market_data = BinanceDataFetcher.get_all_data(symbol)
        
        # Process image if provided
        image_bytes = None
        if request.image_base64:
            image_bytes = base64.b64decode(request.image_base64.split(',')[1])
        
        # Get AI analysis
        analysis = analyzer.analyze(request.text, market_data, image_bytes)
        
        return {
            "success": True,
            "query": request.text,
            "symbol": symbol,
            "market_data": market_data,
            "analysis": analysis
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("Starting Crypto AI Chat API...")
    print("Make sure GEMINI_API_KEY is set in .env file")
    uvicorn.run(app, host="0.0.0.0", port=8000)
