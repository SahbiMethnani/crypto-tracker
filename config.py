# ─── config.py ───────────────────────────────────────────────────────────────
# Toutes les constantes et paramètres globaux du projet
# Modifie ce fichier pour changer les paires, timeframes, couleurs, etc.
# ─────────────────────────────────────────────────────────────────────────────

# ── Paires affichées dans la sidebar ──────────────────────────────────────────
POPULAR_PAIRS = [
    "BTC/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT", "XRP/USDT",
    "ADA/USDT", "DOGE/USDT", "AVAX/USDT", "DOT/USDT", "MATIC/USDT",
]

# ── Paires disponibles dans la comparaison multi-actifs (Tab 3) ───────────────
COMPARE_PAIRS_POOL = [
    "BTC/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT",
    "XRP/USDT", "ADA/USDT", "AVAX/USDT", "DOGE/USDT",
]

# ── Paires utilisées pour la matrice de corrélation ──────────────────────────
CORRELATION_PAIRS = [
    "BTC/USDT", "ETH/USDT", "BNB/USDT",
    "SOL/USDT", "XRP/USDT", "ADA/USDT",
]

# ── Timeframes disponibles ────────────────────────────────────────────────────
TIMEFRAMES = {"1h": "1h", "4h": "4h", "1d": "1d", "1w": "1w"}
TIMEFRAME_LABELS = {
    "1h": "Hourly",
    "4h": "4-Hour",
    "1d": "Daily",
    "1w": "Weekly",
}

# ── Cache TTL (secondes) ──────────────────────────────────────────────────────
CACHE_TTL_MARKET = 60       # Vue marché (rafraîchi toutes les 60s)
CACHE_TTL_OHLCV  = 300      # Bougies OHLCV (rafraîchi toutes les 5min)

# ── Paramètres par défaut de la sidebar ──────────────────────────────────────
DEFAULT_PAIR        = "BTC/USDT"
DEFAULT_TIMEFRAME   = "1d"
DEFAULT_CANDLE_LIMIT = 250
DEFAULT_MARKET_N    = 50

# ── Palette de couleurs des graphiques ───────────────────────────────────────
COLORS = {
    "candle_up":   "#10b981",
    "candle_down": "#ef4444",
    "sma20":       "#06b6d4",
    "sma50":       "#f59e0b",
    "ema9":        "#a78bfa",
    "bb":          "rgba(59,130,246,0.4)",
    "bb_fill":     "rgba(59,130,246,0.04)",
    "rsi":         "#a78bfa",
    "macd":        "#3b82f6",
    "macd_signal": "#f59e0b",
    "vol_ma":      "#f59e0b",
    "atr":         "#a78bfa",
    "compare":     ["#3b82f6", "#10b981", "#f59e0b", "#a78bfa", "#ef4444", "#06b6d4"],
}

# ── Style des axes Plotly (réutilisé partout) ─────────────────────────────────
AXIS_STYLE = dict(gridcolor="#1e293b", showline=False, zeroline=False)

# ── Layout Plotly de base (sans xaxis/yaxis — compatible subplots) ────────────
CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#94a3b8"),
    margin=dict(l=0, r=0, t=30, b=0),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#1e293b"),
    hovermode="x unified",
    hoverlabel=dict(bgcolor="#161d2e", bordercolor="#2d3f5e", font_color="#f1f5f9"),
)

# ── Layout Plotly pour graphiques simples (ajoute xaxis/yaxis) ───────────────
CHART_LAYOUT_SIMPLE = dict(
    **CHART_LAYOUT,
    xaxis=AXIS_STYLE,
    yaxis=AXIS_STYLE,
)