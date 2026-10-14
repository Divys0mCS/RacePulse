"""Build speed-versus-distance charts for a lap's telemetry."""

import plotly.graph_objects as go

from app.models.telemetry import Telemetry
from analytics.processing.cleaner import TelemetryCleaner
from analytics.processing.transformer import TelemetryTransformer
from analytics.processing.resampler import TelemetryResampler


def build_speed_trace(
    telemetry: Telemetry,
    resample_step_m: float | None = None,
) -> go.Figure:
    """Build a speed trace for one lap.

    Args:
        telemetry: Telemetry data belonging to a lap.
        resample_step_m: Optional distance interval in metres for resampling.
            For example, 10.0 produces samples on a regular 10-metre grid.

    Returns:
        A Plotly Figure showing speed against distance.

    Raises:
        ValueError: If telemetry has no samples.
    """
    if not telemetry.samples:
        raise ValueError(
            "Cannot build a speed trace for a Telemetry with no samples"
        )

    # Step 1: Sort samples and remove exact duplicates.
    cleaner = TelemetryCleaner()
    cleaned_samples = cleaner.clean(telemetry.samples)

    # Step 2: Add normalized distance percentages.
    track_length_km = (
        telemetry.lap.session.race.track.length_km
    )

    transformer = TelemetryTransformer()
    transformed_samples = transformer.transform(
        cleaned_samples,
        track_length_km=track_length_km,
    )

    # Step 3: Optionally interpolate onto a regular distance grid.
    if resample_step_m is not None:
        resampler = TelemetryResampler()
        processed_samples = resampler.resample(
            transformed_samples,
            step_m=resample_step_m,
        )
    else:
        processed_samples = transformed_samples

    # Step 4: Extract the values needed for the chart.
    distances = [
        sample["distance_m"] for sample in processed_samples
    ]
    speeds = [
        sample["speed_kph"] for sample in processed_samples
    ]

    lap = telemetry.lap

    # Step 5: Build the Plotly chart.
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=distances,
            y=speeds,
            mode="lines",
            name=f"{lap.driver.name} - Lap {lap.lap_number}",
        )
    )

    fig.update_layout(
        title=(
            f"Speed Trace - {lap.driver.name}, "
            f"Lap {lap.lap_number} ({lap.lap_time_seconds:.3f}s)"
        ),
        xaxis_title="Distance (m)",
        yaxis_title="Speed (kph)",
    )

    return fig