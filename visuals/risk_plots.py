import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def plot_returns(returns: pd.Series, ticker: str):
    plt.figure(figsize=(10, 4))
    plt.plot(returns.index, returns.values)
    plt.axhline(0, linestyle="--")
    plt.title(f"{ticker} Daily Log Returns")
    plt.xlabel("Date")
    plt.ylabel("Return")
    plt.grid(True)
    plt.show()


def plot_rolling_volatility(
    returns: pd.Series,
    ticker: str,
    window: int = 30,
    trading_days: int = 252
):
    rolling_vol = returns.rolling(window).std() * np.sqrt(trading_days)

    plt.figure(figsize=(10, 4))
    plt.plot(rolling_vol.index, rolling_vol.values)
    plt.title(f"{ticker} {window}-Day Rolling Annualized Volatility") # this basically tells how volatile was the past x days and its dragged to the whole year, this matrix does'nt predict anything. 
    plt.xlabel("Date")
    plt.ylabel("Volatility")
    plt.grid(True)
    plt.show()


def plot_drawdown(prices: pd.Series, ticker: str):
    cumulative_max = prices.cummax()
    drawdown = (prices - cumulative_max) / cumulative_max

    plt.figure(figsize=(10, 4))
    plt.plot(drawdown.index, drawdown.values, color="red")
    plt.axhline(0, linestyle="--")
    plt.title(f"{ticker} Drawdown")
    plt.xlabel("Date")
    plt.ylabel("Drawdown")
    plt.grid(True)
    plt.show()
