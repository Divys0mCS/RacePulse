import numpy as np
import pytest

from analytics.prediction.expected_speed import (
    ExpectedSpeedPredictor,
    LapTelemetry,
)


def make_laps(count=8):
    """Create synthetic telemetry for testing."""
    laps = []

    for index in range(count):
        distance = np.linspace(0, 100, 21)
        speed = 120 + 80 * np.sin(np.pi * distance / 100) + index

        laps.append(
            LapTelemetry(
                lap_id=f"lap-{index}",
                distance_pct=distance,
                speed_kph=speed,
            )
        )

    return laps


def test_evaluate_returns_metrics_for_all_models():
    result = ExpectedSpeedPredictor().evaluate(make_laps())

    assert set(result["metrics"]) == {
        "baseline",
        "linear_regression",
        "random_forest",
    }

    for metrics in result["metrics"].values():
        assert set(metrics) == {"mae_kph", "rmse_kph", "r2"}
        assert metrics["mae_kph"] >= 0
        assert metrics["rmse_kph"] >= 0


def test_train_and_test_laps_are_disjoint():
    result = ExpectedSpeedPredictor().evaluate(make_laps())

    assert set(result["train_laps"]).isdisjoint(
        result["test_laps"]
    )


def test_predict_requires_evaluation_first():
    predictor = ExpectedSpeedPredictor()

    with pytest.raises(RuntimeError, match="evaluate"):
        predictor.predict(
            np.array([0.0, 50.0]),
            "linear_regression",
        )


def test_predict_returns_expected_number_of_values():
    predictor = ExpectedSpeedPredictor()
    predictor.evaluate(make_laps())

    predicted = predictor.predict(
        np.array([0.0, 25.0, 50.0, 75.0, 100.0]),
        "random_forest",
    )

    assert predicted.shape == (5,)
    assert np.isfinite(predicted).all()


def test_evaluate_rejects_too_few_laps():
    with pytest.raises(ValueError, match="At least 3 laps"):
        ExpectedSpeedPredictor().evaluate(make_laps(count=2))


def test_evaluate_rejects_non_finite_telemetry():
    laps = make_laps()
    laps[0].speed_kph[3] = np.nan

    with pytest.raises(ValueError, match="finite"):
        ExpectedSpeedPredictor().evaluate(laps)