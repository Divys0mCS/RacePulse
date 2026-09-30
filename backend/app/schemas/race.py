from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class RaceCreate(BaseModel):
    name: str
    season: int = Field(ge=1950)
    round_number: int = Field(ge=1)
    track_id: int = Field(gt=0)
    race_date: date


class RaceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    race_id: int
    name: str
    season: int
    round_number: int
    track_id: int
    race_date: date