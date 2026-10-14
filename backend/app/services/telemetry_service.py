"""Services for loading and summarizing historical telemetry data."""

from pathlib import Path

from analytics.loaders.csv_loader import CSVLoader
from analytics.loaders.telemetry_loader import TelemetryLoader


class TelemetryService:
    """Coordinates lap loading, telemetry loading, and summary generation."""

    def analyze(
        self,
        laps_csv_path: str | Path,
        telemetry_csv_path: str | Path,
    ) -> dict:
        """Load historical data and return telemetry summaries per lap."""

        # Step 1: Load lap records.
        laps = CSVLoader().load(laps_csv_path)

        if not laps:
            return {
                "laps_analyzed": 0,
                "telemetry_laps_analyzed": 0,
                "telemetry_summaries": [],
            }

        # Step 2: Attach telemetry samples to their matching laps.
        telemetry_records = TelemetryLoader(laps).load(
            telemetry_csv_path
        )

        # Step 3: Calculate a summary for each lap with telemetry.
        summaries = []

        for telemetry in telemetry_records:
            samples = telemetry.samples

            if not samples:
                continue

            lap = telemetry.lap

            average_speed = sum(
                sample.speed_kph for sample in samples
            ) / len(samples)

            average_throttle = sum(
                sample.throttle_pct for sample in samples
            ) / len(samples)

            average_brake = sum(
                sample.brake_pct for sample in samples
            ) / len(samples)

            summaries.append(
                {
                    "driver_name": lap.driver.name,
                    "driver_number": lap.driver.number,
                    "lap_number": lap.lap_number,
                    "lap_time_seconds": lap.lap_time_seconds,
                    "sample_count": len(samples),
                    "maximum_speed_kph": telemetry.max_speed_kph(),
                    "average_speed_kph": average_speed,
                    "average_throttle_pct": average_throttle,
                    "average_brake_pct": average_brake,
                }
            )

        # Step 4: Return JSON-ready results.
        return {
            "laps_analyzed": len(laps),
            "telemetry_laps_analyzed": len(summaries),
            "telemetry_summaries": summaries,
        }