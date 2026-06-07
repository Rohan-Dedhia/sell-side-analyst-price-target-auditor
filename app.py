import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ────────────────────────────────────────
st.set_page_config(
    page_title="Sell-Side Analyst Auditor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Bloomberg dark theme CSS ───────────────────────────
st.markdown("""
<style>
  .stApp { background-color: #0B1929; }
  section[data-testid="stSidebar"] { background-color: #0D1F33; }

  h1,h2,h3,h4 { color: #E8EDF2; font-family: 'Segoe UI', sans-serif; }
  p, li       { color: #B8C8D8; }
  label       { color: #B8C8D8 !important; }

  div[data-testid="metric-container"] {
    background-color: #132B45;
    border: 1px solid #1E3A5F;
    border-radius: 8px;
    padding: 16px 20px;
  }
  div[data-testid="metric-container"] label {
    color: #7A9BB5 !important; font-size: 12px;
  }
  div[data-testid="metric-container"] div {
    color: #00A3E0 !important; font-size: 26px; font-weight: 600;
  }

  .stTabs [data-baseweb="tab-list"] {
    background-color: #0D1F33;
    border-bottom: 1px solid #1E3A5F;
    gap: 4px;
  }
  .stTabs [data-baseweb="tab"] {
    color: #7A9BB5; font-size: 13px; font-weight: 500;
    padding: 10px 20px; border-radius: 4px 4px 0 0;
  }
  .stTabs [aria-selected="true"] {
    background-color: #132B45 !important;
    color: #00A3E0 !important;
    border-bottom: 2px solid #00A3E0 !important;
  }

  .stDataFrame { border: 1px solid #1E3A5F; border-radius: 6px; }
  div[data-testid="stDataFrameResizable"] {
    background-color: #0D1F33;
  }

  .finding-card {
    background-color: #132B45;
    border-left: 3px solid #00A3E0;
    border-radius: 0 6px 6px 0;
    padding: 12px 16px;
    margin-bottom: 10px;
  }
  .finding-card span { color: #00A3E0; font-weight: 600; }
  .finding-card p    { color: #B8C8D8; margin: 4px 0 0; font-size: 13px; }
</style>
""", unsafe_allow_html=True)

# ── Load data ──────────────────────────────────────────
@st.cache_data
def load_data():
    firm   = pd.read_csv("outputs/firm_accuracy.csv")
    yearly = pd.read_csv("outputs/yearly_accuracy.csv")
    regime = pd.read_csv("outputs/regime_accuracy.csv")
    analyst = pd.read_csv("outputs/analyst_accuracy.csv")
    return firm, yearly, regime, analyst

firm, yearly, regime, analyst = load_data()

# ── Header ─────────────────────────────────────────────
st.markdown("## 📊 Sell-Side Analyst Price Target Auditor")
st.markdown(
    "<p style='color:#7A9BB5; margin-top:-10px; font-size:14px'>"
    "24 years · 734,331 graded forecasts · 771 US stocks · 2001–2024"
    "</p>", unsafe_allow_html=True
)
st.divider()

# ── Tabs ───────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "  Overview  ",
    "  Firm Rankings  ",
    "  Time Trends  ",
    "  Analyst Leaderboards  "
])

