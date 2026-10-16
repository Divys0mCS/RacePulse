import pytest

from analytics.processing.resampler import TelemetryResampler


def make_point(
    distance_m,
    speed_kph,
    throttle_pct=100.0,
    brake_pct=0.0,
):
    return {
        "distance_m": distance_m,
        "distance_pct": distance_m / 58.91,
        "speed_kph": speed_kph,
        "throttle_pct": throttle_pct,
        "brake_pct": brake_pct,
        "gear": 7,
        "rpm": 11000,
    }


def test_resampler_creates_regular_distance_grid():
    samples = [
        make_point(0, 100),
        make_point(1000, 300),
    ]

    result = TelemetryResampler().resample(samples, step_m=500)

    assert [point["distance_m"] for point in result] == [
        0,
        500,
        1000,
    ]


def test_resampler_linearly_interpolates_continuous_values():
    samples = [
        make_point(0, 100, throttle_pct=0, brake_pct=100),
        make_point(1000, 300, throttle_pct=100, brake_pct=0),
    ]

    result = TelemetryResampler().resample(samples, step_m=500)

    middle = result[1]

    assert middle["speed_kph"] == 200.0
    assert middle["throttle_pct"] == 50.0
    assert middle["brake_pct"] == 50.0


def test_resampler_handles_empty_samples():
    assert TelemetryResampler().resample([], step_m=100) == []


def test_resampler_rejects_non_positive_step():
    samples = [make_point(0, 100)]

    with pytest.raises(ValueError):
        TelemetryResampler().resample(samples, step_m=0)

    with pytest.raises(ValueError):
        TelemetryResampler().resample(samples, step_m=-10)


@pytest.mark.parametrize(
    "invalid_distance",
    [
        -1,
        float("nan"),
        float("inf"),
        float("-inf"),
    ],
    ids=["negative", "nan", "positive-infinity", "negative-infinity"],
)
def test_resampler_rejects_invalid_distances(invalid_distance):
    samples = [
        make_point(0, 100),
        make_point(invalid_distance, 200),
    ]

    with pytest.raises(
        ValueError,
        match="distance_m values must be finite and non-negative",
    ):
        TelemetryResampler().resample(samples, step_m=100)


def test_resampler_rejects_duplicate_distances():
    samples = [
        make_point(0, 100),
        make_point(100, 150),
        make_point(100, 200),
    ]

    with pytest.raises(ValueError, match="Duplicate distance_m"):
        TelemetryResampler().resample(samples, step_m=50)
