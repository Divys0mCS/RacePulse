import statistics
from app.models.lap import Lap
from analytics.analysis.base_analyzer import BaseAnalyzer


class ConsistencyAnalyzer(BaseAnalyzer):
    """Measures how repeatable a driver's lap times are (lower stdev = more consistent)."""

    def analyze(self, laps: list[Lap]) -> dict:
        if not laps:
            return {"consistency_stdev_seconds": None, "laps_analyzed": 0}

        if len(laps) == 1:
            # stdev is undefined for a single sample - not an error, just nothing to measure yet
            return {"consistency_stdev_seconds": None, "laps_analyzed": 1}

        times = [lap.lap_time_seconds for lap in laps]
        return {
            "consistency_stdev_seconds": statistics.stdev(times),  # sample stdev
            "laps_analyzed": len(laps),
        }