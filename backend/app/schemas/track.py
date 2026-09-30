from pydantic import BaseModel, ConfigDict, Field


class TrackCreate(BaseModel):
    name: str
    country: str
    length_km: float = Field(gt=0)
    number_of_corners: int = Field(ge=1)


class TrackResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    track_id: int
    name: str
    country: str
    length_km: float
    number_of_corners: int