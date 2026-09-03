import asyncio
from cmc_terminal.client import CMCClient

def test_client_offline_listings():
    client = CMCClient(api_key=None)
    assert client.is_offline_mode is True

    listings = asyncio.run(client.get_listings(limit=5))
    assert len(listings) == 5
    assert listings[0]["symbol"] == "BTC"
    assert listings[0]["price_usd"] > 0.0
    assert "market_cap_usd" in listings[0]
    assert "volume_24h_usd" in listings[0]

def test_client_offline_global_metrics():
    client = CMCClient(api_key=None)
    metrics = asyncio.run(client.get_global_metrics())
    assert metrics["total_market_cap_usd"] > 1e12
    assert metrics["btc_dominance_percentage"] > 40.0
    assert "eth_dominance_percentage" in metrics

def test_client_quote_lookup():
    client = CMCClient(api_key=None)
    sol = asyncio.run(client.get_quote("SOL"))
    assert sol is not None
    assert sol["symbol"] == "SOL"
    assert sol["price_usd"] > 100.0

    missing = asyncio.run(client.get_quote("NON_EXISTENT_TOKEN_XYZ"))
    assert missing is None

def test_parkinson_volatility_math():
    vol = CMCClient.calculate_parkinson_volatility(110.0, 100.0)
    assert vol > 0.0
    assert isinstance(vol, float)

    flat = CMCClient.calculate_parkinson_volatility(100.0, 100.0)
    assert flat == 0.0

def test_momentum_score_math():
    score = CMCClient.calculate_momentum_score(5.0, 10.0, 1_000_000_000.0, 50_000_000_000.0)
    assert score > 0.0
    assert isinstance(score, float)
