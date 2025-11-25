import React from 'react';
import { AnalysisData } from '../types';
import { SignalBadge } from './SignalBadge';
import { TradeSetupCard } from './TradeSetupCard';
import { Heatmap } from './Heatmap';
import { AlertTriangle, Activity, Database } from 'lucide-react';

interface AnalysisDashboardProps {
    data: AnalysisData;
}

export const AnalysisDashboard: React.FC<AnalysisDashboardProps> = ({ data }) => {
    return (
        <div className="w-full max-w-4xl mx-auto mt-12 animate-fade-in">
            <div className="flex items-center justify-between mb-6">
                <h2 className="text-3xl font-rajdhani font-bold text-white">
                    ANALYSIS RESULT: <span className="text-cyber-cyan">{data.symbol}</span>
                </h2>
                <span className="px-3 py-1 bg-cyber-gray border border-cyber-cyan/30 text-cyber-cyan text-xs font-mono rounded">
                    LIVE DATA
                </span>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Left Column: Signal & Setup */}
                <div className="lg:col-span-2 space-y-6">
                    <SignalBadge signal={data.signal} confidence={data.confidence} />
                    <TradeSetupCard setup={data.tradeSetup} />

                    <div className="bg-cyber-gray/30 p-6 rounded-xl border border-gray-800">
                        <h3 className="text-white font-rajdhani font-bold mb-2">AI Reasoning</h3>
                        <p className="text-gray-400 font-outfit text-sm leading-relaxed">
                            {data.reasoning}
                        </p>
                    </div>
                </div>

                {/* Right Column: Risk & Heatmap */}
                <div className="space-y-6">
                    {/* Risk Radar */}
                    <div className="bg-cyber-gray/30 p-5 rounded-xl border border-gray-800">
                        <h3 className="text-white font-rajdhani font-bold mb-4 flex items-center gap-2">
                            <AlertTriangle className="w-4 h-4 text-yellow-500" />
                            RISK RADAR
                        </h3>
                        <div className="space-y-3">
                            <div className="flex justify-between items-center text-sm">
                                <span className="text-gray-400">Whale Conc.</span>
                                <span className={`font-mono ${data.riskAnalysis.whaleConcentration === 'High' ? 'text-cyber-red' : 'text-cyber-green'}`}>
                                    {data.riskAnalysis.whaleConcentration}
                                </span>
                            </div>
                            <div className="flex justify-between items-center text-sm">
                                <span className="text-gray-400">Vol Anomaly</span>
                                <span className={`font-mono ${data.riskAnalysis.volumeAnomaly ? 'text-cyber-red' : 'text-cyber-green'}`}>
                                    {data.riskAnalysis.volumeAnomaly ? 'DETECTED' : 'NORMAL'}
                                </span>
                            </div>
                            <div className="flex justify-between items-center text-sm">
                                <span className="text-gray-400">Order Book</span>
                                <span className="text-cyber-cyan font-mono">{data.riskAnalysis.orderBookHealth}</span>
                            </div>
                        </div>
                    </div>

                    <Heatmap />
                </div>
            </div>
        </div>
    );
};
