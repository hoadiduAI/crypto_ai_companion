import random

def generate_ai_insight(symbol, price, change_24h, volume, risk_score, signals):
    """
    Simulates an AI Analyst generating a report based on market data.
    Returns a dictionary with 'tldr' and 'conclusion'.
    """
    
    # 1. Analyze Context
    is_pump = change_24h > 5
    is_dump = change_24h < -5
    is_volatile = abs(change_24h) > 10
    is_ghost_town = any(s['type'] == 'ghost_town' for s in signals)
    is_fake_pump = any(s['type'] == 'fake_pump' for s in signals)
    is_high_risk = risk_score >= 70
    is_safe = risk_score < 30
    
    # 2. Generate TL;DR (The "Hook")
    tldr_templates = []
    
    if is_ghost_town:
        tldr_templates.append(f"⚠️ **Cảnh báo Ghost Town:** {symbol} đang trong trạng thái 'Thị trấn ma'. Giá cao nhưng Volume thực rất thấp. Đây thường là bẫy thanh khoản để dụ Fomo.")
    elif is_fake_pump:
        tldr_templates.append(f"🚨 **Báo động Fake Pump:** {symbol} tăng giá {change_24h:.1f}% nhưng không đi kèm Volume tương xứng. Khả năng cao là bẫy Bull Trap của Market Maker.")
    elif is_high_risk:
        tldr_templates.append(f"🔴 **Rủi ro Cao ({risk_score}/100):** Dữ liệu On-chain và biến động giá cho thấy {symbol} đang cực kỳ bất ổn. Không dành cho người yếu tim.")
    elif is_pump:
        tldr_templates.append(f"🚀 **Đà tăng mạnh:** {symbol} đang thu hút dòng tiền tốt (+{change_24h:.1f}%). Tuy nhiên cần chú ý các vùng kháng cự sắp tới.")
    elif is_dump:
        tldr_templates.append(f"📉 **Áp lực bán tháo:** {symbol} đang bị xả mạnh (-{abs(change_24h):.1f}%). Chưa thấy dấu hiệu bắt đáy rõ ràng.")
    else:
        tldr_templates.append(f"⚖️ **Thị trường Sideway:** {symbol} đang đi ngang với biên độ hẹp. Market Maker có vẻ đang gom hàng hoặc chờ tin tức mới.")
        
    tldr = tldr_templates[0]
    
    # 3. Generate Deep Analysis (The "Body")
    analysis_points = []
    
    # Volume Analysis
    if volume > 100_000_000:
        analysis_points.append(f"- **Dòng tiền:** Rất mạnh (${volume/1_000_000:.1f}M). Cá mập đang hoạt động tích cực.")
    elif volume < 5_000_000:
        analysis_points.append(f"- **Thanh khoản:** Kém (${volume/1_000_000:.1f}M). Cẩn thận trượt giá (slippage) khi vào lệnh lớn.")
    else:
        analysis_points.append(f"- **Volume:** Ổn định ở mức ${volume/1_000_000:.1f}M, đủ để trade ngắn hạn.")
        
    # Volatility Analysis
    if is_volatile:
        analysis_points.append(f"- **Biến động:** Biên độ dao động lớn, cơ hội cao nhưng rủi ro cháy tài khoản cũng lớn.")
    
    # Signal Specifics
    if is_ghost_town:
        analysis_points.append("- **Cấu trúc lệnh:** Order book mỏng, dễ bị thao túng giá chỉ với volume nhỏ.")
    
    analysis_body = "\n".join(analysis_points)
    
    # 4. Generate Conclusion (The "Action")
    if is_high_risk:
        conclusion = "🛑 **Khuyến nghị:** Tránh FOMO lúc này. Nếu đang có lãi hãy chốt lời từng phần. Tuyệt đối không DCA (trung bình giá) khi chưa có tín hiệu đảo chiều rõ ràng."
    elif is_safe and not is_dump:
        conclusion = "✅ **Khuyến nghị:** Có thể cân nhắc vị thế Long ngắn hạn (Scalp) nếu giữ được vùng hỗ trợ hiện tại. Stoploss chặt chẽ."
    elif is_dump:
        conclusion = "👀 **Khuyến nghị:** Quan sát thêm. Đừng vội 'bắt dao rơi'. Chờ giá ổn định (sideway) ít nhất 4-6 nến H1 nữa."
    else:
        conclusion = "👀 **Khuyến nghị:** Kiên nhẫn chờ đợi. Thị trường chưa rõ xu hướng. Bảo toàn vốn là ưu tiên hàng đầu."

    return {
        "tldr": tldr,
        "body": analysis_body,
        "conclusion": conclusion
    }
