import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def plot_rolling_sharpe(
    returns: pd.Series,
    ticker: str,
    window: int = 30,
    trading_days: int = 252
):
    """
    Plot rolling Sharpe ratio.
    """
    rolling_mean = returns.rolling(window).mean() * trading_days
    rolling_std = returns.rolling(window).std() * np.sqrt(trading_days)

    rolling_sharpe = rolling_mean / rolling_std

    plt.figure(figsize=(10, 4))
    plt.plot(rolling_sharpe.index, rolling_sharpe.values)
    plt.axhline(0, linestyle="--")
    plt.title(f"{ticker} {window}-Day Rolling Sharpe Ratio")
    plt.xlabel("Date")
    plt.ylabel("Sharpe Ratio")
    plt.grid(True)
    plt.show()

# Show the overall summary of Sharpe, Sortino and Calmar ratios
def show_risk_adjusted_summary(
    sharpe: float,
    sortino: float,
    calmar: float
):
    """
    Display risk-adjusted metrics summary.
    """
    summary = pd.DataFrame({
        "Metric": ["Sharpe Ratio", "Sortino Ratio", "Calmar Ratio"],
        "Value": [sharpe, sortino, calmar]
    })

    print("\nRisk-Adjusted Performance Summary")
    print(summary.to_string(index=False, float_format="%.2f"))

import matplotlib.pyplot as plt
import pandas as pd


def plot_rolling_calmar(
    prices: pd.Series,
    ticker: str,
    window: int = 252,
    trading_days: int = 252
):
    """
    Plot rolling Calmar ratio.

    Rolling Calmar =
    Rolling Annualized Return / Rolling Maximum Drawdown
    """

    # -------------------------
    # 1️⃣ Rolling Annualized Return
    # -------------------------

    rolling_returns = prices.pct_change()

    rolling_mean_return = (
        rolling_returns.rolling(window).mean() * trading_days
    )

    # -------------------------
    # 2️⃣ Rolling Maximum Drawdown
    # -------------------------

    rolling_max_price = prices.rolling(window).max()
    rolling_drawdown = prices / rolling_max_price - 1

    rolling_mdd = rolling_drawdown.rolling(window).min()

    # Avoid divide by zero
    rolling_mdd = rolling_mdd.replace(0, np.nan)

    # -------------------------
    # 3️⃣ Rolling Calmar
    # -------------------------

    rolling_calmar = rolling_mean_return / rolling_mdd.abs()

    # -------------------------
    # 4️⃣ Plot
    # -------------------------

    plt.figure(figsize=(10, 4))
    plt.plot(rolling_calmar.index, rolling_calmar.values)
    plt.axhline(0, linestyle="--")
    plt.title(f"{ticker} {window}-Day Rolling Calmar Ratio")
    plt.xlabel("Date")
    plt.ylabel("Calmar Ratio")
    plt.grid(True)
    plt.show()

def plot_risk_adjusted_summary(
    sharpe: float,
    sortino: float,
    calmar: float,
    ticker: str
):
    """
    Plot a bar chart summary of risk-adjusted metrics.
    """
    metrics = ["Sharpe", "Sortino", "Calmar"]
    values = [sharpe, sortino, calmar]

    plt.figure(figsize=(6, 4))
    bars = plt.bar(metrics, values)

    plt.title(f"{ticker} Risk-Adjusted Performance Summary")
    plt.ylabel("Ratio Value")
    plt.axhline(0, linestyle="--", linewidth=0.8)

    # Annotate values on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f"{height:.2f}",
            ha="center",
            va="bottom"
        )

    plt.grid(axis="y", linestyle="--", alpha=0.6)
    plt.show()
