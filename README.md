# 📊 Options Pricing & Structured Products Analytics Platform

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B)
![Quant](https://img.shields.io/badge/Quant-Black--Scholes--Merton-green)
![Derivatives](https://img.shields.io/badge/Derivatives-Options-orange)

---

### https://greeks-pricing-and-structuring-d5wcwrshlctnqenhhkwtnq.streamlit.app

## 🎓 Context & Objective

This project is a **quantitative derivatives analytics platform** designed to price European options and analyze multi-leg structured strategies in an interactive environment.

The core objective is to:

1. Implement a rigorous analytical framework based on the **Black-Scholes-Merton model**
2. Provide dynamic visualization of option sensitivities and portfolio-level risk exposures

Rather than offering a static pricing calculator, this application delivers a **risk-focused analytical tool** suitable for academic, professional, and interview preparation use cases.

---

# 🚀 Key Features

## 1️⃣ 📈 Greeks Analysis Engine

A complete analytical environment for European option pricing.

### 🔹 Option Pricing

- European **Call & Put**
- Closed-form Black-Scholes-Merton pricing
- Intrinsic vs. Time Value decomposition
- Interactive premium visualization across spot prices

---

### 🔹 First-Order Greeks

Full analytical implementation of:

- **Delta** – Directional exposure  
- **Gamma** – Convexity and curvature  
- **Vega** – Volatility sensitivity  
- **Theta** – Time decay  
- **Rho** – Interest rate sensitivity  

Each Greek includes:

- Real-time value at current spot  
- Sensitivity curve vs. underlying price  
- Dynamic axis scaling (Call vs. Put)  

---

### 🔬 Second-Order Greeks

Advanced cross-sensitivity measures:

- **Vanna** – ∂Delta / ∂Volatility  
- **Volga (Vomma)** – ∂Vega / ∂Volatility  
- **Charm** – ∂Delta / ∂Time  

These metrics provide deeper insight into:

- Volatility convexity  
- Delta decay dynamics  
- Cross-risk exposures  

---

## 2️⃣ 🧱 Structured Product Builder

A fully customizable **multi-leg strategy engine** enabling construction and analysis of complex derivatives structures.

Users can combine:

- Calls / Puts  
- Long / Short positions  
- Custom strikes  
- Custom quantities  

---

### 📋 Predefined Strategies

- Bull Call Spread  
- Bear Put Spread  
- Straddle  
- Strangle  
- Butterfly  
- Iron Condor  

Each strategy can be modified dynamically, allowing full flexibility in structuring custom payoff profiles.

---

## 📊 Strategy Analytics

### 🔹 Combined Payoff & P&L

The platform computes and visualizes:

- Expiration Payoff  
- Net P&L (after premium)  
- Current theoretical value (BSM)  
- Maximum Profit / Maximum Loss  
- Automatic Breakeven detection  

All strikes and the current spot price are clearly displayed on interactive charts.

---

### 🔹 Aggregated Portfolio Greeks

Real-time portfolio-level risk exposures:

- Net Delta  
- Net Gamma  
- Net Vega  
- Net Theta  

This transforms the application into a **mini risk-management framework** for option portfolios and structured products.

---

# 🛠️ Technical Architecture

## Core Stack

- **Python**
- **Streamlit**
- **NumPy**
- **SciPy**
- **Plotly**

---

## Quantitative Implementation

The pricing engine includes:

- Analytical computation of d₁ and d₂  
- Closed-form option pricing formulas  
- Fully analytical Greeks (no numerical approximations)  
- Linear interpolation for breakeven calculation  
- Session state management for multi-leg persistence  

---

# ⚙️ Installation & Usage

## Prerequisites

- Python 3.9+
- Web browser

---

## Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Options-Structured-Analytics.git
cd Options-Structured-Analytics
