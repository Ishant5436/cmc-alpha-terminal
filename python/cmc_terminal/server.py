"""
FastMCP Server for CoinMarketCap Quantitative Intelligence Terminal
Exposes 5 institutional-grade quantitative screening and regime detection tools for AI agents.
"""

import math
from typing import Dict, Any, List
from mcp.server.fastmcp import FastMCP
from cmc_terminal.client import CMCClient

# Initialize FastMCP Server
mcp = FastMCP("cmc-alpha-terminal")
client = CMCClient()


@mcp.tool()
async def cmc_screen_momentum(top_n: int = 10, min_volume_usd: float = 100_000_000.0) -> Dict[str, Any]:
    """
    Screen CoinMarketCap assets by multi-factor cross-sectional momentum score.
    Filters by minimum 24h USD volume and returns rank-ordered institutional candidates.
    Returns structured JSON with candidates list and formatted markdown report for agent tool chaining.
    """
    assert top_n > 0, "top_n must be positive"
    assert min_volume_usd >= 0.0, "min_volume_usd must be non-negative"

    listings = await client.get_listings(limit=100)
    filtered = [item for item in listings if (item.get("volume_24h_usd") or 0.0) >= min_volume_usd]

    if not filtered:
        return {
            "data_source": client.last_data_source,
            "universe_count": len(listings),
            "filtered_count": 0,
            "assets": [],
            "formatted_markdown": "No assets met the minimum volume threshold."
        }

    # Compute momentum scores
    scored = []
    for item in filtered:
        mcap = item.get("market_cap_usd") or 0.0
        score = client.calculate_momentum_score(
            item.get("percent_change_24h") or 0.0,
            item.get("percent_change_7d") or 0.0,
            item.get("volume_24h_usd") or 0.0,
            mcap
        )
        scored.append({**item, "momentum_score": score})

    scored.sort(key=lambda x: x["momentum_score"], reverse=True)
    selected = scored[:top_n]
    n_total = len(scored)

    assets_structured = []
    lines = [
        "### CoinMarketCap Cross-Sectional Momentum Screen",
        f"**Data Source:** `{client.last_data_source}` | **Universe:** {n_total} liquid assets | **Top N Filter:** {len(selected)}",
        "",
        "| Rank | Symbol | Price (USD) | 24h Chg (%) | 7d Chg (%) | 24h Vol ($M) | Momentum Score | Percentile |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
    ]

    for idx, item in enumerate(selected):
        percentile = (n_total - idx) / float(n_total)
        assets_structured.append({
            "rank": idx + 1,
            "symbol": item["symbol"],
            "name": item.get("name", ""),
            "price_usd": item["price_usd"],
            "percent_change_24h": item.get("percent_change_24h", 0.0),
            "percent_change_7d": item.get("percent_change_7d", 0.0),
            "volume_24h_usd": item.get("volume_24h_usd", 0.0),
            "market_cap_usd": item.get("market_cap_usd", 0.0),
            "momentum_score": round(item["momentum_score"], 2),
            "percentile": round(percentile, 4)
        })
        lines.append(
            f"| {idx+1} | **{item['symbol']}** | ${item['price_usd']:,.2f} | "
            f"{item['percent_change_24h']:+.2f}% | {item['percent_change_7d']:+.2f}% | "
            f"${item['volume_24h_usd']/1e6:,.1f}M | {item['momentum_score']:.2f} | {percentile:.2f} |"
        )

    return {
        "data_source": client.last_data_source,
        "universe_count": n_total,
        "filtered_count": len(selected),
        "assets": assets_structured,
        "formatted_markdown": "\n".join(lines)
    }


