import React from 'react';
import { TradeSetup } from '../types';
import { Target, Shield, MousePointerClick } from 'lucide-react';

interface TradeSetupCardProps {
    setup: TradeSetup;
}

export const TradeSetupCard: React.FC<TradeSetupCardProps> = ({ setup }) => {
    return (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
            {/* Entry */}
            <div className="bg-cyber-gray/50 border border-cyber-cyan/20 p-4 rounded-lg flex items-center gap-4">
                <div className="p-3 bg-blue-500/10 rounded-full">
                    <MousePointerClick className="w-6 h-6 text-blue-400" />
                </div>
                <div>
                    <p className="text-gray-400 text-xs font-mono uppercase">Entry Zone</p>
                    <p className="text-xl font-rajdhani font-bold text-white">{setup.entry}</p>
                </div>
            </div>

            {/* Target */}
            <div className="bg-cyber-gray/50 border border-cyber-green/20 p-4 rounded-lg flex items-center gap-4">
                <div className="p-3 bg-cyber-green/10 rounded-full">
                    <Target className="w-6 h-6 text-cyber-green" />
                </div>
                <div>
                    <p className="text-gray-400 text-xs font-mono uppercase">Target (TP)</p>
                    <p className="text-xl font-rajdhani font-bold text-cyber-green">{setup.target}</p>
                </div>
            </div>

            {/* Stop Loss */}
            <div className="bg-cyber-gray/50 border border-cyber-red/20 p-4 rounded-lg flex items-center gap-4">
                <div className="p-3 bg-cyber-red/10 rounded-full">
                    <Shield className="w-6 h-6 text-cyber-red" />
                </div>
                <div>
                    <p className="text-gray-400 text-xs font-mono uppercase">Stop Loss</p>
                    <p className="text-xl font-rajdhani font-bold text-cyber-red">{setup.stopLoss}</p>
                </div>
            </div>
        </div>
    );
};
