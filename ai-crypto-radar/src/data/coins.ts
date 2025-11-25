export interface Coin {
    symbol: string;
    name: string;
}

export const TOP_COINS: Coin[] = [
    { symbol: 'BTC', name: 'Bitcoin' },
    { symbol: 'ETH', name: 'Ethereum' },
    { symbol: 'SOL', name: 'Solana' },
    { symbol: 'BNB', name: 'Binance Coin' },
    { symbol: 'XRP', name: 'Ripple' },
    { symbol: 'ADA', name: 'Cardano' },
    { symbol: 'DOGE', name: 'Dogecoin' },
    { symbol: 'AVAX', name: 'Avalanche' },
    { symbol: 'DOT', name: 'Polkadot' },
    { symbol: 'LINK', name: 'Chainlink' },
    { symbol: 'MATIC', name: 'Polygon' },
    { symbol: 'UNI', name: 'Uniswap' },
    { symbol: 'LTC', name: 'Litecoin' },
    { symbol: 'ATOM', name: 'Cosmos' },
    { symbol: 'NEAR', name: 'Near Protocol' },
];