@mcp.tool()
async def cmc_volatility_regime(symbol: str) -> Dict[str, Any]:
    """
    Compute extreme-value Parkinson realized volatility and classify current market regime.
    Regimes: COMPRESSION (low vol, consolidation), TRENDING (moderate vol, momentum), EXPANSION_VOLATILE (high risk).
    Returns structured volatility metrics, regime classification, and formatted markdown report.
    """
    assert symbol and isinstance(symbol, str), "symbol must be a valid non-empty string"
    clean_sym = symbol.strip().upper()
    quote = await client.get_quote(clean_sym)

    if not quote:
        err_msg = f"Error: Asset '{clean_sym}' not found in CoinMarketCap active listings."
        return {
            "data_source": client.last_data_source,
            "symbol": clean_sym,
            "error": err_msg,
            "formatted_markdown": err_msg
        }

    high = quote.get("high_24h_usd", quote["price_usd"])
    low = quote.get("low_24h_usd", quote["price_usd"])
    parkinson_vol = client.calculate_parkinson_volatility(high, low)

    # Annualized volatility estimate
    ann_vol = parkinson_vol * math.sqrt(365.0)

    # Classify regime
    if parkinson_vol < 0.025:
        regime = "COMPRESSION (Breakout Watch)"
        risk_level = "LOW (Favorable for Range or Squeeze Entries)"
    elif parkinson_vol <= 0.050:
        regime = "TRENDING (Directional Momentum)"
        risk_level = "MODERATE (Standard Risk Allocation)"
    else:
        regime = "EXPANSION_VOLATILE (High Turbulence)"
        risk_level = "HIGH (Requires Parkinson Volatility Gating)"

    md = (
        f"### CoinMarketCap Volatility Regime: {clean_sym}\n"
        f"- **Data Source:** `{client.last_data_source}`\n"
        f"- **Current Price:** ${quote['price_usd']:,.4f}\n"
        f"- **24h Range:** ${low:,.4f} - ${high:,.4f}\n"
        f"- **24h Realized Parkinson Vol:** {parkinson_vol:.4f} ({parkinson_vol*100:.2f}%)\n"
        f"- **Estimated Annualized Volatility:** {ann_vol*100:.2f}%\n"
        f"- **Regime State:** **{regime}**\n"
        f"- **Risk Allocation Directive:** {risk_level}"
    )

    return {
        "data_source": client.last_data_source,
        "symbol": clean_sym,
        "price_usd": quote["price_usd"],
        "low_24h_usd": low,
        "high_24h_usd": high,
        "parkinson_vol": round(parkinson_vol, 6),
        "annualized_vol": round(ann_vol, 4),
        "regime": regime,
        "risk_level": risk_level,
        "formatted_markdown": md
    }


@mcp.tool()
async def cmc_liquidity_depth(symbol: str) -> Dict[str, Any]:
    """
    Analyze institutional liquidity depth, volume-to-market-cap turnover, and execution slippage risks.
    Returns structured turnover ratio, liquidity grade, slippage estimates, and formatted markdown report.
    """
    assert symbol and isinstance(symbol, str), "symbol must be a valid non-empty string"
    clean_sym = symbol.strip().upper()
    quote = await client.get_quote(clean_sym)

    if not quote:
        err_msg = f"Error: Asset '{clean_sym}' not found in CoinMarketCap active listings."
        return {
            "data_source": client.last_data_source,
            "symbol": clean_sym,
            "error": err_msg,
            "formatted_markdown": err_msg
        }

    vol_24h = quote.get("volume_24h_usd") or 0.0
    mcap = quote.get("market_cap_usd") or 0.0

    if mcap <= 0.0:
        turnover_ratio = 0.0
        grade = "N/A (Missing or Non-Positive Market Cap)"
        slippage_est = "Unknown (Insufficient Depth Data)"
    else:
        turnover_ratio = vol_24h / mcap
        if turnover_ratio > 0.15:
            grade = "A+ (Deep Institutional Liquidity)"
            slippage_est = "< 2 bps on $100k clips"
        elif turnover_ratio > 0.05:
            grade = "A (Liquid Benchmark)"
            slippage_est = "2 - 5 bps on $100k clips"
        elif turnover_ratio > 0.01:
            grade = "B (Moderate Liquidity)"
            slippage_est = "5 - 15 bps on $100k clips"
        else:
            grade = "C (Illiquid / High Spread Drag)"
            slippage_est = "> 25 bps (High Spread Risk)"

    md = (
        f"### Institutional Liquidity Audit: {clean_sym}\n"
        f"- **Data Source:** `{client.last_data_source}`\n"
        f"- **24h USD Volume:** ${vol_24h:,.2f}\n"
        f"- **Market Capitalization:** ${mcap:,.2f}\n"
        f"- **Turnover Ratio (Vol / Cap):** {turnover_ratio:.4f} ({turnover_ratio*100:.2f}%)\n"
        f"- **Liquidity Quality Grade:** **{grade}**\n"
        f"- **Execution Friction Estimate:** {slippage_est}"
    )

    return {
        "data_source": client.last_data_source,
        "symbol": clean_sym,
        "volume_24h_usd": vol_24h,
        "market_cap_usd": mcap,
        "turnover_ratio": round(turnover_ratio, 6),
        "liquidity_grade": grade,
        "execution_friction_estimate": slippage_est,
        "formatted_markdown": md
    }


