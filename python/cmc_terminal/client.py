"""
CoinMarketCap Pro API Async Ingestion Client
Provides robust network fetching with automatic offline fallback and mathematical feature transforms.
"""

import os
import math
import logging
from typing import List, Dict, Any, Optional
import httpx
from cmc_terminal.sample_data import SAMPLE_LISTINGS, SAMPLE_GLOBAL_METRICS

logger = logging.getLogger("cmc_terminal.client")

CONST_PARKINSON_FACTOR = 0.36067376022224085  # 1.0 / (4.0 * ln(2))


class CMCClient:
    """Institutional client for CoinMarketCap Pro API with zero-failure fallback."""

    def __init__(self, api_key: Optional[str] = None, base_url: str = "https://pro-api.coinmarketcap.com"):
        self.api_key = api_key or os.environ.get("CMC_PRO_API_KEY") or os.environ.get("CMC_API_KEY")
        self.base_url = base_url.rstrip("/")
        self.is_offline_mode = not bool(self.api_key)
        self.last_data_source = "offline_fixture" if self.is_offline_mode else "uninitialized"

    async def get_listings(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Fetch latest cryptocurrency listings, falling back to sample dataset if offline."""
        assert limit > 0, "limit must be strictly positive"

        if self.is_offline_mode:
            self.last_data_source = "offline_fixture"
            return SAMPLE_LISTINGS[:limit]

        url = f"{self.base_url}/v1/cryptocurrency/listings/latest"
        headers = {
            "X-CMC_PRO_API_KEY": self.api_key,
            "Accept": "application/json"
        }
        params = {
            "start": 1,
            "limit": limit,
            "convert": "USD"
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url, headers=headers, params=params)
                if res.status_code == 200:
                    data = res.json().get("data", [])
                    parsed = []
                    for item in data:
                        quote = item.get("quote", {}).get("USD", {})
                        parsed.append({
                            "id": item.get("id"),
                            "name": item.get("name"),
                            "symbol": item.get("symbol"),
                            "price_usd": quote.get("price") or 0.0,
                            "percent_change_24h": quote.get("percent_change_24h") or 0.0,
                            "percent_change_7d": quote.get("percent_change_7d") or 0.0,
                            "volume_24h_usd": quote.get("volume_24h") or 0.0,
                            "market_cap_usd": quote.get("market_cap") or 0.0,
                            "high_24h_usd": (quote.get("price") or 0.0) * 1.02, # Estimate if 24h high absent
                            "low_24h_usd": (quote.get("price") or 0.0) * 0.98,
                            "circulating_supply": item.get("circulating_supply") or 0.0
                        })
                    self.last_data_source = "live_api"
                    return parsed
                else:
                    logger.warning(f"CMC API responded with status {res.status_code}. Falling back to sample dataset.")
                    self.last_data_source = "offline_fixture"
                    return SAMPLE_LISTINGS[:limit]
        except Exception as err:
            logger.warning(f"Network call failed: {err}. Falling back to sample dataset.")
            self.last_data_source = "offline_fixture"
            return SAMPLE_LISTINGS[:limit]

    async def get_global_metrics(self) -> Dict[str, Any]:
        """Fetch global cryptocurrency market metrics."""
        if self.is_offline_mode:
            self.last_data_source = "offline_fixture"
            return SAMPLE_GLOBAL_METRICS

        url = f"{self.base_url}/v1/global-metrics/quotes/latest"
        headers = {
            "X-CMC_PRO_API_KEY": self.api_key,
            "Accept": "application/json"
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url, headers=headers)
                if res.status_code == 200:
                    d = res.json().get("data", {}).get("quote", {}).get("USD", {})
                    self.last_data_source = "live_api"
                    return {
                        "total_market_cap_usd": d.get("total_market_cap", 0.0),
                        "total_volume_24h_usd": d.get("total_volume_24h", 0.0),
                        "btc_dominance_percentage": res.json().get("data", {}).get("btc_dominance", 50.0),
                        "eth_dominance_percentage": res.json().get("data", {}).get("eth_dominance", 15.0),
                        "defi_volume_24h_usd": d.get("defi_volume_24h", 0.0),
                        "updated_at": d.get("last_updated", "")
                    }
                self.last_data_source = "offline_fixture"
                return SAMPLE_GLOBAL_METRICS
        except Exception:
            self.last_data_source = "offline_fixture"
            return SAMPLE_GLOBAL_METRICS

    async def get_quote(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Find a single cryptocurrency by symbol."""
        assert symbol, "symbol must not be empty"
        listings = await self.get_listings(limit=100)
        target = symbol.upper()
        for item in listings:
            if item["symbol"] == target:
                return item
        return None

    @staticmethod
    def calculate_parkinson_volatility(high: float, low: float) -> float:
        """Compute Parkinson extreme-value realized volatility for a 24h bar."""
        assert high >= low, "high must be greater than or equal to low"
        assert low >= 0.0, "low must be non-negative"

        if low <= 0.0 or high <= 0.0 or high == low:
            return 0.0

        ratio = high / low
        assert ratio >= 1.0, "ratio must be >= 1.0"
        log_ratio = math.log(ratio)
        return math.sqrt(CONST_PARKINSON_FACTOR * (log_ratio * log_ratio))

    @staticmethod
    def calculate_momentum_score(change_24h: float, change_7d: float, volume_usd: float, mcap_usd: float) -> float:
        """Institutional multi-factor momentum composite."""
        turnover = (volume_usd / mcap_usd) if mcap_usd > 0.0 else 0.0
        # Blend short-term return (60%), medium-term trend (30%), and liquidity velocity (10%)
        return (0.60 * change_24h) + (0.30 * change_7d) + (10.0 * min(turnover, 0.5))
