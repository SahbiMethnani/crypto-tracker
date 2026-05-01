import streamlit as st
import ccxt
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CryptoVision Pro",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CUSTOM CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg-primary:    #0a0e1a;
    --bg-secondary:  #111827;
    --bg-card:       #161d2e;
    --bg-card-hover: #1c2540;
    --accent-blue:   #3b82f6;
    --accent-cyan:   #06b6d4;
    --accent-green:  #10b981;
    --accent-red:    #ef4444;
    --accent-gold:   #f59e0b;
    --text-primary:  #f1f5f9;
    --text-secondary:#94a3b8;
    --text-muted:    #475569;
    --border:        #1e293b;
    --border-accent: #2d3f5e;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg-primary);
    color: var(--text-primary);
}

/* Hide default Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* Main container */
.block-container { padding: 1.5rem 2rem; max-width: 100%; }

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border-accent);
}
section[data-testid="stSidebar"] .block-container { padding: 1.5rem 1rem; }

/* ── METRIC CARDS ── */
.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border-accent);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    transition: border-color 0.2s, transform 0.2s;
}
.metric-card:hover {
    border-color: var(--accent-blue);
    transform: translateY(-2px);
}
.metric-label {
    font-size: 0.72rem;
    font-family: 'Space Mono', monospace;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.4rem;
}
.metric-value {
    font-size: 1.6rem;
    font-weight: 600;
    color: var(--text-primary);
    line-height: 1.2;
}
.metric-delta {
    font-size: 0.78rem;
    font-family: 'Space Mono', monospace;
    margin-top: 0.3rem;
}
.delta-pos { color: var(--accent-green); }
.delta-neg { color: var(--accent-red); }

/* ── SECTION HEADERS ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-muted);
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.6rem;
    margin-bottom: 1rem;
}
.section-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--accent-cyan);
}

/* ── TOP BAR LOGO ── */
.top-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid var(--border-accent);
}
.logo {
    font-family: 'Space Mono', monospace;
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: 0.05em;
}
.logo-accent { color: var(--accent-cyan); }
.tagline {
    font-size: 0.72rem;
    color: var(--text-muted);
    font-family: 'Space Mono', monospace;
}
.live-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(16,185,129,0.12);
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.7rem;
    font-family: 'Space Mono', monospace;
    color: var(--accent-green);
    letter-spacing: 0.05em;
}
.live-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--accent-green);
    animation: blink 1.4s infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.2} }

/* ── RANK TABLE ── */
.rank-row {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    padding: 0.6rem 0.8rem;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.15s;
}
.rank-row:hover { background: var(--bg-card-hover); }
.rank-num {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: var(--text-muted);
    width: 18px;
    text-align: right;
}
.symbol-badge {
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    font-weight: 700;
    color: var(--accent-cyan);
    width: 80px;
}
.price-val {
    flex: 1;
    font-size: 0.85rem;
    text-align: right;
    color: var(--text-primary);
}
.change-val {
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    width: 68px;
    text-align: right;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    background: var(--bg-secondary);
    border-radius: 10px;
    padding: 4px;
    border: 1px solid var(--border-accent);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 7px;
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.05em;
    color: var(--text-muted);
    padding: 0.5rem 1.2rem;
}
.stTabs [aria-selected="true"] {
    background: var(--accent-blue) !important;
    color: #fff !important;
}

/* ── SELECTS & INPUTS ── */
.stSelectbox > div > div, .stMultiSelect > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-accent) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}
.stSlider > div > div > div { background: var(--accent-blue) !important; }

/* ── PLOTLY CHARTS ── */
.js-plotly-plot .plotly { border-radius: 12px; }

/* ── DATAFRAME ── */
.stDataFrame { border: 1px solid var(--border-accent); border-radius: 10px; overflow: hidden; }

