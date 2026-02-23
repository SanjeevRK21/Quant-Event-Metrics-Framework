import matplotlib.pyplot as plt
import pandas as pd


def plot_rolling_sharpe(
    rolling_sharpe: pd.Series,
    ticker: str,
    window: int
):
    plt.figure(figsize=(10, 4))
    plt.plot(rolling_sharpe.index, rolling_sharpe.values)

    plt.axhline(0, linestyle="--", linewidth=0.8)
    plt.title(f"{ticker} {window}-Day Rolling Sharpe Ratio")
    plt.xlabel("Date")
    plt.ylabel("Sharpe Ratio")
    plt.grid(True)
    plt.show()


def plot_drawdown_duration(
    drawdown_duration: pd.Series,
    ticker: str
):
    plt.figure(figsize=(10, 4))
    plt.plot(drawdown_duration.index, drawdown_duration.values, color="red")

    plt.title(f"{ticker} Drawdown Duration (Days Underwater)")
    plt.xlabel("Date")
    plt.ylabel("Days Underwater")
    plt.grid(True)
    plt.show()
