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

# ==================== AUTHENTICATION ====================

def login_sidebar():
    """Handle login in sidebar"""
    st.sidebar.header("🔐 Đăng Nhập")
    
    if 'user' not in st.session_state:
        st.sidebar.info("Đăng nhập để quản lý danh sách theo dõi.")
        
        with st.sidebar.form("login_form"):
            code = st.text_input("Nhập mã đăng nhập (từ Bot):", placeholder="123456")
            submitted = st.form_submit_button("Đăng Nhập")
            
            if submitted:
                telegram_id = user_db.verify_login_code(code)
                if telegram_id:
                    user = user_db.get_user(telegram_id)
                    st.session_state['user'] = user
                    st.success("Đăng nhập thành công!")
                    st.rerun()
                else:
                    st.error("Mã không hợp lệ hoặc đã hết hạn.")
        
        st.sidebar.markdown("---")
        st.sidebar.caption("Cách lấy mã:")
        st.sidebar.markdown("[👉 **Lấy mã nhanh (Mở Telegram)**](https://t.me/Radar4Pilot_bot?start=login)")
        st.sidebar.caption("Hoặc chat `/login` với Bot")
    else:
        user = st.session_state['user']
        # Refresh user data
        user = user_db.get_user(user['telegram_id'])
        st.session_state['user'] = user
        
        st.sidebar.success(f"Xin chào, **{user['username']}**!")
        
        status = user_db.get_user_status(user['telegram_id'])
        st.sidebar.info(f"Gói: **{status['tier'].upper()}**")
        st.sidebar.write(f"Đang theo dõi: {status['tracked_count']}/{status['limit']}")
        
        if st.sidebar.button("Đăng Xuất"):
            del st.session_state['user']
            st.rerun()

# ==================== HELPER FUNCTIONS ====================

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

