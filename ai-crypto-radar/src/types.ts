export enum SignalType {
    LONG = 'LONG',
    SHORT = 'SHORT',
    NEUTRAL = 'NEUTRAL',
    HOLD = 'HOLD',
}

export interface GroundingChunk {
    web?: {
        uri: string;
        title: string;
    };
}

export interface TradeSetup {
    entry: string;
    target: string;
    stopLoss: string;
}

export interface ManipulationMetrics {
    score: number;
    whaleConcentration: string;
    volumeStatus: string;
    volume24h: string;
    marketCap: string;
    orderBookHealth: string;
    verdict: string;
}

export interface LiquidationScenario {
    priceLevel: string;
    estimatedVolume: string;
    description: string;
}

export interface AnalysisData {
    coin: string;
    currentPrice: string;
    signal: SignalType;
    confidenceScore: number;
    riskLevel: string;
    tldr: string;
    tradeSetup: TradeSetup;
    manipulation: ManipulationMetrics;
    liquidationScenarios: {
        up: LiquidationScenario;
        down: LiquidationScenario;
    };
    summary: string;
    rawMarkdown: string;
    sources: GroundingChunk[];
}
