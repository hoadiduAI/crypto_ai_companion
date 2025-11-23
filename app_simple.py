import streamlit as st
import ccxt
import pandas as pd
from datetime import datetime
import mm_detector

# Streamlit Page Config
st.set_page_config(
    page_title="Crypto Radar: AI Pilot Companion",
    page_icon="📡",
    layout="wide"
)

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
# ==================== MAIN APP ====================

# Load Custom UI
import app_ui
app_ui.load_custom_css()

# Header
app_ui.render_header()

# Load data
with st.spinner('Đang quét dữ liệu từ Binance Futures...'):
    df, data_source = fetch_data()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

if df.empty:
    st.error("❌ Không thể kết nối Binance. Vui lòng thử lại sau.")
    st.stop()

# Display Data Source Info
if "CoinGecko" in data_source:
    st.warning(f"⚠️ **Lưu ý:** Dữ liệu được lấy từ **{data_source}** do kết nối đến Binance bị chậm. Volume hiển thị là **Tổng Volume toàn thị trường**.")
else:
    st.info(f"✅ Dữ liệu từ: **{data_source}** | Cập nhật: **{current_time}** (Tự động refresh sau 5 phút)")

# ==================== 🏆 TOP MARKET VOLUME ====================

with st.expander("🏆 Top Giao Dịch Sôi Động Nhất (Volume Leaderboard)", expanded=False):
    st.caption("Dòng tiền đang đổ vào đâu? (Sắp xếp theo Volume từ cao xuống thấp)")
    
    # Sort by Volume descending
    top_volume_df = df.sort_values(by='Volume', ascending=False).head(15).copy()
    
    # Format for display
    display_df = top_volume_df.copy()
    display_df['Price'] = display_df['Price'].apply(lambda x: f"${x:.4f}")
    display_df['Change'] = display_df['Change'].apply(lambda x: f"{x:+.2f}%")
    # Keep Volume as number for column config, will format in st.dataframe
    
    # Display interactive table
    st.dataframe(
        display_df[['Symbol', 'Price', 'Change', 'Volume']],
        use_container_width=True,
        column_config={
            "Symbol": st.column_config.TextColumn("Coin", help="Cặp giao dịch"),
            "Price": st.column_config.TextColumn("Giá"),
            "Change": st.column_config.TextColumn("Biến Động 24h"),
            "Volume": st.column_config.ProgressColumn(
                "Volume 24h ($)",
                help="Khối lượng giao dịch 24h",
                format="$%.2f",
                min_value=0,
                max_value=top_volume_df['Volume'].max(),
            ),
        },
        hide_index=True,
    )
    st.caption("💡 *Click vào tiêu đề cột để sắp xếp lại theo ý muốn.*")

# ==================== IMPROVED COIN SELECTOR ====================

st.header("🔍 Chọn Coin Để Phân Tích")

# 1. Quick Select (Top Coins)
st.caption("🔥 Phổ biến:")
cols = st.columns(6)
popular_coins = ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "DOGE/USDT", "XRP/USDT"]

# Initialize session state for coin selection if not exists
if 'selected_coin_state' not in st.session_state:
    st.session_state['selected_coin_state'] = popular_coins[0]

# Create buttons for popular coins
for i, coin in enumerate(popular_coins):
    if cols[i].button(coin.split('/')[0], use_container_width=True):
        st.session_state['selected_coin_state'] = coin
        st.rerun()

# 2. Smart Search Dropdown (Type to search)
all_coins = df['Symbol'].tolist()

# Find index of currently selected coin to set as default
try:
    current_index = all_coins.index(st.session_state['selected_coin_state'])
except ValueError:
    current_index = 0

st.write("") # Spacing

selected_coin = st.selectbox(
    "📋 **Gõ tên coin vào đây để tìm nhanh (VD: gõ 'M' sẽ hiện MATIC, MANA...):**",
    options=all_coins,
    index=current_index,
    key="main_coin_selector",
    help="Hỗ trợ tìm kiếm: Chỉ cần gõ tên coin, danh sách sẽ tự lọc."
)

# Update session state when dropdown changes
if selected_coin != st.session_state['selected_coin_state']:
    st.session_state['selected_coin_state'] = selected_coin
    st.rerun()

st.markdown("---")

# ==================== COMPREHENSIVE ANALYSIS ====================

