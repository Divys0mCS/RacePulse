from pydantic import BaseModel, ConfigDict, Field, field_validator


class TrackCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    country: str = Field(min_length=1, max_length=100)
    length_km: float = Field(gt=0)
    number_of_corners: int = Field(ge=1)

    @field_validator("name", "country")
    @classmethod
    def reject_blank_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("must not be blank")

        return value


class TrackResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    track_id: int
    name: str
    country: str
    length_km: float
    number_of_corners: int