import numpy as np
import pandas as pd


def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ajoute toutes les colonnes d'indicateurs au DataFrame OHLCV.
    Indicateurs calculés :
      - SMA 20, 50, 200
      - EMA 9
      - Bollinger Bands (période 20, écart-type ×2)
      - RSI (période 14)
      - MACD (12/26/9)
      - Volume MA 20
      - ATR (période 14)
    """
    # ── Moyennes mobiles simples ──────────────────────────────────────────────
    df["sma20"]  = df["close"].rolling(20).mean()
    df["sma50"]  = df["close"].rolling(50).mean()
    df["sma200"] = df["close"].rolling(200).mean()   # affiché si assez de bougies

    # ── EMA ───────────────────────────────────────────────────────────────────
    df["ema9"] = df["close"].ewm(span=9, adjust=False).mean()

    # ── Bollinger Bands ───────────────────────────────────────────────────────
    bb_std = df["close"].rolling(20).std()
    df["bb_upper"] = df["sma20"] + 2 * bb_std
    df["bb_lower"] = df["sma20"] - 2 * bb_std

    # ── RSI (14) ──────────────────────────────────────────────────────────────
    delta = df["close"].diff()
    gain  = delta.clip(lower=0).rolling(14).mean()
    loss  = (-delta.clip(upper=0)).rolling(14).mean()
    rs    = gain / loss.replace(0, np.nan)
    df["rsi"] = 100 - (100 / (1 + rs))

    # ── MACD (12 / 26 / 9) ───────────────────────────────────────────────────
    ema12 = df["close"].ewm(span=12, adjust=False).mean()
    ema26 = df["close"].ewm(span=26, adjust=False).mean()
    df["macd"]        = ema12 - ema26
    df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()
    df["macd_hist"]   = df["macd"] - df["macd_signal"]

    # ── Volume MA ─────────────────────────────────────────────────────────────
    df["vol_ma20"] = df["volume"].rolling(20).mean()

    # ── ATR (14) ──────────────────────────────────────────────────────────────
    hl = df["high"] - df["low"]
    hc = (df["high"] - df["close"].shift()).abs()
    lc = (df["low"]  - df["close"].shift()).abs()
    df["atr"] = pd.concat([hl, hc, lc], axis=1).max(axis=1).rolling(14).mean()

    return df


def signal_summary(df: pd.DataFrame) -> dict:
    """
    Génère des signaux BUY / SELL / NEUTRAL à partir de la dernière bougie.
    Retourne un dict : { "Indicateur": ("SIGNAL", "Description") }
    """
    last = df.iloc[-1]
    signals = {}

    # ── Tendance (SMA) ────────────────────────────────────────────────────────
    if last["close"] > last["sma20"] > last["sma50"]:
        signals["Trend"] = ("BUY",     "Price above SMA20 & SMA50")
    elif last["close"] < last["sma20"] < last["sma50"]:
        signals["Trend"] = ("SELL",    "Price below SMA20 & SMA50")
    else:
        signals["Trend"] = ("NEUTRAL", "Mixed moving averages")

    # ── RSI ───────────────────────────────────────────────────────────────────
    rsi = last["rsi"]
    if rsi < 30:
        signals["RSI"] = ("BUY",     f"Oversold ({rsi:.1f})")
    elif rsi > 70:
        signals["RSI"] = ("SELL",    f"Overbought ({rsi:.1f})")
    else:
        signals["RSI"] = ("NEUTRAL", f"Neutral ({rsi:.1f})")

    # ── MACD ──────────────────────────────────────────────────────────────────
    if last["macd"] > last["macd_signal"] and last["macd_hist"] > 0:
        signals["MACD"] = ("BUY",     "MACD above signal")
    elif last["macd"] < last["macd_signal"] and last["macd_hist"] < 0:
        signals["MACD"] = ("SELL",    "MACD below signal")
    else:
        signals["MACD"] = ("NEUTRAL", "Crossing zone")

    # ── Bollinger Bands ───────────────────────────────────────────────────────
    if last["close"] < last["bb_lower"]:
        signals["Bollinger"] = ("BUY",     "Price below lower band")
    elif last["close"] > last["bb_upper"]:
        signals["Bollinger"] = ("SELL",    "Price above upper band")
    else:
        signals["Bollinger"] = ("NEUTRAL", "Inside bands")

    return signals