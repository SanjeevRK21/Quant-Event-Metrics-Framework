# pipeline/run_drawdown_events.py

import pandas as pd

from engine.drawdown_events import drawdown_events_df
from visuals.drawdown_events_plots import (
    show_top_drawdowns,
    show_top_recovery_times,
    show_recent_drawdowns,
    show_recent_recoveries,
    plot_top_drawdowns,
    plot_top_recovery_times,
    plot_recent_drawdown_durations,
    plot_recent_recovery_times
)

from chat.event_explainer import explain_event_with_llm


def _format_drawdown_event(event_row: pd.Series) -> dict:
    """Format a single drawdown/recovery event for display or chatbot context."""
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


def run_drawdown_events(
    prices,
    ticker: str,
    start_date: str,
    end_date: str,
    n: int = 10,
    use_llm: bool = False,
    use_visuals: bool = False,
    verbose: bool = False
):
    """
    Drawdown & Recovery Pipeline (Professional Version)

    Flags:
    - verbose → print tables
    - use_visuals → show plots
    - use_llm → generate explanations
    """

    # -------------------------
    # 1️⃣ Extract drawdown events
    # -------------------------
    dd_events = drawdown_events_df(prices)

    if dd_events.empty:
        if verbose:
            print("No drawdown events detected.")
        return None

    # -------------------------
    # 2️⃣ Tabular summaries
    # -------------------------
    if verbose:
        show_top_drawdowns(dd_events, n=n)
        show_top_recovery_times(dd_events, n=n)
        show_recent_drawdowns(dd_events, n=n)
        show_recent_recoveries(dd_events, n=n)

    # -------------------------
    # 3️⃣ Select key events
    # -------------------------
    worst_drawdown_event = dd_events.sort_values("drawdown_pct").iloc[0]
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

    # -------------------------
    # 4️⃣ Format outputs
    # -------------------------
    formatted_outputs = {
        "worst_drawdown": _format_drawdown_event(worst_drawdown_event),
        "most_recent_drawdown": _format_drawdown_event(most_recent_drawdown_event),
        "worst_recovery": _format_drawdown_event(worst_recovery_event),
        "most_recent_recovery": _format_drawdown_event(most_recent_recovery_event)
    }

    # -------------------------
    # 5️⃣ Optional LLM explanations
    # -------------------------
    explanations = {}

    if use_llm:
        for event_key, event_data in formatted_outputs.items():

            readable_name = event_key.replace("_", " ").title()

            explanation = explain_event_with_llm(
                ticker=ticker,
                start_date=start_date,
                end_date=end_date,
                event_name=readable_name,
                event_outputs=event_data
            )

            explanations[event_key] = explanation

            if verbose:
                print(f"\n📘 {readable_name} Explanation")
                print(explanation)

    # -------------------------
    # 6️⃣ Visual summaries
    # -------------------------
    if use_visuals:
        plot_top_drawdowns(dd_events, n=n)
        plot_top_recovery_times(dd_events, n=n)
        plot_recent_drawdown_durations(dd_events, n=n)
        plot_recent_recovery_times(dd_events, n=n)

    # -------------------------
    # 7️⃣ Return structured result
    # -------------------------
    return {
        "raw_dataframe": dd_events,
        "formatted": formatted_outputs,
        "explanations": explanations if use_llm else None
    }
