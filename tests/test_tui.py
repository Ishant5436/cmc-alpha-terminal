from cmc_terminal.tui import render_dashboard, format_vol_bar, green, red, yellow
from cmc_terminal.sample_data import SAMPLE_LISTINGS, SAMPLE_GLOBAL_METRICS

def test_color_formatters():
    g = green("success")
    assert "\033[32m" in g
    assert "success" in g

    r = red("failure")
    assert "\033[31m" in r

    y = yellow("warning")
    assert "\033[33m" in y

def test_format_vol_bar():
    low_bar = format_vol_bar(0.01)
    assert "█" in low_bar
    assert "░" in low_bar

    high_bar = format_vol_bar(0.07)
    assert "█" in high_bar

def test_render_dashboard():
    output = render_dashboard(SAMPLE_LISTINGS, SAMPLE_GLOBAL_METRICS)
    assert "COINMARKETCAP QUANTITATIVE ALPHA TERMINAL" in output
    assert "MACRO REGIME:" in output
    assert "BTC" in output
    assert "ETH" in output
    assert "SOL" in output
    assert "PARKINSON VOL" in output
    assert "LONG" in output or "HOLD" in output or "AVOID" in output
