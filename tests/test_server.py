import asyncio
import pytest
from cmc_terminal.server import (
    cmc_screen_momentum,
    cmc_volatility_regime,
    cmc_liquidity_depth,
    cmc_global_macro,
    cmc_alpha_signals
)

def test_mcp_screen_momentum():
    res = asyncio.run(cmc_screen_momentum(top_n=3, min_volume_usd=100_000_000.0))
    assert "CoinMarketCap Cross-Sectional Momentum Screen" in res
    assert "Rank" in res
    assert "SOL" in res or "BTC" in res or "ETH" in res

def test_mcp_volatility_regime():
    res = asyncio.run(cmc_volatility_regime("BTC"))
    assert "CoinMarketCap Volatility Regime: BTC" in res
    assert "Realized Parkinson Vol" in res
    assert "Regime State" in res

def test_mcp_volatility_regime_missing():
    res = asyncio.run(cmc_volatility_regime("UNKNOWN_COIN"))
    assert "Error: Asset 'UNKNOWN_COIN' not found" in res

def test_mcp_liquidity_depth():
    res = asyncio.run(cmc_liquidity_depth("ETH"))
    assert "Institutional Liquidity Audit: ETH" in res
    assert "Turnover Ratio" in res
    assert "Liquidity Quality Grade" in res

def test_mcp_global_macro():
    res = asyncio.run(cmc_global_macro())
    assert "CoinMarketCap Global Macro State" in res
    assert "Total Crypto Market Cap" in res
    assert "BTC Market Dominance" in res

def test_mcp_alpha_signals():
    res = asyncio.run(cmc_alpha_signals(limit=4))
    assert "CoinMarketCap Alpha Signal Directives" in res
    assert "Signal Directive" in res
    assert "LONG" in res or "NEUTRAL" in res or "AVOID" in res

def test_mcp_input_validation():
    with pytest.raises(AssertionError):
        asyncio.run(cmc_screen_momentum(top_n=0))

    with pytest.raises(AssertionError):
        asyncio.run(cmc_volatility_regime(""))
