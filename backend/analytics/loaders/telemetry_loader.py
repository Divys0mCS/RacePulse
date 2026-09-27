"""Loads per-sample telemetry data and attaches it to Laps already loaded
(e.g. via CSVLoader).

Expected CSV schema (one row per telemetry sample):

    driver_number, lap_number, distance_m, speed_kph,
    throttle_pct, brake_pct, gear, rpm

Construct one TelemetryLoader per session, passing the list[Lap] already
loaded for that session - (driver_number, lap_number) is only guaranteed
unique within a single session, so mixing laps from multiple sessions here
would risk samples attaching to the wrong lap.
"""

import csv
from pathlib import Path

from app.models.lap import Lap
from app.models.telemetry import Telemetry, TelemetrySample

REQUIRED_COLUMNS = {
    "driver_number", "lap_number", "distance_m", "speed_kph",
    "throttle_pct", "brake_pct", "gear", "rpm",
}


class TelemetryLoader:
    """Loads a flat telemetry-samples CSV, attaching samples to already-loaded Laps."""

    def __init__(self, laps: list[Lap]) -> None:
        self._lap_by_key: dict[tuple[int, int], Lap] = {
            (lap.driver.number, lap.lap_number): lap for lap in laps
        }
        self._telemetry_by_lap_id: dict[int, Telemetry] = {}
        self._next_telemetry_id = 1

    def load(self, csv_path: str | Path) -> list[Telemetry]:
        """Read the CSV at csv_path and return one Telemetry per Lap that had samples."""
        csv_path = Path(csv_path)
        if not csv_path.exists():
            raise FileNotFoundError(f"CSV file not found: {csv_path}")

        with csv_path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            self._validate_header(reader.fieldnames, csv_path)
            for row_number, row in enumerate(reader, start=2):  # row 1 is the header
                try:
                    self._row_to_sample(row)
                except (KeyError, ValueError) as e:
                    raise ValueError(
                        f"Row {row_number} in {csv_path.name} is malformed: {e}"
                    ) from e

        return list(self._telemetry_by_lap_id.values())

    def _validate_header(self, fieldnames, csv_path: Path) -> None:
        missing = REQUIRED_COLUMNS - set(fieldnames or [])
        if missing:
            raise ValueError(
                f"{csv_path.name} is missing required column(s): {sorted(missing)}"
            )

    def _row_to_sample(self, row: dict) -> None:
        key = (int(row["driver_number"]), int(row["lap_number"]))
        lap = self._lap_by_key.get(key)
        if lap is None:
            raise ValueError(
                f"No matching lap for driver_number={key[0]}, lap_number={key[1]} "
                f"- load laps for this session before loading telemetry"
            )

        telemetry = self._get_or_create_telemetry(lap)
        sample = TelemetrySample(
            distance_m=float(row["distance_m"]),
            speed_kph=float(row["speed_kph"]),
            throttle_pct=float(row["throttle_pct"]),
            brake_pct=float(row["brake_pct"]),
            gear=int(row["gear"]),
            rpm=int(row["rpm"]),
        )
        telemetry.add_sample(sample)

    def _get_or_create_telemetry(self, lap: Lap) -> Telemetry:
        if lap.lap_id not in self._telemetry_by_lap_id:
            self._telemetry_by_lap_id[lap.lap_id] = Telemetry(
                telemetry_id=self._next_telemetry_id, lap=lap
            )
            self._next_telemetry_id += 1
        return self._telemetry_by_lap_id[lap.lap_id]