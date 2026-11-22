import math
from pydantic import BaseModel, ConfigDict, Field, field_validator


class LapCreate(BaseModel):
    session_id: int = Field(gt=0)
    driver_id: int = Field(gt=0)
    team_id: int = Field(gt=0)
    lap_number: int = Field(ge=1)
    lap_time_seconds: float = Field(gt=0)
    sector_1_time_seconds: float = Field(gt=0)
    sector_2_time_seconds: float = Field(gt=0)
    sector_3_time_seconds: float = Field(gt=0)

    @field_validator(
        "lap_time_seconds",
        "sector_1_time_seconds",
        "sector_2_time_seconds",
        "sector_3_time_seconds",
    )
    @classmethod
    def reject_non_finite_values(cls, value: float) -> float:
        if not math.isfinite(value):
            raise ValueError("value must be finite")
        return value


class LapUpdate(BaseModel):
    lap_time_seconds: float | None = Field(default=None, gt=0)
    sector_1_time_seconds: float | None = Field(default=None, gt=0)
    sector_2_time_seconds: float | None = Field(default=None, gt=0)
    sector_3_time_seconds: float | None = Field(default=None, gt=0)

    @field_validator(
        "lap_time_seconds",
        "sector_1_time_seconds",
        "sector_2_time_seconds",
        "sector_3_time_seconds",
        mode="after",
    )
    @classmethod
    def reject_non_finite_values(cls, value: float | None) -> float | None:
        if value is not None and not math.isfinite(value):
            raise ValueError("value must be finite")
        return value


class LapResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    lap_id: int
    session_id: int
    driver_id: int
    team_id: int
    lap_number: int
    lap_time_seconds: float
    sector_1_time_seconds: float
    sector_2_time_seconds: float
    sector_3_time_seconds: float
