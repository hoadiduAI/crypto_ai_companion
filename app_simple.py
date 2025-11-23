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

# Header
st.title("📡 Crypto Radar: AI Pilot Companion")
st.caption("Phát hiện Ghost Towns & Fake Pumps - Bảo vệ vị thế của bạn khỏi Market Maker")

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
    st.header(f"📊 Phân Tích Chi Tiết: {selected_coin}")
    
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
        
        # Determine Volume Label based on Source
        if "CoinGecko" in data_source:
            vol_label = "Vol 24h (Global - All Exchanges)"
        else:
            vol_label = "Vol 24h (Binance Futures)"
            
        # Display basic metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Giá Hiện Tại", f"${price:.4f}")
        with col2:
            st.metric(vol_label, f"${vol/1_000_000:.2f}M")
        with col3:
            st.metric("Biến Động 24h", f"{change_24h:+.2f}%", delta=f"{change_24h:+.2f}%")
        
        st.markdown("---")

        # ==================== 🤖 AI PILOT INSIGHT (BETA) ====================
        from ai_insight import generate_ai_insight
        
        # Calculate risk first to pass to AI
        orchestrator = AlertOrchestrator()
        analysis = orchestrator.analyze_coin(selected_coin)
        risk_score = analysis['risk_score'] if not analysis.get('error') else 0
        signals = analysis['signals'] if not analysis.get('error') else []
        
        ai_report = generate_ai_insight(selected_coin, price, change_24h, vol, risk_score, signals)
        
        with st.container():
            st.subheader("🤖 AI Pilot Insight (Beta)")
            st.caption("Phân tích tổng hợp & Khuyến nghị hành động dựa trên dữ liệu thị trường:")
            
            # TL;DR Box
            st.info(ai_report['tldr'])
            
            # Deep Analysis & Conclusion
            col_ai1, col_ai2 = st.columns([2, 1])
            
            with col_ai1:
                st.markdown("### 🧠 Phân Tích Chi Tiết")
                st.markdown(ai_report['body'])
                
            with col_ai2:
                st.markdown("### 🏁 Kết Luận")
                st.success(ai_report['conclusion'])
                
        st.markdown("---")

        # ==================== ON-CHAIN & WHALES RADAR ====================

        # ==================== ON-CHAIN & WHALES RADAR ====================
        
        st.subheader("🕵️ On-Chain & Whales Radar")
        st.caption("Theo dõi dòng tiền thông minh và ví cá mập:")
        
        base_symbol = selected_coin.split('/')[0]
        
        col_link1, col_link2, col_link3, col_link4 = st.columns(4)
        
        with col_link1:
            st.link_button("🦈 Arkham (Soi Ví)", f"https://platform.arkhamintelligence.com/explorer/token/{base_symbol}", use_container_width=True)
        with col_link2:
            st.link_button("🔓 Token Unlocks", f"https://token.unlocks.app/{base_symbol.lower()}", use_container_width=True)
        with col_link3:
            st.link_button("🫧 Bubblemaps", f"https://app.bubblemaps.io/eth/token/{base_symbol.lower()}", use_container_width=True)
        with col_link4:
            st.link_button("📊 Coinglass (Data)", f"https://www.coinglass.com/currencies/{base_symbol}", use_container_width=True)
            
        st.markdown("---")
        
        # ==================== COMPREHENSIVE ANALYSIS ====================
        
        st.subheader("🎯 Phân Tích Toàn Diện")
        
        with st.spinner(f"Đang phân tích {selected_coin}..."):
            try:
                orchestrator = AlertOrchestrator()
                analysis = orchestrator.analyze_coin(selected_coin)
                
                if analysis.get('error'):
                    st.error(f"Lỗi khi phân tích: {analysis['error']}")
                else:
                    risk_score = analysis['risk_score']
                    severity = analysis['severity']
                    signals = analysis['signals']
                    recommendation = analysis['recommendation']
                    
                    # Risk Score Display
                    col_risk1, col_risk2 = st.columns([1, 3])
                    
                    with col_risk1:
                        # Risk score with color
                        if risk_score >= 80:
                            st.markdown(f"### 🔴 {risk_score}/100")
                            st.error("CRITICAL")
                        elif risk_score >= 60:
                            st.markdown(f"### 🟠 {risk_score}/100")
                            st.warning("WARNING")
                        elif risk_score >= 40:
                            st.markdown(f"### 🟡 {risk_score}/100")
                            st.info("CAUTION")
                        else:
                            st.markdown(f"### 🟢 {risk_score}/100")
                            st.success("NORMAL")
                    
                    with col_risk2:
                        # Progress bar
                        if risk_score >= 80:
                            st.progress(risk_score / 100, text=f"Risk Score: {risk_score}/100 - NGUY HIỂM CAO")
                        elif risk_score >= 60:
                            st.progress(risk_score / 100, text=f"Risk Score: {risk_score}/100 - CẢNH BÁO")
                        elif risk_score >= 40:
                            st.progress(risk_score / 100, text=f"Risk Score: {risk_score}/100 - THEO DÕI")
                        else:
                            st.progress(risk_score / 100, text=f"Risk Score: {risk_score}/100 - BÌNH THƯỜNG")
                    
                    st.markdown("---")
                    
                    # Detected Signals
                    if signals:
                        st.subheader("🔍 Tín Hiệu Phát Hiện")
                        
                        for i, signal in enumerate(signals, 1):
                            signal_type = signal['type']
                            signal_severity = signal['severity']
                            signal_message = signal['message']
                            signal_data = signal.get('data', {})
                            
                            # Color based on severity
                            if signal_severity == 'critical':
                                st.error(f"**{i}. {signal_type.upper().replace('_', ' ')}**")
                            elif signal_severity == 'warning':
                                st.warning(f"**{i}. {signal_type.upper().replace('_', ' ')}**")
                            else:
                                st.info(f"**{i}. {signal_type.upper().replace('_', ' ')}**")
                            
                            st.write(signal_message)
                            
                            # Show detailed data
                            if signal_data:
                                with st.expander("Chi tiết"):
                                    for key, value in signal_data.items():
                                        if isinstance(value, float):
                                            st.write(f"- **{key}**: {value:.2f}")
                                        else:
                                            st.write(f"- **{key}**: {value}")
                    else:
                        st.success("✅ Không phát hiện tín hiệu bất thường")
                    
                    st.markdown("---")
                    
                    # Recommendation
                    st.subheader("💡 Khuyến Nghị")
                    
                    if risk_score >= 80:
                        st.error(recommendation)
                    elif risk_score >= 60:
                        st.warning(recommendation)
                    elif risk_score >= 40:
                        st.info(recommendation)
                    else:
                        st.success(recommendation)
                    
            except Exception as e:
                st.error(f"Lỗi khi phân tích: {e}")
                import traceback
                st.code(traceback.format_exc())
        
        st.markdown("---")
        
        # ==================== POSITION HEALTH CHECK ====================
        
        st.subheader("🛡️ Position Health Check")
        
        user_position = st.radio("Vị thế của bạn:", ["Chưa có lệnh (Watching)", "Đang Short", "Đang Long"], horizontal=True)
        
        # Fetch OI data
        oi_data = fetch_oi_and_ratio(selected_coin)
        total_oi = oi_data['oi']
        long_ratio = oi_data['long_ratio']
        short_ratio = oi_data['short_ratio']
        
        # Display market overview
        st.markdown("**📊 Tổng Quan Thị Trường:**")
        col_oi1, col_oi2, col_oi3 = st.columns(3)
        with col_oi1:
            st.metric("Open Interest", f"${total_oi/1_000_000:.2f}M" if total_oi > 0 else "N/A")
        with col_oi2:
            st.metric("Long", f"{long_ratio*100:.1f}%", delta=f"{(long_ratio-0.5)*100:+.1f}%")
        with col_oi3:
            st.metric("Short", f"{short_ratio*100:.1f}%", delta=f"{(short_ratio-0.5)*100:+.1f}%")
        
        # MM Prediction
        if total_oi > 0:
            if short_ratio > 0.55:
                st.success(f"🎯 **Dự đoán MM:** Có xu hướng đẩy giá **TĂNG** để quét Short (vì Short chiếm {short_ratio*100:.0f}%)")
            elif long_ratio > 0.55:
                st.error(f"🎯 **Dự đoán MM:** Có xu hướng đẩy giá **GIẢM** để quét Long (vì Long chiếm {long_ratio*100:.0f}%)")
            else:
                st.info(f"🎯 **Dự đoán MM:** Thị trường cân bằng. Khó dự đoán xu hướng.")
        
        st.markdown("---")
        
        # Liquidation Analysis
        st.markdown("**⚡ Phân Tích Thanh Lý:**")
        
        base_symbol = selected_coin.split('/')[0]
        coinglass_url = f"https://www.coinglass.com/liquidation/{base_symbol}"
        st.link_button(f"🔎 Xem Heatmap trên Coinglass", coinglass_url)
        
        # Estimate liquidation levels
        liq_est = estimate_liquidation_volumes(price, total_oi, long_ratio, short_ratio)
        
        col_liq1, col_liq2 = st.columns(2)
        
        with col_liq1:
            st.markdown("**🔴 Phe Short (Bị thanh lý khi giá TĂNG):**")
            if liq_est:
                short_data = liq_est['short']
                st.write(f"- 💀 **x50:** ${short_data['x50']['price']:.4f} (Vol: ${short_data['x50']['volume']/1_000_000:.2f}M)")
                st.write(f"- 💀 **x20:** ${short_data['x20']['price']:.4f} (Vol: ${short_data['x20']['volume']/1_000_000:.2f}M)")
                st.write(f"- 💀 **x10:** ${short_data['x10']['price']:.4f} (Vol: ${short_data['x10']['volume']/1_000_000:.2f}M)")
            else:
                st.write(f"- 💀 **x50:** ${price * 1.02:.4f}")
                st.write(f"- 💀 **x20:** ${price * 1.05:.4f}")
                st.write(f"- 💀 **x10:** ${price * 1.10:.4f}")
        
        with col_liq2:
            st.markdown("**🟢 Phe Long (Bị thanh lý khi giá GIẢM):**")
            if liq_est:
                long_data = liq_est['long']
                st.write(f"- 🩸 **x50:** ${long_data['x50']['price']:.4f} (Vol: ${long_data['x50']['volume']/1_000_000:.2f}M)")
                st.write(f"- 🩸 **x20:** ${long_data['x20']['price']:.4f} (Vol: ${long_data['x20']['volume']/1_000_000:.2f}M)")
                st.write(f"- 🩸 **x10:** ${long_data['x10']['price']:.4f} (Vol: ${long_data['x10']['volume']/1_000_000:.2f}M)")
            else:
                st.write(f"- 🩸 **x50:** ${price * 0.98:.4f}")
                st.write(f"- 🩸 **x20:** ${price * 0.95:.4f}")
                st.write(f"- 🩸 **x10:** ${price * 0.90:.4f}")

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
