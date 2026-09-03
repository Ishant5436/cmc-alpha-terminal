"""
High-Fidelity Sample Dataset for CoinMarketCap Pro API Offline Replay
Guarantees judge reproducibility and test deterministic execution without API key dependency.
"""

SAMPLE_GLOBAL_METRICS = {
    "total_market_cap_usd": 2_340_000_000_000.0,
    "total_volume_24h_usd": 68_500_000_000.0,
    "btc_dominance_percentage": 54.8,
    "eth_dominance_percentage": 17.2,
    "defi_volume_24h_usd": 5_200_000_000.0,
    "updated_at": "2026-09-04T00:00:00.000Z"
}

SAMPLE_LISTINGS = [
    {
        "id": 1,
        "name": "Bitcoin",
        "symbol": "BTC",
        "price_usd": 64250.0,
        "percent_change_24h": 1.85,
        "percent_change_7d": 4.12,
        "volume_24h_usd": 28_500_000_000.0,
        "market_cap_usd": 1_265_000_000_000.0,
        "high_24h_usd": 65100.0,
        "low_24h_usd": 63800.0,
        "circulating_supply": 19_750_000.0
    },
    {
        "id": 1027,
        "name": "Ethereum",
        "symbol": "ETH",
        "price_usd": 3480.0,
        "percent_change_24h": 2.40,
        "percent_change_7d": 5.60,
        "volume_24h_usd": 14_200_000_000.0,
        "market_cap_usd": 418_000_000_000.0,
        "high_24h_usd": 3550.0,
        "low_24h_usd": 3420.0,
        "circulating_supply": 120_200_000.0
    },
    {
        "id": 5426,
        "name": "Solana",
        "symbol": "SOL",
        "price_usd": 148.5,
        "percent_change_24h": 5.10,
        "percent_change_7d": 12.30,
        "volume_24h_usd": 4_800_000_000.0,
        "market_cap_usd": 69_500_000_000.0,
        "high_24h_usd": 154.2,
        "low_24h_usd": 144.1,
        "circulating_supply": 468_000_000.0
    },
    {
        "id": 1839,
        "name": "BNB",
        "symbol": "BNB",
        "price_usd": 585.0,
        "percent_change_24h": 0.75,
        "percent_change_7d": 1.95,
        "volume_24h_usd": 1_100_000_000.0,
        "market_cap_usd": 89_500_000_000.0,
        "high_24h_usd": 592.0,
        "low_24h_usd": 578.0,
        "circulating_supply": 153_000_000.0
    },
    {
        "id": 52,
        "name": "XRP",
        "symbol": "XRP",
        "price_usd": 0.58,
        "percent_change_24h": -0.40,
        "percent_change_7d": -1.20,
        "volume_24h_usd": 1_350_000_000.0,
        "market_cap_usd": 32_800_000_000.0,
        "high_24h_usd": 0.60,
        "low_24h_usd": 0.57,
        "circulating_supply": 56_500_000_000.0
    },
    {
        "id": 74,
        "name": "Dogecoin",
        "symbol": "DOGE",
        "price_usd": 0.115,
        "percent_change_24h": 3.20,
        "percent_change_7d": 8.40,
        "volume_24h_usd": 850_000_000.0,
        "market_cap_usd": 16_800_000_000.0,
        "high_24h_usd": 0.122,
        "low_24h_usd": 0.111,
        "circulating_supply": 145_000_000_000.0
    },
    {
        "id": 2010,
        "name": "Cardano",
        "symbol": "ADA",
        "price_usd": 0.36,
        "percent_change_24h": 1.10,
        "percent_change_7d": 3.40,
        "volume_24h_usd": 340_000_000.0,
        "market_cap_usd": 12_900_000_000.0,
        "high_24h_usd": 0.375,
        "low_24h_usd": 0.352,
        "circulating_supply": 35_700_000_000.0
    },
    {
        "id": 5805,
        "name": "Avalanche",
        "symbol": "AVAX",
        "price_usd": 26.4,
        "percent_change_24h": 4.30,
        "percent_change_7d": 11.20,
        "volume_24h_usd": 410_000_000.0,
        "market_cap_usd": 10_500_000_000.0,
        "high_24h_usd": 27.8,
        "low_24h_usd": 25.9,
        "circulating_supply": 396_000_000.0
    },
    {
        "id": 1975,
        "name": "Chainlink",
        "symbol": "LINK",
        "price_usd": 11.8,
        "percent_change_24h": 3.80,
        "percent_change_7d": 7.50,
        "volume_24h_usd": 290_000_000.0,
        "market_cap_usd": 7_200_000_000.0,
        "high_24h_usd": 12.4,
        "low_24h_usd": 11.5,
        "circulating_supply": 608_000_000.0
    },
    {
        "id": 6535,
        "name": "NEAR Protocol",
        "symbol": "NEAR",
        "price_usd": 4.55,
        "percent_change_24h": 6.20,
        "percent_change_7d": 15.80,
        "volume_24h_usd": 380_000_000.0,
        "market_cap_usd": 5_400_000_000.0,
        "high_24h_usd": 4.82,
        "low_24h_usd": 4.41,
        "circulating_supply": 1_180_000_000.0
    },
    {
        "id": 20947,
        "name": "Sui",
        "symbol": "SUI",
        "price_usd": 0.88,
        "percent_change_24h": 7.40,
        "percent_change_7d": 21.50,
        "volume_24h_usd": 260_000_000.0,
        "market_cap_usd": 2_350_000_000.0,
        "high_24h_usd": 0.94,
        "low_24h_usd": 0.82,
        "circulating_supply": 2_670_000_000.0
    },
    {
        "id": 21794,
        "name": "Aptos",
        "symbol": "APT",
        "price_usd": 6.75,
        "percent_change_24h": 2.90,
        "percent_change_7d": 4.80,
        "volume_24h_usd": 180_000_000.0,
        "market_cap_usd": 3_200_000_000.0,
        "high_24h_usd": 7.10,
        "low_24h_usd": 6.55,
        "circulating_supply": 474_000_000.0
    }
]
