# backend/analytics/visualization/speed_trace.py

"""Builds a speed-vs-distance chart for a single Lap's telemetry.

This is the first real use of Plotly in the project - everything before this
(PaceAnalyzer, ConsistencyAnalyzer, SectorAnalyzer) only ever printed numbers.
A speed trace is the classic motorsport visualization: where on the track a
driver lifts, brakes, and gets back to full throttle, read directly off the
distance axis.
"""

import plotly.graph_objects as go
from app.models.telemetry import Telemetry


def build_speed_trace(telemetry: Telemetry) -> go.Figure:
    """Return a Plotly Figure plotting speed (kph) against distance (m) for one lap."""
    if not telemetry.samples:
        raise ValueError("Cannot build a speed trace for a Telemetry with no samples")

    samples = sorted(telemetry.samples, key=lambda s: s.distance_m)
    distances = [s.distance_m for s in samples]
    speeds = [s.speed_kph for s in samples]

    lap = telemetry.lap
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=distances,
        y=speeds,
        mode="lines",
        name=f"{lap.driver.name} - Lap {lap.lap_number}",
    ))
    fig.update_layout(
        title=f"Speed Trace - {lap.driver.name}, Lap {lap.lap_number} ({lap.lap_time_seconds:.3f}s)",
        xaxis_title="Distance (m)",
        yaxis_title="Speed (kph)",
    )
    return fig