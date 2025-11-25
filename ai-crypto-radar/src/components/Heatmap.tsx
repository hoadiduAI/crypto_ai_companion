import React from 'react';

export const Heatmap: React.FC = () => {
    return (
        <div className="mt-8 p-6 bg-cyber-dark/50 border border-gray-800 rounded-xl">
            <h3 className="text-cyber-cyan font-rajdhani font-bold text-lg mb-4 flex items-center gap-2">
                <span className="w-2 h-2 bg-cyber-cyan rounded-full animate-pulse"></span>
                LIQUIDATION HEATMAP SIMULATION
            </h3>

            <div className="relative h-48 w-full bg-gray-900 rounded-lg overflow-hidden flex flex-col">
                {/* Short Liquidation Zone (Red) */}
                <div className="flex-1 bg-gradient-to-b from-cyber-red/40 to-transparent w-full flex items-start justify-center pt-2">
                    <span className="text-xs text-cyber-red font-mono bg-black/50 px-2 rounded">SHORT LIQ ZONE</span>
                </div>

                {/* Price Line */}
                <div className="h-0.5 w-full bg-white shadow-[0_0_10px_white] z-10 flex items-center justify-end px-2">
                    <span className="text-[10px] bg-white text-black px-1 font-bold">CURRENT PRICE</span>
                </div>

                {/* Long Liquidation Zone (Green/Cyan) */}
                <div className="flex-1 bg-gradient-to-t from-cyber-cyan/40 to-transparent w-full flex items-end justify-center pb-2">
                    <span className="text-xs text-cyber-cyan font-mono bg-black/50 px-2 rounded">LONG LIQ ZONE</span>
                </div>
            </div>
            <p className="text-gray-500 text-xs mt-2 text-center font-mono">
                *Visual simulation based on estimated leverage clusters.
            </p>
        </div>
    );
};
