from dataclasses import dataclass
from app.models.lap import Lap


@dataclass(frozen=True)
class TelemetrySample:
    """A single telemetry reading at one point along a lap. Immutable once recorded."""
    distance_m: float
    speed_kph: float
    throttle_pct: float   # 0-100
    brake_pct: float       # 0-100
    gear: int
    rpm: int

    def __post_init__(self):
        if self.distance_m < 0:
            raise ValueError(f"distance_m must be non-negative, got {self.distance_m}")
        if self.speed_kph < 0:
            raise ValueError(f"speed_kph must be non-negative, got {self.speed_kph}")
        if not (0 <= self.throttle_pct <= 100):
            raise ValueError(f"throttle_pct must be 0-100, got {self.throttle_pct}")
        if not (0 <= self.brake_pct <= 100):
            raise ValueError(f"brake_pct must be 0-100, got {self.brake_pct}")
        if self.gear < 0:
            raise ValueError(f"gear must be non-negative, got {self.gear}")
        if self.rpm < 0:
            raise ValueError(f"rpm must be non-negative, got {self.rpm}")


class Telemetry:
    """Holds the full sequence of telemetry samples recorded for a single Lap."""

    def __init__(self, telemetry_id: int, lap: Lap):
        if not isinstance(lap, Lap):
            raise TypeError(f"lap must be a Lap, got {type(lap).__name__}")

        self.telemetry_id = telemetry_id
        self.lap = lap
        self.samples: list[TelemetrySample] = []

    def __repr__(self) -> str:
        return f"Telemetry(lap=#{self.lap.lap_number}, {len(self.samples)} sample(s))"

    def add_sample(self, sample: TelemetrySample) -> None:
        if not isinstance(sample, TelemetrySample):
            raise TypeError(f"sample must be a TelemetrySample, got {type(sample).__name__}")
        self.samples.append(sample)

    def max_speed_kph(self) -> float | None:
        """Highest recorded speed, or None if there are no samples yet."""
        if not self.samples:
            return None
        return max(sample.speed_kph for sample in self.samples)

    def average_throttle_pct(self) -> float | None:
        """Mean throttle application across all samples, or None if there are no samples yet."""
        if not self.samples:
            return None
        return sum(sample.throttle_pct for sample in self.samples) / len(self.samples)