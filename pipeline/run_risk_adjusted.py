# pipeline/run_risk_adjusted.py

from engine.returns import compute_log_returns
from engine.risk_adjusted import (
    sharpe_ratio,
    sortino_ratio,
    calmar_ratio
)
from visuals.risk_adjusted_plots import (
    plot_rolling_sharpe,
    show_risk_adjusted_summary,
    plot_risk_adjusted_summary,
    plot_rolling_calmar
)
from chat.event_explainer import explain_event_with_llm


def run_risk_adjusted_metrics(
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
    Risk-Adjusted Metrics Pipeline (Professional Version)

    Flags:
    - verbose → print metrics
    - use_visuals → show plots
    - use_llm → generate explanation
    """

    # -------------------------
    # 1️⃣ Compute returns
    # -------------------------
    returns = compute_log_returns(prices)

    # -------------------------
    # 2️⃣ Compute metrics
    # -------------------------
    sharpe = sharpe_ratio(returns)
    sortino = sortino_ratio(returns)
    calmar = calmar_ratio(prices)

    # -------------------------
    # 3️⃣ Prepare structured outputs
    # -------------------------

    # RAW values (for chatbot context)
    raw_outputs = {
        "sharpe_ratio": sharpe,
        "sortino_ratio": sortino,
        "calmar_ratio": calmar,
        "rolling_window_days": rolling_window
    }

    # Formatted values (for LLM prompt)
    formatted_outputs = {
        "sharpe_ratio": f"{sharpe:.2f}",
        "sortino_ratio": f"{sortino:.2f}",
        "calmar_ratio": f"{calmar:.2f}",
        "rolling_window_days": rolling_window
    }

    # -------------------------
    # 4️⃣ Optional printing
    # -------------------------
    if verbose:
        print("\nRisk-Adjusted Metrics")

        print(
            "Sharpe Ratio: (Reward per unit of total risk) (>1 is good)\n"
            f" {sharpe:.2f}"
        )

        print(
            "Sortino Ratio: (Reward per unit of downside risk) (>1 is good)\n"
            f" {sortino:.2f}"
        )

        print(
            "Calmar Ratio: (Reward per unit of worst-case pain) "
            "(>1 means annual growth exceeded worst drawdown)\n"
            f" {calmar:.2f}"
        )

    # -------------------------
    # 5️⃣ Optional visuals
    # -------------------------
    if use_visuals:
        plot_rolling_sharpe(
            returns,
            ticker,
            window=rolling_window
        )

        show_risk_adjusted_summary(
            sharpe,
            sortino,
            calmar
        )

        plot_rolling_calmar(
        prices,
        ticker,
        window=rolling_window
        )

        plot_risk_adjusted_summary(
            sharpe,
            sortino,
            calmar,
            ticker
        )

        

    # -------------------------
    # 6️⃣ Optional LLM explanation
    # -------------------------
    risk_adjusted_explanation = None

    if use_llm:
        risk_adjusted_explanation = explain_event_with_llm(
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
            event_name="Risk-Adjusted Metrics",
            event_outputs=formatted_outputs
        )

        if verbose:
            print("\n📘 Risk-Adjusted Metrics Explanation")
            print(risk_adjusted_explanation)

    # -------------------------
    # 7️⃣ Return structured result
    # -------------------------
    return {
        "raw": raw_outputs,
        "formatted": formatted_outputs,
        "explanation": risk_adjusted_explanation
    }
