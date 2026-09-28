from pathlib import Path

from analytics.analysis.pace_analysis import PaceAnalyzer
from analytics.loaders.csv_loader import CSVLoader


class PaceAnalysisService:
    """Coordinates lap loading and pace analysis."""

    def analyze(self, csv_path: str | Path) -> dict:
        """Load laps from csv_path and return JSON-ready pace results."""

        laps = CSVLoader().load(csv_path)
        result = PaceAnalyzer().analyze(laps)

        return {
            "fastest_lap_seconds": result["fastest_lap"].lap_time_seconds,
            "average_lap_seconds": result["average_lap_time_seconds"],
            "laps_analyzed": result["laps_analyzed"],
        }