@mcp.tool()
async def cmc_global_macro() -> Dict[str, Any]:
    """
    Retrieve global crypto market capitalization, Bitcoin dominance, and macro market cycle classification.
    Returns structured macro metrics, dominance percentages, and formatted markdown report.
    """
    m = await client.get_global_metrics()
    btc_dom = m.get("btc_dominance_percentage", 50.0)
    eth_dom = m.get("eth_dominance_percentage", 15.0)
    total_mcap = m.get("total_market_cap_usd", 0.0)
    total_vol = m.get("total_volume_24h_usd", 0.0)

    if btc_dom > 55.0:
        cycle_phase = "BTC_LED_CONSOLIDATION (Capital Concentrating in Blue Chips)"
    elif btc_dom < 45.0:
        cycle_phase = "ALT_ROTATION_CYCLE (Aggressive Risk-On Dispersion)"
    else:
        cycle_phase = "EQUILIBRIUM_TREND (Steady Cross-Market Expansion)"

    md = (
        "### CoinMarketCap Global Macro State\n"
        f"- **Data Source:** `{client.last_data_source}`\n"
        f"- **Total Crypto Market Cap:** ${total_mcap:,.2f} (~${total_mcap/1e12:.2f}T)\n"
        f"- **24h Global Volume:** ${total_vol:,.2f} (~${total_vol/1e9:.2f}B)\n"
        f"- **BTC Market Dominance:** {btc_dom:.2f}%\n"
        f"- **ETH Market Dominance:** {eth_dom:.2f}%\n"
        f"- **Macro Cycle Phase:** **{cycle_phase}**"
    )

    return {
        "data_source": client.last_data_source,
        "total_market_cap_usd": total_mcap,
        "total_volume_24h_usd": total_vol,
        "btc_dominance_percentage": btc_dom,
        "eth_dominance_percentage": eth_dom,
        "macro_cycle_phase": cycle_phase,
        "formatted_markdown": md
    }


@mcp.tool()
async def cmc_alpha_signals(limit: int = 5) -> Dict[str, Any]:
    """
    Generate quantitative multi-factor alpha signals (Momentum + Volatility Penalty + Liquidity Guard).
    Returns recommended execution directives (LONG / NEUTRAL / AVOID) and formatted markdown report.
    """
    assert limit > 0, "limit must be positive"
    listings = await client.get_listings(limit=25)

    signals = []
    for item in listings:
        chg_24h = item.get("percent_change_24h") or 0.0
        chg_7d = item.get("percent_change_7d") or 0.0
        vol_24h = item.get("volume_24h_usd") or 0.0
        mcap = item.get("market_cap_usd") or 0.0
        high = item.get("high_24h_usd", item["price_usd"])
        low = item.get("low_24h_usd", item["price_usd"])

        p_vol = client.calculate_parkinson_volatility(high, low)
        mom = client.calculate_momentum_score(chg_24h, chg_7d, vol_24h, mcap)

        # Composite score: momentum rewarded, extreme volatility penalized
        composite = mom - (10.0 * max(0.0, p_vol - 0.04))

        if composite > 5.0 and p_vol < 0.05:
            directive = "LONG (High Momentum, Controlled Vol)"
        elif composite > 2.0:
            directive = "NEUTRAL (Moderate Momentum)"
        else:
            directive = "AVOID (Weak Alpha / High Spread Drag)"

        signals.append({
            "symbol": item["symbol"],
            "price_usd": item["price_usd"],
            "alpha_composite_score": round(composite, 2),
            "parkinson_vol": round(p_vol, 6),
            "directive": directive
        })

    signals.sort(key=lambda x: x["alpha_composite_score"], reverse=True)
    selected = signals[:limit]

    lines = [
        "### CoinMarketCap Alpha Signal Directives",
        f"**Data Source:** `{client.last_data_source}` | **Candidates Evaluated:** {len(signals)} | **Top Signals:** {len(selected)}",
        "",
        "| Symbol | Price (USD) | Alpha Score | Parkinson Vol | Signal Directive |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ]
    for s in selected:
        lines.append(f"| **{s['symbol']}** | ${s['price_usd']:,.2f} | {s['alpha_composite_score']:.2f} | {s['parkinson_vol']:.4f} | {s['directive']} |")

    return {
        "data_source": client.last_data_source,
        "limit": limit,
        "signals": selected,
        "formatted_markdown": "\n".join(lines)
    }


if __name__ == "__main__":
    mcp.run()
