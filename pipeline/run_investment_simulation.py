# pipeline/run_investment_simulation.py

from engine.investment_simulator import simulate_investment
from visuals.investment_plots import (
    plot_portfolio_value,
    plot_portfolio_value_with_extremes,
    plot_daily_pnl,
    plot_drawdown_in_currency
)
from chat.event_explainer import explain_event_with_llm


def run_investment_simulation(
    prices,
    ticker: str,
    start_date: str,
    end_date: str,
    initial_capital: float = 100_000,
    use_llm: bool = False,
    use_visuals: bool = False,
    verbose: bool = False
):
    """
    Investment Simulation Pipeline (Professional Version)

    Flags:
    - verbose → print metrics
    - use_visuals → show charts
    - use_llm → generate explanation
    """

    # -------------------------
    # 1️⃣ Simulate investment
    # -------------------------
    investment_stats = simulate_investment(
        prices,
        initial_capital
    )

    # -------------------------
    # 2️⃣ Prepare structured outputs
    # -------------------------

    # RAW values (for chatbot context)
    raw_outputs = {
        "initial_investment": investment_stats["initial_investment"],
        "final_value": investment_stats["final_value"],
        "min_value": investment_stats["min_value"],
        "min_value_date": investment_stats["min_value_date"],
        "max_value": investment_stats["max_value"],
        "max_value_date": investment_stats["max_value_date"],
        "max_daily_gain": investment_stats["max_daily_gain"],
        "max_daily_gain_date": investment_stats["max_daily_gain_date"],
        "max_daily_loss": investment_stats["max_daily_loss"],
        "max_daily_loss_date": investment_stats["max_daily_loss_date"],
    }

    # Formatted values (for LLM prompt / display)
    formatted_outputs = {
        "initial_investment": f"{investment_stats['initial_investment']:.2f}",
        "final_value": f"{investment_stats['final_value']:.2f}",
        "lowest_value": f"{investment_stats['min_value']:.2f}",
        "lowest_value_date": investment_stats["min_value_date"].date().isoformat(),
        "highest_value": f"{investment_stats['max_value']:.2f}",
        "highest_value_date": investment_stats["max_value_date"].date().isoformat(),
        "largest_daily_gain": f"{investment_stats['max_daily_gain']:.2f}",
        "largest_daily_gain_date": investment_stats["max_daily_gain_date"].date().isoformat(),
        "largest_daily_loss": f"{investment_stats['max_daily_loss']:.2f}",
        "largest_daily_loss_date": investment_stats["max_daily_loss_date"].date().isoformat()
    }

    # -------------------------
    # 3️⃣ Optional printing
    # -------------------------
    if verbose:
        print("\nInvestment Simulation Results")

        print(f"Initial Investment: {raw_outputs['initial_investment']:.2f}")
        print(f"Final Value: {raw_outputs['final_value']:.2f}")

        print(
            f"Lowest Value: {raw_outputs['min_value']:.2f} "
            f"on {raw_outputs['min_value_date'].date()}"
        )

        print(
            f"Highest Value: {raw_outputs['max_value']:.2f} "
            f"on {raw_outputs['max_value_date'].date()}"
        )

        print(
            f"Largest Daily Gain: {raw_outputs['max_daily_gain']:.2f} "
            f"on {raw_outputs['max_daily_gain_date'].date()}"
        )

        print(
            f"Largest Daily Loss: {raw_outputs['max_daily_loss']:.2f} "
            f"on {raw_outputs['max_daily_loss_date'].date()}"
        )

    # -------------------------
    # 4️⃣ Optional LLM explanation
    # -------------------------
    investment_explanation = None

    if use_llm:
        investment_explanation = explain_event_with_llm(
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
            event_name="Investment Simulation",
            event_outputs=formatted_outputs
        )

        if verbose:
            print("\n💰 Investment Simulation Explanation")
            print(investment_explanation)

    # -------------------------
    # 5️⃣ Optional visuals
    # -------------------------
    if use_visuals:
        portfolio_series = investment_stats["portfolio_series"]

        plot_portfolio_value(portfolio_series, ticker)

        plot_portfolio_value_with_extremes(
            portfolio_series,
            investment_stats["min_value_date"],
            investment_stats["max_value_date"],
            ticker
        )

        plot_daily_pnl(
            portfolio_series,
            investment_stats["max_daily_gain_date"],
            investment_stats["max_daily_loss_date"],
            ticker
        )

        plot_drawdown_in_currency(
            portfolio_series,
            ticker
        )

    # -------------------------
    # 6️⃣ Return structured result
    # -------------------------
    return {
        "raw": raw_outputs,
        "formatted": formatted_outputs,
        "explanation": investment_explanation
    }
