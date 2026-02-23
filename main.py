from engine.data_loader import get_available_date_range, load_price_data
from engine.growth import total_return, cagr
from visuals.growth_plots import plot_price_series, plot_cumulative_returns

ticker = "AAPL"
start_date = "2020-01-01"
end_date = "2021-01-01"

prices = load_price_data(ticker, start_date, end_date)

'''
# Growth metrics
print(f"Total Return: {total_return(prices):.2%}")
print(f"CAGR: {cagr(prices):.2%}")

total_return_value = total_return(prices)
cagr_value = cagr(prices)


# Growth Metrics Ollama explanation
from chat.event_explainer_org import explain_event_with_llm

growth_outputs = {
    "total_return": f"{total_return_value:.2%}",
    "cagr": f"{cagr_value:.2%}"
}

growth_explanation = explain_event_with_llm(
    ticker=ticker,
    start_date=start_date,
    end_date=end_date,
    event_name="Growth Metrics",
    event_outputs=growth_outputs
)

print("\n📘 Growth Explanation")
print(growth_explanation)


# Growth visuals
plot_price_series(prices, ticker)
plot_cumulative_returns(prices, ticker)

'''
# Risk Metrics
from engine.returns import compute_log_returns
from engine.risk import (
    annualized_volatility,
    downside_volatility,
    max_drawdown
)

returns = compute_log_returns(prices)

vol = annualized_volatility(returns)
down_vol = downside_volatility(returns)
mdd = max_drawdown(prices)

risk_outputs = {
    "annualized_volatility": f"{vol:.2%}",
    "downside_volatility": f"{down_vol:.2%}",
    "max_drawdown": f"{mdd:.2%}"
}

print("\nRisk Metrics")
print(f"Annualized Volatility: {vol:.2%}") 
print(f"Downside Volatility: {down_vol:.2%}") 
print(f"Max Drawdown: {mdd:.2%}")

# Risk Metrics Ollama explanation

from chat.event_explainer_org import explain_event_with_llm

risk_explanation = explain_event_with_llm(
    ticker=ticker,
    start_date=start_date,
    end_date=end_date,
    event_name="Risk Metrics",
    event_outputs=risk_outputs
)

print("\n📘 Risk Metrics Explanation")
print(risk_explanation)


# Risk visuals
from visuals.risk_plots import (
    plot_returns,
    plot_rolling_volatility,
    plot_drawdown
)

