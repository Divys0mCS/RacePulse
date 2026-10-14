import pytest
from app.models.telemetry import TelemetrySample
from analytics.processing.transformer import TelemetryTransformer


def test_transformer_adds_normalized_distance_percentage():
    samples = [
        TelemetrySample(
            distance_m=0,
            speed_kph=120,
            throttle_pct=80,
            brake_pct=0,
            gear=4,
            rpm=9000,
        ),
        TelemetrySample(
            distance_m=2945.5,
            speed_kph=250,
            throttle_pct=100,
            brake_pct=0,
            gear=7,
            rpm=11000,
        ),
        TelemetrySample(
            distance_m=5891,
            speed_kph=280,
            throttle_pct=100,
            brake_pct=0,
            gear=8,
            rpm=12000,
        ),
    ]

    transformed = TelemetryTransformer().transform(samples, track_length_km=5.891)

    assert [point["distance_pct"] for point in transformed] == [
        0.0,
        50.0,
        100.0,
    ]


def test_transformer_preserves_original_telemetry_values():
    sample = TelemetrySample(
        distance_m=2945.5,
        speed_kph=250,
        throttle_pct=100,
        brake_pct=0,
        gear=7,
        rpm=11000,
    )

    transformed = TelemetryTransformer().transform(
        [sample],
        track_length_km=5.891,
    )

    assert transformed[0]["distance_m"] == 2945.5
    assert transformed[0]["speed_kph"] == 250
    assert transformed[0]["throttle_pct"] == 100
    assert transformed[0]["brake_pct"] == 0
    assert transformed[0]["gear"] == 7
    assert transformed[0]["rpm"] == 11000


def test_transformer_handles_empty_samples():
    assert TelemetryTransformer().transform([], track_length_km=5.891) == []


def test_transformer_rejects_non_positive_track_length():
    samples = [
        TelemetrySample(
            distance_m=100,
            speed_kph=200,
            throttle_pct=100,
            brake_pct=0,
            gear=6,
            rpm=10000,
        )
    ]

    for invalid_length in [0, -1]:
        try:
            TelemetryTransformer().transform(
                samples,
                track_length_km=invalid_length,
            )
            
        except ValueError:
            pass
        else:
            raise AssertionError("Expected ValueError for invalid track length")

def test_transform_rejects_sample_beyond_track_length():
    """Reject telemetry samples beyond the configured track length."""
    transformer = TelemetryTransformer()
    samples = [
        TelemetrySample(
            distance_m=5100,
            speed_kph=250,
            throttle_pct=100,
            brake_pct=0,
            gear=5,
            rpm=10000,
        )
    ]

    with pytest.raises(ValueError, match="exceeds track length"):
        transformer.transform(samples, track_length_km=5)


def test_transform_accepts_sample_at_track_length():
    """Accept a telemetry sample exactly at the track length."""
    transformer = TelemetryTransformer()
    samples = [
        TelemetrySample(
            distance_m=5000,
            speed_kph=250,
            throttle_pct=100,
            brake_pct=0,
            gear=5,
            rpm=10000,
        )
    ]

    result = transformer.transform(samples, track_length_km=5)

    assert result[0]["distance_pct"] == 100.0