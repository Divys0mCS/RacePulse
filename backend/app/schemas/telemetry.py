"""Pydantic schemas for telemetry analysis responses."""

from pydantic import BaseModel, ConfigDict, Field


class TelemetrySummary(BaseModel):
    """Summary of telemetry measurements for a single lap."""

    model_config = ConfigDict(extra="forbid")

    driver_name: str
    driver_number: int = Field(gt=0)
    lap_number: int = Field(ge=1)
    lap_time_seconds: float = Field(gt=0)
    sample_count: int = Field(ge=1)

    maximum_speed_kph: float = Field(ge=0)
    average_speed_kph: float = Field(ge=0)
    average_throttle_pct: float = Field(ge=0, le=100)
    average_brake_pct: float = Field(ge=0, le=100)


class TelemetryAnalysisResponse(BaseModel):
    """Response returned by the telemetry analysis endpoint."""

    model_config = ConfigDict(extra="forbid")

    laps_analyzed: int = Field(ge=0)
    telemetry_laps_analyzed: int = Field(ge=0)
    telemetry_summaries: list[TelemetrySummary]