📊 Options Pricing & Structured Products Analytics Platform



🎓 Context & Objective
This project is a quantitative derivatives analytics platform designed to price European options and analyze multi-leg structured strategies in an interactive environment.
The core objective is to:
Implement a rigorous analytical framework based on the Black-Scholes-Merton model
Provide dynamic visualization of option sensitivities and portfolio-level risk exposures
Rather than offering a static pricing calculator, this application delivers a risk-focused analytical tool suitable for academic, professional, and interview preparation use cases.
🚀 Key Features
1️⃣ 📈 Greeks Analysis Engine
A complete analytical environment for European option pricing.
🔹 Option Pricing
European Call & Put
Closed-form Black-Scholes-Merton pricing
Intrinsic vs. Time Value decomposition
Interactive premium visualization across spot prices
🔹 First-Order Greeks
Full analytical implementation of:
Delta – Directional exposure
Gamma – Convexity and curvature
Vega – Volatility sensitivity
Theta – Time decay
Rho – Interest rate sensitivity
Each Greek includes:
Real-time value at current spot
Sensitivity curve vs. underlying price
Dynamic axis scaling (Call vs. Put)
🔬 Second-Order Greeks
Advanced cross-sensitivity measures:
Vanna – ∂Delta / ∂Volatility
Volga (Vomma) – ∂Vega / ∂Volatility
Charm – ∂Delta / ∂Time
These metrics provide deeper insight into:
Volatility convexity
Delta decay dynamics
Cross-risk exposures
2️⃣ 🧱 Structured Product Builder
A fully customizable multi-leg strategy engine enabling construction and analysis of complex derivatives structures.
Users can combine:
Calls / Puts
Long / Short positions
Custom strikes
Custom quantities
📋 Predefined Strategies
Bull Call Spread
Bear Put Spread
Straddle
Strangle
Butterfly
Iron Condor
Each strategy can be modified dynamically, allowing full flexibility in structuring custom payoff profiles.
📊 Strategy Analytics
🔹 Combined Payoff & P&L
The platform computes and visualizes:
Expiration Payoff
Net P&L (after premium)
Current theoretical value (BSM)
Maximum Profit / Maximum Loss
Automatic Breakeven detection
All strikes and the current spot price are clearly displayed on interactive charts.
🔹 Aggregated Portfolio Greeks
Real-time portfolio-level risk exposures:
Net Delta
Net Gamma
Net Vega
Net Theta
This transforms the application into a mini risk-management framework for option portfolios and structured products.
🛠️ Technical Architecture
Core Stack
Python
Streamlit (Interactive Web Interface)
NumPy (Vectorized numerical computations)
SciPy (Normal distribution functions)
Plotly (Interactive financial charts)
Quantitative Implementation
The pricing engine includes:
Analytical computation of 
d
1
d 
1
​	
  and 
d
2
d 
2
​	
 
Closed-form option pricing formulas
Fully analytical Greeks (no numerical approximations)
Linear interpolation for breakeven calculation
Session state management for multi-leg persistence
Performance Optimization
Vectorized computations across price ranges
Modular plotting architecture
Efficient Streamlit session-state handling
Dynamic axis adaptation for cleaner visualization
⚙️ Installation & Usage
Prerequisites
Python 3.9+
Web browser
Setup
Clone the repository:
git clone https://github.com/YOUR_USERNAME/Options-Structured-Analytics.git
cd Options-Structured-Analytics
Install dependencies:
pip install -r requirements.txt
Launch the application:
streamlit run your_script_name.py
🔮 Future Roadmap
Planned improvements include:
Implied Volatility Solver
Volatility Surface (Smile & Skew modeling)
Monte Carlo Pricing Engine
Barrier & Exotic Options
Historical Strategy Backtesting
Risk Metrics (VaR / Expected Shortfall)
Export to PDF / Excel
⚠️ Disclaimer
This tool is intended for educational and research purposes only.
Model assumptions include:
European options
Constant volatility
Constant interest rate
No transaction costs
No liquidity constraints
Real-world market conditions may significantly differ from theoretical model assumptions.
Author: Mathis Silaghi
Master in Financial Markets & Investments
SKEMA Business School