# ══════════════════════════════════════════════════════
# TAB 1 - OVERVIEW
# ══════════════════════════════════════════════════════
with tab1:

    # ── Methodology credibility bar ────────────────────
    st.markdown("""
    <div style="background:#0D1F33;border:1px solid #1E3A5F;border-radius:8px;
                padding:14px 20px;display:flex;gap:40px;margin-bottom:20px;
                flex-wrap:wrap;">
      <div><div style="color:#00A3E0;font-size:18px;font-weight:600">WRDS IBES</div>
           <div style="color:#7A9BB5;font-size:11px">Data Source</div></div>
      <div><div style="color:#00A3E0;font-size:18px;font-weight:600">734K</div>
           <div style="color:#7A9BB5;font-size:11px">Graded Forecasts</div></div>
      <div><div style="color:#00A3E0;font-size:18px;font-weight:600">2001–2024</div>
           <div style="color:#7A9BB5;font-size:11px">24 Years of History</div></div>
      <div><div style="color:#00A3E0;font-size:18px;font-weight:600">12-Month</div>
           <div style="color:#7A9BB5;font-size:11px">Forecast Horizon</div></div>
      <div><div style="color:#00A3E0;font-size:18px;font-weight:600">771</div>
           <div style="color:#7A9BB5;font-size:11px">US Stocks</div></div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI cards ──────────────────────────────────────
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Forecasts Graded",    "734K")
    col2.metric("Avg Forecast Bias",   "+33.2pp")
    col3.metric("Directional Accuracy","64.6%")
    col4.metric("Years of History",    "24 Years")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Year-by-year bias trend chart ──────────────────
    st.markdown("#### 24-Year Analyst Bias Trend")

    events = {
        2001: "Dot-com bust", 2007: "Pre-GFC peak",
        2008: "GFC",          2020: "COVID",
        2022: "Bear market"
    }

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=yearly["year"], y=yearly["Bias(pp)"],
        mode="lines+markers",
        line=dict(color="#00A3E0", width=2.5),
        marker=dict(size=5, color="#00A3E0"),
        name="Forecast Bias (pp)",
        hovertemplate="<b>%{x}</b><br>Bias: %{y:.1f}pp<extra></extra>"
    ))

    fig.add_trace(go.Scatter(
        x=yearly["year"], y=yearly["Dir.Acc(%)"],
        mode="lines",
        line=dict(color="#F0A500", width=1.5, dash="dot"),
        name="Directional Accuracy (%)",
        hovertemplate="<b>%{x}</b><br>Dir. Acc: %{y:.1f}%<extra></extra>",
        yaxis="y2"
    ))

    fig.add_hline(y=0, line_dash="dash",
                  line_color="#3A5A7A", line_width=1)

    for yr, label in events.items():
        fig.add_vline(x=yr, line_dash="dot",
                      line_color="#3A5A7A", line_width=1)
        fig.add_annotation(
            x=yr, y=115, text=label,
            showarrow=False, textangle=-90,
            font=dict(size=9, color="#7A9BB5"),
            xanchor="left"
        )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0D1F33",
        plot_bgcolor="#0D1F33",
        height=320,
        margin=dict(l=40, r=40, t=20, b=40),
        legend=dict(
            orientation="h", y=-0.15,
            font=dict(color="#B8C8D8", size=11)
        ),
        xaxis=dict(
            showgrid=False,
            color="#7A9BB5",
            tickfont=dict(size=11)
        ),
        yaxis=dict(
    title=dict(
        text="Bias (pp)",
        font=dict(color="#00A3E0", size=11)
    ),
    tickfont=dict(color="#7A9BB5", size=11),
    showgrid=True,
    gridcolor="#1E3A5F"
),
        yaxis2=dict(
    title=dict(
        text="Dir. Accuracy (%)",
        font=dict(color="#F0A500", size=11)
    ),
    tickfont=dict(color="#7A9BB5", size=11),
    overlaying="y",
    side="right",
    showgrid=False,
    range=[0, 100]
),
    )

    st.plotly_chart(fig, use_container_width=True)

    # ── Research conclusion box ────────────────────────
    st.markdown("""
    <div style="background:#0A2540;border:1px solid #00A3E0;border-radius:8px;
                padding:16px 20px;margin:8px 0 20px;">
      <div style="color:#00A3E0;font-size:12px;font-weight:600;
                  letter-spacing:.08em;margin-bottom:6px">
        KEY RESEARCH CONCLUSION
      </div>
      <div style="color:#E8EDF2;font-size:14px;line-height:1.6">
        Sell-side analysts remain directionally useful
        <span style="color:#00A3E0;font-weight:600">(64.6% accuracy)</span>
        but systematically overestimate future returns by
        <span style="color:#F0A500;font-weight:600">33 percentage points</span>
        on average a bias that is worst during market downturns,
        precisely when accurate guidance matters most.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Key findings cards ─────────────────────────────
    st.markdown("#### Key Findings")

    findings = [
        ("Analyst optimism collapsed over two decades",
         "Average forecast bias declined from 118.5pp in 2001 to approximately 1pp in 2023–24 a dramatic improvement in calibration over time."),
        ("Accuracy collapses precisely when it matters most",
         "In 2007, directional accuracy fell to 32.5% worse than a coin flip as analysts remained unanimously bullish heading into the GFC."),
        ("2020: the only year analysts were too bearish",
         "COVID caused analysts to slash targets conservatively just before the V-shaped recovery. Actual returns hit +63.5% while bias turned negative at −30.5pp."),
        ("Independent research firms often outperform bulge-bracket banks",
         "Evercore ISI and Wolfe Research outperform larger banks on accuracy, suggesting independence from investment banking creates better forecasting incentives."),
        ("Best analyst in 23 years of data: MOTEMADEN D (Evercore ISI)",
         "220 forecasts · 14.9pp MAE · 83.6% directional accuracy · near-zero systematic bias. Buried in a dataset nobody else has built."),
    ]

    for title, body in findings:
        st.markdown(
            f'<div class="finding-card"><span>{title}</span>'
            f'<p>{body}</p></div>',
            unsafe_allow_html=True
        )

with tab2:

    # ── Methodology card ───────────────────────────────
    st.markdown("""
    <div style="background:#0D1F33;border:1px solid #1E3A5F;border-radius:8px;
                padding:12px 20px;margin-bottom:16px;display:flex;
                gap:32px;flex-wrap:wrap;align-items:center;">
      <div style="color:#7A9BB5;font-size:11px;font-weight:600;
                  letter-spacing:.08em;">METHODOLOGY</div>
      <div style="color:#B8C8D8;font-size:12px">WRDS IBES Dataset</div>
      <div style="color:#B8C8D8;font-size:12px">734K Graded Forecasts</div>
      <div style="color:#B8C8D8;font-size:12px">24 Years (2001-2024)</div>
      <div style="color:#B8C8D8;font-size:12px">12-Month Forecast Horizon</div>
      <div style="color:#B8C8D8;font-size:12px">
        Accuracy measured against realized 12-month returns
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Research takeaways ─────────────────────────────
    st.markdown("#### Firm-Level Accuracy Rankings")

    takeaways = [
        ("Wolfe Research shows the lowest systematic bias (17.6pp)",
         "Independent research firms with no investment banking conflicts set more realistic targets."),
        ("All 23 firms remain positively biased none are conservative",
         "Structural incentives ensure every firm overshoots. The question is only by how much."),
        ("Evercore ISI combines low bias (19.5pp) with strong directional accuracy (64.1%)",
         "The most well-rounded firm in the dataset across both accuracy dimensions."),
        ("Lehman Brothers shows the largest historical optimism (88.6pp)",
         "Targets issued before the 2008 collapse were never realised, inflating their bias permanently."),
        ("Independent research firms consistently outperform bulge-bracket banks",
         "Freed from investment banking relationships, boutique and independent firms set tighter targets."),
    ]

    cols = st.columns(2)
    for i, (title, body) in enumerate(takeaways):
        with cols[i % 2]:
            st.markdown(
                f'<div class="finding-card"><span>{title}</span>'
                f'<p>{body}</p></div>',
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Executive KPI cards (HTML no truncation)
    firm_named = firm[firm["firm_name"] != "Boutique/Other"].copy()

    lowest_bias  = firm_named.loc[firm_named["Bias(pp)"].idxmin()]
    highest_dir  = firm_named.loc[firm_named["Dir.Acc(%)"].idxmax()]
    lowest_mae   = firm_named.loc[firm_named["MAE(pp)"].idxmin()]
    most_bullish = firm_named.loc[firm_named["Bias(pp)"].idxmax()]

    def kpi_card(label, name, value):
        return f"""
        <div style="background:#132B45;border:1px solid #1E3A5F;
                    border-radius:8px;padding:14px 16px;">
          <div style="color:#7A9BB5;font-size:11px;font-weight:500;
                      margin-bottom:6px;letter-spacing:.04em">{label}</div>
          <div style="color:#E8EDF2;font-size:13px;font-weight:600;
                      line-height:1.4;word-break:break-word">{name}</div>
          <div style="color:#00A3E0;font-size:12px;margin-top:5px">{value}</div>
        </div>"""

    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(kpi_card(
        "LOWEST BIAS FIRM",
        lowest_bias["firm_name"],
        f"{lowest_bias['Bias(pp)']:.1f}pp bias"
    ), unsafe_allow_html=True)
    k2.markdown(kpi_card(
        "BEST DIRECTIONAL ACCURACY",
        highest_dir["firm_name"],
        f"{highest_dir['Dir.Acc(%)']:.1f}% accuracy"
    ), unsafe_allow_html=True)
    k3.markdown(kpi_card(
        "LOWEST MAE FIRM",
        lowest_mae["firm_name"],
        f"{lowest_mae['MAE(pp)']:.1f}pp MAE"
    ), unsafe_allow_html=True)
    k4.markdown(kpi_card(
        "MOST BULLISH FIRM",
        most_bullish["firm_name"],
        f"{most_bullish['Bias(pp)']:.1f}pp bias"
    ), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts ─────────────────────────────────────────
    col1, col2 = st.columns(2)
    firm_bias = firm_named.sort_values("Bias(pp)", ascending=False)
    firm_dir  = firm_named.sort_values("Dir.Acc(%)", ascending=False)

    with col1:
        st.markdown("##### Independent Firms Show the Lowest Forecast Bias")
        st.markdown(
            "<p style='color:#7A9BB5;font-size:12px;margin-top:-8px'>"
            "Lower bias indicates analysts set more realistic price targets. "
            "Dashed line shows dataset average (33.2pp).</p>",
            unsafe_allow_html=True
        )
        bar_colors = [
            "#FF4B4B" if b > 50 else
            "#F0A500" if b > 33 else
            "#00A3E0"
            for b in firm_bias["Bias(pp)"]
        ]
        fig_bias = go.Figure(go.Bar(
            x=firm_bias["Bias(pp)"],
            y=firm_bias["firm_name"],
            orientation="h",
            marker_color=bar_colors,
            text=[f"{b:.1f}pp" for b in firm_bias["Bias(pp)"]],
            textposition="outside",
            textfont=dict(color="#B8C8D8", size=10),
            hovertemplate="<b>%{y}</b><br>Bias: %{x:.1f}pp<extra></extra>"
        ))
        fig_bias.add_vline(x=33.2, line_dash="dash",
                           line_color="#F0A500", line_width=1.5)
        fig_bias.add_annotation(
            x=33.2, y=0, text="Avg 33.2pp",
            showarrow=False,
            font=dict(size=9, color="#F0A500"),
            xanchor="left", yanchor="bottom"
        )
        fig_bias.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0D1F33", plot_bgcolor="#0D1F33",
            height=560, margin=dict(l=10, r=80, t=10, b=30),
            showlegend=False,
            xaxis=dict(title="Forecast Bias (pp)",
                       title_font=dict(color="#7A9BB5", size=11),
                       tickfont=dict(color="#7A9BB5", size=10),
                       showgrid=True, gridcolor="#1E3A5F"),
            yaxis=dict(tickfont=dict(color="#B8C8D8", size=10),
                       showgrid=False)
        )
        st.plotly_chart(fig_bias, use_container_width=True)

    with col2:
        st.markdown("##### Directional Accuracy Differs Far Less Than Bias")
        st.markdown(
            "<p style='color:#7A9BB5;font-size:12px;margin-top:-8px'>"
            "Higher directional accuracy means analysts correctly predicted "
            "stock direction more often. Lines show 50% random and 64.6% average.</p>",
            unsafe_allow_html=True
        )
        dir_colors = [
            "#00C49A" if d >= 67 else
            "#00A3E0" if d >= 63 else
            "#F0A500"
            for d in firm_dir["Dir.Acc(%)"]
        ]
        fig_dir = go.Figure(go.Bar(
            x=firm_dir["Dir.Acc(%)"],
            y=firm_dir["firm_name"],
            orientation="h",
            marker_color=dir_colors,
            text=[f"{d:.1f}%" for d in firm_dir["Dir.Acc(%)"]],
            textposition="outside",
            textfont=dict(color="#B8C8D8", size=10),
            hovertemplate="<b>%{y}</b><br>Dir. Acc: %{x:.1f}%<extra></extra>"
        ))
        fig_dir.add_vline(x=50,   line_dash="dash",
                          line_color="#3A5A7A", line_width=1)
        fig_dir.add_vline(x=64.6, line_dash="dash",
                          line_color="#F0A500", line_width=1.5)
        fig_dir.add_annotation(x=50.5, y=0, text="50% random",
            showarrow=False, font=dict(size=9, color="#7A9BB5"),
            xanchor="left", yanchor="bottom")
        fig_dir.add_annotation(x=65.1, y=0, text="Avg 64.6%",
            showarrow=False, font=dict(size=9, color="#F0A500"),
            xanchor="left", yanchor="bottom")
        fig_dir.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0D1F33", plot_bgcolor="#0D1F33",
            height=560, margin=dict(l=10, r=80, t=10, b=30),
            showlegend=False,
            xaxis=dict(title="Directional Accuracy (%)",
                       title_font=dict(color="#7A9BB5", size=11),
                       tickfont=dict(color="#7A9BB5", size=10),
                       showgrid=True, gridcolor="#1E3A5F",
                       range=[45, 78]),
            yaxis=dict(tickfont=dict(color="#B8C8D8", size=10),
                       showgrid=False)
        )
        st.plotly_chart(fig_dir, use_container_width=True)

    # ── Table ──────────────────────────────────────────
    st.markdown("##### Full Rankings Table")

    search = st.text_input("Filter by firm name", "",
                           placeholder="e.g. Goldman")

    firm_display = firm.copy()

    # Round all numeric columns cleanly
    for col in ["Bias(pp)", "MAE(pp)", "Dir.Acc(%)",
                "Actual Ret(%)", "Implied Up(%)"]:
        firm_display[col] = firm_display[col].round(1)

    firm_display["Bias Rank"] = firm_display["Bias(pp)"].rank(
        method="min").astype(int)
    firm_display["MAE Rank"]  = firm_display["MAE(pp)"].rank(
        method="min").astype(int)
    firm_display["Dir Rank"]  = firm_display["Dir.Acc(%)"].rank(
        method="min", ascending=False).astype(int)

    if search:
        firm_display = firm_display[
            firm_display["firm_name"].str.contains(
                search, case=False, na=False)
        ]

    col_dl, _ = st.columns([1, 5])
    col_dl.download_button(
        label="Download CSV",
        data=firm_display.to_csv(index=False),
        file_name="firm_rankings.csv",
        mime="text/csv"
    )

    def color_bias_cell(val):
        if val <= 25:   return "color: #00C49A; font-weight:600"
        elif val <= 35: return "color: #F0A500"
        else:           return "color: #FF4B4B"

    def color_dir_cell(val):
        if val >= 67:   return "color: #00C49A; font-weight:600"
        elif val >= 63: return "color: #00A3E0"
        else:           return "color: #F0A500"

    def color_mae_cell(val):
        if val <= 45:   return "color: #00C49A; font-weight:600"
        elif val <= 55: return "color: #F0A500"
        else:           return "color: #FF4B4B"

    styled = (
        firm_display.style
        .format({
            "Targets":       "{:,}",
            "Bias(pp)":      "{:.1f}pp",
            "MAE(pp)":       "{:.1f}pp",
            "Dir.Acc(%)":    "{:.1f}%",
            "Actual Ret(%)": "{:.1f}%",
            "Implied Up(%)": "{:.1f}%",
        })
        .map(color_bias_cell, subset=["Bias(pp)"])
        .map(color_dir_cell,  subset=["Dir.Acc(%)"])
        .map(color_mae_cell,  subset=["MAE(pp)"])
    )
    st.dataframe(styled, use_container_width=True, hide_index=True)

    # ── Interpretation panel ───────────────────────────
    st.markdown("""
    <div style="background:#0A2540;border:1px solid #1E3A5F;border-radius:8px;
                padding:16px 20px;margin-top:16px;">
      <div style="color:#7A9BB5;font-size:11px;font-weight:600;
                  letter-spacing:.08em;margin-bottom:8px">WHAT THIS MEANS</div>
      <div style="color:#E8EDF2;font-size:13px;line-height:1.7">
        While nearly all firms demonstrate similar directional forecasting ability,
        large differences remain in target-setting behaviour.
        Independent research firms generally produce less optimistic forecasts
        than major investment banks, consistent with academic literature suggesting
        that investment banking relationships create pressure to issue bullish targets.
        For investors, directional calls remain broadly useful but price targets
        should be treated with significant scepticism, particularly from
        firms with historically high bias.
      </div>
    </div>
    """, unsafe_allow_html=True)

with tab3:

    # ── Research takeaways ─────────────────────────────
    st.markdown("#### Analyst Accuracy Across Market Cycles")

    takeaways3 = [
        ("Forecast bias fell from 118.5pp (2001) to 1.1pp (2024)",
         "A 117pp decline over 23 years. The data suggests sustained regulatory and reputational pressure has forced meaningful improvement in target discipline."),
        ("2007 directional accuracy: 32.5% the worst year on record",
         "Analysts issued uniformly bullish targets heading into the GFC. Directional accuracy fell below random, making consensus targets actively misleading that year."),
        ("2020 is the only year with negative bias (-30.5pp)",
         "Analysts reduced targets sharply in response to COVID. The V-shaped recovery produced 63.5% actual returns, leaving targets well below realized prices."),
        ("Analyst accuracy weakens during market stress",
         "Directional accuracy fell to 32.5% in 2007 and 53.4% in 2022, both below the 64.6% long-run average though the degree of deterioration varies by cycle."),
    ]

    cols = st.columns(2)
    for i, (title, body) in enumerate(takeaways3):
        with cols[i % 2]:
            st.markdown(
                f'<div class="finding-card"><span>{title}</span>'
                f'<p>{body}</p></div>',
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── KPI summary row ────────────────────────────────
    hi_bias_row  = yearly.loc[yearly["Bias(pp)"].idxmax()]
    lo_bias_row  = yearly.loc[yearly["Bias(pp)"].idxmin()]
    worst_acc_row= yearly.loc[yearly["Dir.Acc(%)"].idxmin()]
    best_acc_row = yearly.loc[yearly["Dir.Acc(%)"].idxmax()]

    kq1, kq2, kq3, kq4 = st.columns(4)
    kq1.markdown(f"""
    <div style="background:#132B45;border:1px solid #1E3A5F;border-radius:8px;
                padding:14px 16px;">
      <div style="color:#7A9BB5;font-size:11px;font-weight:500;
                  letter-spacing:.04em;margin-bottom:6px">HIGHEST BIAS YEAR</div>
      <div style="color:#FF4B4B;font-size:22px;font-weight:600">
        {int(hi_bias_row['year'])}</div>
      <div style="color:#B8C8D8;font-size:12px;margin-top:4px">
        {hi_bias_row['Bias(pp)']:.1f}pp avg bias</div>
    </div>""", unsafe_allow_html=True)

    kq2.markdown(f"""
    <div style="background:#132B45;border:1px solid #1E3A5F;border-radius:8px;
                padding:14px 16px;">
      <div style="color:#7A9BB5;font-size:11px;font-weight:500;
                  letter-spacing:.04em;margin-bottom:6px">LOWEST BIAS YEAR</div>
      <div style="color:#00C49A;font-size:22px;font-weight:600">
        {int(lo_bias_row['year'])}</div>
      <div style="color:#B8C8D8;font-size:12px;margin-top:4px">
        {lo_bias_row['Bias(pp)']:.1f}pp avg bias</div>
    </div>""", unsafe_allow_html=True)

    kq3.markdown(f"""
    <div style="background:#132B45;border:1px solid #1E3A5F;border-radius:8px;
                padding:14px 16px;">
      <div style="color:#7A9BB5;font-size:11px;font-weight:500;
                  letter-spacing:.04em;margin-bottom:6px">WORST ACCURACY YEAR</div>
      <div style="color:#FF4B4B;font-size:22px;font-weight:600">
        {int(worst_acc_row['year'])}</div>
      <div style="color:#B8C8D8;font-size:12px;margin-top:4px">
        {worst_acc_row['Dir.Acc(%)']:.1f}% directional accuracy</div>
    </div>""", unsafe_allow_html=True)

    kq4.markdown(f"""
    <div style="background:#132B45;border:1px solid #1E3A5F;border-radius:8px;
                padding:14px 16px;">
      <div style="color:#7A9BB5;font-size:11px;font-weight:500;
                  letter-spacing:.04em;margin-bottom:6px">BEST ACCURACY YEAR</div>
      <div style="color:#00C49A;font-size:22px;font-weight:600">
        {int(best_acc_row['year'])}</div>
      <div style="color:#B8C8D8;font-size:12px;margin-top:4px">
        {best_acc_row['Dir.Acc(%)']:.1f}% directional accuracy</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Year-by-year chart ─────────────────────────────
    st.markdown("##### Forecast Bias and Directional Accuracy - 2001 to 2024")
    st.markdown(
        "<p style='color:#7A9BB5;font-size:12px;margin-top:-8px'>"
        "Shaded regions mark major market dislocations. "
        "Blue bars show annual forecast bias. "
        "Orange line shows directional accuracy (right axis).</p>",
        unsafe_allow_html=True
    )

    fig_trend = go.Figure()

    # Shaded recession / dislocation bands
    bands = [
        (2001, 2002,  "Dot-com bust"),
        (2007, 2009,  "GFC"),
        (2020, 2020,  "COVID"),
        (2022, 2022,  "Bear market"),
    ]
    for x0, x1, label in bands:
        fig_trend.add_vrect(
            x0=x0 - 0.4, x1=x1 + 0.4,
            fillcolor="#FF4B4B", opacity=0.07,
            layer="below", line_width=0,
        )
        fig_trend.add_annotation(
            x=(x0 + x1) / 2, y=125,
            text=label, showarrow=False,
            font=dict(size=8, color="#7A9BB5"),
            textangle=-90, xanchor="center"
        )

    # Zero reference line
    fig_trend.add_hline(
        y=0, line_dash="dash",
        line_color="#3A5A7A", line_width=1
    )

    # Bias bars
    bar_colors_yr = [
        "#FF4B4B" if b > 80 else
        "#F0A500" if b > 40 else
        "#00A3E0" if b >= 0 else
        "#00C49A"
        for b in yearly["Bias(pp)"]
    ]
    fig_trend.add_trace(go.Bar(
        x=yearly["year"],
        y=yearly["Bias(pp)"],
        name="Forecast Bias (pp)",
        marker_color=bar_colors_yr,
        opacity=0.85,
        hovertemplate="<b>%{x}</b><br>Bias: %{y:.1f}pp<extra></extra>",
        yaxis="y1"
    ))

    # Directional accuracy line
    fig_trend.add_trace(go.Scatter(
        x=yearly["year"],
        y=yearly["Dir.Acc(%)"],
        name="Directional Accuracy (%)",
        mode="lines+markers",
        line=dict(color="#F0A500", width=2),
        marker=dict(size=5, color="#F0A500"),
        hovertemplate="<b>%{x}</b><br>Dir. Acc: %{y:.1f}%<extra></extra>",
        yaxis="y2"
    ))

    # 50% reference on secondary axis
    fig_trend.add_hline(
        y=50, line_dash="dot",
        line_color="#3A5A7A", line_width=1,
        secondary_y=True
    )

    fig_trend.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0D1F33",
        plot_bgcolor="#0D1F33",
        height=420,
        margin=dict(l=20, r=60, t=20, b=40),
        legend=dict(
            orientation="h", y=-0.15,
            font=dict(color="#B8C8D8", size=11)
        ),
        barmode="relative",
        xaxis=dict(
            tickfont=dict(color="#7A9BB5", size=11),
            showgrid=False, dtick=2
        ),
        yaxis=dict(
            title="Forecast Bias (pp)",
            title_font=dict(color="#00A3E0", size=11),
            tickfont=dict(color="#7A9BB5", size=10),
            showgrid=True, gridcolor="#1E3A5F"
        ),
        yaxis2=dict(
            title="Directional Accuracy (%)",
            title_font=dict(color="#F0A500", size=11),
            tickfont=dict(color="#7A9BB5", size=10),
            overlaying="y", side="right",
            showgrid=False, range=[25, 95]
        )
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    # ── Regime chart ───────────────────────────────────
    st.markdown("##### Bias and Accuracy by Market Regime")
    st.markdown(
        "<p style='color:#7A9BB5;font-size:12px;margin-top:-8px'>"
        "Analyst accuracy is worst precisely when investors need it most"
        "during market downturns.</p>",
        unsafe_allow_html=True
    )

    regime_order = [
        "Dot-com bust (2001-02)",
        "Bull market (2003-07)",
        "GFC (2008-09)",
        "Bull market (2010-21)",
        "Bear market (2022)",
        "Recovery (2023-24)",
    ]
    regime_plot = regime.set_index("regime").reindex(regime_order).reset_index()

    rc1, rc2 = st.columns(2)

    with rc1:
        reg_colors = [
            "#FF4B4B" if b > 70 else
            "#F0A500" if b > 30 else
            "#00C49A" if b < 5 else
            "#00A3E0"
            for b in regime_plot["Bias(pp)"]
        ]
        fig_reg_bias = go.Figure(go.Bar(
            x=regime_plot["regime"],
            y=regime_plot["Bias(pp)"],
            marker_color=reg_colors,
            text=[f"{b:.1f}pp" for b in regime_plot["Bias(pp)"]],
            textposition="outside",
            textfont=dict(color="#B8C8D8", size=10),
            hovertemplate="<b>%{x}</b><br>Bias: %{y:.1f}pp<extra></extra>"
        ))
        fig_reg_bias.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0D1F33", plot_bgcolor="#0D1F33",
            height=320,
            margin=dict(l=10, r=20, t=30, b=80),
            title=dict(
                text="Forecast Bias by Regime",
                font=dict(color="#E8EDF2", size=13), x=0
            ),
            showlegend=False,
            xaxis=dict(tickfont=dict(color="#B8C8D8", size=10),
                       showgrid=False, tickangle=-20),
            yaxis=dict(tickfont=dict(color="#7A9BB5", size=10),
                       showgrid=True, gridcolor="#1E3A5F",
                       title="Bias (pp)",
                       title_font=dict(color="#7A9BB5", size=10))
        )
        st.plotly_chart(fig_reg_bias, use_container_width=True)

    with rc2:
        dir_reg_colors = [
            "#FF4B4B" if d < 55 else
            "#F0A500" if d < 65 else
            "#00C49A"
            for d in regime_plot["Dir.Acc(%)"]
        ]
        fig_reg_dir = go.Figure(go.Bar(
            x=regime_plot["regime"],
            y=regime_plot["Dir.Acc(%)"],
            marker_color=dir_reg_colors,
            text=[f"{d:.1f}%" for d in regime_plot["Dir.Acc(%)"]],
            textposition="outside",
            textfont=dict(color="#B8C8D8", size=10),
            hovertemplate="<b>%{x}</b><br>Dir. Acc: %{y:.1f}%<extra></extra>"
        ))
        fig_reg_dir.add_hline(
            y=50, line_dash="dash",
            line_color="#3A5A7A", line_width=1
        )
        fig_reg_dir.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0D1F33", plot_bgcolor="#0D1F33",
            height=320,
            margin=dict(l=10, r=20, t=30, b=80),
            title=dict(
                text="Directional Accuracy by Regime",
                font=dict(color="#E8EDF2", size=13), x=0
            ),
            showlegend=False,
            xaxis=dict(tickfont=dict(color="#B8C8D8", size=10),
                       showgrid=False, tickangle=-20),
            yaxis=dict(tickfont=dict(color="#7A9BB5", size=10),
                       showgrid=True, gridcolor="#1E3A5F",
                       title="Directional Accuracy (%)",
                       title_font=dict(color="#7A9BB5", size=10),
                       range=[0, 95])
        )
        st.plotly_chart(fig_reg_dir, use_container_width=True)

    # ── Interpretation panel ───────────────────────────
    st.markdown("""
    <div style="background:#0A2540;border:1px solid #1E3A5F;border-radius:8px;
                padding:16px 20px;margin-top:8px;">
      <div style="color:#7A9BB5;font-size:11px;font-weight:600;
                  letter-spacing:.08em;margin-bottom:8px">WHAT THIS MEANS</div>
      <div style="color:#E8EDF2;font-size:13px;line-height:1.7">
        Analyst forecast quality is pro-cyclical: accuracy improves in bull markets
        and deteriorates sharply during downturns. The 2007 reading of 32.5%
        directional accuracy confirms that consensus analyst opinion provided
        negative informational value heading into the global financial crisis.
        The long-run improvement in bias from 118pp to near zero suggests
        greater regulatory scrutiny and reputational pressure have forced
        meaningful improvements in target-setting discipline since 2001.
      </div>
    </div>
    """, unsafe_allow_html=True)

