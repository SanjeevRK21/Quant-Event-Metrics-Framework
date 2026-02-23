# visuals/investment_plots.py

import matplotlib.pyplot as plt
import pandas as pd


def plot_portfolio_value(portfolio_series: pd.Series, ticker: str):
    """
    Plot portfolio value over time.
    """
    plt.figure(figsize=(10, 4))
    plt.plot(portfolio_series.index, portfolio_series.values)

    plt.title(f"Portfolio Value Over Time ({ticker})")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value")
    plt.grid(True)
    plt.show()


def plot_portfolio_value_with_extremes(
    portfolio_series: pd.Series,
    min_value_date,
    max_value_date,
    ticker: str
):
    """
    Plot portfolio value with markers for min and max value.
    """
    plt.figure(figsize=(10, 4))
    plt.plot(portfolio_series.index, portfolio_series.values)

    # Mark extremes
    plt.scatter(
        min_value_date,
        portfolio_series.loc[min_value_date],
        marker="v",
        s=100,
        label="Lowest Value"
    )

    plt.scatter(
        max_value_date,
        portfolio_series.loc[max_value_date],
        marker="^",
        s=100,
        label="Highest Value"
    )

    plt.title(f"Portfolio Value with Extremes ({ticker})")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value")
    plt.legend()
    plt.grid(True)
    plt.show()


def plot_daily_pnl(
    portfolio_series: pd.Series,
    max_gain_date,
    max_loss_date,
    ticker: str
):
    """
    Plot daily profit/loss in absolute currency terms.
    """
    daily_pnl = portfolio_series.diff()

    plt.figure(figsize=(10, 4))
    plt.bar(daily_pnl.index, daily_pnl.values)

    # Highlight extremes
    plt.scatter(
        max_gain_date,
        daily_pnl.loc[max_gain_date],
        s=100,
        label="Largest Gain"
    )

    plt.scatter(
        max_loss_date,
        daily_pnl.loc[max_loss_date],
        s=100,
        label="Largest Loss"
    )

    plt.axhline(0, linestyle="--", linewidth=0.8)
    plt.title(f"Daily P&L (Absolute) ({ticker})")
    plt.xlabel("Date")
    plt.ylabel("Daily Change in Value")
    plt.legend()
    plt.grid(True, axis="y")
    plt.show()


def plot_drawdown_in_currency(portfolio_series: pd.Series, ticker: str):
    """
    Plot drawdown in absolute currency terms.
    """
    cumulative_max = portfolio_series.cummax()
    drawdown_currency = portfolio_series - cumulative_max

    plt.figure(figsize=(10, 4))
    plt.plot(drawdown_currency.index, drawdown_currency.values)

    plt.axhline(0, linestyle="--", linewidth=0.8)
    plt.title(f"Drawdown in Currency Terms ({ticker})")
    plt.xlabel("Date")
    plt.ylabel("Drawdown Value")
    plt.grid(True)
    plt.show()
