# ─── ui.py ───────────────────────────────────────────────────────────────────
# Composants HTML/CSS réutilisables (cartes KPI, badges, lignes de classement)
# Modifie ce fichier pour changer l'apparence des composants de l'interface
# ─────────────────────────────────────────────────────────────────────────────

import streamlit as st


# ─── CSS GLOBAL ──────────────────────────────────────────────────────────────
def inject_css() -> None:
    """Injecte tout le CSS personnalisé de l'application."""
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

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
.block-container { padding: 1.5rem 2rem; max-width: 100%; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border-accent);
}
section[data-testid="stSidebar"] .block-container { padding: 1.5rem 1rem; }

/* ── Metric cards ── */
.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border-accent);
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    transition: border-color 0.2s, transform 0.2s;
}
.metric-card:hover { border-color: var(--accent-blue); transform: translateY(-2px); }
.metric-label {
    font-size: 0.72rem; font-family: 'Space Mono', monospace;
    letter-spacing: 0.12em; text-transform: uppercase;
    color: var(--text-muted); margin-bottom: 0.4rem;
}
.metric-value { font-size: 1.6rem; font-weight: 600; color: var(--text-primary); line-height: 1.2; }
.metric-delta { font-size: 0.78rem; font-family: 'Space Mono', monospace; margin-top: 0.3rem; }
.delta-pos { color: var(--accent-green); }
.delta-neg { color: var(--accent-red); }

/* ── Section headers ── */
.section-header {
    display: flex; align-items: center; gap: 0.6rem;
    font-family: 'Space Mono', monospace; font-size: 0.78rem;
    letter-spacing: 0.1em; text-transform: uppercase;
    color: var(--text-muted); border-bottom: 1px solid var(--border);
    padding-bottom: 0.6rem; margin-bottom: 1rem;
}
.section-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--accent-cyan); }

/* ── Top bar ── */
.top-bar {
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 1.5rem; padding-bottom: 1rem;
    border-bottom: 1px solid var(--border-accent);
}
.logo { font-family: 'Space Mono', monospace; font-size: 1.1rem; font-weight: 700; letter-spacing: 0.05em; }
.logo-accent { color: var(--accent-cyan); }
.tagline { font-size: 0.72rem; color: var(--text-muted); font-family: 'Space Mono', monospace; }

/* ── Live badge ── */
.live-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(16,185,129,0.12); border: 1px solid rgba(16,185,129,0.3);
    border-radius: 20px; padding: 4px 12px; font-size: 0.7rem;
    font-family: 'Space Mono', monospace; color: var(--accent-green); letter-spacing: 0.05em;
}
.live-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: var(--accent-green); animation: blink 1.4s infinite;
}
@keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.2} }

