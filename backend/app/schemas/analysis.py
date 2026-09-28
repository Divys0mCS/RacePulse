from pydantic import BaseModel


class PaceAnalysisResponse(BaseModel):
    fastest_lap_seconds: float
    average_lap_seconds: float
    laps_analyzed: int


class SectorAnalysisResponse(BaseModel):
    fastest_sector_1_seconds: float
    fastest_sector_2_seconds: float
    fastest_sector_3_seconds: float
    laps_analyzed: int


class ConsistencyAnalysisResponse(BaseModel):
    consistency_stdev_seconds: float | None
    laps_analyzed: int


class LapAnalysisResponse(BaseModel):
    laps_analyzed: int
    lap_times_seconds: list[float]
    lap_time_deltas_seconds: list[float]