# pipeline/run_full_analysis.py

import os
import json
from engine.data_loader import load_price_data

from pipeline.run_growth import run_growth_metrics
from pipeline.run_risk import run_risk_metrics
from pipeline.run_risk_adjusted import run_risk_adjusted_metrics
from pipeline.run_tail_risk import run_tail_risk_metrics
from pipeline.run_market_sensitivity import run_market_sensitivity_metrics
from pipeline.run_stability import run_stability_metrics
from pipeline.run_investment_simulation import run_investment_simulation
from pipeline.run_drawdown_events import run_drawdown_events


def run_full_analysis(
    ticker: str,
    start_date: str,
    end_date: str,
    initial_capital: float = 100_000,
    use_cache: bool = False
):

    cache_file = f"cache_{ticker}_{start_date}_{end_date}.json"

    # -------------------------------------
    # Load From Cache
    # -------------------------------------
    if use_cache and os.path.exists(cache_file):
        print("⚡ Loading analysis from cache...")
        with open(cache_file, "r") as f:
            return json.load(f)

    print("📊 Running fresh analysis...")

    # -------------------------------------
    # Load Data
    # -------------------------------------
    prices = load_price_data(
        ticker=ticker,
        start=start_date,
        end=end_date
    )

    # -------------------------------------
    # Run Pipelines
    # -------------------------------------

    growth_results = run_growth_metrics(
        prices, ticker, start_date, end_date
    )

    risk_results = run_risk_metrics(
        prices, ticker, start_date, end_date
    )

    risk_adjusted_results = run_risk_adjusted_metrics(
        prices, ticker, start_date, end_date
    )

    tail_risk_results = run_tail_risk_metrics(
        prices, ticker, start_date, end_date
    )

    market_results = run_market_sensitivity_metrics(
        prices, ticker, start_date, end_date
    )

    stability_results = run_stability_metrics(
        prices, ticker, start_date, end_date
    )

    investment_results = run_investment_simulation(
        prices, ticker, start_date, end_date,
        initial_capital=initial_capital
    )

    # ✅ NEW: Drawdown Events
    drawdown_results = run_drawdown_events(
        prices,
        ticker,
        start_date,
        end_date,
        use_llm=False   # keep off unless needed
    )

    # -------------------------------------
    # Build Structured Chatbot Context
    # -------------------------------------

    context = {
        "ticker": ticker,
        "start_date": start_date,
        "end_date": end_date,
        "growth": growth_results,
        "risk": risk_results,
        "risk_adjusted": risk_adjusted_results,
        "tail_risk": tail_risk_results,
        "market_sensitivity": market_results,
        "stability": stability_results,
        "investment_simulation": investment_results,
        "drawdown_events": drawdown_results   # ✅ added here
    }

    # -------------------------------------
    # Save Cache
    # -------------------------------------

    if use_cache:
        with open(cache_file, "w") as f:
            json.dump(context, f, indent=2, default=str)
        print("💾 Context saved to cache.")

    return context
