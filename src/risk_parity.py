import yfinance as yf
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import warnings
warnings.filterwarnings('ignore')


def download_stock_data(tickers_list, start_date, end_date):
    stock_prices = pd.DataFrame()
    for ticker in tickers_list:
        data = yf.download(ticker, start_date, end_date, auto_adjust=False)
        stock_prices[ticker] = data['Adj Close']
    return stock_prices


def calculate_daily_returns(stock_prices):
    daily_return = stock_prices.pct_change()
    daily_return.dropna(inplace=True)
    return daily_return


def calculate_annualized_metrics(stock_prices):
    annualised_returns = (((stock_prices.iloc[-1] - stock_prices.iloc[0]) / stock_prices.iloc[0] + 1) ** (252 / len(stock_prices)) - 1) * 100
    daily_return = stock_prices.pct_change()
    daily_return.dropna(inplace=True)
    annualised_std_dev = daily_return.std() * math.sqrt(252) * 100
    return annualised_returns, annualised_std_dev


def calculate_risk_parity_weights(annualised_std_dev):
    weights = {}
    for ticker in annualised_std_dev.index:
        std = annualised_std_dev[ticker]
        weights[ticker] = 0.0 if std == 0 else 1.0 / std
    total = sum(weights.values())
    weights = {k: v / total for k, v in weights.items()}
    return weights


def calculate_portfolio_returns(daily_returns, weights):
    portfolio_returns = (daily_returns * pd.Series(weights)).sum(axis=1)
    return portfolio_returns


def calculate_portfolio_metrics(portfolio_returns, market_returns, risk_free_rate=0.02):
    trading_days = 252
    common_index = portfolio_returns.index.intersection(market_returns.index)
    pf = portfolio_returns.loc[common_index].values.flatten()
    mkt = market_returns.loc[common_index].values.flatten()

    avg_daily = pf.mean()
    annual_returns = ((1 + avg_daily) ** trading_days - 1) * 100
    daily_std = pf.std()
    annual_volatility = daily_std * np.sqrt(trading_days) * 100
    daily_rf = risk_free_rate / trading_days
    excess_daily = pf - daily_rf
    sharpe_ratio = (excess_daily.mean() / excess_daily.std()) * np.sqrt(trading_days)
    net_ret = pf - avg_daily
    negative_ret = net_ret[net_ret < 0]
    semi_dev = np.sqrt(np.sum(negative_ret ** 2) / len(pf))
    sortino_ratio = (excess_daily.mean() / semi_dev) * np.sqrt(trading_days)

    cov_value = np.cov(mkt, pf)[0, 1]
    mkt_var = mkt.var()
    beta = cov_value / mkt_var

    treynor_ratio = (excess_daily.mean() * trading_days) / beta
    information_ratio = ((avg_daily - mkt.mean()) / (pf - mkt).std()) * np.sqrt(trading_days)
    skewness = pd.Series(pf).skew()
    excess_kurtosis = pd.Series(pf).kurtosis()
    cumprod_ret = (pd.Series(pf) + 1).cumprod() * 100
    trough_index = (np.maximum.accumulate(cumprod_ret) - cumprod_ret).idxmax()
    peak_index = cumprod_ret.loc[:trough_index].idxmax()
    maximum_drawdown = 100 * ((cumprod_ret[trough_index] - cumprod_ret[peak_index]) / cumprod_ret[peak_index])

    return {
        'annual_returns': annual_returns,
        'annual_volatility': annual_volatility,
        'sharpe_ratio': sharpe_ratio,
        'sortino_ratio': sortino_ratio,
        'beta': beta,
        'treynor_ratio': treynor_ratio,
        'information_ratio': information_ratio,
        'skewness': skewness,
        'excess_kurtosis': excess_kurtosis,
        'maximum_drawdown': maximum_drawdown
    }


def print_portfolio_results(metrics):
    table = pd.DataFrame({
        'Parameters': ['Annual Returns', 'Annual Volatility', 'Sharpe Ratio', 'Sortino Ratio',
                      'Beta', 'Treynor Ratio', 'Information Ratio', 'Skewness', 'Kurtosis',
                      'Maximum Drawdown'],
        'Value': [metrics['annual_returns'], metrics['annual_volatility'], metrics['sharpe_ratio'], 
                 metrics['sortino_ratio'], metrics['beta'], metrics['treynor_ratio'], 
                 metrics['information_ratio'], metrics['skewness'], metrics['excess_kurtosis'], 
                 metrics['maximum_drawdown']]
    })
    print(tabulate(table, headers='keys', tablefmt='psql'))


