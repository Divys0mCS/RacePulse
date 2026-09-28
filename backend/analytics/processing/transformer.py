from app.models.telemetry import TelemetrySample


class TelemetryTransformer:
    """Transforms telemetry samples into an analytical representation."""

    def transform(
        self,
        samples: list[TelemetrySample],
        track_length_km: float,
    ) -> list[dict]:
        """Add normalized distance percentage while preserving telemetry values."""

        if track_length_km <= 0:
            raise ValueError("track_length_km must be greater than zero")

        track_length_m = track_length_km * 1000

        transformed = []

        for sample in samples:
            transformed.append(
                {
                    "distance_m": sample.distance_m,
                    "distance_pct": round(
                        (sample.distance_m / track_length_m) * 100,
                        3,
                    ),
                    "speed_kph": sample.speed_kph,
                    "throttle_pct": sample.throttle_pct,
                    "brake_pct": sample.brake_pct,
                    "gear": sample.gear,
                    "rpm": sample.rpm,
                }
            )

        return transformed