if selected_coin:
    # Import alert orchestrator
    from alert_orchestrator import AlertOrchestrator
    
    # Get coin data
    coin_data = df[df['Symbol'] == selected_coin]
    
    if coin_data.empty:
        st.warning(f"Không tìm thấy dữ liệu cho {selected_coin}")
    else:
        coin_data = coin_data.iloc[0]
        price = coin_data['Price']
        vol = coin_data['Volume']
        change_24h = coin_data['Change']
        
        # Calculate Analysis & Risk
        orchestrator = AlertOrchestrator()
        analysis = orchestrator.analyze_coin(selected_coin)
        risk_score = analysis['risk_score'] if not analysis.get('error') else 0
        signals = analysis['signals'] if not analysis.get('error') else []
        
        # Generate AI Insight
        from ai_insight import generate_ai_insight
        ai_report = generate_ai_insight(selected_coin, price, change_24h, vol, risk_score, signals)
        
        # Determine Signal & Trade Setup (Simulation Logic)
        signal_type = "NEUTRAL"
        if risk_score >= 70: signal_type = "SHORT"
        elif risk_score <= 30: signal_type = "LONG"
        
        # Volatility-based Setup
        volatility = price * 0.02 # Est 2% volatility base
        if abs(change_24h) > 5: volatility = price * 0.04
        
        entry = price
        if signal_type == "LONG":
            target = price + (volatility * 1.5)
            stoploss = price - (volatility * 0.8)
        elif signal_type == "SHORT":
            target = price - (volatility * 1.5)
            stoploss = price + (volatility * 0.8)
        else:
            target = price * 1.01
            stoploss = price * 0.99

        # ==================== DASHBOARD UI ====================
        
        # 1. HUD SECTION (Signal + TL;DR + Setup)
        col_hud_1, col_hud_2 = st.columns([1, 2])
        
        with col_hud_1:
            app_ui.render_signal_badge(signal_type, 100 - risk_score if signal_type == "LONG" else risk_score)
            
            # Mini Sentiment Chart
            st.caption("📈 Xu Hướng Tâm Lý")
            chart_data = pd.DataFrame({'Value': [50, 52, 48, 55, 60, 58, 65, 70] if signal_type == "LONG" else [50, 48, 52, 45, 40, 42, 35, 30]})
            st.area_chart(chart_data, height=120, color="#00ff9d" if signal_type == "LONG" else "#ff003c")
            
        with col_hud_2:
            app_ui.render_tldr(ai_report['tldr'])
            app_ui.render_trade_setup(f"${entry:.4f}", f"${target:.4f}", f"${stoploss:.4f}")

        st.markdown("---")

        # 2. RADAR METRICS (Risk & Volume)
        st.subheader("📡 Radar Thao Túng & Dữ Liệu")
        
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("Risk Score", f"{risk_score}/100", delta="Cao" if risk_score > 70 else "Thấp", delta_color="inverse")
        with col_m2:
            vol_label = "Volume (Binance)" if "Binance" in data_source else "Volume (Global)"
            st.metric(vol_label, f"${vol/1_000_000:.2f}M", delta="Ghost Town" if vol < 5000000 else "Active")
        with col_m3:
            st.metric("Biến Động 24h", f"{change_24h:+.2f}%", delta=f"{change_24h:+.2f}%")

        # 3. DETAILED REPORT
        with st.expander("📄 Báo Cáo Chi Tiết (AI Analysis)", expanded=True):
            st.markdown(ai_report['body'])
            st.caption(f"🏁 **Kết Luận:** {ai_report['conclusion']}")
            st.caption("ℹ️ *Dữ liệu được phân tích từ Binance Futures.*")

        st.markdown("---")

        # 4. LIQUIDATION HEATMAP (Simulated)
        st.subheader("⚡ Heatmap Thanh Lý (Mô Phỏng)")
        
        # Fetch OI data for context
        oi_data = fetch_oi_and_ratio(selected_coin)
        total_oi = oi_data['oi']
        long_ratio = oi_data['long_ratio']
        short_ratio = oi_data['short_ratio']
        
        col_liq1, col_liq2 = st.columns(2)
        with col_liq1:
            st.markdown(f"**🔴 Phe Short ({short_ratio*100:.1f}%)**")
            st.progress(short_ratio, text="Short Interest")
            st.caption(f"Vùng thanh lý ước tính: ${price*1.02:.4f} - ${price*1.05:.4f}")
        with col_liq2:
            st.markdown(f"**🟢 Phe Long ({long_ratio*100:.1f}%)**")
            st.progress(long_ratio, text="Long Interest")
            st.caption(f"Vùng thanh lý ước tính: ${price*0.98:.4f} - ${price*0.95:.4f}")
            
        base_symbol = selected_coin.split('/')[0]
        st.link_button(f"🔎 Xem Heatmap Chi Tiết trên Coinglass", f"https://www.coinglass.com/liquidation/{base_symbol}")

# ==================== MARKET SCANNER (COLLAPSIBLE) ====================

st.markdown("---")

with st.expander("🔍 Quét Thị Trường (Ghost Towns & Fake Pumps)"):
    # Sidebar filters
    col_filter1, col_filter2 = st.columns(2)
    with col_filter1:
        min_price = st.number_input("Giá tối thiểu ($)", value=0.5)
    with col_filter2:
        max_vol = st.number_input("Volume tối đa (Triệu $)", value=10.0) * 1_000_000
    
    # Ghost Towns
    st.subheader("👻 Ghost Towns (Thị Trấn Ma)")
    st.info(f"Các coin có Giá > {min_price}$ nhưng Volume < {max_vol/1_000_000}M $. Dấu hiệu MM giữ giá.")
    
    ghost_towns = mm_detector.detect_ghost_towns(df, min_price, max_vol)
    
    display_df = ghost_towns.copy()
    display_df['Volume'] = display_df['Volume'].apply(lambda x: f"${x:,.0f}")
    display_df['Price'] = display_df['Price'].apply(lambda x: f"${x:.4f}")
    display_df['Change'] = display_df['Change'].apply(lambda x: f"{x:+.2f}%")
    
    st.dataframe(display_df[['Symbol', 'Price', 'Change', 'Volume']], use_container_width=True)

    # Fake Pumps
    st.subheader("🚀 Fake Pumps (Bơm Thổi Ảo)")
    st.warning("Các coin tăng giá mạnh (>5%) nhưng Volume thấp. Cẩn thận Bull Trap.")
    
    fake_pumps = mm_detector.detect_fake_pumps(df, 5, 20_000_000)
    
    pump_df = fake_pumps.copy()
    pump_df['Volume'] = pump_df['Volume'].apply(lambda x: f"${x:,.0f}")
    pump_df['Price'] = pump_df['Price'].apply(lambda x: f"${x:.4f}")
    pump_df['Change'] = pump_df['Change'].apply(lambda x: f"{x:+.2f}%")
    
    st.dataframe(pump_df[['Symbol', 'Price', 'Change', 'Volume']], use_container_width=True)

# Footer
st.markdown("---")
st.caption("💡 **Lưu ý:** Đây là công cụ phân tích, không phải lời khuyên đầu tư. Luôn DYOR (Do Your Own Research)!")
