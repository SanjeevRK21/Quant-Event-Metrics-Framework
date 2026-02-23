import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def plot_price_series(prices: pd.Series, ticker: str):
    plt.figure(figsize=(10, 4))
    plt.plot(prices.index, prices.values)
    plt.title(f"{ticker} Price Series")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)
    plt.show()


def plot_cumulative_returns(prices: pd.Series, ticker: str):
    cumulative_returns = prices / prices.iloc[0]

    plt.figure(figsize=(10, 4))
    plt.plot(cumulative_returns.index, cumulative_returns.values)
    plt.title(f"{ticker} Cumulative Return")
    plt.xlabel("Date")
    plt.ylabel("Growth of $1")
    plt.grid(True)
    plt.show()
