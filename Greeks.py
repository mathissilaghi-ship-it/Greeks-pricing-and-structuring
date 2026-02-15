import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st
from scipy.stats import norm
from math import log, sqrt, exp

# --- 1. Définition des bornes fixes de base ---
BASE_RANGES = {
    "Delta": [0, 1],
    "Vega":  [0, 1],
    "Theta": [-0.03, 0.02],
    "Gamma": [0, 0.08],
    "Rho":   [0, 1]
}

# --- 2. Fonctions Black-Scholes-Merton (Call & Put) ---

def calculate_d1_d2(S, K, T, r, q, sigma):
    d1 = (log(S / K) + (r - q + (0.5 * (sigma ** 2))) * T) / (sigma * sqrt(T))
    d2 = d1 - sigma * sqrt(T)
    return d1, d2

def call_price(S, K, T, r, q, sigma):
    d1, d2 = calculate_d1_d2(S, K, T, r, q, sigma)
    return S * exp(-q * T) * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)

def put_price(S, K, T, r, q, sigma):
    d1, d2 = calculate_d1_d2(S, K, T, r, q, sigma)
    return K * exp(-r * T) * norm.cdf(-d2) - S * exp(-q * T) * norm.cdf(-d1)


def delta(S, K, T, r, q, sigma, option_type):
    if T <= 0 or sigma <= 0: return 0
    d1, _ = calculate_d1_d2(S, K, T, r, q, sigma)
    
    if option_type == "Call":
        return exp(-q * T) * norm.cdf(d1)
    else: # Put
        return exp(-q * T) * (norm.cdf(d1) - 1)

def gamma(S, K, T, r, q, sigma, option_type):
    # Gamma est le même pour Call et Put
    if T <= 0 or sigma <= 0: return 0
    d1, _ = calculate_d1_d2(S, K, T, r, q, sigma)
    return (exp(-q * T) * norm.pdf(d1)) / (S * sigma * sqrt(T))

def vega(S, K, T, r, q, sigma, option_type):
    # Vega est le même pour Call et Put
    if T <= 0 or sigma <= 0: return 0
    d1, _ = calculate_d1_d2(S, K, T, r, q, sigma)
    return S * exp(-q * T) * norm.pdf(d1) * sqrt(T) / 100 

def theta(S, K, T, r, q, sigma, option_type):
    if T <= 0 or sigma <= 0: return 0
    d1, d2 = calculate_d1_d2(S, K, T, r, q, sigma)
    
    # Terme commun
    term1 = - (S * exp(-q * T) * norm.pdf(d1) * sigma) / (2 * sqrt(T))
    
    if option_type == "Call":
        term2 = - r * K * exp(-r * T) * norm.cdf(d2)
        term3 = + q * S * exp(-q * T) * norm.cdf(d1)
        return (term1 + term2 + term3) / 365
    else: # Put
        term2 = + r * K * exp(-r * T) * norm.cdf(-d2)
        term3 = - q * S * exp(-q * T) * norm.cdf(-d1)
        return (term1 + term2 + term3) / 365

def rho(S, K, T, r, q, sigma, option_type):
    if T <= 0 or sigma <= 0: return 0
    d1, d2 = calculate_d1_d2(S, K, T, r, q, sigma)
    
    if option_type == "Call":
        return K * T * exp(-r * T) * norm.cdf(d2) / 100
    else: # Put
        return -K * T * exp(-r * T) * norm.cdf(-d2) / 100

# --- Second-Order Greeks ---

def vanna(S, K, T, r, q, sigma, option_type):
    """dDelta/dSigma = dVega/dS"""
    if T <= 0 or sigma <= 0: return 0
    d1, d2 = calculate_d1_d2(S, K, T, r, q, sigma)
    return -exp(-q * T) * norm.pdf(d1) * d2 / sigma

def volga(S, K, T, r, q, sigma, option_type):
    """dVega/dSigma (Vomma)"""
    if T <= 0 or sigma <= 0: return 0
    d1, d2 = calculate_d1_d2(S, K, T, r, q, sigma)
    vega_val = S * exp(-q * T) * norm.pdf(d1) * sqrt(T)
    return vega_val * d1 * d2 / sigma

def charm(S, K, T, r, q, sigma, option_type):
    """dDelta/dT (Delta decay)"""
    if T <= 0 or sigma <= 0: return 0
    d1, d2 = calculate_d1_d2(S, K, T, r, q, sigma)
    
    common = exp(-q * T) * norm.pdf(d1) * (2 * (r - q) * T - d2 * sigma * sqrt(T)) / (2 * T * sigma * sqrt(T))
    if option_type == "Call":
        return q * exp(-q * T) * norm.cdf(d1) - common
    else:
        return -q * exp(-q * T) * norm.cdf(-d1) - common

