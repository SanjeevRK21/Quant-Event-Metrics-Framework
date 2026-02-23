# pipeline/run_growth.py

from engine.growth import total_return, cagr
from visuals.growth_plots import (
    plot_price_series,
    plot_cumulative_returns
)
from chat.event_explainer import explain_event_with_llm


def run_growth_metrics(
    prices,
    ticker: str,
    start_date: str,
    end_date: str,
    use_llm: bool = False,
    use_visuals: bool = True,
    verbose: bool = False
):
    """
    Growth Metrics Pipeline (Professional Version)

    Flags:
    - verbose → print metrics
    - use_visuals → show charts
    - use_llm → generate explanation
    """

    # -------------------------
    # 1️⃣ Compute growth metrics
    # -------------------------
    total_return_value = total_return(prices)
    cagr_value = cagr(prices)

    # Raw numerical outputs (for chatbot context)
    raw_outputs = {
        "total_return": total_return_value,
        "cagr": cagr_value
    }

    # Formatted outputs (for LLM prompt / display)
    formatted_outputs = {
        "total_return": f"{total_return_value:.2%}",
        "cagr": f"{cagr_value:.2%}"
    }

    # -------------------------
    # 2️⃣ Print metrics (optional)
    # -------------------------
    if verbose:
        print("\nGrowth Metrics")
        print(f"Total Return: {total_return_value:.2%}")
        print(f"CAGR: {cagr_value:.2%}")

    # -------------------------
    # 3️⃣ Optional LLM explanation
    # -------------------------
    growth_explanation = None

    if use_llm:
        growth_explanation = explain_event_with_llm(
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
            event_name="Growth Metrics",
            event_outputs=formatted_outputs
        )

        if verbose:
            print("\n📘 Growth Metrics Explanation")
            print(growth_explanation)

    # -------------------------
    # 4️⃣ Visuals (optional)
    # -------------------------
    if use_visuals:
        plot_price_series(prices, ticker)
        plot_cumulative_returns(prices, ticker)

    # -------------------------
    # 5️⃣ Return structured result
    # -------------------------
    return {
        "raw": raw_outputs,
        "formatted": formatted_outputs,
        "explanation": growth_explanation
    }
