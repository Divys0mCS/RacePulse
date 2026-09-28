from pathlib import Path

from analytics.analysis.pace_analysis import PaceAnalyzer
from analytics.loaders.csv_loader import CSVLoader
from analytics.analysis.sector_analysis import SectorAnalyzer
from analytics.analysis.consistency_analysis import ConsistencyAnalyzer
from analytics.analysis.lap_analysis import LapAnalyzer


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

class SectorAnalysisService:
    """Coordinates lap loading and sector analysis."""

    def analyze(self, csv_path: str | Path) -> dict:
        """Load laps from csv_path and return sector analysis results."""

        laps = CSVLoader().load(csv_path)
        return SectorAnalyzer().analyze(laps)

class ConsistencyAnalysisService:
    """Coordinates lap loading and consistency analysis."""

    def analyze(self, csv_path: str | Path) -> dict:
        """Load laps from csv_path and return consistency analysis results."""

        laps = CSVLoader().load(csv_path)
        return ConsistencyAnalyzer().analyze(laps)
class LapAnalysisService:
    """Coordinates lap loading and lap-by-lap analysis."""

    def analyze(self, csv_path: str | Path) -> dict:
        """Load laps from csv_path and return lap analysis results."""

        laps = CSVLoader().load(csv_path)
        return LapAnalyzer().analyze(laps)