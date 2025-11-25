import { GoogleGenAI } from "@google/genai";
import { AnalysisData, SignalType, GroundingChunk } from '../types';

// Support both standard process.env (Node/Webpack) and import.meta.env (Vite)
const apiKey = process.env.API_KEY || (import.meta as any).env?.VITE_GEMINI_API_KEY || '';

// If no key is found, we might want to throw or handle it, but for now allow empty 
// (which will fail at call time) or rely on the frontend check.
const ai = new GoogleGenAI({ apiKey });

// Helper to extract value using Regex safely
const extractValue = (text: string, label: string, defaultValue: string = "N/A"): string => {
    const regex = new RegExp(`${label}:\\s*(.*)`, 'i');
    const match = text.match(regex);
    return match ? match[1].trim() : defaultValue;
};

const parseAnalysisResponse = (text: string, coin: string, sources: GroundingChunk[]): AnalysisData => {
    let signal = SignalType.NEUTRAL;
    let confidenceScore = 50;

    // Extract Signal
    const signalMatch = text.match(/SIGNAL:\s*(LONG|SHORT|NEUTRAL|HOLD)/i);
    if (signalMatch) {
        const rawSignal = signalMatch[1].toUpperCase();
        if (rawSignal === 'LONG') signal = SignalType.LONG;
        else if (rawSignal === 'SHORT') signal = SignalType.SHORT;
        else if (rawSignal === 'HOLD') signal = SignalType.HOLD;
    }

    // Extract Confidence
    const scoreMatch = text.match(/CONFIDENCE:\s*(\d+)/i);
    if (scoreMatch) {
        confidenceScore = parseInt(scoreMatch[1], 10);
    }

    // Extract Trade Setup
    const entry = extractValue(text, "ENTRY_ZONE");
    const target = extractValue(text, "TARGET_PRICE");
    const stopLoss = extractValue(text, "STOP_LOSS");
    const riskLevel = extractValue(text, "RISK_LEVEL");
    const currentPrice = extractValue(text, "CURRENT_PRICE", "---");

    // Extract Manipulation & Market Data
    const manipScoreMatch = text.match(/MANIPULATION_SCORE:\s*(\d+)/i);
    const manipulationScore = manipScoreMatch ? parseInt(manipScoreMatch[1], 10) : 0;

    const whaleConc = extractValue(text, "WHALE_CONCENTRATION");
    const volStatus = extractValue(text, "VOLUME_ANALYSIS");
    const vol24h = extractValue(text, "24H_VOLUME");
    const mcap = extractValue(text, "MARKET_CAP");
    const obHealth = extractValue(text, "ORDER_BOOK_HEALTH");
    const manipVerdict = extractValue(text, "MANIPULATION_VERDICT");

    // Extract Liquidation Scenarios (New Logic)
    // Format expected: LIQ_UP: 68000 | 500M
    const liqUpRaw = extractValue(text, "LIQ_UP", "---|---");
    const liqDownRaw = extractValue(text, "LIQ_DOWN", "---|---");

    const [upPrice, upVol] = liqUpRaw.split('|').map(s => s.trim());
    const [downPrice, downVol] = liqDownRaw.split('|').map(s => s.trim());

    // Extract TL;DR (Handle multi-line)
    const tldrMatch = text.match(/TL;DR:([\s\S]*?)---/);
    const tldr = tldrMatch ? tldrMatch[1].trim() : "Đang cập nhật phân tích nhanh...";

    return {
        coin,
        currentPrice,
        signal,
        confidenceScore,
        riskLevel,
        tldr,
        tradeSetup: {
            entry,
            target,
            stopLoss
        },
        manipulation: {
            score: manipulationScore,
            whaleConcentration: whaleConc,
            volumeStatus: volStatus,
            volume24h: vol24h,
            marketCap: mcap,
            orderBookHealth: obHealth,
            verdict: manipVerdict
        },
        liquidationScenarios: {
            up: {
                priceLevel: upPrice || "N/A",
                estimatedVolume: upVol || "N/A",
                description: "Short Squeeze (Quét Short)"
            },
            down: {
                priceLevel: downPrice || "N/A",
                estimatedVolume: downVol || "N/A",
                description: "Long Squeeze (Quét Long)"
            }
        },
        summary: "Analysis complete.",
        rawMarkdown: text,
        sources,
    };
};