# ==================== CUSTOM CSS (CYBERPUNK THEME) ====================
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #050505;
        background-image: radial-gradient(circle at 50% 50%, #1a1a2e 0%, #050505 60%);
    }
    
    /* Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@500;700&family=Roboto+Mono:wght@400;700&display=swap');
    
    h1, h2, h3 {
        font-family: 'Rajdhani', sans-serif;
        text-transform: uppercase;
        color: #fff;
        text-shadow: 0 0 10px rgba(0, 242, 255, 0.5);
    }
    
    /* Hero Title */
    .hero-title {
        font-size: 4rem !important;
        text-align: center;
        background: -webkit-linear-gradient(0deg, #fff, #00f2ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        font-family: 'Roboto Mono', monospace;
        text-align: center;
        color: #8892b0;
        margin-bottom: 3rem;
        font-size: 1rem;
    }

    /* Search Box Container */
    .search-container {
        max-width: 700px;
        margin: 0 auto;
        padding: 2px;
        background: linear-gradient(90deg, #00f2ff, #bc13fe);
        border-radius: 10px;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.2);
    }
    
    .search-inner {
        background: #0a0a0a;
        border-radius: 8px;
        padding: 20px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Custom Input Styling */
    div[data-baseweb="input"] {
        background-color: transparent !important;
        border: none !important;
        color: white !important;
    }
    
    input {
        color: white !important;
        font-family: 'Roboto Mono', monospace !important;
        font-size: 1.2rem !important;
    }

    /* Neon Button */
    div.stButton > button {
        background: linear-gradient(90deg, #00f2ff, #00a8ff);
        color: black !important;
        font-family: 'Rajdhani', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.2rem !important;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        transition: all 0.3s ease;
        text-transform: uppercase;
        width: 100%;
    }
    
    div.stButton > button:hover {
        box-shadow: 0 0 20px #00f2ff;
        transform: scale(1.02);
    }

    /* Cards/Metrics */
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 242, 255, 0.2);
        padding: 15px;
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }
    
    div[data-testid="stMetricLabel"] {
        color: #8892b0;
    }
    
    div[data-testid="stMetricValue"] {
        color: #00f2ff;
        font-family: 'Roboto Mono', monospace;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background-color: rgba(255, 255, 255, 0.02);
        border: 1px solid #333;
        color: #fff;
    }
</style>
""", unsafe_allow_html=True)

# ==================== MAIN LAYOUT ====================

# Login Sidebar (Keep it but maybe minimal)
login_sidebar()

# 1. Header Section
col1, col2 = st.columns([1, 5])
with col1:
    st.markdown("### 🌀 AI CRYPTO RADAR")
with col2:
    st.markdown('<div style="text-align: right; padding-top: 10px;"><span style="color: #00f2ff; border: 1px solid #00f2ff; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem;">BETA v1.0</span></div>', unsafe_allow_html=True)

st.markdown("<div style='height: 50px'></div>", unsafe_allow_html=True)

# 2. Hero Section
st.markdown('<h1 class="hero-title">RADAR TÍN HIỆU THỊ TRƯỜNG</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle">Phân tích AI thời gian thực cho Trader. Nhập mã coin để nhận tín hiệu Long/Short<br>dựa trên dòng tiền và tâm lý thị trường mới nhất.</p>', unsafe_allow_html=True)

# 3. Search Section
col_spacer1, col_search, col_spacer2 = st.columns([1, 2, 1])

with col_search:
    with st.form("search_form"):
        col_input, col_btn = st.columns([3, 1])
        with col_input:
            search_term = st.text_input("", placeholder="NHẬP MÃ CẶP (VD: BTC, ETH)...", label_visibility="collapsed")
        with col_btn:
            submitted = st.form_submit_button("PHÂN TÍCH")

# 4. Analysis Result Section
if submitted and search_term:
    symbol = search_term.upper()
    if '/USDT' not in symbol:
        symbol += '/USDT'
    
    st.markdown("---")
    st.markdown(f"### 📡 KẾT QUẢ PHÂN TÍCH: <span style='color:#00f2ff'>{symbol}</span>", unsafe_allow_html=True)
    
    with st.spinner('Đang quét dữ liệu từ Binance & Coinglass...'):
        # Fetch Data
        df = fetch_data()
        coin_data = df[df['Symbol'] == symbol]
        
        if not coin_data.empty:
            row = coin_data.iloc[0]
            oi_data = fetch_oi_and_ratio(symbol)
            
            # Metrics Row
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Giá Hiện Tại", f"${row['Price']:.4f}")
            m2.metric("Volume 24h", f"${row['Volume']/1_000_000:.1f}M")
            m3.metric("Biến Động", f"{row['Change']:+.2f}%", delta=row['Change'])
            m4.metric("Open Interest", f"${oi_data['oi']/1_000_000:.1f}M")
            
            st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
            
            # AI Analysis Cards
            c1, c2 = st.columns(2)
            
            with c1:
                st.markdown("""
                <div style="padding: 20px; border: 1px solid #333; border-radius: 10px; background: rgba(0,0,0,0.3);">
                    <h4 style="color: #00f2ff; margin-top: 0;">🛡️ Dòng Tiền & Tâm Lý</h4>
                """, unsafe_allow_html=True)
                
                long_ratio = oi_data['long_ratio'] * 100
                short_ratio = oi_data['short_ratio'] * 100
                
                st.progress(long_ratio/100, text=f"Long: {long_ratio:.1f}% vs Short: {short_ratio:.1f}%")
                
                if long_ratio > 60:
                    st.error("⚠️ Cảnh báo: Phe Long quá đông (Crowded Trade). Dễ bị Long Squeeze.")
                elif short_ratio > 60:
                    st.success("✅ Cơ hội: Phe Short quá đông. Có thể có Short Squeeze (Đẩy giá lên).")
                else:
                    st.info("⚖️ Thị trường cân bằng.")
                    
                st.markdown("</div>", unsafe_allow_html=True)

            with c2:
                st.markdown("""
                <div style="padding: 20px; border: 1px solid #333; border-radius: 10px; background: rgba(0,0,0,0.3);">
                    <h4 style="color: #bc13fe; margin-top: 0;">🤖 AI Dự Đoán (MM Hunter)</h4>
                """, unsafe_allow_html=True)
                
                # Simple Logic check (can be replaced with mm_logic later)
                if row['Change'] > 3 and row['Volume'] < 10_000_000:
                    st.warning("👻 Phát hiện: Fake Pump (Giá tăng nhưng Vol thấp).")
                elif row['Change'] < -3 and row['Volume'] > 50_000_000:
                    st.success("🐳 Phát hiện: Stopping Volume (Có lực bắt đáy mạnh).")
                else:
                    st.write("Chưa phát hiện hành vi thao túng rõ ràng.")
                    
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Liquidation Analysis (Added back)
            st.markdown("<div style='height: 20px'></div>", unsafe_allow_html=True)
            st.subheader("⚡ Phân Tích Thanh Lý")
            
            liq_est = estimate_liquidation_volumes(row['Price'], oi_data['oi'], oi_data['long_ratio'], oi_data['short_ratio'])
            
            col_liq1, col_liq2 = st.columns(2)
            with col_liq1:
                st.markdown("**🔴 Phe Short (Bị thanh lý khi giá TĂNG):**")
                if liq_est:
                    short_data = liq_est['short']
                    st.write(f"- 💀 **x50:** ${short_data['x50']['price']:.4f} (Vol: ${short_data['x50']['volume']/1_000_000:.2f}M)")
                    st.write(f"- 💀 **x20:** ${short_data['x20']['price']:.4f} (Vol: ${short_data['x20']['volume']/1_000_000:.2f}M)")
                else:
                    st.write("Không đủ dữ liệu.")
            
            with col_liq2:
                st.markdown("**🟢 Phe Long (Bị thanh lý khi giá GIẢM):**")
                if liq_est:
                    long_data = liq_est['long']
                    st.write(f"- 🩸 **x50:** ${long_data['x50']['price']:.4f} (Vol: ${long_data['x50']['volume']/1_000_000:.2f}M)")
                    st.write(f"- 🩸 **x20:** ${long_data['x20']['price']:.4f} (Vol: ${long_data['x20']['volume']/1_000_000:.2f}M)")
                else:
                    st.write("Không đủ dữ liệu.")
                
        else:
            st.error(f"Không tìm thấy dữ liệu cho {symbol}. Vui lòng kiểm tra lại mã.")

# 5. Footer / Placeholder (Only show if no search)
if not submitted:
    st.markdown("<div style='height: 50px'></div>", unsafe_allow_html=True)
    col_ph1, col_ph2, col_ph3 = st.columns(3)
    
    style_card = 'border: 1px dashed #333; padding: 30px; text-align: center; color: #555; border-radius: 10px;'
    
    with col_ph1:
        st.markdown(f'<div style="{style_card}">Waiting for Input...</div>', unsafe_allow_html=True)
    with col_ph2:
        st.markdown(f'<div style="{style_card}">Live News (Coming Soon)</div>', unsafe_allow_html=True)
    with col_ph3:
        st.markdown(f'<div style="{style_card}">Price Action (Coming Soon)</div>', unsafe_allow_html=True)
