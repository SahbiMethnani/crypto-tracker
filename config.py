POPULAR_PAIRS = [
    "BTC/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT", "XRP/USDT",
    "ADA/USDT", "DOGE/USDT", "AVAX/USDT", "DOT/USDT", "MATIC/USDT",
]

COMPARE_PAIRS_POOL = [
    "BTC/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT",
    "XRP/USDT", "ADA/USDT", "AVAX/USDT", "DOGE/USDT",
]

CORRELATION_PAIRS = [
    "BTC/USDT", "ETH/USDT", "BNB/USDT",
    "SOL/USDT", "XRP/USDT", "ADA/USDT",
]

TIMEFRAMES = {"1h": "1h", "4h": "4h", "1d": "1d", "1w": "1w"}
TIMEFRAME_LABELS = {
    "1h": "Hourly",
    "4h": "4-Hour",
    "1d": "Daily",
    "1w": "Weekly",
}

CACHE_TTL_MARKET = 60       
CACHE_TTL_OHLCV  = 300      

DEFAULT_PAIR        = "BTC/USDT"
DEFAULT_TIMEFRAME   = "1d"
DEFAULT_CANDLE_LIMIT = 250
DEFAULT_MARKET_N    = 50

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

AXIS_STYLE = dict(gridcolor="#1e293b", showline=False, zeroline=False)

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#94a3b8"),
    margin=dict(l=0, r=0, t=30, b=0),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#1e293b"),
    hovermode="x unified",
    hoverlabel=dict(bgcolor="#161d2e", bordercolor="#2d3f5e", font_color="#f1f5f9"),
)

CHART_LAYOUT_SIMPLE = dict(
    **CHART_LAYOUT,
    xaxis=AXIS_STYLE,
    yaxis=AXIS_STYLE,
)

import socket



def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except socket.error as e:
        print(f"Erreur lors de la récupération de l'adresse IP : {e}")
        return None

IP_PROXY=get_local_ip()  

def get_available_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
     s.bind(("", 0))  
     port_libre = s.getsockname()[1]
     return port_libre
PORT_PROXY=get_available_port()