from app.models.lap import Lap
from analytics.analysis.base_analyzer import BaseAnalyzer


class PaceAnalyzer(BaseAnalyzer):
    """Computes fastest lap and average pace over a set of Laps."""

    def analyze(self, laps: list[Lap]) -> dict:
        if not laps:
            return {"fastest_lap": None, "average_lap_time_seconds": None, "laps_analyzed": 0}

        return {
            "fastest_lap": min(laps),  # uses the __lt__ you already wrote on Lap
            "average_lap_time_seconds": sum(lap.lap_time_seconds for lap in laps) / len(laps),
            "laps_analyzed": len(laps),
        }