# --- 3. Fonction de plot intelligente ---
def plot_sensitivity(S_current, K, T, r, q, sigma, option_type, greek_function):
    # Génération des données
    S_values = np.linspace(0.5 * K, 1.5 * K, 100)
    greek_values = [greek_function(s, K, T, r, q, sigma, option_type) for s in S_values]
    
    current_val = greek_function(S_current, K, T, r, q, sigma, option_type)
    g_name = greek_function.__name__.capitalize()
    
    # --- Gestion Dynamique des Axes selon Call/Put ---
    y_range_limit = BASE_RANGES.get(g_name, None)
    
    if option_type == "Put":
        if g_name == "Delta":
            y_range_limit = [-1, 0]
        elif g_name == "Rho":
            y_range_limit = [-1, 0]
    
    # --- Affichage ---
    st.metric(label=f"{g_name} ({option_type})", value=f"{current_val:.4f}")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=S_values, y=greek_values, mode='lines', name=g_name,
        line=dict(color='#1f77b4', width=3)
    ))
    
    fig.add_vline(x=K, line_width=1, line_dash="dash", line_color="red", opacity=0.5)
    fig.add_vline(x=S_current, line_width=1, line_dash="dash", line_color="white", opacity=0.5,
                  annotation_text=f"Spot", annotation_position="top right")

    fig.update_layout(
        title=f"{g_name} vs Spot",
        xaxis_title="Prix du Sous-jacent (S)",
        yaxis_title=g_name,
        yaxis=dict(range=y_range_limit),
        height=300,
        margin=dict(l=20, r=20, t=30, b=20),
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

# --- 4. Interface Utilisateur ---
st.set_page_config(layout="wide", page_title="Greeks Analysis")

# --- Sidebar: Navigation + Shared Params ---
with st.sidebar:
    page = st.radio("📄 Navigation", ["Greeks Analyse", "Produit Structuré"], horizontal=True)

# ============================================================
# PAGE 1 : GREEKS ANALYSE (existing)
# ============================================================
if page == "Greeks Analyse":
    st.title(" Prix d'option et Analyse de Sensibilité des Greeks")

    with st.sidebar:
        st.header("Paramètres")
        with st.container(border=True):
            option_type = st.radio("Type d'Option", ["Call", "Put"], horizontal=True)
            st.markdown("---")
            S = st.number_input("Prix Spot (S)", value=100)
            K = st.number_input("Strike (K)", value=100)
            T = st.slider("Maturité (Années)", 0.01, 5.0, 1.0, 0.01)
            r = st.slider("Taux sans risque (r)", -0.1, 0.2, 0.05, 0.01)
            q = st.slider("Dividende (q)", 0.0, 0.2, 0.0, 0.005) 
            sigma = st.slider("Volatilité (σ)", 0.01, 1.0, 0.2, 0.01)

    # --- Prix de l'option ---
    if option_type == "Call":
        price = call_price(S, K, T, r, q, sigma)
        intrinsic = max(S - K, 0)
    else:
        price = put_price(S, K, T, r, q, sigma)
        intrinsic = max(K - S, 0)
    time_value = price - intrinsic

    def price_card(label, value, color, icon):
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {color}18, {color}08);
            border-left: 4px solid {color};
            border-radius: 10px;
            padding: 18px 20px;
            text-align: center;
        ">
            <div style="font-size: 0.85rem; color: #aaa; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px;">
                {icon} {label}
            </div>
            <div style="font-size: 2rem; font-weight: 700; color: {color};">
                {value:.4f}
            </div>
        </div>
        """, unsafe_allow_html=True)

    price_col1, price_col2, price_col3 = st.columns(3)
    with price_col1:
        price_card(f"Prix du {option_type}", price, "#1f77b4", "💰")
    with price_col2:
        price_card("Valeur Intrinsèque", intrinsic, "#ff7f0e", "📊")
    with price_col3:
        price_card("Valeur Temps", time_value, "#2ca02c", "⏳")

    st.markdown("---")

    # --- Graphique Premium / Payoff ---
    with st.container(border=True):
        S_range = np.linspace(0.5 * K, 1.5 * K, 200)
        if option_type == "Call":
            prices = [call_price(s, K, T, r, q, sigma) for s in S_range]
            intrinsic_vals = [max(s - K, 0) for s in S_range]
        else:
            prices = [put_price(s, K, T, r, q, sigma) for s in S_range]
            intrinsic_vals = [max(K - s, 0) for s in S_range]
        time_vals = [p - iv for p, iv in zip(prices, intrinsic_vals)]

        fig_payoff = go.Figure()
        fig_payoff.add_trace(go.Scatter(
            x=S_range, y=prices, mode='lines', name=f"Prix {option_type} (BSM)",
            line=dict(color='#1f77b4', width=3)
        ))
        fig_payoff.add_trace(go.Scatter(
            x=S_range, y=intrinsic_vals, mode='lines', name="Valeur Intrinsèque",
            line=dict(color='#ff7f0e', width=2, dash='dash')
        ))
        fig_payoff.add_trace(go.Scatter(
            x=S_range, y=time_vals, mode='lines', name="Valeur Temps",
            line=dict(color='#2ca02c', width=2, dash='dot'),
            fill='tozeroy', fillcolor='rgba(44, 160, 44, 0.1)'
        ))
        fig_payoff.add_vline(x=S, line_width=1, line_dash="dash", line_color="white", opacity=0.5,
                             annotation_text=f"Spot = {S}", annotation_position="top right")
        fig_payoff.add_vline(x=K, line_width=1, line_dash="dash", line_color="red", opacity=0.5,
                             annotation_text=f"Strike = {K}", annotation_position="top left")
        fig_payoff.update_layout(
            title=f"Premium & Payoff — {option_type}",
            xaxis_title="Prix du Sous-jacent (S)",
            yaxis_title="Prix de l'option",
            height=350,
            margin=dict(l=20, r=20, t=40, b=20),
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_payoff, use_container_width=True)

    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)
    row3_col1, row3_col2 = st.columns(2)

    with row1_col1:
        with st.container(border=True):
            plot_sensitivity(S, K, T, r, q, sigma, option_type, delta)
    with row1_col2:
        with st.container(border=True):
            plot_sensitivity(S, K, T, r, q, sigma, option_type, gamma)      
    with row2_col1:
        with st.container(border=True):
            plot_sensitivity(S, K, T, r, q, sigma, option_type, theta)
    with row2_col2:
        with st.container(border=True):
            plot_sensitivity(S, K, T, r, q, sigma, option_type, vega)
    with row3_col1:
        with st.container(border=True):
            plot_sensitivity(S, K, T, r, q, sigma, option_type, rho)

    st.markdown("---")
    st.subheader("Greeks de Second Ordre")

    row4_col1, row4_col2 = st.columns(2)
    row5_col1, row5_col2 = st.columns(2)

    with row4_col1:
        with st.container(border=True):
            plot_sensitivity(S, K, T, r, q, sigma, option_type, vanna)
    with row4_col2:
        with st.container(border=True):
            plot_sensitivity(S, K, T, r, q, sigma, option_type, volga)
    with row5_col1:
        with st.container(border=True):
            plot_sensitivity(S, K, T, r, q, sigma, option_type, charm)

# ============================================================
# PAGE 2 : PRODUIT STRUCTURÉ
# ============================================================
elif page == "Produit Structuré":
    st.title("🧱 Réplication de Produit Structuré")

    # --- Presets ---
    PRESETS = {
        "— Personnalisé —": [],
        "Bull Call Spread": [
            {"type": "Call", "strike": 95, "position": "Long", "qty": 1},
            {"type": "Call", "strike": 105, "position": "Short", "qty": 1},
        ],
        "Bear Put Spread": [
            {"type": "Put", "strike": 105, "position": "Long", "qty": 1},
            {"type": "Put", "strike": 95, "position": "Short", "qty": 1},
        ],
        "Straddle": [
            {"type": "Call", "strike": 100, "position": "Long", "qty": 1},
            {"type": "Put", "strike": 100, "position": "Long", "qty": 1},
        ],
        "Strangle": [
            {"type": "Call", "strike": 110, "position": "Long", "qty": 1},
            {"type": "Put", "strike": 90, "position": "Long", "qty": 1},
        ],
        "Butterfly": [
            {"type": "Call", "strike": 90, "position": "Long", "qty": 1},
            {"type": "Call", "strike": 100, "position": "Short", "qty": 2},
            {"type": "Call", "strike": 110, "position": "Long", "qty": 1},
        ],
        "Iron Condor": [
            {"type": "Put", "strike": 85, "position": "Long", "qty": 1},
            {"type": "Put", "strike": 95, "position": "Short", "qty": 1},
            {"type": "Call", "strike": 105, "position": "Short", "qty": 1},
            {"type": "Call", "strike": 115, "position": "Long", "qty": 1},
        ]
    }

    # --- Sidebar: shared market params ---
    with st.sidebar:
        st.header("Paramètres Marché")
        with st.container(border=True):
            S = st.number_input("Prix Spot (S)", value=100, key="struct_S")
            T = st.slider("Maturité (Années)", 0.01, 5.0, 1.0, 0.01, key="struct_T")
            r = st.slider("Taux sans risque (r)", -0.1, 0.2, 0.05, 0.01, key="struct_r")
            q = st.slider("Dividende (q)", 0.0, 0.2, 0.0, 0.005, key="struct_q")
            sigma = st.slider("Volatilité (σ)", 0.01, 1.0, 0.2, 0.01, key="struct_sigma")

    # --- Session state init ---
    if "legs" not in st.session_state:
        st.session_state.legs = [
            {"type": "Call", "strike": 100, "position": "Long", "qty": 1},
        ]
    if "legs_version" not in st.session_state:
        st.session_state.legs_version = 0

    # --- Preset selector ---
    col_preset, col_add = st.columns([3, 1])
    with col_preset:
        preset_choice = st.selectbox("📋 Stratégies prédéfinies", list(PRESETS.keys()))
        if preset_choice != "— Personnalisé —":
            new_legs = [leg.copy() for leg in PRESETS[preset_choice]]
            if st.session_state.legs != new_legs:
                st.session_state.legs = new_legs
                st.session_state.legs_version += 1
                st.rerun()

    with col_add:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("➕ Ajouter un leg", use_container_width=True):
            st.session_state.legs.append({"type": "Call", "strike": 100, "position": "Long", "qty": 1})
            st.session_state.legs_version += 1
            st.rerun()

    st.markdown("---")

    # --- Legs editor ---
    st.subheader("📐 Legs de la stratégie")
    v = st.session_state.legs_version
    legs_to_remove = []

    for i, leg in enumerate(st.session_state.legs):
        cols = st.columns([1.5, 1.5, 1.5, 1, 0.5])
        with cols[0]:
            st.session_state.legs[i]["type"] = st.selectbox(
                "Type", ["Call", "Put"], index=0 if leg["type"] == "Call" else 1, key=f"type_{v}_{i}"
            )
        with cols[1]:
            st.session_state.legs[i]["strike"] = st.number_input(
                "Strike", value=leg["strike"], min_value=1, key=f"strike_{v}_{i}"
            )
        with cols[2]:
            st.session_state.legs[i]["position"] = st.selectbox(
                "Position", ["Long", "Short"], index=0 if leg["position"] == "Long" else 1, key=f"pos_{v}_{i}"
            )
        with cols[3]:
            st.session_state.legs[i]["qty"] = st.number_input(
                "Qté", value=leg["qty"], min_value=1, max_value=50, key=f"qty_{v}_{i}"
            )
        with cols[4]:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("❌", key=f"del_{v}_{i}"):
                legs_to_remove.append(i)

    # Process removals
    if legs_to_remove:
        for idx in sorted(legs_to_remove, reverse=True):
            if len(st.session_state.legs) > 1:
                st.session_state.legs.pop(idx)
        st.session_state.legs_version += 1
        st.rerun()

    st.markdown("---")

    # --- Calculations ---
    legs = st.session_state.legs
    S_range = np.linspace(0.5 * S, 1.5 * S, 300)

    # Combined payoff at expiration
    combined_payoff = np.zeros_like(S_range)
    # Combined BSM price
    combined_price = np.zeros_like(S_range)
    # Total premium paid
    total_premium = 0.0

    for leg in legs:
        k = leg["strike"]
        sign = 1 if leg["position"] == "Long" else -1
        qty = leg["qty"]
        
        for j, s in enumerate(S_range):
            if leg["type"] == "Call":
                combined_payoff[j] += sign * qty * max(s - k, 0)
                combined_price[j] += sign * qty * call_price(s, k, T, r, q, sigma)
            else:
                combined_payoff[j] += sign * qty * max(k - s, 0)
                combined_price[j] += sign * qty * put_price(s, k, T, r, q, sigma)

        # Premium at current spot
        if leg["type"] == "Call":
            total_premium += sign * qty * call_price(S, k, T, r, q, sigma)
        else:
            total_premium += sign * qty * put_price(S, k, T, r, q, sigma)

    # P&L = Payoff - premium paid (at expiry)
    combined_pnl = combined_payoff - total_premium

    # --- Charts ---
    # 1. Payoff + P&L at expiry
    with st.container(border=True):
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=S_range, y=combined_payoff, mode='lines', name="Payoff à Expiration",
            line=dict(color='#ff7f0e', width=3)
        ))
        fig1.add_trace(go.Scatter(
            x=S_range, y=combined_pnl, mode='lines', name="P&L (net de prime)",
            line=dict(color='#1f77b4', width=3)
        ))
        fig1.add_trace(go.Scatter(
            x=S_range, y=combined_price, mode='lines', name="Valeur BSM actuelle",
            line=dict(color='#2ca02c', width=2, dash='dot')
        ))
        fig1.add_hline(y=0, line_width=1, line_color="white", opacity=0.3)
        fig1.add_vline(x=S, line_width=1, line_dash="dash", line_color="white", opacity=0.5,
                       annotation_text=f"Spot = {S}", annotation_position="top right")
        # Mark each strike
        for leg in legs:
            fig1.add_vline(x=leg["strike"], line_width=1, line_dash="dash", line_color="red", opacity=0.3)

        fig1.update_layout(
            title="Payoff Combiné & P&L",
            xaxis_title="Prix du Sous-jacent (S)",
            yaxis_title="Valeur",
            height=450,
            margin=dict(l=20, r=20, t=40, b=20),
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig1, use_container_width=True)

    # --- Summary metrics ---
    max_profit_payoff = max(combined_pnl)
    max_loss_payoff = min(combined_pnl)
    # Breakeven: where P&L crosses zero
    breakevens = []
    for j in range(len(S_range) - 1):
        if combined_pnl[j] * combined_pnl[j+1] < 0:
            # Linear interpolation
            s_be = S_range[j] + (0 - combined_pnl[j]) * (S_range[j+1] - S_range[j]) / (combined_pnl[j+1] - combined_pnl[j])
            breakevens.append(round(s_be, 2))

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Prime Nette", f"{total_premium:.2f}")
    with m2:
        prof_str = f"{max_profit_payoff:.2f}" if max_profit_payoff < 1e6 else "∞"
        st.metric("Profit Max", prof_str)
    with m3:
        loss_str = f"{max_loss_payoff:.2f}" if max_loss_payoff > -1e6 else "-∞"
        st.metric("Perte Max", loss_str)
    with m4:
        be_str = " / ".join(str(b) for b in breakevens) if breakevens else "—"
        st.metric("Breakeven(s)", be_str)

    st.markdown("---")

    # 2. Combined Greeks
    st.subheader("Greeks Combinés")

    greek_functions = {"Delta": delta, "Gamma": gamma, "Vega": vega, "Theta": theta}
    
    g_col1, g_col2 = st.columns(2)
    g_col3, g_col4 = st.columns(2)
    g_cols = [g_col1, g_col2, g_col3, g_col4]

    for idx, (g_name, g_func) in enumerate(greek_functions.items()):
        # Compute combined greek
        combined_greek = np.zeros_like(S_range)
        for leg in legs:
            k = leg["strike"]
            sign = 1 if leg["position"] == "Long" else -1
            qty = leg["qty"]
            for j, s in enumerate(S_range):
                combined_greek[j] += sign * qty * g_func(s, k, T, r, q, sigma, leg["type"])

        current_greek = sum(
            (1 if l["position"] == "Long" else -1) * l["qty"] * g_func(S, l["strike"], T, r, q, sigma, l["type"])
            for l in legs
        )

        with g_cols[idx]:
            with st.container(border=True):
                st.metric(label=f"{g_name} combiné", value=f"{current_greek:.4f}")
                fig_g = go.Figure()
                fig_g.add_trace(go.Scatter(
                    x=S_range, y=combined_greek, mode='lines', name=g_name,
                    line=dict(color='#1f77b4', width=3)
                ))
                fig_g.add_hline(y=0, line_width=1, line_color="white", opacity=0.2)
                fig_g.add_vline(x=S, line_width=1, line_dash="dash", line_color="white", opacity=0.5,
                               annotation_text="Spot", annotation_position="top right")
                for leg in legs:
                    fig_g.add_vline(x=leg["strike"], line_width=1, line_dash="dash", line_color="red", opacity=0.3)
                fig_g.update_layout(
                    title=f"{g_name} vs Spot",
                    xaxis_title="S",
                    yaxis_title=g_name,
                    height=300,
                    margin=dict(l=20, r=20, t=30, b=20),
                    hovermode="x unified"
                )
                st.plotly_chart(fig_g, use_container_width=True)
