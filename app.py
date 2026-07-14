from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent / "src"))
from pyrisklab.application_service import run_portfolio_scenario
from pyrisklab.greeks import calculate_greeks
from pyrisklab.scenarios import MARKET_PRESETS, PORTFOLIO_PROFILES, ScenarioInputs

st.set_page_config(
    page_title="PyRiskLab | Portfolio Scenario Explorer", page_icon="◈", layout="wide"
)
st.markdown(
    """<style>
:root{--black:#030303;--panel:#080808;--line:rgba(255,255,255,.22);--soft:rgba(255,255,255,.08);--muted:#8D8D8D;--white:#F5F5F5}
@keyframes scan{from{background-position:0 0}to{background-position:0 80px}}@keyframes reveal{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
*{font-family:"IBM Plex Mono","SFMono-Regular",Consolas,monospace}.stApp{color:var(--white);background-color:var(--black);background-image:linear-gradient(rgba(255,255,255,.018) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.018) 1px,transparent 1px),radial-gradient(circle at 78% 18%,rgba(255,255,255,.055),transparent 25%);background-size:40px 40px,40px 40px,auto;animation:scan 18s linear infinite}
.block-container{max-width:1500px;padding-top:1rem;padding-bottom:4rem}h1,h2,h3{color:#FFF;letter-spacing:.055em;text-transform:uppercase}
.hero{position:relative;min-height:470px;padding:70px clamp(28px,6vw,88px);border:1px solid var(--line);background:radial-gradient(circle at 76% 50%,rgba(255,255,255,.08),transparent 19%),linear-gradient(115deg,#050505 0%,#090909 62%,#030303 100%);margin-bottom:14px;overflow:hidden;animation:reveal .6s ease-out}
.hero:before,.hero:after{content:"";position:absolute;width:42px;height:42px;z-index:3}.hero:before{left:-1px;top:-1px;border-left:2px solid #fff;border-top:2px solid #fff}.hero:after{right:-1px;bottom:-1px;border-right:2px solid #fff;border-bottom:2px solid #fff}
.hero-grid{position:relative;z-index:1;display:grid;grid-template-columns:1.35fr .65fr;gap:50px;align-items:center}.eyebrow{display:flex;align-items:center;gap:10px;color:#999;font-size:.66rem;letter-spacing:.18em;text-transform:uppercase}.eyebrow:before,.eyebrow:after{content:"";height:1px;background:rgba(255,255,255,.45)}.eyebrow:before{width:32px}.eyebrow:after{width:90px}.pulse{width:4px;height:4px;background:#fff;border-radius:50%}.hero h1{font-size:clamp(2.35rem,3.7vw,4.25rem);line-height:1.03;font-weight:700;letter-spacing:.07em;margin:28px 0 22px}.gradient-word{display:block;color:#BDBDBD;white-space:nowrap}.hero p{max-width:650px;color:#A0A0A0;font-size:.91rem;line-height:1.9;border-left:1px solid rgba(255,255,255,.4);padding-left:18px}
.trust-card{position:relative;border:1px solid var(--line);background:repeating-linear-gradient(0deg,transparent 0,transparent 3px,rgba(255,255,255,.018) 4px);padding:28px}.trust-card:before{content:"RISK // ENGINE";position:absolute;right:12px;top:10px;color:#4A4A4A;font-size:.55rem;letter-spacing:.18em}.trust-label{font-size:.62rem;letter-spacing:.17em;color:#777;text-transform:uppercase}.trust-value{font-size:2rem;font-weight:700;margin:15px 0 5px}.trust-sub{font-size:.72rem;color:#888}.micro-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:0;margin-top:28px;padding-top:20px;border-top:1px solid var(--line)}.micro-grid div{border-right:1px solid var(--soft);padding-left:12px}.micro-grid div:first-child{padding-left:0}.micro-grid div:last-child{border:0}.micro-grid b{display:block;font-size:.95rem}.micro-grid span{font-size:.53rem;color:#666;text-transform:uppercase;letter-spacing:.1em}
[data-testid="stMetric"]{position:relative;background:#070707;border:1px solid var(--line);padding:20px;min-height:118px;box-shadow:none;animation:reveal .5s ease-out}[data-testid="stMetric"]:before{content:"";position:absolute;left:-1px;top:-1px;width:9px;height:9px;border-left:1px solid #fff;border-top:1px solid #fff}[data-testid="stMetricLabel"]{color:#808080;text-transform:uppercase;letter-spacing:.09em;font-size:.68rem}[data-testid="stMetricValue"]{letter-spacing:-.03em}
[data-testid="stSidebar"]{background:#050505;border-right:1px solid var(--line)}[data-testid="stSidebar"] h2{font-size:1.15rem;letter-spacing:.08em}.disclaimer{padding:10px 14px;background:#050505;border:1px solid var(--line);color:#999;font-size:.72rem;letter-spacing:.03em}
.stButton>button{border-radius:0;font-weight:700;border:1px solid #fff;letter-spacing:.08em;text-transform:uppercase;transition:all .16s}.stButton>button:hover{background:#fff!important;color:#000!important}.stButton>button[kind="primary"]{background:transparent;color:#fff;border-color:#fff}
div[data-testid="stTabs"]{border-top:1px solid var(--line)}div[data-testid="stTabs"] button{font-weight:650;color:#777;letter-spacing:.05em;text-transform:uppercase;font-size:.72rem}div[data-testid="stTabs"] button[aria-selected="true"]{color:#FFF}.stPlotlyChart,.stDataFrame{border:1px solid var(--line);border-radius:0;overflow:hidden;background:#050505;padding:5px}details{border:1px solid var(--line)!important;border-radius:0!important;background:#050505!important}
@media(max-width:900px){.hero-grid{grid-template-columns:1fr}.hero{min-height:0;padding:52px 32px}.trust-card{max-width:500px}}@media(max-width:700px){.hero{padding:42px 20px}.hero h1{font-size:2.25rem;letter-spacing:.05em}.block-container{padding:.65rem}.trust-card{display:none}.hero p{font-size:.78rem}}
</style>""",
    unsafe_allow_html=True,
)

