import React from 'react';

export const RadarLoader: React.FC = () => {
    return (
        <div className="flex flex-col items-center justify-center py-12">
            <div className="relative w-32 h-32">
                {/* Outer Ring */}
                <div className="absolute inset-0 border-4 border-cyber-gray rounded-full"></div>

                {/* Scanning Line */}
                <div className="absolute inset-0 rounded-full animate-radar-spin border-t-4 border-cyber-cyan shadow-[0_0_20px_#00f0ff]"></div>

                {/* Inner Dot */}
                <div className="absolute top-1/2 left-1/2 w-4 h-4 bg-cyber-cyan rounded-full transform -translate-x-1/2 -translate-y-1/2 animate-pulse"></div>

                {/* Grid Background (Optional) */}
                <div className="absolute inset-0 rounded-full bg-[radial-gradient(circle,transparent_20%,#00f0ff_20%,transparent_21%)] opacity-20"></div>
            </div>
            <p className="mt-6 text-cyber-cyan font-rajdhani text-xl tracking-widest animate-pulse">
                SCANNING MARKET DATA...
            </p>
        </div>
    );
};
