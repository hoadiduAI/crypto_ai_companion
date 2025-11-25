/**
 * Token Address Mapping Database
 * Maps Binance Futures symbols to blockchain token contract addresses
 * 
 * Usage:
 * const btcAddress = TOKEN_MAPPING['BTC'].chains['ETH'].address;
 */

const TOKEN_MAPPING = {
    'BTC': {
        name: 'Bitcoin',
        chains: {
            'ETH': {
                address: '0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599',
                symbol: 'WBTC',
                decimals: 8
            },
            'BSC': {
                address: '0x7130d2A12B9BCbFAe4f2634d864A1Ee1Ce3Ead9c',
                symbol: 'BTCB',
                decimals: 18
            }
        }
    },
    'ETH': {
        name: 'Ethereum',
        chains: {
            'ETH': {
                address: '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2',
                symbol: 'WETH',
                decimals: 18
            },
            'BSC': {
                address: '0x2170Ed0880ac9A755fd29B2688956BD959F933F8',
                symbol: 'ETH',
                decimals: 18
            }
        }
    },
    'BNB': {
        name: 'BNB',
        chains: {
            'BSC': {
                address: '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c',
                symbol: 'WBNB',
                decimals: 18
            },
            'ETH': {
                address: '0xB8c77482e45F1F44dE1745F52C74426C631bDD52',
                symbol: 'BNB',
                decimals: 18
            }
        }
    },
    'SOL': {
        name: 'Solana',
        chains: {
            'ETH': {
                address: '0xD31a59c85aE9D8edEFeC411D448f90841571b89c',
                symbol: 'SOL',
                decimals: 9
            },
            'BSC': {
                address: '0x570A5D26f7765Ecb712C0924E4De545B89fD43dF',
                symbol: 'SOL',
                decimals: 18
            }
        }
    },
    'XRP': {
        name: 'Ripple',
        chains: {
            'ETH': {
                address: '0x1d2F0da169ceB9fC7B3144628dB156f3F6c60dBE',
                symbol: 'XRP',
                decimals: 18
            },
            'BSC': {
                address: '0x1D2F0da169ceB9fC7B3144628dB156f3F6c60dBE',
                symbol: 'XRP',
                decimals: 18
            }
        }
    },
    'ADA': {
        name: 'Cardano',
        chains: {
            'ETH': {
                address: '0x3EE2200Efb3400fAbB9AacF31297cBdD1d435D47',
                symbol: 'ADA',
                decimals: 18
            },
            'BSC': {
                address: '0x3EE2200Efb3400fAbB9AacF31297cBdD1d435D47',
                symbol: 'ADA',
                decimals: 18
            }
        }
    },
    'DOGE': {
        name: 'Dogecoin',
        chains: {
            'ETH': {
                address: '0x4206931337dc273a630d328dA6441786BfaD668f',
                symbol: 'DOGE',
                decimals: 8
            },
            'BSC': {
                address: '0xbA2aE424d960c26247Dd6c32edC70B295c744C43',
                symbol: 'DOGE',
                decimals: 8
            }
        }
    },
    'MATIC': {
        name: 'Polygon',
        chains: {
            'ETH': {
                address: '0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0',
                symbol: 'MATIC',
                decimals: 18
            },
            'BSC': {
                address: '0xCC42724C6683B7E57334c4E856f4c9965ED682bD',
                symbol: 'MATIC',
                decimals: 18
            }
        }
    },
    'DOT': {
        name: 'Polkadot',
        chains: {
            'ETH': {
                address: '0x7083609fCE4d1d8Dc0C979AAb8c869Ea2C873402',
                symbol: 'DOT',
                decimals: 10
            },
            'BSC': {
                address: '0x7083609fCE4d1d8Dc0C979AAb8c869Ea2C873402',
                symbol: 'DOT',
                decimals: 18
            }
        }
    },
    'AVAX': {
        name: 'Avalanche',
        chains: {
            'ETH': {
                address: '0x85f138bfEE4ef8e540890CFb48F620571d67Eda3',
                symbol: 'WAVAX',
                decimals: 18
            },
            'BSC': {
                address: '0x1CE0c2827e2eF14D5C4f29a091d735A204794041',
                symbol: 'AVAX',
                decimals: 18
            }
        }
    },
    'LINK': {
        name: 'Chainlink',
        chains: {
            'ETH': {
                address: '0x514910771AF9Ca656af840dff83E8264EcF986CA',
                symbol: 'LINK',
                decimals: 18
            },
            'BSC': {
                address: '0xF8A0BF9cF54Bb92F17374d9e9A321E6a111a51bD',
                symbol: 'LINK',
                decimals: 18
            }
        }
    },
    'UNI': {
        name: 'Uniswap',
        chains: {
            'ETH': {
                address: '0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984',
                symbol: 'UNI',
                decimals: 18
            },
            'BSC': {
                address: '0xBf5140A22578168FD562DCcF235E5D43A02ce9B1',
                symbol: 'UNI',
                decimals: 18
            }
        }
    },
    'ATOM': {
        name: 'Cosmos',
        chains: {
            'ETH': {
                address: '0x8D983cb9388EaC77af0474fA441C4815500Cb7BB',
                symbol: 'ATOM',
                decimals: 6
            },
            'BSC': {
                address: '0x0Eb3a705fc54725037CC9e008bDede697f62F335',
                symbol: 'ATOM',
                decimals: 18
            }
        }
    },
    'LTC': {
        name: 'Litecoin',
        chains: {
            'ETH': {
                address: '0x6DEA81C8171D0bA574754EF6F8b412F2Ed88c54D',
                symbol: 'LTC',
                decimals: 8
            },
            'BSC': {
                address: '0x4338665CBB7B2485A8855A139b75D5e34AB0DB94',
                symbol: 'LTC',
                decimals: 18
            }
        }
    },
    'SHIB': {
        name: 'Shiba Inu',
        chains: {
            'ETH': {
                address: '0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE',
                symbol: 'SHIB',
                decimals: 18
            },
            'BSC': {
                address: '0x2859e4544C4bB03966803b044A93563Bd2D0DD4D',
                symbol: 'SHIB',
                decimals: 18
            }
        }
    },
    'ARB': {
        name: 'Arbitrum',
        chains: {
            'ETH': {
                address: '0xB50721BCf8d664c30412Cfbc6cf7a15145234ad1',
                symbol: 'ARB',
                decimals: 18
            }
        }
    },
    'OP': {
        name: 'Optimism',
        chains: {
            'ETH': {
                address: '0x4200000000000000000000000000000000000042',
                symbol: 'OP',
                decimals: 18
            }
        }
    },
    'AAVE': {
        name: 'Aave',
        chains: {
            'ETH': {
                address: '0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9',
                symbol: 'AAVE',
                decimals: 18
            },
            'BSC': {
                address: '0xfb6115445Bff7b52FeB98650C87f44907E58f802',
                symbol: 'AAVE',
                decimals: 18
            }
        }
    },
    'FIL': {
        name: 'Filecoin',
        chains: {
            'ETH': {
                address: '0x6e1A19F235bE7ED8E3369eF73b196C07257494DE',
                symbol: 'FIL',
                decimals: 18
            },
            'BSC': {
                address: '0x0D8Ce2A99Bb6e3B7Db580eD848240e4a0F9aE153',
                symbol: 'FIL',
                decimals: 18
            }
        }
    },
    'APT': {
        name: 'Aptos',
        chains: {
            'ETH': {
                address: '0x4Fabb145d64652a948d72533023f6E7A623C7C53',
                symbol: 'APT',
                decimals: 8
            }
        }
    },
    'NEAR': {
        name: 'NEAR Protocol',
        chains: {
            'ETH': {
                address: '0x85F17Cf997934a597031b2E18a9aB6ebD4B9f6a4',
                symbol: 'NEAR',
                decimals: 24
            }
        }
    }
};

