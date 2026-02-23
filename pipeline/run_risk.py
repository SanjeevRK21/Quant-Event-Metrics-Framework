# pipeline/run_risk.py

from engine.returns import compute_log_returns
from engine.risk import (
    annualized_volatility,
    downside_volatility,
    max_drawdown
)
from visuals.risk_plots import (
    plot_returns,
    plot_rolling_volatility,
    plot_drawdown
)
from chat.event_explainer import explain_event_with_llm


def run_risk_metrics(
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
    Risk Metrics Pipeline (Unified Professional Version)

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
    # 2️⃣ Compute Risk Metrics
    # -------------------------
    vol = annualized_volatility(returns)
    down_vol = downside_volatility(returns)
    mdd = max_drawdown(prices)

    # -------------------------
    # 3️⃣ Prepare Structured Outputs
    # -------------------------

    # RAW values (for chatbot context)
    raw_outputs = {
        "annualized_volatility": vol,
        "downside_volatility": down_vol,
        "max_drawdown": mdd,
        "rolling_window_days": rolling_window
    }

    # Formatted values (for LLM prompt)
    formatted_outputs = {
        "annualized_volatility": f"{vol:.2%}",
        "downside_volatility": f"{down_vol:.2%}",
        "max_drawdown": f"{mdd:.2%}",
        "rolling_window_days": rolling_window
    }

    # -------------------------
    # 4️⃣ Optional Printing
    # -------------------------
    if verbose:
        print("\nRisk Metrics")
        print(f"Annualized Volatility: {vol:.2%}")
        print(f"Downside Volatility: {down_vol:.2%}")
        print(f"Max Drawdown: {mdd:.2%}")

    # -------------------------
    # 5️⃣ Optional Visualizations
    # -------------------------
    if use_visuals:
        plot_returns(returns, ticker)

        plot_rolling_volatility(
            returns,
            ticker,
            window=rolling_window
        )

        plot_drawdown(prices, ticker)

    # -------------------------
    # 6️⃣ Optional LLM Explanation
    # -------------------------
    risk_explanation = None

    if use_llm:
        risk_explanation = explain_event_with_llm(
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
            event_name="Risk Metrics",
            event_outputs=formatted_outputs
        )

        if verbose:
            print("\n📘 Risk Metrics Explanation")
            print(risk_explanation)

    # -------------------------
    # 7️⃣ Return Structured Result
    # -------------------------
    return {
        "raw": raw_outputs,
        "formatted": formatted_outputs,
        "explanation": risk_explanation
    }
