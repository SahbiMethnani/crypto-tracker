import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from config import COLORS, AXIS_STYLE, CHART_LAYOUT, CHART_LAYOUT_SIMPLE


def candlestick_chart(
    df: pd.DataFrame,
    symbol: str,
    show_bb: bool = True,
    show_sma: bool = True,
) -> go.Figure:
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        row_heights=[0.6, 0.2, 0.2],
        vertical_spacing=0.02,
    )
    """
    # ── Chandeliers ───────────────────────────────────────────────────────────
    fig.add_trace(go.Candlestick(
        x=df["time"], open=df["open"], high=df["high"],
        low=df["low"], close=df["close"],
        increasing_line_color=COLORS["candle_up"],
        decreasing_line_color=COLORS["candle_down"],
        increasing_fillcolor=COLORS["candle_up"].replace(")", ",0.7)").replace("#10b981", "rgba(16,185,129"),
        decreasing_fillcolor=COLORS["candle_down"].replace(")", ",0.7)").replace("#ef4444", "rgba(239,68,68"),
        name=symbol, showlegend=False,
    ), row=1, col=1)
    """
    fig.add_trace(go.Candlestick(
    x=df["time"],
    open=df["open"],
    high=df["high"],
    low=df["low"],
    close=df["close"],
    increasing_line_color=COLORS["candle_up"],
    decreasing_line_color=COLORS["candle_down"],
    increasing_fillcolor="rgba(16,185,129,0.7)",
    decreasing_fillcolor="rgba(239,68,68,0.7)",
    name=symbol,
    showlegend=False,
), row=1, col=1)
    if show_bb:
        fig.add_trace(go.Scatter(
            x=df["time"], y=df["bb_upper"],
            line=dict(color=COLORS["bb"], width=1),
            name="BB Upper", showlegend=False,
        ), row=1, col=1)
        fig.add_trace(go.Scatter(
            x=df["time"], y=df["bb_lower"],
            line=dict(color=COLORS["bb"], width=1),
            fill="tonexty", fillcolor=COLORS["bb_fill"],
            name="BB Lower", showlegend=False,
        ), row=1, col=1)

    if show_sma:
        for col_name, color, label in [
            ("sma20", COLORS["sma20"], "SMA20"),
            ("sma50", COLORS["sma50"], "SMA50"),
        ]:
            fig.add_trace(go.Scatter(
                x=df["time"], y=df[col_name],
                line=dict(color=color, width=1.2),
                name=label,
            ), row=1, col=1)

    bar_colors = np.where(
    df["close"] >= df["open"],
    "rgba(16,185,129,0.6)",
    "rgba(239,68,68,0.6)"
)
    fig.add_trace(go.Bar(
        x=df["time"], y=df["volume"],
        marker_color=bar_colors, name="Volume", showlegend=False,
    ), row=2, col=1)
    fig.add_trace(go.Scatter(
        x=df["time"], y=df["vol_ma20"],
        line=dict(color=COLORS["vol_ma"], width=1.2),
        name="Vol MA20", showlegend=False,
    ), row=2, col=1)

    fig.add_trace(go.Scatter(
        x=df["time"], y=df["rsi"],
        line=dict(color=COLORS["rsi"], width=1.5),
        name="RSI", showlegend=False,
    ), row=3, col=1)
    for lvl, color in [
        (30, "rgba(16,185,129,0.3)"),
        (70, "rgba(239,68,68,0.3)"),
        (50, "rgba(148,163,184,0.15)"),
    ]:
        fig.add_hline(y=lvl, line=dict(color=color, width=1, dash="dot"), row=3, col=1)

    fig.update_layout(**CHART_LAYOUT, height=520, xaxis_rangeslider_visible=False)
    fig.update_layout(legend=dict(orientation="h", y=1.02, x=0, bgcolor="rgba(0,0,0,0)"))
    fig.update_xaxes(**AXIS_STYLE)
    fig.update_yaxes(**AXIS_STYLE)
    return fig


def macd_chart(df: pd.DataFrame) -> go.Figure:
    hist_colors = [
        "rgba(16,185,129,0.7)" if v >= 0 else "rgba(239,68,68,0.7)"
        for v in df["macd_hist"]
    ]
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["time"], y=df["macd_hist"],
        marker_color=hist_colors, name="Histogram",
    ))
    fig.add_trace(go.Scatter(
        x=df["time"], y=df["macd"],
        line=dict(color=COLORS["macd"], width=1.5), name="MACD",
    ))
    fig.add_trace(go.Scatter(
        x=df["time"], y=df["macd_signal"],
        line=dict(color=COLORS["macd_signal"], width=1.5, dash="dot"), name="Signal",
    ))
    fig.update_layout(**CHART_LAYOUT_SIMPLE, height=240, title=dict(text="MACD", font=dict(size=12)))
    return fig


def volume_dist_chart(df_market: pd.DataFrame) -> go.Figure:
    top = df_market.nlargest(15, "volume_usdt")
    fig = go.Figure(go.Bar(
        x=top["symbol"],
        y=top["volume_usdt"] / 1e6,
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


def scatter_chart(df_market: pd.DataFrame) -> go.Figure:
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
    fig.update_layout(
        **CHART_LAYOUT_SIMPLE, height=350,
        xaxis_title="Volume (M USDT)", yaxis_title="24h Change %",
    )
    return fig


def comparison_chart(data: dict) -> go.Figure:
    """
    data = { "BTC": pd.Series(performance_normalisée), ... }
    """
    fig = go.Figure()
    for i, (name, series) in enumerate(data.items()):
        fig.add_trace(go.Scatter(
            x=series.index, y=series.values,
            mode="lines", name=name,
            line=dict(color=COLORS["compare"][i % len(COLORS["compare"])], width=2),
        ))
    fig.add_hline(y=0, line=dict(color="rgba(148,163,184,0.2)", width=1))
    fig.update_layout(**CHART_LAYOUT_SIMPLE, height=320, yaxis_title="Performance (%)")
    return fig


def correlation_heatmap(corr_df: pd.DataFrame) -> go.Figure:
    fig = go.Figure(go.Heatmap(
        z=corr_df.values,
        x=corr_df.columns,
        y=corr_df.index,
        colorscale=[[0, "#ef4444"], [0.5, "#1e293b"], [1, "#10b981"]],
        zmin=-1, zmax=1,
        text=np.round(corr_df.values, 2),
        texttemplate="%{text}",
        textfont=dict(size=11),
        showscale=True,
    ))
    fig.update_layout(**CHART_LAYOUT_SIMPLE, height=320)
    return fig


def atr_chart(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["time"], y=df["atr"],
        fill="tozeroy",
        fillcolor="rgba(167,139,250,0.12)",
        line=dict(color=COLORS["atr"], width=1.5),
        name="ATR(14)",
    ))
    fig.update_layout(**CHART_LAYOUT_SIMPLE, height=240)
    return fig


def returns_histogram(returns: pd.Series) -> go.Figure:
    fig = go.Figure(go.Histogram(
        x=returns,
        nbinsx=40,
        marker_color="rgba(59,130,246,0.6)",
        marker_line=dict(color="rgba(59,130,246,0.9)", width=0.5),
    ))
    fig.add_vline(x=0, line=dict(color="rgba(148,163,184,0.4)", width=1))
    fig.update_layout(
        **CHART_LAYOUT_SIMPLE, height=240,
        xaxis_title="Retour (%)", yaxis_title="Fréquence",
    )
    return fig