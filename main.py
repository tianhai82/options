import yfinance as yf
import pandas as pd
import numpy as np


def sharpe_ratio(returns):
    return returns.mean() / returns.std() * 252**0.5


def get_returns(history):
    return history['Close'].pct_change()


def min_max(series):
    return (series-series.min())/(series.max()-series.min())


def standardise(series):
    return (series-series.mean())/series.std()


symbols = pd.read_csv("trading_view.csv")
symbols['sharpe'] = np.nan
symbols['volume'] = np.nan
symbols['volume_pct'] = np.nan
symbols['std_dev'] = np.nan
symbols['last_trade'] = np.nan


for i, row in symbols.iterrows():
    stock = yf.Ticker(row["symbol"])
    history = stock.history(period="3mo")
    returns = get_returns(history)
    symbols.loc[i, 'std_dev'] = returns.std()
    symbols.loc[i, 'sharpe'] = sharpe_ratio(returns)
    symbols.loc[i, 'volume'] = history.iloc[-1]['Volume']
    symbols.loc[i, 'volume_pct'] = history['Volume'].rank(pct=True)[-1]
    symbols.loc[i, 'last_trade'] = history.iloc[-1]['Close']

symbols['volume_norm'] = min_max(symbols['volume'])
symbols['volume_stan'] = standardise(symbols['volume'])
symbols['volume_pct_norm'] = min_max(symbols['volume_pct'])
symbols['volume_pct_stan'] = standardise(symbols['volume_pct'])
symbols['sharpe_norm'] = min_max(symbols['sharpe'])
symbols['sharpe_stan'] = standardise(symbols['sharpe'])

symbols.to_excel("trading_view_out.xlsx", index=False)