st.markdown(
    """<div class="hero"><div class="hero-grid"><div><div class="eyebrow"><span class="pulse"></span> PRL // 001</div><h1>MODEL<br><span class="gradient-word">UNCERTAINTY</span></h1><p>PYRISKLAB // A reproducible portfolio scenario instrument. Inspect simulated outcomes, option sensitivities, and every risk decision without mistaking a model for a forecast.</p></div><div class="trust-card"><div class="trust-label">SYSTEM.STATUS</div><div class="trust-value">ENGINE ACTIVE</div><div class="trust-sub">500 PATHS // SEED 42 // LOCAL MODEL</div><div class="micro-grid"><div><b>05</b><span>Modules</span></div><div><b>100%</b><span>Traceable</span></div><div><b>00</b><span>Live trades</span></div></div></div></div></div>""",
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="disclaimer">ⓘ Educational simulation only. Results are generated from assumptions and random scenarios, not forecasts or investment advice.</div>',
    unsafe_allow_html=True,
)

if "result" not in st.session_state:
    st.session_state.result = run_portfolio_scenario(ScenarioInputs())
if "comparison" not in st.session_state:
    st.session_state.comparison = None

with st.sidebar:
    st.markdown("## Configure scenario")
    preset = st.selectbox(
        "Market environment",
        MARKET_PRESETS,
        help="A preset fills drift, volatility, and seed. You can refine them below.",
    )
    profile = st.segmented_control(
        "Portfolio profile",
        list(PORTFOLIO_PROFILES),
        default="Balanced Growth",
        help=(
            "A quick allocation template. Capital Preservation holds the most cash; "
            "Growth Focused allocates more to stocks and options. You can edit the percentages below."
        ),
    )
    capital = st.number_input(
        "Starting capital ($)",
        1_000,
        1_000_000,
        10_000,
        1_000,
        help="The hypothetical amount available at the beginning of the simulation. No real money is used.",
    )
    horizon_label = st.select_slider(
        "Investment horizon",
        ["1 month", "6 months", "1 year", "3 years", "5 years"],
        value="1 year",
        help="How long each simulated portfolio path runs. Longer horizons contain more trading-day steps.",
    )
    horizon = {"1 month": 21, "6 months": 126, "1 year": 252, "3 years": 756, "5 years": 1260}[
        horizon_label
    ]
    paths = st.selectbox(
        "Simulation paths",
        [100, 500, 1000, 5000],
        index=1,
        help=(
            "The number of independent hypothetical market journeys generated. More paths make "
            "percentile estimates smoother but require more computation."
        ),
    )
    allocations = PORTFOLIO_PROFILES[profile or "Balanced Growth"]
    st.caption("Allocation · profile defaults")
    cash_pct = st.slider(
        "Cash (%)",
        0,
        100,
        allocations[0],
        help="The portion kept unchanged as cash. It reduces market exposure but does not earn interest in this model.",
    )
    stock_pct = st.slider(
        "Stock (%)",
        0,
        100,
        allocations[1],
        help="The portion invested in the simulated stock using fractional shares.",
    )
    option_pct = 100 - cash_pct - stock_pct
    if option_pct < 0:
        st.error("Cash and stock cannot exceed 100%.")
    else:
        st.markdown(f"**Options: {option_pct}%** · ${capital * option_pct / 100:,.0f}")
        st.caption(
            "Options receive the percentage left after cash and stock; all three allocations total 100%."
        )
    with st.expander("Advanced model assumptions"):
        st.caption(
            "Technical settings control how synthetic prices and option values are generated."
        )
        p = MARKET_PRESETS[preset]
        initial_price = st.number_input(
            "Initial stock price ($)",
            1.0,
            10000.0,
            100.0,
            help="The synthetic stock price at the first simulation date. It is not a live market quote.",
        )
        drift = (
            st.number_input(
                "Model drift (%)",
                -50.0,
                50.0,
                p["drift"] * 100,
                1.0,
                help=(
                    "The assumed annual direction of the synthetic price process. This is a model input, "
                    "not an expected or promised investment return."
                ),
            )
            / 100
        )
        vol = (
            st.slider(
                "Market uncertainty · annual volatility (%)",
                0,
                80,
                int(p["volatility"] * 100),
                help=(
                    "The assumed annual variability of stock returns. Higher volatility creates a wider "
                    "range of simulated gains and losses."
                ),
            )
            / 100
        )
        seed = st.number_input(
            "Random seed",
            0,
            999999,
            p["seed"],
            help="A reproducibility code. The same seed and inputs generate the same simulated paths.",
        )
        option_type = st.segmented_control(
            "European option type",
            ["call", "put"],
            default="call",
            help="A call gains modeled value as the stock rises; a put gains modeled value as the stock falls. Exercise is only at expiry.",
        )
        strike = st.number_input(
            "Option strike ($)",
            1.0,
            10000.0,
            105.0,
            help="The fixed price used to determine the option payoff at expiry.",
        )
        option_vol = (
            st.slider(
                "Option volatility (%)",
                1,
                100,
                22,
                help="The volatility supplied to Black-Scholes option pricing. It can differ from stock-path volatility for experimentation.",
            )
            / 100
        )
        max_notional = st.number_input(
            "Maximum trade notional ($)",
            1000.0,
            1000000.0,
            25000.0,
            help="The largest dollar exposure a single simulated allocation decision may create. Larger proposals are blocked.",
        )
        max_dd = st.slider(
            "Maximum drawdown stop (%)",
            1,
            90,
            20,
            help="The permitted decline from a previous portfolio peak before the configured risk stop is considered breached.",
        )
    inputs = ScenarioInputs(
        preset,
        capital,
        horizon,
        paths,
        initial_price,
        drift,
        vol,
        int(seed),
        cash_pct,
        stock_pct,
        max(option_pct, 0),
        option_type or "call",
        strike,
        option_vol,
        0.04,
        min(horizon, 504),
        max_notional,
        max_dd,
    )
    errors = inputs.validate()
    if errors:
        for e in errors:
            st.error(e)
    run = st.button(
        "Run scenario  →", type="primary", use_container_width=True, disabled=bool(errors)
    )
    if run:
        with st.status("Building scenario…", expanded=True) as status:
            st.write("✓ Inputs validated")
            st.write(f"✓ Simulating {paths:,} market paths")
            st.session_state.result = run_portfolio_scenario(inputs)
            st.write("✓ Calculating outcomes and risk decisions")
            status.update(label="Scenario ready", state="complete", expanded=False)
    st.caption(
        f"Active result · seed {st.session_state.result.inputs.seed} · {st.session_state.result.inputs.paths:,} paths"
    )

