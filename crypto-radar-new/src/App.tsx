import React, { useState, useEffect, useRef } from 'react';
import './index.css'; // Import Tailwind CSS
import { Header } from './components/Header';
import { IconSearch } from './components/Icons';
import { analyzeCryptoToken } from './services/geminiService';
import { AnalysisData } from './types';
import { RadarLoader } from './components/RadarLoader';
import { AnalysisDashboard } from './components/AnalysisDashboard';
import { TOP_COINS, Coin } from './data/coins';

const App: React.FC = () => {
  const [searchInput, setSearchInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [analysisData, setAnalysisData] = useState<AnalysisData | null>(null);

  // Autocomplete state
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [filteredCoins, setFilteredCoins] = useState<Coin[]>([]);
  const searchContainerRef = useRef<HTMLDivElement>(null);

  // Close suggestions when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (searchContainerRef.current && !searchContainerRef.current.contains(event.target as Node)) {
        setShowSuggestions(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Filter coins when input changes
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setSearchInput(value);

    if (value.trim().length > 0) {
      const lowerValue = value.toLowerCase();
      const filtered = TOP_COINS.filter(coin =>
        coin.symbol.toLowerCase().includes(lowerValue) ||
        coin.name.toLowerCase().includes(lowerValue)
      ).slice(0, 8); // Limit to 8 suggestions
      setFilteredCoins(filtered);
      setShowSuggestions(true);
    } else {
      setShowSuggestions(false);
    }
  };

  const handleSelectCoin = (coin: Coin) => {
    setSearchInput(coin.symbol);
    setShowSuggestions(false);
    // Optional: Auto trigger search here if desired
    // handleSearch(null, coin.symbol);
  };

  const handleSearch = async (e: React.FormEvent | null, specificSymbol?: string) => {
    if (e) e.preventDefault();
    const query = specificSymbol || searchInput;
    if (!query.trim()) return;

    setLoading(true);
    setError(null);
    setAnalysisData(null);
    setShowSuggestions(false);

    try {
      const data = await analyzeCryptoToken(query);
      setAnalysisData(data);
    } catch (err: any) {
      setError("Không thể phân tích token. Vui lòng kiểm tra mã hoặc kết nối API.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  // Check for API Key in either standard process.env or Vite's import.meta.env
  // Note: import.meta.env is cleaner for Vite, but process.env shim is added in vite.config.ts for compatibility
  const hasApiKey = !!(process.env.API_KEY || (import.meta as any).env?.VITE_GEMINI_API_KEY);

  return (
    <div className="min-h-screen bg-radar-black bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-900 via-black to-black text-radar-text font-body selection:bg-radar-blue selection:text-black">
      <Header />

      <main className="max-w-4xl mx-auto px-4 sm:px-6 py-12">

        {/* Hero Section */}
        <div className="text-center mb-12 space-y-4">
          <h2 className="text-4xl md:text-5xl font-display font-bold text-white tracking-tight">
            RADAR <span className="text-transparent bg-clip-text bg-gradient-to-r from-radar-blue to-purple-500">TÍN HIỆU</span> THỊ TRƯỜNG
          </h2>
          <p className="text-lg text-gray-400 max-w-2xl mx-auto">
            Phân tích AI thời gian thực cho Trader. Nhập mã coin để nhận tín hiệu Long/Short dựa trên tin tức và tâm lý thị trường mới nhất.
          </p>
        </div>

        {/* Search Bar Container */}
        <div className="relative max-w-2xl mx-auto mb-16 z-20" ref={searchContainerRef}>
          <div className="absolute -inset-1 bg-gradient-to-r from-radar-blue to-radar-red rounded-lg blur opacity-25 hover:opacity-50 transition duration-1000"></div>

          <form onSubmit={(e) => handleSearch(e)} className="relative flex items-center bg-radar-panel rounded-lg border border-gray-800 p-2 shadow-2xl">
            <IconSearch />
            <input
              type="text"
              value={searchInput}
              onChange={handleInputChange}
              onFocus={() => searchInput.trim().length > 0 && setShowSuggestions(true)}
              placeholder="NHẬP MÃ CẶP (VD: BTC, ETH)..."
              className="flex-1 bg-transparent border-none outline-none text-white text-lg px-4 font-display uppercase placeholder-gray-600"
              disabled={loading || !hasApiKey}
              autoComplete="off"
            />
            <button
              type="submit"
              disabled={loading || !searchInput || !hasApiKey}
              className="bg-radar-blue hover:bg-cyan-400 text-black font-bold py-2 px-6 rounded transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed font-display tracking-wide"
            >
              {loading ? 'ĐANG QUÉT' : 'PHÂN TÍCH'}
            </button>
          </form>

          {!hasApiKey && (
            <p className="text-radar-red text-center mt-4 text-sm font-bold">
              THIẾU API KEY. VUI LÒNG CẤU HÌNH API_KEY
            </p>
          )}

          {/* Autocomplete Dropdown */}
          {showSuggestions && filteredCoins.length > 0 && (
            <div className="absolute top-full left-0 right-0 mt-2 bg-radar-panel border border-radar-blue/30 rounded-lg shadow-xl overflow-hidden animate-fade-in max-h-64 overflow-y-auto custom-scrollbar">
              {filteredCoins.map((coin, index) => (
                <div
                  key={index}
                  onClick={() => handleSelectCoin(coin)}
                  className="flex items-center justify-between px-4 py-3 hover:bg-radar-blue/10 cursor-pointer border-b border-gray-800 last:border-none transition-colors group"
                >
                  <div className="flex flex-col">
                    <span className="font-display font-bold text-white group-hover:text-radar-blue transition-colors">
                      {coin.symbol}/USDT
                    </span>
                    <span className="text-xs text-gray-500 font-body uppercase tracking-wider">
                      {coin.name}
                    </span>
                  </div>
                  <span className="text-gray-600 text-xs group-hover:text-radar-blue opacity-0 group-hover:opacity-100 transition-all">
                    CHỌN ↵
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Content Area */}
        <div className="min-h-[400px]">
          {loading && <RadarLoader />}

          {error && (
            <div className="bg-red-900/20 border border-red-500/50 text-red-200 p-6 rounded-xl text-center animate-pulse">
              <p className="font-bold font-display text-lg mb-2">LỖI QUÉT DỮ LIỆU</p>
              <p>{error}</p>
            </div>
          )}

          {analysisData && !loading && (
            <AnalysisDashboard data={analysisData} />
          )}

          {!analysisData && !loading && !error && (
            <div className="text-center opacity-30 mt-20">
              <div className="grid grid-cols-3 gap-4 max-w-lg mx-auto">
                <div className="h-32 border border-dashed border-gray-600 rounded-lg flex items-center justify-center font-display text-gray-500">CHỜ NHẬP LIỆU</div>
                <div className="h-32 border border-dashed border-gray-600 rounded-lg flex items-center justify-center font-display text-gray-500">TIN TỨC LIVE</div>
                <div className="h-32 border border-dashed border-gray-600 rounded-lg flex items-center justify-center font-display text-gray-500">HÀNH ĐỘNG GIÁ</div>
              </div>
            </div>
          )}
        </div>
      </main>

      <footer className="border-t border-gray-900 py-8 mt-12 bg-black">
        <div className="max-w-7xl mx-auto px-4 text-center">
          <p className="text-gray-600 text-sm mb-2">
            AI Crypto Radar sử dụng Gemini 2.5 Flash kết hợp Google Search Grounding.
          </p>
          <p className="text-xs text-gray-700">
            MIỄN TRỪ TRÁCH NHIỆM: Công cụ này chỉ mang tính chất tham khảo và giải trí.
            AI có thể đưa ra thông tin sai lệch (hallucinate). Đây KHÔNG phải lời khuyên đầu tư. Hãy luôn tự nghiên cứu (DYOR).
          </p>
        </div>
      </footer>
    </div>
  );
};

export default App;
