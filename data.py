import ccxt
import pandas as pd
import streamlit as st

from config import CACHE_TTL_MARKET, CACHE_TTL_OHLCV, IP_PROXY, PORT_PROXY



@st.cache_resource
def get_exchange():
    return ccxt.binance({
        "enableRateLimit": True,
        "timeout": 30000,
       # "httpsProxy": f"http://{IP_PROXY}:{PORT_PROXY}",
    })



@st.cache_data(ttl=CACHE_TTL_MARKET)
def fetch_market_overview(n: int = 50) -> pd.DataFrame:
    
    ex = get_exchange()
    markets = ex.load_markets()
    pairs = [s for s in markets if s.endswith("/USDT") and "/" in s][:n]

    rows = []
    for sym in pairs:
        try:
            t = ex.fetch_ticker(sym)
            rows.append({
                "symbol":      sym.replace("/USDT", ""),
                "pair":        sym,
                "price":       t.get("last") or 0,
                "change_pct":  t.get("percentage") or 0,
                "volume_usdt": t.get("quoteVolume") or 0,
                "high_24h":    t.get("high") or 0,
                "low_24h":     t.get("low") or 0,
                "bid":         t.get("bid") or 0,
                "ask":         t.get("ask") or 0,
            })
        except Exception:
            pass  

    df = pd.DataFrame(rows)
    return df.dropna().reset_index(drop=True)


@st.cache_data(ttl=CACHE_TTL_OHLCV)
def fetch_ohlcv(symbol: str, timeframe: str, limit: int = 500) -> pd.DataFrame:

    ex = get_exchange()
    raw = ex.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(raw, columns=["time", "open", "high", "low", "close", "volume"])
    df["time"] = pd.to_datetime(df["time"], unit="ms")
    return df