with tab4:

    # ── Prepare analyst data ───────────────────────────
    analyst["ALYSNAM"] = analyst["ALYSNAM"].str.strip()

    def fmt_name(raw):
        parts = raw.split()
        if len(parts) >= 2:
            return f"{parts[0].title()}, {parts[-1]}."
        return raw.title()

    analyst["Analyst"] = analyst["ALYSNAM"].apply(fmt_name)
    qualified = analyst[analyst["Targets"] >= 100].copy()
    qualified["abs_bias"] = qualified["Bias(pp)"].abs()

    l1 = qualified.sort_values("MAE(pp)").head(15).reset_index(drop=True)
    l2 = qualified.sort_values("abs_bias").head(15).reset_index(drop=True)
    l3 = qualified.sort_values("Dir.Acc(%)", ascending=False).head(15).reset_index(drop=True)
    l4 = qualified.sort_values("Bias(pp)", ascending=False).head(15).reset_index(drop=True)

    # ── Takeaways ──────────────────────────────────────
    st.markdown("#### Individual Analyst Performance")

    takeaways4 = [
        ("Best analyst in 23 years: Motemaden, D. (Evercore ISI)",
         "220 forecasts, 14.9pp MAE, 83.6% directional accuracy, near-zero systematic bias. "
         "All three metrics rank in the top tier simultaneously."),
        ("MAE and calibration identify different analysts",
         "The lowest-MAE and lowest-abs-bias leaderboards share almost no overlap, "
         "confirming these measure distinct dimensions of forecasting skill."),
        ("High directional accuracy does not imply low bias",
         "Several analysts in the top direction leaderboard carry 100pp+ bias, "
         "correctly predicting direction while massively overestimating magnitude."),
        ("Minimum 100 forecasts required for all leaderboards",
         "Small samples produce misleading rankings. "
         "All four leaderboards filter to analysts with at least 100 graded targets."),
    ]

    cols = st.columns(2)
    for i, (title, body) in enumerate(takeaways4):
        with cols[i % 2]:
            st.markdown(
                f'<div class="finding-card"><span>{title}</span>'
                f'<p>{body}</p></div>',
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── KPI row ────────────────────────────────────────
    best_mae  = l1.iloc[0]
    best_cal  = l2.iloc[0]
    best_dir  = l3.iloc[0]
    most_bull = l4.iloc[0]

    ka, kb, kc, kd = st.columns(4)

    def analyst_kpi(col, label, rank_label, row,
                    primary_val, primary_color, secondary_val):
        col.markdown(f"""
        <div style="background:#132B45;border:1px solid #1E3A5F;
                    border-radius:8px;padding:14px 16px;position:relative;">
          <div style="display:flex;justify-content:space-between;
                      align-items:flex-start;margin-bottom:7px;">
            <div style="color:#7A9BB5;font-size:10px;font-weight:600;
                        letter-spacing:.06em">{label}</div>
            <div style="background:#0A2540;border:1px solid #1E3A5F;
                        border-radius:4px;padding:2px 7px;
                        color:#00A3E0;font-size:10px;font-weight:600">
              {rank_label}
            </div>
          </div>
          <div style="color:#E8EDF2;font-size:13px;font-weight:600;
                      line-height:1.4;word-break:break-word">
            {row['Analyst']}
          </div>
          <div style="color:#7A9BB5;font-size:11px;margin-top:2px">
            {row['firm_name']}
          </div>
          <div style="margin-top:9px;padding-top:9px;
                      border-top:1px solid #1E3A5F;
                      display:flex;flex-direction:column;gap:4px;">
            <div style="color:#7A9BB5;font-size:11px">
              {int(row['Targets']):,} forecasts
            </div>
            <div style="color:{primary_color};font-size:12px;font-weight:600">
              {primary_val}
            </div>
            <div style="color:#7A9BB5;font-size:11px">
              {secondary_val}
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

    analyst_kpi(ka, "LOWEST MAE", "#1 Accuracy",
                best_mae,
                f"{best_mae['MAE(pp)']:.1f}pp Mean Abs. Error",  "#00C49A",
                f"{best_mae['Dir.Acc(%)']:.1f}% Directional Accuracy")

    analyst_kpi(kb, "MOST CALIBRATED", "#1 Calibration",
                best_cal,
                f"{abs(best_cal['Bias(pp)']):.1f}pp Absolute Bias", "#00A3E0",
                f"{best_cal['Dir.Acc(%)']:.1f}% Directional Accuracy")

    analyst_kpi(kc, "BEST DIRECTION", "#1 Direction",
                best_dir,
                f"{best_dir['Dir.Acc(%)']:.1f}% Directional Accuracy", "#00C49A",
                f"{best_dir['MAE(pp)']:.1f}pp Mean Abs. Error")

    analyst_kpi(kd, "MOST BULLISH", "#1 Bullish",
                most_bull,
                f"{most_bull['Bias(pp)']:.1f}pp Forecast Bias",   "#FF4B4B",
                f"{most_bull['Dir.Acc(%)']:.1f}% Directional Accuracy")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Four leaderboard sub-tabs ──────────────────────
    lt1, lt2, lt3, lt4 = st.tabs([
        "  Most Accurate (MAE)  ",
        "  Most Calibrated (Bias)  ",
        "  Best Direction  ",
        "  Most Bullish  ",
    ])

    def render_leaderboard(data, rank_col, color_fn, subtitle):
        st.markdown(
            f"<p style='color:#7A9BB5;font-size:12px;margin-bottom:12px'>"
            f"{subtitle}</p>",
            unsafe_allow_html=True
        )
        display = data[["Analyst","firm_name","Targets",
                         "Bias(pp)","MAE(pp)","Dir.Acc(%)"]].copy()
        display.index = range(1, len(display) + 1)
        display.index.name = "Rank"
        display.columns = ["Analyst","Firm","Targets",
                            "Bias (pp)","MAE (pp)","Dir. Acc (%)"]

        def fmt_bias(v): return f"{v:.1f}pp"
        def fmt_mae(v):  return f"{v:.1f}pp"
        def fmt_dir(v):  return f"{v:.1f}%"

        styled = (
            display.style
            .format({
                "Targets":      "{:,}",
                "Bias (pp)":    fmt_bias,
                "MAE (pp)":     fmt_mae,
                "Dir. Acc (%)": fmt_dir,
            })
            .map(color_fn, subset=[rank_col])
        )
        st.dataframe(styled, use_container_width=True)

    def color_mae_lb(v):
        raw = float(str(v).replace("pp",""))
        if raw <= 25:   return "color:#00C49A;font-weight:600"
        elif raw <= 40: return "color:#00A3E0"
        else:           return "color:#F0A500"

    def color_bias_lb(v):
        raw = float(str(v).replace("pp",""))
        if abs(raw) <= 5:    return "color:#00C49A;font-weight:600"
        elif abs(raw) <= 15: return "color:#00A3E0"
        else:                return "color:#F0A500"

    def color_dir_lb(v):
        raw = float(str(v).replace("%",""))
        if raw >= 85:   return "color:#00C49A;font-weight:600"
        elif raw >= 75: return "color:#00A3E0"
        else:           return "color:#F0A500"

    def color_bull_lb(v):
        raw = float(str(v).replace("pp",""))
        if raw >= 200:  return "color:#FF4B4B;font-weight:600"
        elif raw >= 150:return "color:#F0A500"
        else:           return "color:#B8C8D8"

    with lt1:
        render_leaderboard(l1, "MAE (pp)", color_mae_lb,
            "Ranked by mean absolute error how close targets were to realized prices. "
            "Minimum 100 graded forecasts.")

    with lt2:
        render_leaderboard(l2, "Bias (pp)", color_bias_lb,
            "Ranked by absolute systematic bias how consistently calibrated targets were. "
            "Near-zero means neither persistently bullish nor bearish.")

    with lt3:
        render_leaderboard(l3, "Dir. Acc (%)", color_dir_lb,
            "Ranked by directional accuracy how often the analyst correctly predicted "
            "whether the stock would rise or fall over 12 months.")

    with lt4:
        render_leaderboard(l4, "Bias (pp)", color_bull_lb,
            "Ranked by highest systematic upward bias. "
            "High directional accuracy alongside high bias indicates correct direction "
            "but massively overestimated magnitude.")

    # ── Interpretation ─────────────────────────────────
    st.markdown("""
    <div style="background:#0A2540;border:1px solid #1E3A5F;border-radius:8px;
                padding:16px 20px;margin-top:16px;">
      <div style="color:#7A9BB5;font-size:11px;font-weight:600;
                  letter-spacing:.08em;margin-bottom:8px">WHAT THIS MEANS</div>
      <div style="color:#E8EDF2;font-size:13px;line-height:1.7">
        Forecasting skill is multi-dimensional. An analyst can achieve near-perfect
        directional accuracy while simultaneously issuing price targets that are
        wildly optimistic in magnitude. Investors should evaluate analysts across
        all three dimensions MAE, calibration, and directional accuracy rather
        than relying on any single metric. The rarest combination, demonstrated by
        only a handful of analysts in 23 years of data, is simultaneously low bias,
        low MAE, and high directional accuracy.
      </div>
    </div>
    """, unsafe_allow_html=True)