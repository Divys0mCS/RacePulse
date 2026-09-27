from app.models.lap import Lap
from analytics.analysis.base_analyzer import BaseAnalyzer


class SectorAnalyzer(BaseAnalyzer):
    """Computes the fastest time for each sector over a set of Laps."""

    def analyze(self, laps: list[Lap]) -> dict:
        if not laps:
            return {
                "fastest_sector_1_seconds": None,
                "fastest_sector_2_seconds": None,
                "fastest_sector_3_seconds": None,
                "laps_analyzed": 0,
            }

        sector_1_times = [lap.sector_times[0] for lap in laps]
        sector_2_times = [lap.sector_times[1] for lap in laps]
        sector_3_times = [lap.sector_times[2] for lap in laps]

        return {
            "fastest_sector_1_seconds": min(sector_1_times),
            "fastest_sector_2_seconds": min(sector_2_times),
            "fastest_sector_3_seconds": min(sector_3_times),
            "laps_analyzed": len(laps),
        }