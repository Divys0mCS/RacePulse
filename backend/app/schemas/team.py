from pydantic import BaseModel, ConfigDict, Field, field_validator


class TeamCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    base_country: str = Field(min_length=1, max_length=100)

    @field_validator("name", "base_country")
    @classmethod
    def reject_blank_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value must not be blank")
        return value


class TeamResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    team_id: int
    name: str
    base_country: str