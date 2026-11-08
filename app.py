import pandas as pd
import streamlit as st
from datetime import datetime

from config import (
    POPULAR_PAIRS, COMPARE_PAIRS_POOL, CORRELATION_PAIRS,
    TIMEFRAMES, TIMEFRAME_LABELS,
    DEFAULT_PAIR, DEFAULT_TIMEFRAME, DEFAULT_CANDLE_LIMIT, DEFAULT_MARKET_N,
)
from data import fetch_market_overview, fetch_ohlcv
from indicators import compute_indicators, signal_summary
from charts import (
    candlestick_chart, macd_chart,
    volume_dist_chart, scatter_chart,
    comparison_chart, correlation_heatmap,
    atr_chart, returns_histogram,
)
from ui import inject_css, section_header, kpi_card, signal_card, stats_box, rank_row, top_bar

st.set_page_config(
    page_title="CryptoVision Pro",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()

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

    section_header("INSTRUMENT")
    selected_pair = st.selectbox("Paire", POPULAR_PAIRS,
                                 index=POPULAR_PAIRS.index(DEFAULT_PAIR))
    selected_tf   = st.selectbox(
        "Timeframe", list(TIMEFRAMES.keys()),
        index=list(TIMEFRAMES.keys()).index(DEFAULT_TIMEFRAME),
        format_func=lambda x: f"{x} — {TIMEFRAME_LABELS[x]}",
    )
    candle_limit = st.slider("Nombre de bougies", 100, 500, DEFAULT_CANDLE_LIMIT, 50)

    section_header("AFFICHAGE")
    show_bb  = st.toggle("Bollinger Bands", value=True)
    show_sma = st.toggle("SMA 20 / 50",    value=True)

    section_header("MARCHÉ")
    market_n = st.slider("Nb. de paires USDT", 20, 100, DEFAULT_MARKET_N, 10)

    st.markdown("---")
    if st.button("⟳  Actualiser les données", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    now = datetime.utcnow().strftime("%H:%M:%S UTC")
    st.markdown(
        f'<div style="text-align:center;font-size:0.65rem;color:#475569;'
        f'font-family:Space Mono,monospace;margin-top:0.5rem">{now}</div>',
        unsafe_allow_html=True,
    )


top_bar(selected_pair, selected_tf)

with st.spinner("Chargement des données de marché…"):
    df_market = fetch_market_overview(market_n)
    df_ohlcv  = fetch_ohlcv(selected_pair, TIMEFRAMES[selected_tf], candle_limit)
    df_ohlcv  = compute_indicators(df_ohlcv)


sym_row = df_market[df_market["pair"] == selected_pair]
if not sym_row.empty:
    r = sym_row.iloc[0]
    price, chg, vol, hi, lo = (
        r["price"], r["change_pct"], r["volume_usdt"], r["high_24h"], r["low_24h"]
    )
else:
    last  = df_ohlcv.iloc[-1]
    price, chg = last["close"], 0.0
    vol   = last["volume"] * price
    hi, lo = last["high"], last["low"]

last_rsi = df_ohlcv["rsi"].iloc[-1]
sign     = "▲" if chg >= 0 else "▼"
rsi_lbl  = "Suracheté" if last_rsi > 70 else ("Survendu" if last_rsi < 30 else "Neutre")

c1, c2, c3, c4, c5 = st.columns(5)
with c1: st.markdown(kpi_card("Prix actuel", f"${price:,.4f}", f"{sign} {abs(chg):.2f}% 24h", chg >= 0), unsafe_allow_html=True)
with c2: st.markdown(kpi_card("Volume 24h",  f"${vol/1e6:.1f}M"), unsafe_allow_html=True)
with c3: st.markdown(kpi_card("High 24h",    f"${hi:,.4f}"), unsafe_allow_html=True)
with c4: st.markdown(kpi_card("Low 24h",     f"${lo:,.4f}"), unsafe_allow_html=True)
with c5: st.markdown(kpi_card("RSI (14)",    f"{last_rsi:.1f}", rsi_lbl, last_rsi < 50), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


tab1, tab2, tab3 = st.tabs([
    "  📈  Graphique & Technique  ",
    "  🌐  Vue Marché  ",
    "  🔬  Analyse Avancée  ",
])


with tab1:
    col_chart, col_signals = st.columns([3, 1])

    with col_chart:
        section_header(f"{selected_pair} — {TIMEFRAME_LABELS[selected_tf]}")
        st.plotly_chart(
            candlestick_chart(df_ohlcv, selected_pair, show_bb, show_sma),
            use_container_width=True, config={"displayModeBar": False},
        )
        st.plotly_chart(
            macd_chart(df_ohlcv),
            use_container_width=True, config={"displayModeBar": False},
        )

    with col_signals:
        section_header("SIGNAUX")
        for indicator, (sig, desc) in signal_summary(df_ohlcv).items():
            signal_card(indicator, sig, desc)

        section_header("STATISTIQUES")
        last = df_ohlcv.iloc[-1]
        stats_box({
            "ATR (14)": f"{last['atr']:.4f}",
            "SMA 20":   f"${last['sma20']:,.4f}",
            "SMA 50":   f"${last['sma50']:,.4f}",
            "BB Upper": f"${last['bb_upper']:,.4f}",
            "BB Lower": f"${last['bb_lower']:,.4f}",
            "EMA 9":    f"${last['ema9']:,.4f}",
        })


with tab2:
    col_left, col_right = st.columns([1, 2])

    with col_left:
        gainers = df_market.nlargest(10,  "change_pct")
        losers  = df_market.nsmallest(10, "change_pct")

        section_header("TOP GAINERS")
        for i, (_, r) in enumerate(gainers.iterrows()):
            rank_row(i + 1, r["symbol"], r["price"], r["change_pct"])

        st.markdown("<br>", unsafe_allow_html=True)
        section_header("TOP LOSERS")
        for i, (_, r) in enumerate(losers.iterrows()):
            rank_row(i + 1, r["symbol"], r["price"], r["change_pct"])

    with col_right:
        section_header("VOLUME PAR SYMBOLE (M USDT)")
        st.plotly_chart(volume_dist_chart(df_market), use_container_width=True, config={"displayModeBar": False})

        section_header("VOLUME vs VARIATION 24H")
        st.plotly_chart(scatter_chart(df_market),     use_container_width=True, config={"displayModeBar": False})

    section_header("TOUTES LES PAIRES USDT")
    df_display = df_market.copy()
    df_display["change_pct"]  = df_display["change_pct"].apply(lambda x: f"{x:+.2f}%")
    df_display["volume_usdt"] = df_display["volume_usdt"].apply(lambda x: f"${x/1e6:.2f}M")
    df_display["price"]       = df_display["price"].apply(lambda x: f"${x:,.6f}")
    df_display = df_display.rename(columns={
        "symbol": "Symbole", "price": "Prix", "change_pct": "Var. 24h",
        "volume_usdt": "Volume 24h", "high_24h": "High", "low_24h": "Low",
    })
    st.dataframe(
        df_display[["Symbole", "Prix", "Var. 24h", "Volume 24h", "High", "Low"]],
        use_container_width=True, height=350, hide_index=True,
    )

with tab3:

    section_header("COMPARAISON MULTI-ACTIFS (performance normalisée)")
    _options = [p for p in COMPARE_PAIRS_POOL if p in df_market["pair"].tolist()]
    _default = [p for p in ["BTC/USDT", "ETH/USDT", "SOL/USDT"] if p in _options]
    compare_pairs = st.multiselect("Sélectionner les paires à comparer", _options, default=_default)

    if compare_pairs:
        cmp_data = {}
        for pair in compare_pairs:
            try:
                d = fetch_ohlcv(pair, "1d", 90)
                normed = (d["close"] / d["close"].iloc[0] - 1) * 100
                normed.index = d["time"]
                cmp_data[pair.replace("/USDT", "")] = normed
            except Exception:
                pass
        if cmp_data:
            st.plotly_chart(comparison_chart(cmp_data), use_container_width=True, config={"displayModeBar": False})

    section_header("MATRICE DE CORRÉLATION (retours journaliers 90j)")
    closes = {}
    for p in CORRELATION_PAIRS:
        try:
            d = fetch_ohlcv(p, "1d", 90)
            closes[p.replace("/USDT", "")] = d.set_index("time")["close"].pct_change()
        except Exception:
            pass
    if closes:
        corr_df = pd.DataFrame(closes).corr()
        st.plotly_chart(correlation_heatmap(corr_df), use_container_width=True, config={"displayModeBar": False})

    col_v1, col_v2 = st.columns(2)
    with col_v1:
        section_header("VOLATILITÉ HISTORIQUE (ATR)")
        st.plotly_chart(atr_chart(df_ohlcv), use_container_width=True, config={"displayModeBar": False})
    with col_v2:
        section_header("DISTRIBUTION DES RETOURS")
        returns = df_ohlcv["close"].pct_change().dropna() * 100
        st.plotly_chart(returns_histogram(returns), use_container_width=True, config={"displayModeBar": False})