/* ── SIGNAL PILLS ── */
.signal-pill {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.68rem;
    font-family: 'Space Mono', monospace;
    font-weight: 700;
    letter-spacing: 0.06em;
}
.signal-buy { background: rgba(16,185,129,0.15); color: var(--accent-green); border: 1px solid rgba(16,185,129,0.3); }
.signal-sell { background: rgba(239,68,68,0.15); color: var(--accent-red); border: 1px solid rgba(239,68,68,0.3); }
.signal-neutral { background: rgba(148,163,184,0.1); color: var(--text-secondary); border: 1px solid rgba(148,163,184,0.2); }
</style>
""", unsafe_allow_html=True)

# ─── CONSTANTS ───────────────────────────────────────────────────────────────
TIMEFRAMES = {"1h": "1h", "4h": "4h", "1d": "1d", "1w": "1w"}
TIMEFRAME_LABELS = {"1h": "Hourly", "4h": "4-Hour", "1d": "Daily", "1w": "Weekly"}

_AXIS_STYLE = dict(gridcolor="#1e293b", showline=False, zeroline=False)

# Base layout WITHOUT xaxis/yaxis — safe for both simple and subplot figures
CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#94a3b8"),
    margin=dict(l=0, r=0, t=30, b=0),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#1e293b"),
    hovermode="x unified",
    hoverlabel=dict(bgcolor="#161d2e", bordercolor="#2d3f5e", font_color="#f1f5f9"),
)

# Layout for simple (non-subplot) figures — adds single axis styling
CHART_LAYOUT_SIMPLE = dict(
    **CHART_LAYOUT,
    xaxis=_AXIS_STYLE,
    yaxis=_AXIS_STYLE,
)

# ─── DATA LAYER ──────────────────────────────────────────────────────────────
@st.cache_resource
def get_exchange():
    return ccxt.binance({"enableRateLimit": True})

@st.cache_data(ttl=60)
def fetch_market_overview(n=50):
    ex = get_exchange()
    markets = ex.load_markets()
    pairs = [s for s in markets if s.endswith("/USDT") and "/" in s][:n]
    rows = []
    for sym in pairs:
        try:
            t = ex.fetch_ticker(sym)
            rows.append({
                "symbol": sym.replace("/USDT", ""),
                "pair": sym,
                "price": t.get("last") or 0,
                "change_pct": t.get("percentage") or 0,
                "volume_usdt": t.get("quoteVolume") or 0,
                "high_24h": t.get("high") or 0,
                "low_24h": t.get("low") or 0,
                "bid": t.get("bid") or 0,
                "ask": t.get("ask") or 0,
            })
        except Exception:
            pass
    df = pd.DataFrame(rows)
    return df.dropna().reset_index(drop=True)

@st.cache_data(ttl=300)
def fetch_ohlcv(symbol: str, timeframe: str, limit: int = 500):
    ex = get_exchange()
    raw = ex.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(raw, columns=["time", "open", "high", "low", "close", "volume"])
    df["time"] = pd.to_datetime(df["time"], unit="ms")
    return df

# ─── INDICATORS ──────────────────────────────────────────────────────────────
def compute_indicators(df: pd.DataFrame) -> pd.DataFrame:
    # SMAs
    df["sma20"] = df["close"].rolling(20).mean()
    df["sma50"] = df["close"].rolling(50).mean()
    df["sma200"] = df["close"].rolling(200).mean()

    # EMA
    df["ema9"] = df["close"].ewm(span=9, adjust=False).mean()

    # Bollinger Bands
    bb_std = df["close"].rolling(20).std()
    df["bb_upper"] = df["sma20"] + 2 * bb_std
    df["bb_lower"] = df["sma20"] - 2 * bb_std

    # RSI
    delta = df["close"].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss.replace(0, np.nan)
    df["rsi"] = 100 - (100 / (1 + rs))

    # MACD
    ema12 = df["close"].ewm(span=12, adjust=False).mean()
    ema26 = df["close"].ewm(span=26, adjust=False).mean()
    df["macd"] = ema12 - ema26
    df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()
    df["macd_hist"] = df["macd"] - df["macd_signal"]

    # Volume MA
    df["vol_ma20"] = df["volume"].rolling(20).mean()

    # ATR
    hl = df["high"] - df["low"]
    hc = (df["high"] - df["close"].shift()).abs()
    lc = (df["low"] - df["close"].shift()).abs()
    df["atr"] = pd.concat([hl, hc, lc], axis=1).max(axis=1).rolling(14).mean()

    return df

def signal_summary(df: pd.DataFrame) -> dict:
    last = df.iloc[-1]
    signals = {}
    # Trend
    if last["close"] > last["sma20"] > last["sma50"]:
        signals["Trend"] = ("BUY", "Price above SMA20 & SMA50")
    elif last["close"] < last["sma20"] < last["sma50"]:
        signals["Trend"] = ("SELL", "Price below SMA20 & SMA50")
    else:
        signals["Trend"] = ("NEUTRAL", "Mixed moving averages")
    # RSI
    if last["rsi"] < 30:
        signals["RSI"] = ("BUY", f"Oversold ({last['rsi']:.1f})")
    elif last["rsi"] > 70:
        signals["RSI"] = ("SELL", f"Overbought ({last['rsi']:.1f})")
    else:
        signals["RSI"] = ("NEUTRAL", f"Neutral ({last['rsi']:.1f})")
    # MACD
    if last["macd"] > last["macd_signal"] and last["macd_hist"] > 0:
        signals["MACD"] = ("BUY", "MACD above signal")
    elif last["macd"] < last["macd_signal"] and last["macd_hist"] < 0:
        signals["MACD"] = ("SELL", "MACD below signal")
    else:
        signals["MACD"] = ("NEUTRAL", "Crossing zone")
    # BB
    if last["close"] < last["bb_lower"]:
        signals["Bollinger"] = ("BUY", "Price below lower band")
    elif last["close"] > last["bb_upper"]:
        signals["Bollinger"] = ("SELL", "Price above upper band")
    else:
        signals["Bollinger"] = ("NEUTRAL", "Inside bands")
    return signals

# ─── CHART BUILDERS ──────────────────────────────────────────────────────────
def candlestick_chart(df: pd.DataFrame, symbol: str, show_bb=True, show_sma=True):
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        row_heights=[0.6, 0.2, 0.2],
        vertical_spacing=0.02,
    )
    # Candles
    fig.add_trace(go.Candlestick(
        x=df["time"], open=df["open"], high=df["high"],
        low=df["low"], close=df["close"],
        increasing_line_color="#10b981", decreasing_line_color="#ef4444",
        increasing_fillcolor="rgba(16,185,129,0.7)",
        decreasing_fillcolor="rgba(239,68,68,0.7)",
        name=symbol, showlegend=False,
    ), row=1, col=1)

    if show_bb:
        fig.add_trace(go.Scatter(x=df["time"], y=df["bb_upper"], line=dict(color="rgba(59,130,246,0.4)", width=1), name="BB Upper", showlegend=False), row=1, col=1)
        fig.add_trace(go.Scatter(x=df["time"], y=df["bb_lower"], line=dict(color="rgba(59,130,246,0.4)", width=1), fill="tonexty", fillcolor="rgba(59,130,246,0.04)", name="BB Lower", showlegend=False), row=1, col=1)
    if show_sma:
        for col_name, color, label in [("sma20", "#06b6d4", "SMA20"), ("sma50", "#f59e0b", "SMA50")]:
            fig.add_trace(go.Scatter(x=df["time"], y=df[col_name], line=dict(color=color, width=1.2), name=label), row=1, col=1)

    # Volume
    colors = ["rgba(16,185,129,0.6)" if r["close"] >= r["open"] else "rgba(239,68,68,0.6)" for _, r in df.iterrows()]
    fig.add_trace(go.Bar(x=df["time"], y=df["volume"], marker_color=colors, name="Volume", showlegend=False), row=2, col=1)
    fig.add_trace(go.Scatter(x=df["time"], y=df["vol_ma20"], line=dict(color="#f59e0b", width=1.2), name="Vol MA20", showlegend=False), row=2, col=1)

    # RSI
    fig.add_trace(go.Scatter(x=df["time"], y=df["rsi"], line=dict(color="#a78bfa", width=1.5), name="RSI", showlegend=False), row=3, col=1)
    for lvl, color in [(30, "rgba(16,185,129,0.3)"), (70, "rgba(239,68,68,0.3)"), (50, "rgba(148,163,184,0.15)")]:
        fig.add_hline(y=lvl, line=dict(color=color, width=1, dash="dot"), row=3, col=1)

    fig.update_layout(
    **CHART_LAYOUT,
    height=520,
    xaxis_rangeslider_visible=False,
      )
    fig.update_layout(legend=dict(orientation="h", y=1.02, x=0, bgcolor="rgba(0,0,0,0)"))
    # Apply axis styling to every subplot axis individually
    fig.update_xaxes(**_AXIS_STYLE)
    fig.update_yaxes(**_AXIS_STYLE)
    return fig

def macd_chart(df: pd.DataFrame):
    fig = go.Figure()
    colors = ["rgba(16,185,129,0.7)" if v >= 0 else "rgba(239,68,68,0.7)" for v in df["macd_hist"]]
    fig.add_trace(go.Bar(x=df["time"], y=df["macd_hist"], marker_color=colors, name="Histogram"))
    fig.add_trace(go.Scatter(x=df["time"], y=df["macd"], line=dict(color="#3b82f6", width=1.5), name="MACD"))
    fig.add_trace(go.Scatter(x=df["time"], y=df["macd_signal"], line=dict(color="#f59e0b", width=1.5, dash="dot"), name="Signal"))
    fig.update_layout(**CHART_LAYOUT_SIMPLE, height=240, title=dict(text="MACD", font=dict(size=12)))
    return fig

def volume_dist_chart(df_market: pd.DataFrame):
    top = df_market.nlargest(15, "volume_usdt")
    fig = go.Figure(go.Bar(
        x=top["symbol"], y=top["volume_usdt"] / 1e6,
        marker=dict(
            color=top["change_pct"],
            colorscale=[[0, "#ef4444"], [0.5, "#475569"], [1, "#10b981"]],
            showscale=True,
            colorbar=dict(title="Chg%", thickness=10, len=0.7),
        ),
        text=top["change_pct"].apply(lambda x: f"{x:+.1f}%"),
        textposition="outside",
    ))
    fig.update_layout(**CHART_LAYOUT_SIMPLE, height=300, yaxis_title="Volume (M USDT)")
    return fig

def scatter_chart(df_market: pd.DataFrame):
    fig = go.Figure(go.Scatter(
        x=df_market["volume_usdt"] / 1e6,
        y=df_market["change_pct"],
        mode="markers+text",
        text=df_market["symbol"],
        textposition="top center",
        textfont=dict(size=8, color="#94a3b8"),
        marker=dict(
            size=np.log1p(df_market["volume_usdt"] / 1e5) * 3,
            color=df_market["change_pct"],
            colorscale=[[0, "#ef4444"], [0.5, "#475569"], [1, "#10b981"]],
            showscale=False,
            line=dict(color="rgba(255,255,255,0.1)", width=1),
        ),
    ))
    fig.add_hline(y=0, line=dict(color="rgba(148,163,184,0.2)", width=1))
    fig.update_layout(**CHART_LAYOUT_SIMPLE, height=350, xaxis_title="Volume (M USDT)", yaxis_title="24h Change %")
    return fig

# ─── SIDEBAR ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;margin-bottom:1.5rem;">
        <div style="font-family:'Space Mono',monospace;font-size:1.2rem;font-weight:700;">
            ⬡ <span style="color:#06b6d4">CRYPTO</span>VISION
        </div>
        <div style="font-size:0.65rem;color:#475569;font-family:'Space Mono',monospace;margin-top:4px;">
            MARKET INTELLIGENCE PLATFORM
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header"><span class="section-dot"></span>INSTRUMENT</div>', unsafe_allow_html=True)

    popular = ["BTC/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT", "XRP/USDT",
               "ADA/USDT", "DOGE/USDT", "AVAX/USDT", "DOT/USDT", "MATIC/USDT"]
    selected_pair = st.selectbox("Paire", popular, index=0)
    selected_tf = st.selectbox("Timeframe", list(TIMEFRAMES.keys()), index=2, format_func=lambda x: f"{x} — {TIMEFRAME_LABELS[x]}")
    candle_limit = st.slider("Nombre de bougies", 100, 500, 250, 50)

    st.markdown('<div class="section-header" style="margin-top:1rem"><span class="section-dot"></span>AFFICHAGE</div>', unsafe_allow_html=True)
    show_bb = st.toggle("Bollinger Bands", value=True)
    show_sma = st.toggle("SMA 20 / 50", value=True)

    st.markdown('<div class="section-header" style="margin-top:1rem"><span class="section-dot"></span>MARCHÉ</div>', unsafe_allow_html=True)
    market_n = st.slider("Nb. de paires USDT", 20, 100, 50, 10)

    st.markdown("---")
    if st.button("⟳  Actualiser les données", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    now = datetime.utcnow().strftime("%H:%M:%S UTC")
    st.markdown(f'<div style="text-align:center;font-size:0.65rem;color:#475569;font-family:Space Mono,monospace;margin-top:0.5rem">{now}</div>', unsafe_allow_html=True)

# ─── HEADER ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="top-bar">
    <div>
        <div class="logo">⬡ <span class="logo-accent">CRYPTO</span>VISION <span style="font-weight:300">PRO</span></div>
        <div class="tagline">Real-time market intelligence · Binance data feed</div>
    </div>
    <div style="display:flex;align-items:center;gap:12px;">
        <span class="live-badge"><span class="live-dot"></span>LIVE</span>
        <span style="font-family:'Space Mono',monospace;font-size:0.7rem;color:#475569">{selected_pair} · {selected_tf.upper()}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── LOAD DATA ───────────────────────────────────────────────────────────────
with st.spinner("Chargement des données de marché…"):
    df_market = fetch_market_overview(market_n)
    df_ohlcv = fetch_ohlcv(selected_pair, TIMEFRAMES[selected_tf], candle_limit)
    df_ohlcv = compute_indicators(df_ohlcv)

# ─── KPI ROW ─────────────────────────────────────────────────────────────────
sym_data = df_market[df_market["pair"] == selected_pair]
if not sym_data.empty:
    r = sym_data.iloc[0]
    price, chg, vol, hi, lo = r["price"], r["change_pct"], r["volume_usdt"], r["high_24h"], r["low_24h"]
else:
    last = df_ohlcv.iloc[-1]
    price, chg = last["close"], 0
    vol = df_ohlcv["volume"].iloc[-1] * price
    hi, lo = last["high"], last["low"]

spread = ((df_ohlcv.iloc[-1].get("ask", hi) - df_ohlcv.iloc[-1].get("bid", lo)) / price * 100) if price else 0
last_rsi = df_ohlcv["rsi"].iloc[-1]

def kpi(label, value, delta="", delta_pos=True):
    delta_class = "delta-pos" if delta_pos else "delta-neg"
    delta_html = f'<div class="metric-delta {delta_class}">{delta}</div>' if delta else ""
    return f"""<div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>"""

c1, c2, c3, c4, c5 = st.columns(5)
sign = "▲" if chg >= 0 else "▼"
with c1: st.markdown(kpi("Prix actuel", f"${price:,.4f}", f"{sign} {abs(chg):.2f}% 24h", chg >= 0), unsafe_allow_html=True)
with c2: st.markdown(kpi("Volume 24h", f"${vol/1e6:.1f}M"), unsafe_allow_html=True)
with c3: st.markdown(kpi("High 24h", f"${hi:,.4f}"), unsafe_allow_html=True)
with c4: st.markdown(kpi("Low 24h", f"${lo:,.4f}"), unsafe_allow_html=True)
with c5:
    rsi_lbl = "Suracheté" if last_rsi > 70 else ("Survendu" if last_rsi < 30 else "Neutre")
    st.markdown(kpi("RSI (14)", f"{last_rsi:.1f}", rsi_lbl, last_rsi < 50), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── TABS ────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["  📈  Graphique & Technique  ", "  🌐  Vue Marché  ", "  🔬  Analyse Avancée  "])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — CHART + SIGNALS
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    col_chart, col_signals = st.columns([3, 1])

    with col_chart:
        st.markdown(f'<div class="section-header"><span class="section-dot"></span>{selected_pair} — {TIMEFRAME_LABELS[selected_tf]}</div>', unsafe_allow_html=True)
        st.plotly_chart(candlestick_chart(df_ohlcv, selected_pair, show_bb, show_sma), use_container_width=True, config={"displayModeBar": False})
        st.plotly_chart(macd_chart(df_ohlcv), use_container_width=True, config={"displayModeBar": False})

    with col_signals:
        st.markdown('<div class="section-header"><span class="section-dot"></span>SIGNAUX</div>', unsafe_allow_html=True)
        sigs = signal_summary(df_ohlcv)
        for ind, (sig, desc) in sigs.items():
            pill_class = {"BUY": "signal-buy", "SELL": "signal-sell", "NEUTRAL": "signal-neutral"}[sig]
            st.markdown(f"""
            <div style="margin-bottom:1rem;padding:0.9rem;background:var(--bg-card);border-radius:10px;border:1px solid var(--border-accent)">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.4rem">
                    <span style="font-family:'Space Mono',monospace;font-size:0.7rem;color:var(--text-muted)">{ind}</span>
                    <span class="signal-pill {pill_class}">{sig}</span>
                </div>
                <div style="font-size:0.75rem;color:var(--text-secondary)">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

        # Stats box
        last = df_ohlcv.iloc[-1]
        st.markdown('<div class="section-header" style="margin-top:0.5rem"><span class="section-dot"></span>STATISTIQUES</div>', unsafe_allow_html=True)
        stats = {
            "ATR (14)": f"{last['atr']:.4f}",
            "SMA 20": f"${last['sma20']:,.4f}",
            "SMA 50": f"${last['sma50']:,.4f}",
            "BB Upper": f"${last['bb_upper']:,.4f}",
            "BB Lower": f"${last['bb_lower']:,.4f}",
            "EMA 9": f"${last['ema9']:,.4f}",
        }
        rows_html = "".join(f"""
        <div style="display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px solid var(--border)">
            <span style="font-size:0.72rem;color:var(--text-muted)">{k}</span>
            <span style="font-size:0.72rem;font-family:'Space Mono',monospace;color:var(--text-primary)">{v}</span>
        </div>""" for k, v in stats.items())
        st.markdown(f'<div style="background:var(--bg-card);border:1px solid var(--border-accent);border-radius:10px;padding:0.8rem">{rows_html}</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — MARKET OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    col_left, col_right = st.columns([1, 2])

    with col_left:
        # Top gainers / losers
        gainers = df_market.nlargest(10, "change_pct")[["symbol", "price", "change_pct"]]
        losers = df_market.nsmallest(10, "change_pct")[["symbol", "price", "change_pct"]]

        st.markdown('<div class="section-header"><span class="section-dot"></span>TOP GAINERS</div>', unsafe_allow_html=True)
        for i, (_, r) in enumerate(gainers.iterrows()):
            st.markdown(f"""
            <div class="rank-row">
                <span class="rank-num">{i+1}</span>
                <span class="symbol-badge">{r['symbol']}</span>
                <span class="price-val">${r['price']:,.4f}</span>
                <span class="change-val delta-pos">▲ {r['change_pct']:.2f}%</span>
            </div>""", unsafe_allow_html=True)

        st.markdown('<div class="section-header" style="margin-top:1.2rem"><span class="section-dot"></span>TOP LOSERS</div>', unsafe_allow_html=True)
        for i, (_, r) in enumerate(losers.iterrows()):
            st.markdown(f"""
            <div class="rank-row">
                <span class="rank-num">{i+1}</span>
                <span class="symbol-badge">{r['symbol']}</span>
                <span class="price-val">${r['price']:,.4f}</span>
                <span class="change-val delta-neg">▼ {abs(r['change_pct']):.2f}%</span>
            </div>""", unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="section-header"><span class="section-dot"></span>VOLUME PAR SYMBOLE (M USDT)</div>', unsafe_allow_html=True)
        st.plotly_chart(volume_dist_chart(df_market), use_container_width=True, config={"displayModeBar": False})

        st.markdown('<div class="section-header"><span class="section-dot"></span>VOLUME vs VARIATION 24H</div>', unsafe_allow_html=True)
        st.plotly_chart(scatter_chart(df_market), use_container_width=True, config={"displayModeBar": False})

    # Full table
    st.markdown('<div class="section-header" style="margin-top:0.5rem"><span class="section-dot"></span>TOUTES LES PAIRES USDT</div>', unsafe_allow_html=True)
    df_display = df_market.copy()
    df_display["change_pct"] = df_display["change_pct"].apply(lambda x: f"{x:+.2f}%")
    df_display["volume_usdt"] = df_display["volume_usdt"].apply(lambda x: f"${x/1e6:.2f}M")
    df_display["price"] = df_display["price"].apply(lambda x: f"${x:,.6f}")
    df_display = df_display.rename(columns={
        "symbol": "Symbole", "price": "Prix", "change_pct": "Var. 24h",
        "volume_usdt": "Volume 24h", "high_24h": "High", "low_24h": "Low"
    })
    st.dataframe(df_display[["Symbole", "Prix", "Var. 24h", "Volume 24h", "High", "Low"]],
                 use_container_width=True, height=350, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — ADVANCED ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    # Compare multiple assets
    st.markdown('<div class="section-header"><span class="section-dot"></span>COMPARAISON MULTI-ACTIFS (performance normalisée)</div>', unsafe_allow_html=True)

    _cmp_options = [s for s in df_market["pair"].tolist() if s in ["BTC/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT", "XRP/USDT", "ADA/USDT", "AVAX/USDT", "DOGE/USDT"]]
    _cmp_default = [s for s in ["BTC/USDT", "ETH/USDT", "SOL/USDT"] if s in _cmp_options]

    compare_pairs = st.multiselect(
    "Sélectionner les paires à comparer",
    _cmp_options,
    default=_cmp_default,
     )

    if compare_pairs:
        fig_cmp = go.Figure()
        palette = ["#3b82f6", "#10b981", "#f59e0b", "#a78bfa", "#ef4444", "#06b6d4"]
        for i, pair in enumerate(compare_pairs):
            try:
                d = fetch_ohlcv(pair, "1d", 90)
                normed = (d["close"] / d["close"].iloc[0] - 1) * 100
                fig_cmp.add_trace(go.Scatter(
                    x=d["time"], y=normed,
                    mode="lines", name=pair.replace("/USDT", ""),
                    line=dict(color=palette[i % len(palette)], width=2),
                ))
            except Exception:
                pass
        fig_cmp.add_hline(y=0, line=dict(color="rgba(148,163,184,0.2)", width=1))
        fig_cmp.update_layout(**CHART_LAYOUT_SIMPLE, height=320, yaxis_title="Performance (%)")
        st.plotly_chart(fig_cmp, use_container_width=True, config={"displayModeBar": False})

    # Heatmap: correlation
    st.markdown('<div class="section-header"><span class="section-dot"></span>MATRICE DE CORRÉLATION (retours journaliers 90j)</div>', unsafe_allow_html=True)
    corr_pairs = ["BTC/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT", "XRP/USDT", "ADA/USDT"]
    closes = {}
    for p in corr_pairs:
        try:
            d = fetch_ohlcv(p, "1d", 90)
            closes[p.replace("/USDT", "")] = d.set_index("time")["close"].pct_change()
        except Exception:
            pass
    if closes:
        corr_df = pd.DataFrame(closes).corr()
        fig_heat = go.Figure(go.Heatmap(
            z=corr_df.values, x=corr_df.columns, y=corr_df.index,
            colorscale=[[0, "#ef4444"], [0.5, "#1e293b"], [1, "#10b981"]],
            zmin=-1, zmax=1,
            text=np.round(corr_df.values, 2),
            texttemplate="%{text}",
            textfont=dict(size=11),
            showscale=True,
        ))
        fig_heat.update_layout(**CHART_LAYOUT_SIMPLE, height=320)
        st.plotly_chart(fig_heat, use_container_width=True, config={"displayModeBar": False})

    # Volatility analysis
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        st.markdown('<div class="section-header"><span class="section-dot"></span>VOLATILITÉ HISTORIQUE (ATR)</div>', unsafe_allow_html=True)
        fig_atr = go.Figure()
        fig_atr.add_trace(go.Scatter(
            x=df_ohlcv["time"], y=df_ohlcv["atr"],
            fill="tozeroy", fillcolor="rgba(167,139,250,0.12)",
            line=dict(color="#a78bfa", width=1.5), name="ATR(14)",
        ))
        fig_atr.update_layout(**CHART_LAYOUT_SIMPLE, height=240)
        st.plotly_chart(fig_atr, use_container_width=True, config={"displayModeBar": False})

    with col_v2:
        st.markdown('<div class="section-header"><span class="section-dot"></span>DISTRIBUTION DES RETOURS</div>', unsafe_allow_html=True)
        returns = df_ohlcv["close"].pct_change().dropna() * 100
        fig_hist = go.Figure(go.Histogram(
            x=returns,
            nbinsx=40,
            marker_color="rgba(59,130,246,0.6)",
            marker_line=dict(color="rgba(59,130,246,0.9)", width=0.5),
        ))
        fig_hist.add_vline(x=0, line=dict(color="rgba(148,163,184,0.4)", width=1))
        fig_hist.update_layout(**CHART_LAYOUT_SIMPLE, height=240, xaxis_title="Retour (%)", yaxis_title="Fréquence")
        st.plotly_chart(fig_hist, use_container_width=True, config={"displayModeBar": False})