plot_returns(returns, ticker)
plot_rolling_volatility(returns, ticker)
plot_drawdown(prices, ticker)
'''

#Risk Adjusted Metrics
from engine.risk_adjusted import sharpe_ratio, sortino_ratio, calmar_ratio

sharpe = sharpe_ratio(returns)
sortino = sortino_ratio(returns)
calmar = calmar_ratio(prices)

risk_adjusted_outputs = {
    "sharpe_ratio": f"{sharpe:.2f}",
    "sortino_ratio": f"{sortino:.2f}",
    "calmar_ratio": f"{calmar:.2f}"
}

print("\nRisk-Adjusted Metrics")
print(f"Sharpe Ratio: (Reward per unit of total risk) (>1 is good)\n {sharpe:.2f}")
print(f"Sortino Ratio: (Reward per unit of downside risk) (>1 is good)\n {sortino:.2f}")
print(f"Calmar Ratio: (Reward per unit of worst-case pain) (>1 means annual growth exceeded worst drawdown)\n {calmar:.2f}")


# Risk Adjusted Ollama explainer
from chat.event_explainer_org import explain_event_with_llm

risk_adjusted_explanation = explain_event_with_llm(
    ticker=ticker,
    start_date=start_date,
    end_date=end_date,
    event_name="Risk-Adjusted Metrics",
    event_outputs=risk_adjusted_outputs
)

print("\n📘 Risk-Adjusted Metrics Explanation")
print(risk_adjusted_explanation)


#Risk Adjusted visuals
from visuals.risk_adjusted_plots import (
    plot_rolling_sharpe,
    show_risk_adjusted_summary
)

# Risk-adjusted visuals
plot_rolling_sharpe(returns, ticker)
show_risk_adjusted_summary(sharpe, sortino, calmar)

from visuals.risk_adjusted_plots import plot_risk_adjusted_summary
plot_risk_adjusted_summary(sharpe, sortino, calmar, ticker)


# Tail_Risk Metrics
from engine.tail_risk import (
    skewness,
    kurtosis_excess,
    value_at_risk,
    conditional_value_at_risk
)

skew_val = skewness(returns)
kurt_val = kurtosis_excess(returns)
var_95 = value_at_risk(returns, 0.95)
cvar_95 = conditional_value_at_risk(returns, 0.95)

tail_risk_outputs = {
    "skewness": f"{skew_val:.2f}",
    "kurtosis": f"{kurt_val:.2f}",
    "value_at_risk_95": f"{var_95:.2%}",
    "conditional_var_95": f"{cvar_95:.2%}"
}

print("\nTail Risk Metrics (What do losses look like when things go really wrong?)")
print(f"Skewness: \n(>0 - rare big gains, <0 - rare big losses(most days looks fine, but crashes are sudden and severe), ~~0 normal most of the days)\n{skew_val:.2f}")
print(f"Excess Kurtosis: \n(How frequently extreme event happen)\n(>0 (fat tails) crashes more frequently, <0 (thin tails) very rare extremes)\n{kurt_val:.2f}")
print(f"VaR (95%): \n(worst loss that you could face for the 95% of days, like this shows the threshold limit, loses wont go beyond this 95% of the times)\n{var_95:.2%}")
print(f"CVaR (95%): \n(avg loss on those remaining 5% of the days (the worst condition days))\n{cvar_95:.2%}")
print(f"\n In the graph: \n Blue Histogram shows daily return distribution, it is backed by density on the x axis which means the number of days the perticular daily return occured \n Orange curve - shows the average values of the histogram bars \n Red Dashed Vertical Line — VaR (95%) - i.e 95% of days had losses smaller than this value \n Dark Red Solid Line — CVaR (95%) - Avg loss incurred during the remaining worst 5%")


# Tail Risk Ollama Explainer
from chat.event_explainer_org import explain_event_with_llm

tail_risk_explanation = explain_event_with_llm(
    ticker=ticker,
    start_date=start_date,
    end_date=end_date,
    event_name="Tail Risk Metrics",
    event_outputs=tail_risk_outputs
)

print("\n📘 Tail Risk Metrics Explanation")
print(tail_risk_explanation)


# Tail_risk Visuals
from visuals.tail_risk_plots import plot_return_distribution
plot_return_distribution(returns, ticker, var_95, cvar_95)



# Market Sensitivity depended Metrics
market_ticker = "^GSPC"  # S&P 500

market_prices = load_price_data(market_ticker, start_date, end_date)
market_returns = compute_log_returns(market_prices)

from engine.market import market_metrics

market_stats = market_metrics(returns, market_returns)

market_outputs = {
    "beta": f"{market_stats['Beta']:.2f}",
    "alpha_daily": f"{market_stats['Alpha']:.2%}",
    "r_squared": f"{market_stats['R2']:.2f}"
}

print("\nMarket Sensitivity Metrics\n")
print(f"Beta: {market_stats['Beta']:.2f} \n(Beta > 1 → more aggressive than market)\n")
print(f"Alpha (annual):  {market_stats['Alpha']:.2%} \n(Positive alpha → outperformed market-adjusted expectations)\n ")
print(f"R²: {market_stats['R2']:.2f} \n(R² = 0.62 → 62% of movement explained by market)\n ")

# Market Sensitivity Ollama explainer
from chat.event_explainer_org import explain_event_with_llm

market_explanation = explain_event_with_llm(
    ticker=ticker,
    start_date=start_date,
    end_date=end_date,
    event_name="Market Sensitivity Metrics",
    event_outputs=market_outputs
)

print("\n📘 Market Sensitivity Explanation")
print(market_explanation)


# Market depended visuals
from visuals.market_plots import plot_stock_vs_market

plot_stock_vs_market(
    stock_returns=returns,
    market_returns=market_returns,
    stock_ticker=ticker,
    market_ticker=market_ticker
)


# Stability Metrics
from engine.stability import (
    rolling_sharpe,
    max_drawdown_duration,
    recovery_time
)

rolling_sharpe_series = rolling_sharpe(returns)

max_dd_duration = max_drawdown_duration(prices)
recovery_days = recovery_time(prices)

stability_outputs = {
    "max_underwater_duration_days": f"{max_dd_duration}",
    "recovery_time_days": f"{recovery_days}",
    "rolling_sharpe_window_days": "30"
}

print("\nStability Metrics")
print(f"Max Drawdown Duration (days): {max_dd_duration} \n The longest continuous period during which the stock stayed below its previous peak")
print(f"Recovery Time (days): {recovery_days} \n After the deepest drawdown (worst crash), how many days it took for the stock to climb back to its previous peak.")

# Stability Ollama explainer
from chat.event_explainer_org import explain_event_with_llm

stability_explanation = explain_event_with_llm(
    ticker=ticker,
    start_date=start_date,
    end_date=end_date,
    event_name="Stability Metrics",
    event_outputs=stability_outputs
)

print("\n📘 Stability Metrics Explanation")
print(stability_explanation)


# Stability Visuals
from visuals.stability_plots import (
    plot_rolling_sharpe,
    plot_drawdown_duration
)

from engine.stability import drawdown_duration

# Rolling Sharpe plot
plot_rolling_sharpe(
    rolling_sharpe_series,
    ticker,
    window=30
)

# Drawdown duration plot
dd_duration_series = drawdown_duration(prices)
plot_drawdown_duration(dd_duration_series, ticker)



# Drawdown and recovery historical Metrics

from engine.drawdown_events import drawdown_events_df
from visuals.drawdown_events_plots import (
    show_top_drawdowns,
    show_top_recovery_times,
    show_recent_drawdowns,
    show_recent_recoveries
)

# Extract drawdown events
dd_events = drawdown_events_df(prices)

# Historical extremes
show_top_drawdowns(dd_events, n=10)
show_top_recovery_times(dd_events, n=10)

# Recent behavior
show_recent_drawdowns(dd_events, n=10)
show_recent_recoveries(dd_events, n=10)

# Ollama Explanation is  not required for the below event as the tabular values are enough to understand
# Drawdown and recovery historical Ollama explanation

worst_drawdown_event = dd_events.sort_values(
    "drawdown_pct"
).iloc[0]

most_recent_drawdown_event = dd_events.sort_values(
    "trough_date", ascending=False
).iloc[0]

worst_recovery_event = (
    dd_events
    .dropna(subset=["recovery_time_days"])
    .sort_values("recovery_time_days", ascending=False)
    .iloc[0]
)

most_recent_recovery_event = (
    dd_events
    .dropna(subset=["recovery_date"])
    .sort_values("recovery_date", ascending=False)
    .iloc[0]
)


import pandas as pd

def format_drawdown_event(event_row):
    return {
        "peak_date": event_row["peak_date"].date().isoformat(),
        "trough_date": event_row["trough_date"].date().isoformat(),
        "recovery_date": (
            event_row["recovery_date"].date().isoformat()
            if pd.notna(event_row["recovery_date"])
            else "Not yet recovered"
        ),
        "drawdown_percent": f"{event_row['drawdown_pct']:.2f}%",
        "drawdown_duration_days": int(event_row["drawdown_duration_days"]),
        "recovery_time_days": (
            int(event_row["recovery_time_days"])
            if pd.notna(event_row["recovery_time_days"])
            else "Ongoing"
        )
    }

worst_drawdown_outputs = format_drawdown_event(worst_drawdown_event)
recent_drawdown_outputs = format_drawdown_event(most_recent_drawdown_event)
worst_recovery_outputs = format_drawdown_event(worst_recovery_event)
recent_recovery_outputs = format_drawdown_event(most_recent_recovery_event)

# Drawdown and recovery historical Ollama explanation
from chat.event_explainer_org import explain_event_with_llm

worst_drawdown_explanation = explain_event_with_llm(
    ticker=ticker,
    start_date=start_date,
    end_date=end_date,
    event_name="Worst Drawdown Event",
    event_outputs=worst_drawdown_outputs
)

print("\n📕 Worst Drawdown Explanation")
print(worst_drawdown_explanation)

recent_drawdown_explanation = explain_event_with_llm(
    ticker=ticker,
    start_date=start_date,
    end_date=end_date,
    event_name="Most Recent Drawdown Event",
    event_outputs=recent_drawdown_outputs
)

print("\n📘 Most Recent Drawdown Explanation")
print(recent_drawdown_explanation)

from chat.event_explainer_org import explain_event_with_llm

worst_recovery_explanation = explain_event_with_llm(
    ticker=ticker,
    start_date=start_date,
    end_date=end_date,
    event_name="Worst Recovery Event",
    event_outputs=worst_recovery_outputs
)

print("\n📕 Worst Recovery Explanation")
print(worst_recovery_explanation)

recent_recovery_explanation = explain_event_with_llm(
    ticker=ticker,
    start_date=start_date,
    end_date=end_date,
    event_name="Most Recent Recovery Event",
    event_outputs=recent_recovery_outputs
)

print("\n📘 Most Recent Recovery Explanation")
print(recent_recovery_explanation)


# Drawdown and recovery historical visuals

from visuals.drawdown_events_plots import (
    plot_top_drawdowns,
    plot_top_recovery_times,
    plot_recent_drawdown_durations,
    plot_recent_recovery_times
)

plot_top_drawdowns(dd_events, n=10)
plot_top_recovery_times(dd_events, n=10)
plot_recent_drawdown_durations(dd_events, n=10)
plot_recent_recovery_times(dd_events, n=10)


# Investment_simulator engine
from engine.investment_simulator import simulate_investment

initial_capital = 100000  # example

investment_stats = simulate_investment(prices, initial_capital)

print("\nInvestment Simulation Results")
print(f"Initial Investment: {investment_stats['initial_investment']:.2f}")
print(f"Final Value: {investment_stats['final_value']:.2f}")

print(f"Lowest Value: {investment_stats['min_value']:.2f} on {investment_stats['min_value_date'].date()}")
print(f"Highest Value: {investment_stats['max_value']:.2f} on {investment_stats['max_value_date'].date()}")

print(f"Largest Daily Gain: {investment_stats['max_daily_gain']:.2f} on {investment_stats['max_daily_gain_date'].date()}")
print(f"Largest Daily Loss: {investment_stats['max_daily_loss']:.2f} on {investment_stats['max_daily_loss_date'].date()}")

# Investment_simulator Ollama Explanation
investment_outputs = {
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

from chat.event_explainer_org import explain_event_with_llm

investment_explanation = explain_event_with_llm(
    ticker=ticker,
    start_date=start_date,
    end_date=end_date,
    event_name="Investment Simulation",
    event_outputs=investment_outputs
)

print("\n💰 Investment Simulation Explanation")
print(investment_explanation)



# Investment_plots
from visuals.investment_plots import (
    plot_portfolio_value,
    plot_portfolio_value_with_extremes,
    plot_daily_pnl,
    plot_drawdown_in_currency
)

plot_portfolio_value(
    investment_stats["portfolio_series"],
    ticker
)

plot_portfolio_value_with_extremes(
    investment_stats["portfolio_series"],
    investment_stats["min_value_date"],
    investment_stats["max_value_date"],
    ticker
)

plot_daily_pnl(
    investment_stats["portfolio_series"],
    investment_stats["max_daily_gain_date"],
    investment_stats["max_daily_loss_date"],
    ticker
)

plot_drawdown_in_currency(
    investment_stats["portfolio_series"],
    ticker
)
'''

