from app.models.telemetry import TelemetrySample
from analytics.processing.cleaner import TelemetryCleaner


def test_cleaner_sorts_samples_by_distance():
    samples = [
        TelemetrySample(
            distance_m=500,
            speed_kph=250,
            throttle_pct=100,
            brake_pct=0,
            gear=7,
            rpm=11000,
        ),
        TelemetrySample(
            distance_m=0,
            speed_kph=120,
            throttle_pct=80,
            brake_pct=0,
            gear=4,
            rpm=9000,
        ),
        TelemetrySample(
            distance_m=1000,
            speed_kph=280,
            throttle_pct=100,
            brake_pct=0,
            gear=8,
            rpm=12000,
        ),
    ]

    cleaned = TelemetryCleaner().clean(samples)

    assert [sample.distance_m for sample in cleaned] == [
        0,
        500,
        1000,
    ]


def test_cleaner_does_not_modify_original_list():
    samples = [
        TelemetrySample(
            distance_m=500,
            speed_kph=250,
            throttle_pct=100,
            brake_pct=0,
            gear=7,
            rpm=11000,
        ),
        TelemetrySample(
            distance_m=0,
            speed_kph=120,
            throttle_pct=80,
            brake_pct=0,
            gear=4,
            rpm=9000,
        ),
    ]

    original = list(samples)

    TelemetryCleaner().clean(samples)

    assert samples == original


def test_cleaner_handles_empty_samples():
    assert TelemetryCleaner().clean([]) == []

def test_cleaner_removes_exact_duplicate_samples():
    sample = TelemetrySample(
        distance_m=500,
        speed_kph=250,
        throttle_pct=100,
        brake_pct=0,
        gear=7,
        rpm=11000,
    )

    samples = [
        sample,
        sample,
        TelemetrySample(
            distance_m=1000,
            speed_kph=280,
            throttle_pct=100,
            brake_pct=0,
            gear=8,
            rpm=12000,
        ),
    ]

    cleaned = TelemetryCleaner().clean(samples)

    assert cleaned == [sample, samples[2]]

def test_cleaner_keeps_different_samples_at_same_distance():
    samples = [
        TelemetrySample(
            distance_m=500,
            speed_kph=250,
            throttle_pct=100,
            brake_pct=0,
            gear=7,
            rpm=11000,
        ),
        TelemetrySample(
            distance_m=500,
            speed_kph=251,
            throttle_pct=100,
            brake_pct=0,
            gear=7,
            rpm=11050,
        ),
    ]

    cleaned = TelemetryCleaner().clean(samples)

    assert cleaned == samples