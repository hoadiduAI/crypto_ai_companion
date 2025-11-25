import React from 'react';
import { Radar } from 'lucide-react';

export const Header: React.FC = () => {
    return (
        <header className="w-full py-6 px-8 flex justify-between items-center border-b border-white/5 bg-black/20 backdrop-blur-sm sticky top-0 z-50">
            <div className="flex items-center gap-3">
                <Radar className="w-8 h-8 text-cyber-cyan animate-spin-slow" />
                <h1 className="text-2xl font-rajdhani font-bold tracking-wider text-white">
                    AI <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyber-cyan to-cyber-purple">CRYPTO RADAR</span>
                </h1>
            </div>
            <div className="flex gap-6 text-sm font-rajdhani font-semibold text-gray-400">
                <span className="hover:text-cyber-cyan cursor-pointer transition">MARKET SCAN</span>
                <span className="hover:text-cyber-cyan cursor-pointer transition">SIGNALS</span>
                <span className="px-2 py-0.5 border border-cyber-cyan text-cyber-cyan rounded text-xs">BETA v2.0</span>
            </div>
        </header>
    );
};
