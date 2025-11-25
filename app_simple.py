import streamlit as st
import ccxt
import pandas as pd
from datetime import datetime
import user_db
import mm_detector

# Streamlit Page Config
st.set_page_config(
    page_title="Crypto Radar: AI Pilot Companion",
    page_icon="📡",
    layout="wide"
)

# ==================== HELPER FUNCTIONS ====================

@st.cache_data(ttl=3600)
def fetch_all_symbols():
    """Fetch all USDT futures symbols from Binance"""
    try:
        exchange = ccxt.binance({
            'options': {'defaultType': 'future'}
        })
        markets = exchange.load_markets()
        symbols = [market for market in markets if '/USDT' in market]
        return sorted(symbols)
    except:
        return ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "DOGE/USDT", "XRP/USDT"]

@st.cache_data(ttl=300)
def fetch_data():
    """Fetch data from Binance Futures using mm_detector"""
    return mm_detector.fetch_binance_data()

@st.cache_data(ttl=300)
def fetch_oi_and_ratio(symbol):
    """Fetch Open Interest and Long/Short ratio for a symbol"""
    exchange = ccxt.binance({
        'options': {'defaultType': 'future'},
        'enableRateLimit': True
    })
    
    try:
        oi_data = exchange.fetch_open_interest(symbol)
        total_oi = oi_data.get('openInterestAmount', 0)
        
        try:
            funding = exchange.fetch_funding_rate(symbol)
            funding_rate = funding.get('fundingRate', 0)
            
            if funding_rate > 0:
                long_ratio = 0.5 + min(funding_rate * 1000, 0.15)
            else:
                long_ratio = 0.5 + max(funding_rate * 1000, -0.15)
            
            short_ratio = 1 - long_ratio
        except:
            long_ratio = 0.5
            short_ratio = 0.5
        
        return {
            'oi': total_oi,
            'long_ratio': long_ratio,
            'short_ratio': short_ratio
        }
    except Exception as e:
        return {'oi': 0, 'long_ratio': 0.5, 'short_ratio': 0.5}

def estimate_liquidation_volumes(price, oi, long_ratio, short_ratio):
    """Estimate liquidation volumes at different leverage levels"""
    if oi == 0:
        return None
    
    short_oi = oi * short_ratio
    long_oi = oi * long_ratio
    
    return {
        'short': {
            'x50': {'price': price * (1 + 1/50), 'volume': short_oi * 0.3},
            'x20': {'price': price * (1 + 1/20), 'volume': short_oi * 0.4},
            'x10': {'price': price * (1 + 1/10), 'volume': short_oi * 0.3},
            'total': short_oi
        },
        'long': {
            'x50': {'price': price * (1 - 1/50), 'volume': long_oi * 0.3},
            'x20': {'price': price * (1 - 1/20), 'volume': long_oi * 0.4},
            'x10': {'price': price * (1 - 1/10), 'volume': long_oi * 0.3},
            'total': long_oi
        }
    }

