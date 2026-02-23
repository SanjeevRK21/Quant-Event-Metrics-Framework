# pipeline/run_tail_risk.py

from engine.returns import compute_log_returns
from engine.tail_risk import (
    skewness,
    kurtosis_excess,
    value_at_risk,
    conditional_value_at_risk
)
from visuals.tail_risk_plots import plot_return_distribution
from chat.event_explainer import explain_event_with_llm


def run_tail_risk_metrics(
    prices,
    ticker: str,
    start_date: str,
    end_date: str,
    confidence_level: float = 0.95,
    use_llm: bool = False,
    use_visuals: bool = False,
    verbose: bool = False
):
    """
    Tail Risk Pipeline (Professional Version)

    Flags:
    - verbose → print metrics
    - use_visuals → show charts
    - use_llm → generate explanation
    """

    # -------------------------
    # 1️⃣ Compute returns
    # -------------------------
    returns = compute_log_returns(prices)

    # -------------------------
    # 2️⃣ Compute tail risk metrics
    # -------------------------
    skew_val = skewness(returns)
    kurt_val = kurtosis_excess(returns)
    var_val = value_at_risk(returns, confidence_level)
    cvar_val = conditional_value_at_risk(returns, confidence_level)

    confidence_pct = int(confidence_level * 100)

    # -------------------------
    # 3️⃣ Prepare structured outputs
    # -------------------------

    # RAW values (for research chatbot context)
    raw_outputs = {
        "skewness": skew_val,
        "kurtosis_excess": kurt_val,
        "value_at_risk": var_val,
        "conditional_value_at_risk": cvar_val,
        "confidence_level": confidence_level
    }

    # Formatted values (for LLM prompts)
    formatted_outputs = {
        "skewness": f"{skew_val:.2f}",
        "kurtosis_excess": f"{kurt_val:.2f}",
        "value_at_risk": f"{var_val:.2%}",
        "conditional_value_at_risk": f"{cvar_val:.2%}",
        "confidence_level": f"{confidence_pct}%"
    }

    # -------------------------
    # 4️⃣ Optional Printing
    # -------------------------
    if verbose:
        print("\nTail Risk Metrics")
        print(
            "Skewness:\n"
            "(>0 → rare big gains, <0 → rare crashes)\n"
            f"{skew_val:.2f}"
        )

        print(
            "Excess Kurtosis:\n"
            "(>0 → fat tails, more extreme events)\n"
            f"{kurt_val:.2f}"
        )

        print(
            f"VaR ({confidence_pct}%):\n"
            "(Loss threshold for most days)\n"
            f"{var_val:.2%}"
        )

        print(
            f"CVaR ({confidence_pct}%):\n"
            "(Average loss during worst tail days)\n"
            f"{cvar_val:.2%}"
        )

    # -------------------------
    # 5️⃣ Optional Visuals
    # -------------------------
    if use_visuals:
        plot_return_distribution(
            returns,
            ticker,
            var_val,
            cvar_val
        )

    # -------------------------
    # 6️⃣ Optional LLM Explanation
    # -------------------------
    tail_risk_explanation = None

    if use_llm:
        tail_risk_explanation = explain_event_with_llm(
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
            event_name="Tail Risk Metrics",
            event_outputs=formatted_outputs
        )

        if verbose:
            print("\n📘 Tail Risk Metrics Explanation")
            print(tail_risk_explanation)

    # -------------------------
    # 7️⃣ Return structured result
    # -------------------------
    return {
        "raw": raw_outputs,
        "formatted": formatted_outputs,
        "explanation": tail_risk_explanation
    }
