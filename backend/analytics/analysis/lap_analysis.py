from app.models.lap import Lap
from analytics.analysis.base_analyzer import BaseAnalyzer


class LapAnalyzer(BaseAnalyzer):
    """Analyzes lap-by-lap progression within a set of laps."""

    def analyze(self, laps: list[Lap]) -> dict:
        if not laps:
            return {
                "laps_analyzed": 0,
                "lap_times_seconds": [],
                "lap_time_deltas_seconds": [],
            }

        ordered_laps = sorted(laps, key=lambda lap: lap.lap_number)
        lap_times = [lap.lap_time_seconds for lap in ordered_laps]

        lap_time_deltas = [
            round(lap_times[i] - lap_times[i - 1], 3)
            for i in range(1, len(lap_times))
        ]

        return {
            "laps_analyzed": len(ordered_laps),
            "lap_times_seconds": lap_times,
            "lap_time_deltas_seconds": lap_time_deltas,
        }