r = st.session_state.result
s = r.summary
a = r.analytics
rep = r.representative
tabs = st.tabs(["Overview", "Risk & Decisions", "Greeks Lab", "Compare", "How It Works"])
with tabs[0]:
    cols = st.columns(3)
    cols[0].metric("Starting capital", f"${s['starting_capital']:,.0f}")
    cols[1].metric(
        "Median ending value", f"${s['median_ending']:,.0f}", f"{s['median_return']:+.1%}"
    )
    cols[2].metric("Median simulated return", f"{s['median_return']:+.1%}")
    cols = st.columns(3)
    cols[0].metric("Probability below start", f"{s['probability_below_start']:.1%}")
    cols[1].metric("Representative max drawdown", f"{s['max_drawdown']:.1%}")
    cols[2].metric(
        "10th–90th outcome range", f"USD {s['p10_ending']:,.0f} – {s['p90_ending']:,.0f}"
    )
    st.markdown("### Portfolio projection")
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x=r.dates, y=a["p90"], line=dict(width=0), showlegend=False, hoverinfo="skip")
    )
    fig.add_trace(
        go.Scatter(
            x=r.dates,
            y=a["p10"],
            fill="tonexty",
            fillcolor="rgba(255,255,255,.10)",
            line=dict(width=0),
            name="10th–90th percentile band",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=r.dates, y=a["median"], line=dict(color="#F5F5F5", width=2), name="Median portfolio"
        )
    )
    for idx, label, color in [
        (0, "Start", "#0B1F33"),
        (a["high_idx"], "High", "#D4D4D4"),
        (a["low_idx"], "Low", "#666666"),
        (len(r.dates) - 1, "End", "#FFFFFF"),
    ]:
        fig.add_trace(
            go.Scatter(
                x=[r.dates[idx]],
                y=[a["representative"][idx]],
                mode="markers+text",
                text=[label],
                textposition="top center",
                marker=dict(size=10, color=color),
                name=f"Representative · {label}",
                showlegend=False,
                hovertemplate=f"{label}<br>%{{x|%b %d, %Y}}<br>$%{{y:,.2f}}<extra></extra>",
            )
        )
    fig.update_layout(
        height=470,
        hovermode="x unified",
        margin=dict(l=10, r=10, t=15, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#A1A1AA"),
        yaxis_title="Portfolio value ($)",
        legend=dict(orientation="h", y=1.08),
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor="rgba(255,255,255,.08)"),
    )
    st.plotly_chart(fig, use_container_width=True)
    c1, c2 = st.columns([1.7, 1])
    with c1:
        st.markdown("### Ending-value distribution")
        hist = go.Figure(
            go.Histogram(
                x=a["ending"],
                marker_color="#BDBDBD",
                opacity=0.82,
                nbinsx=35,
                hovertemplate="$%{x:,.0f}<br>%{y} paths<extra></extra>",
            )
        )
        hist.add_vline(
            x=r.inputs.starting_capital,
            line_color="#FFFFFF",
            line_dash="dash",
            annotation_text="Starting capital",
        )
        hist.update_layout(
            height=330,
            margin=dict(l=10, r=10, t=15, b=10),
            xaxis_title="Ending value ($)",
            yaxis_title="Number of paths",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#A1A1AA"),
        )
        st.plotly_chart(hist, use_container_width=True)
    with c2:
        st.markdown("### Where the ending value came from")
        rc = r.reconciliation
        st.markdown(
            f"The representative path ends at <strong>&#36;{rc['ending_value']:,.2f}</strong>: "
            f"remaining cash of <strong>&#36;{rc['cash']:,.2f}</strong>, plus "
            f"<strong>&#36;{rc['stock_value']:,.2f}</strong> in fractional stock holdings and "
            f"<strong>&#36;{rc['option_value']:,.2f}</strong> in modeled option value.",
            unsafe_allow_html=True,
        )
        st.caption(
            f"Holdings: {rc['shares']:.3f} shares and {rc['contracts']:.3f} option contracts. Fractional holdings are supported for educational allocation precision."
        )
        with st.expander("How was this calculated?"):
            st.latex(r"V_t = Cash + Shares \times S_t + Contracts \times 100 \times OptionPrice_t")
            st.write(
                "Option prices use the existing `pyrisklab.pricing.black_scholes_price` implementation. All charts and KPIs read from the same structured scenario result."
            )
