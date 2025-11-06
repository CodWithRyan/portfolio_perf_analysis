# Portfolio Performance Analysis - Risk Parity

## 🎯 Description
Implementation of a Risk Parity portfolio strategy with comprehensive performance metrics and visualizations.

## 🛠️ Installation
# install the local package in editable mode 
pip install -U pip
pip install -e .
pip install -r requirements.txt


## 🧑🏽‍💻 Usage
from portfolio_perf_analysis import (
    download_stock_data,
    calculate_daily_returns,
    calculate_annualized_metrics,
    calculate_risk_parity_weights,
    calculate_portfolio_returns,
    calculate_portfolio_metrics,
    print_portfolio_results,
    plot_cumulative_returns,
    plot_running_maximum_drawdown,
    plot_returns_histogram,
    plot_monthly_heatmap,
    plot_portfolio_vs_benchmark,
)
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
# Features
- Risk Parity weight calculation
- Performance metrics (Sharpe, Sortino, Treynor, Information Ratio, Beta)
- Visualization tools (cumulative returns, drawdown, heatmaps)
- Benchmark comparison

# 🧮 Calculate and display metrics
metrics = calculate_portfolio_metrics(portfolio_returns, market_returns)
print_portfolio_results(metrics)

## ⚙️ Project Structure

portfolio_perf_analysis/
├── src/
│   └── portfolio_perf_analysis/
│       ├── __init__.py
│       └── risk_parity.py
├── notebooks/
│   ├── nb_risk_parity.ipynb
│   └── outputs/
│       ├── cumulative_returns.png
│       ├── maximum_drawdown.png
│       ├── monthly_heatmap.png
│       ├── portfolio_vs_benchmark.png
│       └── returns_histogram.png
├── setup.py
├── requirements.txt
└── README.md

# 👤 Author
Bonny Ryan Fotsing