# ==================== CUSTOM CSS (FIXED FONT & BUTTON) ====================
st.markdown("""
<style>
    /* 1. BACKGROUND & GLOBAL */
    .stApp {
        background-color: #000000;
        background-image: 
            radial-gradient(circle at 50% 0%, #1a1a40 0%, transparent 60%),
            radial-gradient(circle at 50% 100%, #0d0d1a 0%, transparent 60%);
    }
    
    /* Fonts - Using Inter for better Vietnamese support */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Rajdhani:wght@700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }

    /* 2. NAVBAR */
    .logo {
        font-family: 'Rajdhani', sans-serif;
        font-weight: 700;
        font-size: 1.8rem;
        background: linear-gradient(90deg, #00f2ff, #00a8ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 1px;
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .beta-tag {
        border: 1px solid #00f2ff;
        color: #00f2ff;
        padding: 4px 12px;
        border-radius: 4px;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        font-size: 0.8rem;
        letter-spacing: 1px;
        box-shadow: 0 0 10px rgba(0, 242, 255, 0.2);
    }

    /* 3. HERO TITLE */
    .hero-title {
        font-family: 'Rajdhani', sans-serif;
        font-weight: 700;
        font-size: 5rem !important;
        text-align: center;
        color: #ffffff !important;
        margin-bottom: 0;
        text-transform: uppercase;
        letter-spacing: 2px;
        line-height: 1.1;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.2);
    }
    
    .gradient-text {
        background: linear-gradient(90deg, #00f2ff 0%, #bc13fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-shadow: 0 0 40px rgba(0, 242, 255, 0.5);
    }
    
    .hero-subtitle {
        font-family: 'Inter', sans-serif;
        text-align: center;
        color: #a0a0a0;
        margin-top: 1rem;
        margin-bottom: 3rem;
        font-size: 1.1rem;
        font-weight: 400;
        letter-spacing: 0.5px;
    }

    /* 4. SEARCH BAR */
    div[data-testid="stForm"] {
        background: rgba(20, 20, 30, 0.8);
        border: 1px solid rgba(0, 242, 255, 0.3);
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 0 30px rgba(0, 242, 255, 0.1);
        backdrop-filter: blur(10px);
    }

    /* Selectbox Styling */
    div[data-baseweb="select"] > div {
        background-color: #0a0a0a !important;
        border: 1px solid #333 !important;
        color: white !important;
        border-radius: 8px !important;
    }
    
    /* Dropdown Menu */
    div[role="listbox"] ul {
        background-color: #0a0a0a !important;
    }
    
    div[role="option"] {
        color: white !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    div[role="option"]:hover {
        background-color: #1a1a2e !important;
        color: #00f2ff !important;
    }

    /* Analyze Button - FIXED HOVER BLUR */
    div.stButton > button {
        background: linear-gradient(90deg, #00f2ff, #0066ff);
        color: #000 !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        width: 100%;
        transition: all 0.3s ease;
        height: 46px;
        margin-top: 2px;
    }
    
    div.stButton > button:hover {
        box-shadow: 0 0 25px rgba(0, 242, 255, 0.6);
        transform: translateY(-2px);
        color: #000 !important; /* Ensure text stays black */
        opacity: 1 !important;
    }
    
    div.stButton > button:active {
        color: #000 !important;
    }

    /* 5. PLACEHOLDER CARDS */
    .placeholder-card {
        border: 1px dashed #333;
        border-radius: 12px;
        padding: 40px 20px;
        text-align: center;
        color: #555;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 600;
        font-size: 1.2rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        background: rgba(0,0,0,0.3);
        height: 100%;
        transition: all 0.3s ease;
    }
    
    .placeholder-card:hover {
        border-color: #00f2ff;
        color: #00f2ff;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.1);
    }

</style>
""", unsafe_allow_html=True)

# ==================== MAIN LAYOUT ====================

# 1. Navbar
col_nav1, col_nav2 = st.columns([1, 1])
with col_nav1:
    st.markdown('<div class="logo">🌀 AI CRYPTO RADAR</div>', unsafe_allow_html=True)
