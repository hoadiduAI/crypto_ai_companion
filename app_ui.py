import streamlit as st

def load_custom_css():
    st.markdown("""
        <style>
        /* IMPORT FONTS */
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;600;800&display=swap');

        :root {
            --radar-bg: #050505;
            --radar-panel: #111111;
            --radar-blue: #00f0ff;
            --radar-red: #ff003c;
            --radar-green: #00ff9d;
            --radar-text: #e0e0e0;
            --radar-gray: #333333;
        }

        /* GLOBAL STYLES */
        .stApp {
            background-color: var(--radar-bg);
            color: var(--radar-text);
            font-family: 'Inter', sans-serif;
        }
        
        h1, h2, h3 {
            font-family: 'Inter', sans-serif;
            font-weight: 800 !important;
            letter-spacing: -0.5px;
        }
        
        .font-mono {
            font-family: 'JetBrains Mono', monospace;
        }

        /* CUSTOM COMPONENTS */
        
        /* 1. HERO HEADER */
        .radar-header {
            text-align: center;
            padding: 2rem 0;
            margin-bottom: 2rem;
        }
        .radar-title {
            font-size: 3rem;
            font-weight: 900;
            background: linear-gradient(to right, #fff, #888);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }
        .radar-subtitle {
            color: #666;
            font-size: 1.1rem;
        }
        .radar-highlight {
            background: linear-gradient(to right, var(--radar-blue), #aa00ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* 2. CARDS */
        .radar-card {
            background-color: rgba(17, 17, 17, 0.6);
            border: 1px solid #222;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }
        .radar-card:hover {
            border-color: #444;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        }

        /* 3. SIGNAL BADGE */
        .signal-badge {
            display: inline-block;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-weight: 900;
            font-size: 1.2rem;
            letter-spacing: 1px;
            text-transform: uppercase;
        }
        .signal-long {
            background: rgba(0, 255, 157, 0.1);
            border: 1px solid var(--radar-green);
            color: var(--radar-green);
            box-shadow: 0 0 15px rgba(0, 255, 157, 0.2);
        }
        .signal-short {
            background: rgba(255, 0, 60, 0.1);
            border: 1px solid var(--radar-red);
            color: var(--radar-red);
            box-shadow: 0 0 15px rgba(255, 0, 60, 0.2);
        }
        .signal-neutral {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid #666;
            color: #aaa;
        }

        /* 4. TRADE SETUP GRID */
        .trade-setup-grid {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 10px;
            margin-top: 1rem;
        }
        .setup-box {
            background: #0a0a0a;
            border: 1px solid #222;
            border-radius: 8px;
            padding: 1rem;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        .setup-label {
            font-size: 0.7rem;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 0.3rem;
            font-family: 'JetBrains Mono', monospace;
        }
        .setup-value {
            font-size: 1.1rem;
            font-weight: 700;
            font-family: 'JetBrains Mono', monospace;
        }
        .val-entry { color: #fff; border-color: var(--radar-blue); }
        .val-target { color: var(--radar-green); border-color: var(--radar-green); }
        .val-stop { color: var(--radar-red); border-color: var(--radar-red); }

        /* 5. TL;DR BOX */
        .tldr-box {
            background: linear-gradient(90deg, rgba(0, 240, 255, 0.05), rgba(0,0,0,0));
            border-left: 4px solid var(--radar-blue);
            padding: 1rem;
            border-radius: 0 8px 8px 0;
            margin-bottom: 1.5rem;
        }
        .tldr-title {
            color: var(--radar-blue);
            font-weight: 800;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
        }
        .tldr-content {
            color: #ccc;
            line-height: 1.5;
        }

        /* 6. METRIC ROW */
        .metric-label {
            font-size: 0.8rem;
            color: #888;
            text-transform: uppercase;
        }
        .metric-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: #fff;
        }
        
        /* STREAMLIT OVERRIDES */
        div[data-testid="stMetricValue"] {
            font-family: 'JetBrains Mono', monospace !important;
        }
        div[data-testid="stExpander"] {
            background-color: #0a0a0a !important;
            border: 1px solid #222 !important;
        }
        </style>
    """, unsafe_allow_html=True)

def render_header():
    st.markdown("""
        <div class="radar-header">
            <div class="radar-title">RADAR <span class="radar-highlight">TÍN HIỆU</span> THỊ TRƯỜNG</div>
            <div class="radar-subtitle">Phân tích AI thời gian thực cho Trader (Binance Futures)</div>
        </div>
    """, unsafe_allow_html=True)

def render_signal_badge(signal_type, score):
    css_class = "signal-neutral"
    if signal_type == "LONG": css_class = "signal-long"
    elif signal_type == "SHORT": css_class = "signal-short"
    
    st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem;">
            <div class="signal-badge {css_class}">
                {signal_type}
            </div>
            <div style="font-family: 'JetBrains Mono'; color: #666;">
                CONFIDENCE: <span style="color: #fff; font-weight: bold;">{score}/100</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_trade_setup(entry, target, stoploss):
    st.markdown(f"""
        <div class="trade-setup-grid">
            <div class="setup-box" style="border-top: 2px solid var(--radar-blue);">
                <div class="setup-label">ENTRY ZONE</div>
                <div class="setup-value val-entry">{entry}</div>
            </div>
            <div class="setup-box" style="border-top: 2px solid var(--radar-green);">
                <div class="setup-label">TARGET (TP)</div>
                <div class="setup-value val-target">{target}</div>
            </div>
            <div class="setup-box" style="border-top: 2px solid var(--radar-red);">
                <div class="setup-label">STOP LOSS</div>
                <div class="setup-value val-stop">{stoploss}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_tldr(content):
    st.markdown(f"""
        <div class="tldr-box">
            <div class="tldr-title">⚡ TL;DR (Tóm Tắt)</div>
            <div class="tldr-content">{content}</div>
        </div>
    """, unsafe_allow_html=True)
