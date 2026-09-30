from pydantic import BaseModel, ConfigDict


class DriverCreate(BaseModel):
    name: str
    nationality: str


class DriverResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    driver_id: int
    name: str
    nationality: str