from datetime import date

from pydantic import BaseModel, ConfigDict, Field, field_validator


class RaceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    season: int = Field(ge=1950)
    round_number: int = Field(ge=1)
    track_id: int = Field(gt=0)
    race_date: date

    @field_validator("name")
    @classmethod
    def reject_blank_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("name must not be blank")
        return value


class RaceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    race_id: int
    name: str
    season: int
    round_number: int
    track_id: int
    race_date: date