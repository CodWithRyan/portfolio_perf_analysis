# Portfolio Performance Analysis - Risk Parity

## 🎯 Description
Implementation of a Risk Parity portfolio strategy with comprehensive performance metrics and visualizations.

## 🛠️ Installation
```bash
pip install -r requirements.txt
```

## 🧑🏽‍💻 Usage
```python
from src.risk_parity import *
import yfinance as yf

# 📊 Define parameters
tickers_list = ['NVDA', 'META', 'TSLA', 'JPM', 'GLD', 'CAT', 'UNH']
start_date = '2015-01-01'
end_date = '2024-12-31'

# 📈 Download and analyze
stock_prices = download_stock_data(tickers_list, start_date, end_date)
stock_returns = calculate_daily_returns(stock_prices)
annual_returns, annualized_std_dev = calculate_annualized_metrics(stock_prices)
weights = calculate_risk_parity_weights(annualized_std_dev)
portfolio_returns = calculate_portfolio_returns(stock_returns, weights)

# 💹 Get market benchmark
market = yf.download('QQQ', start_date, end_date, auto_adjust=False)['Adj Close']
market_returns = market.pct_change().dropna()

# 📉 Calculate and display metrics
metrics = calculate_portfolio_metrics(portfolio_returns, market_returns)
print_portfolio_results(metrics)
```

## Features
- Risk Parity weight calculation
- Performance metrics (Sharpe, Sortino, Treynor, Information Ratio, Beta)
- Visualization tools (cumulative returns, drawdown, heatmaps)
- Benchmark comparison

## Project Structure
```
portfolio_perf_analysis/
├── src/
│   └── risk_parity.py
├── notebooks/
│   └── nb_risk_parity.ipynb
├── requirements.txt
└── README.md
```
# 👤 Author
Bonny Ryan Fotsing
