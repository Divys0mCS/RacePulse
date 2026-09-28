"""Builds a lap-time chart for a driver's laps."""

import plotly.graph_objects as go

from app.models.lap import Lap


def build_lap_chart(laps: list[Lap]) -> go.Figure:
    """Return a Plotly Figure plotting lap number against lap time."""

    if not laps:
        raise ValueError("Cannot build a lap chart with no laps")

    ordered_laps = sorted(laps, key=lambda lap: lap.lap_number)

    lap_numbers = [lap.lap_number for lap in ordered_laps]
    lap_times = [lap.lap_time_seconds for lap in ordered_laps]

    driver_name = ordered_laps[0].driver.name

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=lap_numbers,
            y=lap_times,
            mode="lines+markers",
            name=driver_name,
        )
    )

    fig.update_layout(
        title=f"Lap Times - {driver_name}",
        xaxis_title="Lap Number",
        yaxis_title="Lap Time (s)",
    )

    return fig