def plot_cumulative_returns(portfolio_returns, figsize=(10, 7)):
    cumprod_ret = (portfolio_returns + 1).cumprod() * 100
    cumprod_ret.index = pd.to_datetime(cumprod_ret.index)
    trough_index = (np.maximum.accumulate(cumprod_ret) - cumprod_ret).idxmax()
    peak_index = cumprod_ret.loc[:trough_index].idxmax()

    plt.figure(figsize=figsize)
    plt.plot(cumprod_ret, label='Cumulative Returns')
    plt.plot([peak_index, trough_index], [cumprod_ret[peak_index], cumprod_ret[trough_index]], 'o', color='r', markersize=5)
    plt.title('Cumulative Returns', fontsize=16)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Returns in %', fontsize=14)
    plt.legend(['Cumulative Returns', 'Peak and Trough'], fontsize=14)
    plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
    plt.show()


def plot_running_maximum_drawdown(portfolio_returns, figsize=(10, 7)):
    cumprod_ret = (portfolio_returns + 1).cumprod() * 100
    running_max = np.maximum.accumulate(cumprod_ret)
    running_max[running_max < 1] = 1
    running_max_drawdown = (cumprod_ret / running_max) - 1

    plt.figure(figsize=figsize)
    plt.plot(running_max_drawdown, color='red')
    plt.title('Running Maximum Drawdown', fontsize=16)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Maximum Drawdown', fontsize=14)
    plt.legend(['Running Maximum Drawdown'], fontsize=14)
    plt.grid(which='major', color='k', linestyle='--', linewidth=0.2)
    plt.fill_between(running_max_drawdown.index, running_max_drawdown, alpha=0.5, color='r', linewidth=0)
    plt.show()


def plot_returns_histogram(portfolio_returns, figsize=(10, 7)):
    returns_clean = portfolio_returns.dropna()

    plt.figure(figsize=figsize)
    plt.hist(returns_clean, bins=50, alpha=0.5, edgecolor='purple', color='purple')
    plt.title('Returns', fontsize=16)
    plt.xlabel('Returns in %', fontsize=14)
    plt.ylabel('Number of Days', fontsize=14)
    plt.show()


def plot_monthly_heatmap(portfolio_returns, figsize=(10, 7)):
    returns = portfolio_returns.copy()
    returns.index = pd.to_datetime(returns.index)

    portfolio_monthly_mean = returns.resample('ME').mean()
    portfolio_monthly_count = returns.resample('ME').count()
    portfolio_monthly_ret = (portfolio_monthly_mean + 1) ** portfolio_monthly_count - 1

    monthly_data = pd.DataFrame({
        'returns': portfolio_monthly_ret.values,
        'date': portfolio_monthly_ret.index
    })
    monthly_data['Year'] = monthly_data['date'].dt.year
    monthly_data['Month'] = monthly_data['date'].dt.strftime('%b')

    portfolio_pivot = monthly_data.pivot(index='Year', columns='Month', values='returns')

    plt.figure(figsize=figsize)
    sns.heatmap(portfolio_pivot, annot=True, fmt=".2f", cmap='plasma', cbar=True)
    plt.title('Monthly Returns', fontsize=16)
    plt.xlabel('Month', fontsize=14)
    plt.ylabel('Year', fontsize=14)
    plt.show()


def plot_portfolio_vs_benchmark(portfolio_returns, market_returns, leverage=2, figsize=(10, 7)):
    cumprod_ret_leverage = ((portfolio_returns * leverage) + 1).cumprod() * 100
    cumprod_market_ret = (market_returns + 1).cumprod() * 100

    plt.figure(figsize=figsize)
    plt.plot(cumprod_ret_leverage, label='Portfolio')
    plt.plot(cumprod_market_ret, label='QQQ')
    plt.title('Nasdaq-100 VS Portfolio', fontsize=16)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Annualized Returns', fontsize=14)
    plt.legend(['Portfolio', 'QQQ'], fontsize=14)
    plt.grid(which='major', color='k', linestyle='-.', linewidth=0.5)
    plt.show()