export const analyzeCryptoToken = async (coinSymbol: string): Promise<AnalysisData> => {
    if (!apiKey) {
        throw new Error("API Key is missing");
    }

    const modelId = "gemini-2.5-flash";

    const prompt = `
    Đóng vai trò là Market Maker & Chuyên gia On-chain. Phân tích đồng "${coinSymbol}".

    CẤU TRÚC DỮ LIỆU BẮT BUỘC (Header format):
    Giữ nguyên từ khóa tiếng Anh (KEY: Value).
    
    SIGNAL: [LONG or SHORT or NEUTRAL or HOLD]
    CONFIDENCE: [0-100]
    RISK_LEVEL: [LOW or MEDIUM or HIGH]
    CURRENT_PRICE: [Giá hiện tại, vd: $65,000]
    ENTRY_ZONE: [Vùng vào lệnh]
    TARGET_PRICE: [TP]
    STOP_LOSS: [SL]
    
    MARKET_DATA:
    24H_VOLUME: [Số cụ thể, vd: $1.2B]
    MARKET_CAP: [Số cụ thể, vd: $500M]
    
    MANIPULATION_METRICS:
    MANIPULATION_SCORE: [0-100]
    WHALE_CONCENTRATION: [Nhận xét ngắn về Top holders]
    VOLUME_ANALYSIS: [Nhận xét Volume so với Cap]
    ORDER_BOOK_HEALTH: [Độ dày thanh khoản]
    MANIPULATION_VERDICT: [Kết luận rủi ro]

    LIQUIDATION_SCENARIOS (Ước tính các vùng thanh lý lớn):
    Dựa trên kháng cự/hỗ trợ, hãy ước tính:
    LIQ_UP: [Giá Kháng cự trên] | [Ước tính Volume Short bị thanh lý nến giá chạm mức này, vd: $50M]
    LIQ_DOWN: [Giá Hỗ trợ dưới] | [Ước tính Volume Long bị thanh lý nếu giá chạm mức này, vd: $100M]

    TL;DR:
    [Tóm tắt 2-3 câu quan trọng nhất bằng Tiếng Việt]
    ---

    PHẦN BÁO CÁO CHI TIẾT (Markdown Tiếng Việt):
    
    ### 1. Phân Tích Kịch Bản Thanh Lý (Heatmap Logic)
    *   **Kịch bản 1 (Giá tăng lên [Giá Up]):** Sẽ kích hoạt thanh lý bao nhiêu Short? Tại sao MM muốn đẩy lên đây?
    *   **Kịch bản 2 (Giá giảm xuống [Giá Down]):** Sẽ kích hoạt thanh lý bao nhiêu Long?

    ### 2. Tokenomics & Vesting
    ...

    ### 3. Dữ liệu On-chain (BẮT BUỘC 2 BẢNG)
    ...

    ### 4. Kết Luận & Khuyến nghị
  `;

    try {
        const response = await ai.models.generateContent({
            model: modelId,
            contents: prompt,
            config: {
                tools: [{ googleSearch: {} }],
                temperature: 0.3
            },
        });

        const text = response.text || "Không thể tạo phân tích.";

        const groundingChunks = response.candidates?.[0]?.groundingMetadata?.groundingChunks || [];
        const sources: GroundingChunk[] = groundingChunks.map((chunk: any) => ({
            web: chunk.web ? { uri: chunk.web.uri, title: chunk.web.title } : undefined
        })).filter((c: any) => c.web !== undefined);

        return parseAnalysisResponse(text, coinSymbol, sources);

    } catch (error) {
        console.error("Gemini Analysis Failed:", error);
        throw error;
    }
};
