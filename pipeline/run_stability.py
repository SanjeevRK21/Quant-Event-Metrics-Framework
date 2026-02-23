# pipeline/run_stability.py

from engine.returns import compute_log_returns
from engine.stability import (
    rolling_sharpe,
    max_drawdown_duration,
    recovery_time,
    drawdown_duration
)
from visuals.stability_plots import (
    plot_rolling_sharpe,
    plot_drawdown_duration
)
from chat.event_explainer import explain_event_with_llm


def run_stability_metrics(
    prices,
    ticker: str,
    start_date: str,
    end_date: str,
    rolling_window: int = 30,
    use_llm: bool = False,
    use_visuals: bool = False,
    verbose: bool = False
):
    """
    Stability Metrics Pipeline (Unified Professional Version)

    Flags:
    - verbose → print metrics
    - use_visuals → show plots
    - use_llm → generate explanation
    """

    # -------------------------
    # 1️⃣ Compute Returns
    # -------------------------
    returns = compute_log_returns(prices)

    # -------------------------
    # 2️⃣ Compute Stability Metrics
    # -------------------------
    rolling_sharpe_series = rolling_sharpe(
        returns,
        window=rolling_window
    )

    max_dd_duration = max_drawdown_duration(prices)
    recovery_days = recovery_time(prices)
    dd_duration_series = drawdown_duration(prices)

    # Safe rolling stats (avoid NaN issues)
    rolling_mean = rolling_sharpe_series.mean()
    rolling_min = rolling_sharpe_series.min()
    rolling_max = rolling_sharpe_series.max()

    # -------------------------
    # 3️⃣ Prepare Structured Outputs
    # -------------------------

    # RAW values (for chatbot context)
    raw_outputs = {
        "max_drawdown_duration_days": max_dd_duration,
        "recovery_time_days": recovery_days,
        "rolling_window_days": rolling_window,
        "rolling_sharpe_mean": rolling_mean,
        "rolling_sharpe_min": rolling_min,
        "rolling_sharpe_max": rolling_max
    }

    # Formatted values (for LLM)
    formatted_outputs = {
        "max_drawdown_duration_days": f"{max_dd_duration}",
        "recovery_time_days": f"{recovery_days}",
        "rolling_window_days": f"{rolling_window}",
        "rolling_sharpe_mean": f"{rolling_mean:.2f}",
        "rolling_sharpe_min": f"{rolling_min:.2f}",
        "rolling_sharpe_max": f"{rolling_max:.2f}"
    }

    # -------------------------
    # 4️⃣ Optional Printing
    # -------------------------
    if verbose:
        print("\nStability Metrics")

        print(
            f"Max Drawdown Duration (days): {max_dd_duration}\n"
            "Longest continuous time below previous peak."
        )

        print(
            f"Recovery Time (days): {recovery_days}\n"
            "Time taken to recover from deepest drawdown."
        )

        print(
            f"Rolling Sharpe (mean/min/max): "
            f"{rolling_mean:.2f} / {rolling_min:.2f} / {rolling_max:.2f}"
        )

    # -------------------------
    # 5️⃣ Optional Visualizations
    # -------------------------
    if use_visuals:
        plot_rolling_sharpe(
            rolling_sharpe_series,
            ticker,
            window=rolling_window
        )

        plot_drawdown_duration(
            dd_duration_series,
            ticker
        )

    # -------------------------
    # 6️⃣ Optional LLM Explanation
    # -------------------------
    stability_explanation = None

    if use_llm:
        stability_explanation = explain_event_with_llm(
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
            event_name="Stability Metrics",
            event_outputs=formatted_outputs
        )

        if verbose:
            print("\n📘 Stability Metrics Explanation")
            print(stability_explanation)

    # -------------------------
    # 7️⃣ Return Structured Result
    # -------------------------
    return {
        "raw": raw_outputs,
        "formatted": formatted_outputs,
        "series": {
            "rolling_sharpe": rolling_sharpe_series,
            "drawdown_duration": dd_duration_series
        },
        "explanation": stability_explanation
    }
