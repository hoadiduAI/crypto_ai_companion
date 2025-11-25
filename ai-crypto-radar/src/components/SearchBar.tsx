import React, { useState } from 'react';
import { Search } from 'lucide-react';

interface SearchBarProps {
    onSearch: (symbol: string) => void;
    isLoading: boolean;
}

export const SearchBar: React.FC<SearchBarProps> = ({ onSearch, isLoading }) => {
    const [input, setInput] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (input.trim()) {
            onSearch(input.trim());
        }
    };

    return (
        <form onSubmit={handleSubmit} className="w-full max-w-2xl mx-auto relative group">
            <div className="absolute inset-0 bg-gradient-to-r from-cyber-cyan to-cyber-purple rounded-lg blur opacity-25 group-hover:opacity-50 transition duration-500"></div>
            <div className="relative flex items-center bg-cyber-dark border border-cyber-cyan/30 rounded-lg p-1">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="ENTER TOKEN SYMBOL (e.g., BTC, ETH)..."
                    className="w-full bg-transparent text-white font-rajdhani text-xl px-4 py-3 focus:outline-none placeholder-gray-600 uppercase"
                    disabled={isLoading}
                />
                <button
                    type="submit"
                    disabled={isLoading}
                    className="bg-cyber-cyan/10 hover:bg-cyber-cyan/20 text-cyber-cyan p-3 rounded-md transition-all duration-300 border border-cyber-cyan/50 hover:shadow-[0_0_15px_#00f0ff]"
                >
                    <Search className="w-6 h-6" />
                </button>
            </div>
        </form>
    );
};
