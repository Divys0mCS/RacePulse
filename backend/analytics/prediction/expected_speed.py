"""Expected-speed prediction using historical lap telemetry."""

from dataclasses import dataclass

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GroupShuffleSplit


@dataclass
class LapTelemetry:
    """Telemetry samples collected from a single lap."""

    lap_id: str
    distance_pct: np.ndarray
    speed_kph: np.ndarray


class ExpectedSpeedPredictor:
    """Compare baseline, linear regression, and random forest predictions."""

    def __init__(self, test_size: float = 0.25, random_state: int = 42):
        if not 0 < test_size < 1:
            raise ValueError("test_size must be between 0 and 1.")

        self.test_size = test_size
        self.random_state = random_state
        self.models = {}
        self.is_evaluated = False

    @staticmethod
    def _validate_laps(laps: list[LapTelemetry]) -> None:
        if len(laps) < 3:
            raise ValueError("At least 3 laps are required.")

        for lap in laps:
            distance = np.asarray(lap.distance_pct, dtype=float)
            speed = np.asarray(lap.speed_kph, dtype=float)

            if distance.ndim != 1 or speed.ndim != 1:
                raise ValueError("Telemetry arrays must be one-dimensional.")

            if len(distance) == 0 or len(distance) != len(speed):
                raise ValueError(
                    "Distance and speed arrays must be non-empty "
                    "and have equal lengths."
                )

            if not np.isfinite(distance).all() or not np.isfinite(speed).all():
                raise ValueError("Telemetry values must be finite.")

            if not lap.lap_id:
                raise ValueError("Each lap must have a lap_id.")

        if len({lap.lap_id for lap in laps}) < 3:
            raise ValueError("At least 3 unique laps are required.")

    def evaluate(self, laps: list[LapTelemetry]) -> dict:
        """Train and compare models while holding out complete laps."""
        self._validate_laps(laps)

        distances = np.concatenate(
            [np.asarray(lap.distance_pct, dtype=float) for lap in laps]
        )
        speeds = np.concatenate(
            [np.asarray(lap.speed_kph, dtype=float) for lap in laps]
        )
        sample_groups = np.concatenate(
            [
                np.full(len(lap.speed_kph), lap.lap_id)
                for lap in laps
            ]
        )

        X = distances.reshape(-1, 1)
        y = speeds

        splitter = GroupShuffleSplit(
            n_splits=1,
            test_size=self.test_size,
            random_state=self.random_state,
        )
        train_idx, test_idx = next(
            splitter.split(X, y, groups=sample_groups)
        )

        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]

        train_laps = sorted(set(sample_groups[train_idx]))
        test_laps = sorted(set(sample_groups[test_idx]))

        baseline_prediction = np.full(
            len(y_test), float(np.mean(y_train))
        )

        linear_model = LinearRegression()
        linear_model.fit(X_train, y_train)
        linear_prediction = linear_model.predict(X_test)

        forest_model = RandomForestRegressor(
            n_estimators=100,
            random_state=self.random_state,
            n_jobs=-1,
        )
        forest_model.fit(X_train, y_train)
        forest_prediction = forest_model.predict(X_test)

        predictions = {
            "baseline": baseline_prediction,
            "linear_regression": linear_prediction,
            "random_forest": forest_prediction,
        }

        metrics = {}
        for name, prediction in predictions.items():
            mse = mean_squared_error(y_test, prediction)
            metrics[name] = {
                "mae_kph": float(mean_absolute_error(y_test, prediction)),
                "rmse_kph": float(np.sqrt(mse)),
                "r2": float(r2_score(y_test, prediction)),
            }

        self.models = {
            "linear_regression": linear_model,
            "random_forest": forest_model,
        }
        self.is_evaluated = True

        return {
            "metrics": metrics,
            "train_laps": train_laps,
            "test_laps": test_laps,
            "y_true": y_test.copy(),
            "predictions": {
                name: prediction.copy()
                for name, prediction in predictions.items()
            },
        }

    def predict(
        self,
        distance_pct: np.ndarray,
        model_name: str = "random_forest",
    ) -> np.ndarray:
        """Predict speed at supplied track-distance percentages."""
        if not self.is_evaluated:
            raise RuntimeError(
                "Call evaluate() before predict() to train the models."
            )

        if model_name not in self.models:
            raise ValueError(
                "model_name must be 'linear_regression' or 'random_forest'."
            )

        distance = np.asarray(distance_pct, dtype=float)

        if distance.ndim != 1:
            raise ValueError("distance_pct must be a one-dimensional array.")

        if not np.isfinite(distance).all():
            raise ValueError("distance_pct values must be finite.")

        return self.models[model_name].predict(distance.reshape(-1, 1))