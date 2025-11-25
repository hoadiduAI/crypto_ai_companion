import React from 'react';
import { ArrowUpCircle, ArrowDownCircle, MinusCircle } from 'lucide-react';

interface SignalBadgeProps {
    signal: 'LONG' | 'SHORT' | 'NEUTRAL';
    confidence: number;
}

export const SignalBadge: React.FC<SignalBadgeProps> = ({ signal, confidence }) => {
    const styles = {
        LONG: { color: 'text-cyber-green', border: 'border-cyber-green', shadow: 'shadow-cyber-green/50', icon: ArrowUpCircle },
        SHORT: { color: 'text-cyber-red', border: 'border-cyber-red', shadow: 'shadow-cyber-red/50', icon: ArrowDownCircle },
        NEUTRAL: { color: 'text-gray-400', border: 'border-gray-400', shadow: 'shadow-gray-400/50', icon: MinusCircle },
    };

    const style = styles[signal];
    const Icon = style.icon;

    return (
        <div className={`flex flex-col items-center justify-center p-6 border-2 ${style.border} rounded-xl bg-cyber-dark/80 backdrop-blur-md shadow-[0_0_30px_rgba(0,0,0,0.5)] ${style.shadow}`}>
            <div className="flex items-center gap-3 mb-2">
                <Icon className={`w-10 h-10 ${style.color} animate-pulse`} />
                <h2 className={`text-4xl font-rajdhani font-bold ${style.color} tracking-wider`}>
                    {signal}
                </h2>
            </div>
            <div className="w-full bg-gray-800 rounded-full h-2.5 mt-2">
                <div
                    className={`h-2.5 rounded-full ${signal === 'LONG' ? 'bg-cyber-green' : signal === 'SHORT' ? 'bg-cyber-red' : 'bg-gray-400'}`}
                    style={{ width: `${confidence}%` }}
                ></div>
            </div>
            <p className="text-gray-400 font-mono text-sm mt-2">AI Confidence: {confidence}%</p>
        </div>
    );
};