/* ── Rank rows ── */
.rank-row {
    display: flex; align-items: center; gap: 0.8rem;
    padding: 0.6rem 0.8rem; border-radius: 8px;
    cursor: pointer; transition: background 0.15s;
}
.rank-row:hover { background: var(--bg-card-hover); }
.rank-num { font-family: 'Space Mono', monospace; font-size: 0.7rem; color: var(--text-muted); width: 18px; text-align: right; }
.symbol-badge { font-family: 'Space Mono', monospace; font-size: 0.78rem; font-weight: 700; color: var(--accent-cyan); width: 80px; }
.price-val { flex: 1; font-size: 0.85rem; text-align: right; color: var(--text-primary); }
.change-val { font-family: 'Space Mono', monospace; font-size: 0.78rem; width: 68px; text-align: right; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0; background: var(--bg-secondary); border-radius: 10px;
    padding: 4px; border: 1px solid var(--border-accent);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 7px; font-family: 'Space Mono', monospace;
    font-size: 0.72rem; letter-spacing: 0.05em;
    color: var(--text-muted); padding: 0.5rem 1.2rem;
}
.stTabs [aria-selected="true"] { background: var(--accent-blue) !important; color: #fff !important; }

/* ── Inputs ── */
.stSelectbox > div > div, .stMultiSelect > div > div {
    background: var(--bg-card) !important; border: 1px solid var(--border-accent) !important;
    border-radius: 8px !important; color: var(--text-primary) !important;
}
.stSlider > div > div > div { background: var(--accent-blue) !important; }

/* ── Misc ── */
.js-plotly-plot .plotly { border-radius: 12px; }
.stDataFrame { border: 1px solid var(--border-accent); border-radius: 10px; overflow: hidden; }

/* ── Signal pills ── */
.signal-pill {
    display: inline-block; padding: 2px 10px; border-radius: 20px;
    font-size: 0.68rem; font-family: 'Space Mono', monospace;
    font-weight: 700; letter-spacing: 0.06em;
}
.signal-buy     { background: rgba(16,185,129,0.15); color: var(--accent-green); border: 1px solid rgba(16,185,129,0.3); }
.signal-sell    { background: rgba(239,68,68,0.15);  color: var(--accent-red);   border: 1px solid rgba(239,68,68,0.3); }
.signal-neutral { background: rgba(148,163,184,0.1); color: var(--text-secondary); border: 1px solid rgba(148,163,184,0.2); }
</style>
""", unsafe_allow_html=True)


# ─── COMPOSANTS RÉUTILISABLES ─────────────────────────────────────────────────

def section_header(label: str) -> None:
    st.markdown(
        f'<div class="section-header"><span class="section-dot"></span>{label}</div>',
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str, delta: str = "", delta_pos: bool = True) -> str:
    """Retourne le HTML d'une carte KPI."""
    delta_class = "delta-pos" if delta_pos else "delta-neg"
    delta_html  = f'<div class="metric-delta {delta_class}">{delta}</div>' if delta else ""
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>"""


def signal_card(indicator: str, signal: str, description: str) -> None:
    """Affiche une carte de signal technique."""
    pill_class = {"BUY": "signal-buy", "SELL": "signal-sell", "NEUTRAL": "signal-neutral"}[signal]
    st.markdown(f"""
    <div style="margin-bottom:1rem;padding:0.9rem;background:var(--bg-card);
                border-radius:10px;border:1px solid var(--border-accent)">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.4rem">
            <span style="font-family:'Space Mono',monospace;font-size:0.7rem;color:var(--text-muted)">{indicator}</span>
            <span class="signal-pill {pill_class}">{signal}</span>
        </div>
        <div style="font-size:0.75rem;color:var(--text-secondary)">{description}</div>
    </div>""", unsafe_allow_html=True)


def stats_box(stats: dict) -> None:
    """Affiche un tableau de statistiques clé/valeur."""
    rows_html = "".join(f"""
    <div style="display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px solid var(--border)">
        <span style="font-size:0.72rem;color:var(--text-muted)">{k}</span>
        <span style="font-size:0.72rem;font-family:'Space Mono',monospace;color:var(--text-primary)">{v}</span>
    </div>""" for k, v in stats.items())
    st.markdown(
        f'<div style="background:var(--bg-card);border:1px solid var(--border-accent);border-radius:10px;padding:0.8rem">{rows_html}</div>',
        unsafe_allow_html=True,
    )


def rank_row(rank: int, symbol: str, price: float, change_pct: float) -> None:
    """Affiche une ligne dans le classement gainers/losers."""
    if change_pct >= 0:
        change_html = f'<span class="change-val delta-pos">▲ {change_pct:.2f}%</span>'
    else:
        change_html = f'<span class="change-val delta-neg">▼ {abs(change_pct):.2f}%</span>'
    st.markdown(f"""
    <div class="rank-row">
        <span class="rank-num">{rank}</span>
        <span class="symbol-badge">{symbol}</span>
        <span class="price-val">${price:,.4f}</span>
        {change_html}
    </div>""", unsafe_allow_html=True)


def top_bar(selected_pair: str, selected_tf: str) -> None:
    """Affiche la barre de titre avec le badge LIVE."""
    st.markdown(f"""
    <div class="top-bar">
        <div>
            <div class="logo">⬡ <span class="logo-accent">CRYPTO</span>VISION
                <span style="font-weight:300">PRO</span>
            </div>
            <div class="tagline">Real-time market intelligence · Binance data feed</div>
        </div>
        <div style="display:flex;align-items:center;gap:12px;">
            <span class="live-badge"><span class="live-dot"></span>LIVE</span>
            <span style="font-family:'Space Mono',monospace;font-size:0.7rem;color:#475569">
                {selected_pair} · {selected_tf.upper()}
            </span>
        </div>
    </div>""", unsafe_allow_html=True)