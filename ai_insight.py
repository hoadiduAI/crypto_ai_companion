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
        analysis_points.append(f"- **Dòng tiền:** Rất mạnh (**${volume/1_000_000:.1f}M** > $100M). Cá mập đang hoạt động tích cực.")
    elif volume < 5_000_000:
        analysis_points.append(f"- **Thanh khoản:** Kém (**${volume/1_000_000:.1f}M** < $5M). Rủi ro trượt giá (slippage) cao.")
    else:
        analysis_points.append(f"- **Volume:** Ổn định (**${volume/1_000_000:.1f}M**), đủ thanh khoản để trade ngắn hạn.")
        
    # Volatility Analysis
    if is_volatile:
        analysis_points.append(f"- **Biến động:** Rất mạnh (**{abs(change_24h):.1f}%** trong 24h). Cơ hội lớn đi kèm rủi ro cháy tài khoản cao.")
    else:
        analysis_points.append(f"- **Biến động:** Thấp (**{abs(change_24h):.1f}%**). Thị trường đang tích lũy.")
    
    # Signal Specifics
    if is_ghost_town:
        analysis_points.append("- **Cấu trúc lệnh:** Phát hiện tín hiệu **Ghost Town** (Giá tăng nhưng Volume giảm). Dấu hiệu thao túng.")
    if is_fake_pump:
        analysis_points.append("- **Bất thường:** Phát hiện **Fake Pump** (Giá đẩy ảo không có volume hỗ trợ).")
    
    analysis_body = "\n".join(analysis_points)
    
    # 4. Generate Conclusion (The "Action")
    if is_high_risk:
        conclusion = f"🛑 **Khuyến nghị:** Rủi ro quá cao (**Risk Score: {risk_score}/100**). Tránh FOMO, bảo toàn vốn là ưu tiên."
    elif is_safe and not is_dump:
        conclusion = f"✅ **Khuyến nghị:** An toàn (**Risk Score: {risk_score}/100**). Có thể tìm điểm vào Long (Scalp) nếu giữ được hỗ trợ."
    elif is_dump:
        conclusion = f"👀 **Khuyến nghị:** Đang xả mạnh (**-{abs(change_24h):.1f}%**). Đừng bắt dao rơi, chờ sideway."
    else:
        conclusion = "👀 **Khuyến nghị:** Thị trường chưa rõ xu hướng. Kiên nhẫn chờ đợi tín hiệu xác nhận."

    return {
        "tldr": tldr,
        "body": analysis_body,
        "conclusion": conclusion
    }
