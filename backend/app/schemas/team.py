from pydantic import BaseModel, ConfigDict


class TeamCreate(BaseModel):
    name: str
    base_country: str


class TeamResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    team_id: int
    name: str
    base_country: str