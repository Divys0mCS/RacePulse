from pydantic import BaseModel, ConfigDict, Field


class LapCreate(BaseModel):
    session_id: int = Field(gt=0)
    driver_id: int = Field(gt=0)
    team_id: int = Field(gt=0)
    lap_number: int = Field(ge=1)
    lap_time_seconds: float = Field(gt=0)
    sector_1_time_seconds: float = Field(gt=0)
    sector_2_time_seconds: float = Field(gt=0)
    sector_3_time_seconds: float = Field(gt=0)


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