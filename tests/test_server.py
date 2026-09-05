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
    assert isinstance(res, dict)
    assert res["data_source"] in ("live_api", "offline_fixture")
    assert res["filtered_count"] <= 3
    assert len(res["assets"]) <= 3
    assert isinstance(res["assets"][0]["symbol"], str) and len(res["assets"][0]["symbol"]) > 0
    assert res["assets"][0]["price_usd"] > 0.0
    assert "formatted_markdown" in res
    assert "CoinMarketCap Cross-Sectional Momentum Screen" in res["formatted_markdown"]

def test_mcp_volatility_regime():
    res = asyncio.run(cmc_volatility_regime("BTC"))
    assert isinstance(res, dict)
    assert res["symbol"] == "BTC"
    assert res["parkinson_vol"] >= 0.0
    assert res["regime"] in ("COMPRESSION (Breakout Watch)", "TRENDING (Directional Momentum)", "EXPANSION_VOLATILE (High Turbulence)")
    assert "formatted_markdown" in res
    assert "CoinMarketCap Volatility Regime: BTC" in res["formatted_markdown"]

def test_mcp_volatility_regime_missing():
    res = asyncio.run(cmc_volatility_regime("UNKNOWN_COIN"))
    assert isinstance(res, dict)
    assert "error" in res
    assert "not found" in res["error"]

def test_mcp_liquidity_depth():
    res = asyncio.run(cmc_liquidity_depth("ETH"))
    assert isinstance(res, dict)
    assert res["symbol"] == "ETH"
    assert res["volume_24h_usd"] > 0.0
    assert res["turnover_ratio"] >= 0.0
    assert "formatted_markdown" in res
    assert "Institutional Liquidity Audit: ETH" in res["formatted_markdown"]

def test_mcp_global_macro():
    res = asyncio.run(cmc_global_macro())
    assert isinstance(res, dict)
    assert res["total_market_cap_usd"] > 1e12
    assert res["btc_dominance_percentage"] > 40.0
    assert "formatted_markdown" in res
    assert "CoinMarketCap Global Macro State" in res["formatted_markdown"]

def test_mcp_alpha_signals():
    res = asyncio.run(cmc_alpha_signals(limit=4))
    assert isinstance(res, dict)
    assert len(res["signals"]) <= 4
    assert res["signals"][0]["directive"] in ("LONG (High Momentum, Controlled Vol)", "NEUTRAL (Moderate Momentum)", "AVOID (Weak Alpha / High Spread Drag)")
    assert "formatted_markdown" in res
    assert "CoinMarketCap Alpha Signal Directives" in res["formatted_markdown"]

def test_mcp_agent_tool_chaining():
    """Verify that an AI agent can chain screen_momentum -> volatility_regime -> liquidity_depth programmatically."""
    screen_res = asyncio.run(cmc_screen_momentum(top_n=1))
    assert len(screen_res["assets"]) == 1
    top_symbol = screen_res["assets"][0]["symbol"]

    vol_res = asyncio.run(cmc_volatility_regime(top_symbol))
    assert vol_res["symbol"] == top_symbol
    assert vol_res["parkinson_vol"] >= 0.0

    liq_res = asyncio.run(cmc_liquidity_depth(top_symbol))
    assert liq_res["symbol"] == top_symbol
    assert liq_res["turnover_ratio"] >= 0.0

def test_mcp_input_validation():
    with pytest.raises(AssertionError):
        asyncio.run(cmc_screen_momentum(top_n=0))

    with pytest.raises(AssertionError):
        asyncio.run(cmc_volatility_regime(""))
