# pipeline/run_market_sensitivity.py

from engine.data_loader import load_price_data
from engine.returns import compute_log_returns
from engine.market import market_metrics
from visuals.market_plots import plot_stock_vs_market
from chat.event_explainer import explain_event_with_llm


def run_market_sensitivity_metrics(
    prices,
    ticker: str,
    start_date: str,
    end_date: str,
    market_ticker: str = "^GSPC",
    use_llm: bool = False,
    use_visuals: bool = False,
    verbose: bool = False
):
    """
    Market Sensitivity Pipeline (Professional Version)

    Flags:
    - verbose → print metrics
    - use_visuals → show regression plot
    - use_llm → generate explanation
    """

    # -------------------------
    # 1️⃣ Compute stock returns
    # -------------------------
    stock_returns = compute_log_returns(prices)

    # -------------------------
    # 2️⃣ Load market data
    # -------------------------
    market_prices = load_price_data(
        ticker=market_ticker,
        start=start_date,
        end=end_date
    )

    market_returns = compute_log_returns(market_prices)

    # -------------------------
    # 3️⃣ Compute metrics
    # -------------------------
    market_stats = market_metrics(
        stock_returns,
        market_returns
    )

    beta = market_stats["Beta"]
    alpha_annual = market_stats["Alpha"]
    r_squared = market_stats["R2"]

    # -------------------------
    # 4️⃣ Prepare structured outputs
    # -------------------------

    # RAW values (for chatbot context)
    raw_outputs = {
        "beta": beta,
        "alpha_annual": alpha_annual,
        "r_squared": r_squared,
        "market_ticker": market_ticker
    }

    # Formatted values (for LLM prompt)
    formatted_outputs = {
        "beta": f"{beta:.2f}",
        "alpha_annual": f"{alpha_annual:.2%}",
        "r_squared": f"{r_squared:.2f}",
        "market_ticker": market_ticker
    }

    # -------------------------
    # 5️⃣ Optional printing
    # -------------------------
    if verbose:
        print("\nMarket Sensitivity Metrics\n")

        print(
            f"Beta: {beta:.2f}\n"
            "(Beta > 1 → more aggressive than market)\n"
        )

        print(
            f"Alpha (annual): {alpha_annual:.2%}\n"
            "(Positive alpha → outperformed market-adjusted expectations)\n"
        )

        print(
            f"R²: {r_squared:.2f}\n"
            "(Higher R² → stock movement strongly explained by market)\n"
        )

    # -------------------------
    # 6️⃣ Optional LLM explanation
    # -------------------------
    market_explanation = None

    if use_llm:
        market_explanation = explain_event_with_llm(
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
            event_name="Market Sensitivity Metrics",
            event_outputs=formatted_outputs
        )

        if verbose:
            print("\n📘 Market Sensitivity Explanation")
            print(market_explanation)

    # -------------------------
    # 7️⃣ Optional visuals
    # -------------------------
    if use_visuals:
        plot_stock_vs_market(
            stock_returns=stock_returns,
            market_returns=market_returns,
            stock_ticker=ticker,
            market_ticker=market_ticker
        )

    # -------------------------
    # 8️⃣ Return structured result
    # -------------------------
    return {
        "raw": raw_outputs,
        "formatted": formatted_outputs,
        "explanation": market_explanation
    }
