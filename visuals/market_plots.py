import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import linregress


def plot_stock_vs_market(
    stock_returns: pd.Series,
    market_returns: pd.Series,
    stock_ticker: str,
    market_ticker: str
):
    """
    Scatter plot of stock returns vs market returns with regression line.
    """

    # Align dates
    data = pd.concat([stock_returns, market_returns], axis=1).dropna()
    data.columns = ["stock", "market"]

    # Regression
    regression = linregress(data["market"], data["stock"])
    beta = regression.slope
    alpha = regression.intercept
    r_squared = regression.rvalue ** 2

    # Scatter plot
    plt.figure(figsize=(6, 6))
    plt.scatter(
        data["market"],
        data["stock"],
        alpha=0.4,
        s=15,
        color = 'lightcoral'
    )

    # Regression line
    x = np.linspace(data["market"].min(), data["market"].max(), 100)
    y = alpha + beta * x
    plt.plot(x, y, color="darkred", linewidth=2)

    plt.xlabel(f"{market_ticker} Daily Returns")
    plt.ylabel(f"{stock_ticker} Daily Returns")
    plt.title(f"{stock_ticker} vs {market_ticker} Returns")

    # Annotate stats
    plt.text(
        0.05,
        0.95,
        f"Beta = {beta:.2f}\nAlpha (daily) = {alpha:.4f}\nR² = {r_squared:.2f}",
        transform=plt.gca().transAxes,
        verticalalignment="top",
        bbox=dict(boxstyle="round", alpha=0.2)
    )

    plt.axhline(0, linestyle="--", linewidth=0.8)
    plt.axvline(0, linestyle="--", linewidth=0.8)
    plt.grid(True)
    print('Steep slope → high beta (aggressive) \nFlat slope → low beta (defensive) \nTight cluster → high R² (market-driven) \nWide scatter → low R² (stock specifics \nAlpha - shows what would stock\'s price be if the market returns to 0)')
    plt.show()
