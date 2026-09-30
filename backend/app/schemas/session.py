from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


SessionType = Literal[
    "FP1",
    "FP2",
    "FP3",
    "SPRINT_QUALIFYING",
    "SPRINT",
    "QUALIFYING",
    "RACE",
]


class SessionCreate(BaseModel):
    race_id: int = Field(gt=0)
    session_type: SessionType


class SessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    session_id: int
    race_id: int
    session_type: SessionType