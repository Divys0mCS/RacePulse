"""Builds a sector-time chart for a driver's laps."""

import plotly.graph_objects as go

from app.models.lap import Lap


def build_sector_chart(laps: list[Lap]) -> go.Figure:
    """Return a Plotly Figure showing all three sector times per lap."""

    if not laps:
        raise ValueError("Cannot build a sector chart with no laps")

    ordered_laps = sorted(laps, key=lambda lap: lap.lap_number)

    lap_numbers = [lap.lap_number for lap in ordered_laps]

    sector_1_times = [lap.sector_times[0] for lap in ordered_laps]
    sector_2_times = [lap.sector_times[1] for lap in ordered_laps]
    sector_3_times = [lap.sector_times[2] for lap in ordered_laps]

    driver_name = ordered_laps[0].driver.name

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=lap_numbers,
            y=sector_1_times,
            mode="lines+markers",
            name="Sector 1",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=lap_numbers,
            y=sector_2_times,
            mode="lines+markers",
            name="Sector 2",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=lap_numbers,
            y=sector_3_times,
            mode="lines+markers",
            name="Sector 3",
        )
    )

    fig.update_layout(
        title=f"Sector Times - {driver_name}",
        xaxis_title="Lap Number",
        yaxis_title="Sector Time (s)",
    )

    return fig