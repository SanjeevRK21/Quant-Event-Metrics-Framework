# visuals/drawdown_events_plots.py

import pandas as pd
from tabulate import tabulate

def _print_table(df: pd.DataFrame, title: str):
    print("\n" + title)
    print("=" * len(title))
    print(
        tabulate(
            df,
            headers="keys",
            tablefmt="fancy_grid",   # pretty borders
            showindex=False
        )
    )


def show_top_drawdowns(df: pd.DataFrame, n: int = 10):
    result = (
        df.sort_values("drawdown_pct")
          .head(n)[[
              "peak_date",
              "trough_date",
              "drawdown_pct",
              "drawdown_duration_days",
              "recovery_time_days"
          ]]
    )
    _print_table(result, f"Top {n} Worst Drawdowns (by Depth)")


def show_top_recovery_times(df: pd.DataFrame, n: int = 10):
    result = (
        df.dropna(subset=["recovery_time_days"])
          .sort_values("recovery_time_days", ascending=False)
          .head(n)[[
              "trough_date",
              "recovery_date",
              "recovery_time_days",
              "drawdown_pct"
          ]]
    )
    _print_table(result, f"Top {n} Slowest Recoveries")


def show_recent_drawdowns(df: pd.DataFrame, n: int = 10):
    result = (
        df.sort_values("trough_date", ascending=False)
          .head(n)[[
              "peak_date",
              "trough_date",
              "drawdown_pct",
              "drawdown_duration_days",
              "recovery_time_days"
          ]]
    )
    _print_table(result, f"Most Recent {n} Drawdowns")


def show_recent_recoveries(df: pd.DataFrame, n: int = 10):
    result = (
        df.dropna(subset=["recovery_date"])
          .sort_values("recovery_date", ascending=False)
          .head(n)[[
              "trough_date",
              "recovery_date",
              "recovery_time_days",
              "drawdown_pct"
          ]]
    )
    _print_table(result, f"Most Recent {n} Recoveries")


########################
import matplotlib.pyplot as plt
import pandas as pd


def plot_top_drawdowns(df: pd.DataFrame, n: int = 10):
    data = df.sort_values("drawdown_pct").head(n)

    plt.figure(figsize=(8, 4))
    plt.barh(
        range(len(data)),
        data["drawdown_pct"]
    )
    plt.yticks(range(len(data)), data["trough_date"].dt.date)
    plt.xlabel("Drawdown (%)")
    plt.title(f"Top {n} Worst Drawdowns")
    plt.gca().invert_yaxis()
    plt.grid(True, axis="x")
    plt.show()


def plot_top_recovery_times(df: pd.DataFrame, n: int = 10):
    data = (
        df.dropna(subset=["recovery_time_days"])
          .sort_values("recovery_time_days", ascending=False)
          .head(n)
    )

    plt.figure(figsize=(8, 4))
    plt.barh(
        range(len(data)),
        data["recovery_time_days"]
    )
    plt.yticks(range(len(data)), data["trough_date"].dt.date)
    plt.xlabel("Recovery Time (Days)")
    plt.title(f"Top {n} Slowest Recoveries")
    plt.gca().invert_yaxis()
    plt.grid(True, axis="x")
    plt.show()


def plot_recent_drawdown_durations(df: pd.DataFrame, n: int = 10):
    data = df.sort_values("trough_date", ascending=False).head(n)

    plt.figure(figsize=(8, 4))
    plt.bar(
        range(len(data)),
        data["drawdown_duration_days"]
    )
    plt.xticks(range(len(data)), data["trough_date"].dt.date, rotation=45)
    plt.ylabel("Duration (Days)")
    plt.title(f"Most Recent {n} Drawdown Durations")
    plt.grid(True, axis="y")
    plt.show()


def plot_recent_recovery_times(df: pd.DataFrame, n: int = 10):
    data = (
        df.dropna(subset=["recovery_date"])
          .sort_values("recovery_date", ascending=False)
          .head(n)
    )

    plt.figure(figsize=(8, 4))
    plt.bar(
        range(len(data)),
        data["recovery_time_days"]
    )
    plt.xticks(range(len(data)), data["recovery_date"].dt.date, rotation=45)
    plt.ylabel("Recovery Time (Days)")
    plt.title(f"Most Recent {n} Recovery Times")
    plt.grid(True, axis="y")
    plt.show()
