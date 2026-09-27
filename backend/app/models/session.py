from enum import Enum
from app.models.race import Race

class SessionType(Enum):
    FP1 = "Practice 1"
    FP2 = "Practice 2"
    FP3 = "Practice 3"
    SPRINT_QUALIFYING = "Sprint Qualifying"
    SPRINT = "Sprint"
    QUALIFYING = "Qualifying"
    RACE = "Race"


class Session:
    """Represents a single session (e.g. Qualifying, Race) within a race weekend."""

    def __init__(self, session_id: int, race: Race, session_type: SessionType):
        if not isinstance(race, Race):
            raise TypeError(f"race must be a Race, got {type(race).__name__}")
        if not isinstance(session_type, SessionType):
            raise TypeError(f"session_type must be a SessionType, got {type(session_type).__name__}")

        self.session_id = session_id
        self.race = race
        self.session_type = session_type
        self.laps: list = []

    def __repr__(self) -> str:
        return f"Session({self.session_type.value}, {self.race.name})"

    def add_lap(self, lap) -> None:
        """Add a lap to this session, avoiding duplicate entries."""
        if lap not in self.laps:
            self.laps.append(lap)