from pydantic import BaseModel, ConfigDict, Field, field_validator


class DriverCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    nationality: str = Field(min_length=1, max_length=100)

    @field_validator("name", "nationality")
    @classmethod
    def reject_blank_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value must not be blank")
        return value


class DriverUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    nationality: str | None = Field(default=None, min_length=1, max_length=100)

    @field_validator("name", "nationality", mode="after")
    @classmethod
    def reject_blank_text(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("value must not be blank")
        return value


class DriverResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    driver_id: int
    name: str
    nationality: str