with col_nav2:
    st.markdown("""
        <div style="display: flex; justify-content: flex-end; gap: 20px; align-items: center;">
            <span style="color: #666; font-family: 'Rajdhani'; font-size: 0.9rem;">QUÉT THỊ TRƯỜNG</span>
            <span style="color: #666; font-family: 'Rajdhani'; font-size: 0.9rem;">TÍN HIỆU</span>
            <span class="beta-tag">BETA v1.0</span>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<div style='height: 60px'></div>", unsafe_allow_html=True)

# 2. Hero Section
st.markdown("""
    <h1 class="hero-title">
        RADAR <span class="gradient-text">TÍN HIỆU</span> THỊ TRƯỜNG
    </h1>
""", unsafe_allow_html=True)

st.markdown("""
    <p class="hero-subtitle">
        Phân tích AI thời gian thực cho Trader. Nhập mã coin để nhận tín hiệu Long/Short<br>
        dựa trên tin tức và tâm lý thị trường mới nhất.
    </p>
""", unsafe_allow_html=True)

# 3. Search Section (Updated with FULL COIN LIST)
col_spacer1, col_search, col_spacer2 = st.columns([1, 1.5, 1])

# Fetch all available symbols
all_symbols = fetch_all_symbols()

with col_search:
    with st.form("search_form"):
        c1, c2 = st.columns([3, 1])
        with c1:
            # Use selectbox with full list
            search_term = st.selectbox(
                "Chọn Coin", 
                options=[""] + all_symbols, 
                index=0,
                placeholder="NHẬP MÃ CẶP (VD: BTC, ETH)...",
                label_visibility="collapsed"
            )
        with c2:
            submitted = st.form_submit_button("PHÂN TÍCH")

# 4. Content Section
if submitted and search_term:
    symbol = search_term.upper()
    if '/USDT' not in symbol:
        symbol += '/USDT'
    
    st.markdown("<div style='height: 30px'></div>", unsafe_allow_html=True)
    st.markdown(f"### 📡 KẾT QUẢ: <span style='color:#00f2ff'>{symbol}</span>", unsafe_allow_html=True)
    
    with st.spinner('Đang quét dữ liệu...'):
        df = fetch_data()
        coin_data = df[df['Symbol'] == symbol]
        
        if not coin_data.empty:
            row = coin_data.iloc[0]
            oi_data = fetch_oi_and_ratio(symbol)
            
            # Metrics
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Giá", f"${row['Price']:.4f}")
            m2.metric("Volume 24h", f"${row['Volume']/1_000_000:.1f}M")
            m3.metric("Biến Động", f"{row['Change']:+.2f}%", delta=row['Change'])
            m4.metric("Open Interest", f"${oi_data['oi']/1_000_000:.1f}M")
            
            st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
            
            # Cards
            c1, c2 = st.columns(2)
            with c1:
                st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
                st.markdown("#### 🛡️ Dòng Tiền & Tâm Lý")
                long_ratio = oi_data['long_ratio'] * 100
                short_ratio = oi_data['short_ratio'] * 100
                st.progress(long_ratio/100, text=f"Long: {long_ratio:.1f}% vs Short: {short_ratio:.1f}%")
                
                if long_ratio > 60:
                    st.error("⚠️ Cảnh báo: Phe Long quá đông. Dễ bị Long Squeeze.")
                elif short_ratio > 60:
                    st.success("✅ Cơ hội: Phe Short quá đông. Có thể có Short Squeeze.")
                else:
                    st.info("⚖️ Thị trường cân bằng.")
                st.markdown('</div>', unsafe_allow_html=True)
                
            with c2:
                st.markdown('<div class="analysis-card">', unsafe_allow_html=True)
                st.markdown("#### 🤖 AI Dự Đoán")
                if row['Change'] > 3 and row['Volume'] < 10_000_000:
                    st.warning("👻 Fake Pump: Giá tăng nhưng Vol thấp.")
                elif row['Change'] < -3 and row['Volume'] > 50_000_000:
                    st.success("🐳 Stopping Volume: Lực bắt đáy mạnh.")
                else:
                    st.write("Chưa có tín hiệu thao túng rõ ràng.")
                st.markdown('</div>', unsafe_allow_html=True)
                
        else:
            st.error(f"Không tìm thấy {symbol}")

else:
    # Placeholder Boxes (Only show when no search)
    st.markdown("<div style='height: 50px'></div>", unsafe_allow_html=True)
    
    col_ph1, col_ph2, col_ph3 = st.columns(3)
    
    with col_ph1:
        st.markdown('<div class="placeholder-card">CHỜ NHẬP LIỆU</div>', unsafe_allow_html=True)
    with col_ph2:
        st.markdown('<div class="placeholder-card">TIN TỨC LIVE</div>', unsafe_allow_html=True)
    with col_ph3:
        st.markdown('<div class="placeholder-card">HÀNH ĐỘNG GIÁ</div>', unsafe_allow_html=True)