/**
 * Helper function to get token address
 * @param {string} symbol - Trading symbol (e.g., 'BTC', 'ETH')
 * @param {string} chain - Blockchain ('ETH' or 'BSC')
 * @returns {string|null} Contract address or null if not found
 */
function getTokenAddress(symbol, chain = 'ETH') {
    const baseSymbol = symbol.replace('/USDT', '').replace('USDT', '');
    return TOKEN_MAPPING[baseSymbol]?.chains[chain]?.address || null;
}

/**
 * Get all available chains for a token
 * @param {string} symbol - Trading symbol
 * @returns {string[]} Array of chain names
 */
function getAvailableChains(symbol) {
    const baseSymbol = symbol.replace('/USDT', '').replace('USDT', '');
    const token = TOKEN_MAPPING[baseSymbol];
    return token ? Object.keys(token.chains) : [];
}

/**
 * Check if token is supported
 * @param {string} symbol - Trading symbol
 * @returns {boolean}
 */
function isTokenSupported(symbol) {
    const baseSymbol = symbol.replace('/USDT', '').replace('USDT', '');
    return baseSymbol in TOKEN_MAPPING;
}

// Export for use in modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        TOKEN_MAPPING,
        getTokenAddress,
        getAvailableChains,
        isTokenSupported
    };
}
