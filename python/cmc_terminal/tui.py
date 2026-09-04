"""
Interactive ASCII Terminal Dashboard for CoinMarketCap Quantitative Intelligence
Provides real-time terminal rendering with ANSI formatting, volatility gauges, and multi-factor signals.
"""

import sys
import asyncio
from pathlib import Path
from typing import List, Dict, Any

sys.path.insert(0, str(Path(__file__).parent.parent))

from cmc_terminal.client import CMCClient


def color_text(text: str, color_code: str) -> str:
    """Wrap text in ANSI color codes."""
    return f"\033[{color_code}m{text}\033[0m"


def green(text: str) -> str:
    return color_text(text, "32")


def red(text: str) -> str:
    return color_text(text, "31")


def yellow(text: str) -> str:
    return color_text(text, "33")


def cyan(text: str) -> str:
    return color_text(text, "36")


def bold(text: str) -> str:
    return color_text(text, "1")


def format_vol_bar(vol: float, max_vol: float = 0.08, width: int = 10) -> str:
    """Render an ASCII bar representing realized volatility."""
    fraction = min(1.0, max(0.0, vol / max_vol))
    filled = int(round(fraction * width))
    bar = "█" * filled + "░" * (width - filled)
    if vol > 0.05:
        return red(bar)
    elif vol > 0.03:
        return yellow(bar)
    return green(bar)


def render_dashboard(listings: List[Dict[str, Any]], macro: Dict[str, Any]) -> str:
    """Generate the full ANSI terminal dashboard layout."""
    lines = []
    w = 96
    border = "=" * w

    lines.append(cyan(border))
    lines.append(cyan("  ⚡ COINMARKETCAP QUANTITATIVE ALPHA TERMINAL | C++20 ZERO-HEAP CORE & FastMCP GATEWAY ⚡"))
    lines.append(cyan(border))

    # 1. Global Macro Section
    total_mcap = macro.get("total_market_cap_usd", 0.0) / 1e12
    total_vol = macro.get("total_volume_24h_usd", 0.0) / 1e9
    btc_dom = macro.get("btc_dominance_percentage", 50.0)
    eth_dom = macro.get("eth_dominance_percentage", 15.0)

    lines.append(bold("  MACRO REGIME:"))
    lines.append(
        f"  Total Market Cap: {bold(f'${total_mcap:.2f}T')} | "
        f"24h Volume: {bold(f'${total_vol:.1f}B')} | "
        f"BTC Dom: {cyan(f'{btc_dom:.1f}%')} | "
        f"ETH Dom: {cyan(f'{eth_dom:.1f}%')}"
    )
    lines.append("-" * w)

    # 2. Market Screen Table Header
    header = (
        f"  {bold('SYMBOL'):<10} {bold('PRICE'):<12} {bold('24H CHG'):<12} {bold('7D CHG'):<12} "
        f"{bold('PARKINSON VOL'):<16} {bold('MOMENTUM'):<12} {bold('SIGNAL')}"
    )
    lines.append(header)
    lines.append("-" * w)

    client = CMCClient()
    for item in listings[:10]:
        sym = item["symbol"]
        price = item["price_usd"]
        chg_24 = item["percent_change_24h"]
        chg_7d = item["percent_change_7d"]
        vol_usd = item["volume_24h_usd"]
        mcap_usd = item["market_cap_usd"]
        high = item.get("high_24h_usd", price)
        low = item.get("low_24h_usd", price)

        p_vol = client.calculate_parkinson_volatility(high, low)
        mom = client.calculate_momentum_score(chg_24, chg_7d, vol_usd, mcap_usd)
        vol_bar = format_vol_bar(p_vol)

        # Colorize changes
        c24_str = green(f"{chg_24:+.2f}%") if chg_24 >= 0 else red(f"{chg_24:+.2f}%")
        c7d_str = green(f"{chg_7d:+.2f}%") if chg_7d >= 0 else red(f"{chg_7d:+.2f}%")

        if mom > 5.0 and p_vol < 0.05:
            sig = green("LONG ↗")
        elif mom > 2.0:
            sig = yellow("HOLD →")
        else:
            sig = red("AVOID ↘")

        row = (
            f"  {bold(sym):<19} ${price:<11,.2f} {c24_str:<21} {c7d_str:<21} "
            f"{p_vol:.4f} {vol_bar}   {mom:<11.2f} {sig}"
        )
        lines.append(row)

    lines.append(cyan(border))
    lines.append("  [STATUS: 100% OPERATIONAL | MCP SERVER READY: `python3 -m cmc_terminal.server`]")
    lines.append(cyan(border) + "\n")
    return "\n".join(lines)


async def main_async():
    client = CMCClient()
    listings = await client.get_listings(limit=12)
    macro = await client.get_global_metrics()
    output = render_dashboard(listings, macro)
    print(output)


def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