with tabs[1]:
    st.markdown("## Risk & Decisions")
    accepted = int((r.risk_decisions.status == "ACCEPTED").sum())
    blocked = len(r.risk_decisions) - accepted
    c = st.columns(4)
    c[0].metric("Proposed", len(r.risk_decisions))
    c[1].metric("Accepted", accepted)
    c[2].metric("Blocked", blocked)
    c[3].metric("Executed", accepted)
    status_filter = st.multiselect(
        "Filter by decision status", ["ACCEPTED", "BLOCKED"], default=["ACCEPTED", "BLOCKED"]
    )
    view = r.risk_decisions[r.risk_decisions.status.isin(status_filter)].copy()
    st.dataframe(
        view,
        column_config={
            "notional": st.column_config.NumberColumn("Notional", format="$%.2f"),
            "observed": st.column_config.NumberColumn("Observed value", format="$%.2f"),
            "status": st.column_config.TextColumn("Decision status"),
        },
        hide_index=True,
        use_container_width=True,
    )
    st.info(
        view.iloc[0].explanation if not view.empty else "No decisions match the selected filter."
    )
with tabs[2]:
    st.markdown("## Greeks sensitivity lab")
    st.write(
        "Explore how the existing Black–Scholes model responds as the simulated stock price changes."
    )
    spots = np.linspace(r.inputs.initial_price * 0.55, r.inputs.initial_price * 1.45, 120)
    gs = calculate_greeks(
        spots,
        r.inputs.strike,
        r.inputs.option_expiry_days / 252,
        r.inputs.risk_free_rate,
        r.inputs.option_volatility,
        r.inputs.option_type,
    )
    greek = st.segmented_control(
        "Sensitivity", ["delta", "gamma", "vega", "theta", "rho"], default="delta"
    )
    gfig = go.Figure(
        go.Scatter(x=spots, y=gs[greek], line=dict(color="#F5F5F5", width=2), name=greek.title())
    )
    gfig.add_vline(
        x=r.inputs.initial_price,
        line_color="#888888",
        line_dash="dash",
        annotation_text="Current input",
    )
    gfig.update_layout(
        height=430,
        xaxis_title="Underlying stock price ($)",
        yaxis_title=greek.title(),
        margin=dict(l=10, r=10, t=20, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#A1A1AA"),
    )
    st.plotly_chart(gfig, use_container_width=True)
    st.markdown(" ".join([f"**{k.title()}** {v:.4f}　" for k, v in r.greeks.items()]))
    st.caption(
        "Delta: price change per $1 move · Gamma: delta curvature · Vega: change per 1 volatility point · Theta: daily time decay · Rho: change per 1 interest-rate point."
    )
with tabs[3]:
    st.markdown("## Compare scenarios")
    st.write(
        "Save the active result, adjust assumptions in the sidebar, run again, then compare outcomes."
    )
    if st.button("Save active scenario for comparison"):
        st.session_state.comparison = r
    other = st.session_state.comparison
    if other:
        comparison = pd.DataFrame(
            {
                r.inputs.name: [
                    s["median_ending"],
                    s["median_return"],
                    s["probability_below_start"],
                    s["max_drawdown"],
                ],
                other.inputs.name: [
                    other.summary["median_ending"],
                    other.summary["median_return"],
                    other.summary["probability_below_start"],
                    other.summary["max_drawdown"],
                ],
            },
            index=[
                "Median ending value",
                "Median return",
                "Probability below start",
                "Representative max drawdown",
            ],
        )
        st.dataframe(comparison, use_container_width=True)
        cf = go.Figure()
        cf.add_trace(
            go.Scatter(
                x=r.dates,
                y=a["median"],
                name=f"Active · {r.inputs.name}",
                line=dict(color="#F5F5F5", width=2),
            )
        )
        cf.add_trace(
            go.Scatter(
                x=other.dates,
                y=other.analytics["median"],
                name=f"Saved · {other.inputs.name}",
                line=dict(color="#777777", width=2, dash="dash"),
            )
        )
        cf.update_layout(
            height=430,
            yaxis_title="Median portfolio value ($)",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#A1A1AA"),
        )
        st.plotly_chart(cf, use_container_width=True)
    else:
        st.info("No saved comparison yet. Save this result, then run another scenario.")
with tabs[4]:
    st.markdown("## How it works")
    st.markdown(
        "**Browser controls → validated scenario service → GBM market paths → existing Black–Scholes & Greeks engine → tested analytics → Plotly explanations**"
    )
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Model assumptions")
        st.write(
            f"Synthetic geometric Brownian motion · {r.inputs.horizon_days} trading steps · {r.inputs.paths:,} paths · {r.inputs.volatility:.1%} annual volatility · {r.inputs.drift:.1%} drift · seed {r.inputs.seed}."
        )
        st.write(
            "European options, 252 trading days/year, 100-share contract multiplier, no liquidity effects or slippage. Buy-and-hold allocation with fractional shares and contracts."
        )
    with c2:
        st.markdown("#### Reproducible by design")
        st.write(
            "The random seed and complete validated configuration travel with every result. The same inputs produce the same simulated paths."
        )
        st.download_button(
            "Download active configuration (JSON)",
            json.dumps(r.inputs.to_dict(), indent=2),
            f"pyrisklab-{r.inputs.name.lower().replace(' ', '-')}.json",
            "application/json",
            use_container_width=True,
        )
        st.download_button(
            "Download representative path (CSV)",
            r.representative.to_csv(index=False),
            "representative-path.csv",
            "text/csv",
            use_container_width=True,
        )
    with st.expander("Technical formulas and limitations"):
        st.latex(r"S_{t+1}=S_t\exp((\mu-\frac{1}{2}\sigma^2)\Delta t+\sigma\sqrt{\Delta t}Z_t)")
        st.latex(r"Drawdown_t=\frac{V_t-Peak_t}{Peak_t}")
        st.write(
            "Percentile bands are cross-sectional quantiles at each date. Maximum drawdown is path-specific and explicitly labeled. This demonstration does not use real market data and does not predict returns."
        )
st.caption(
    "PyRiskLab · Simulation-only portfolio project · Python, NumPy, SciPy, pandas, Streamlit, Plotly, pytest"
)
