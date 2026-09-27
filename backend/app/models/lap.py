from app.models.session import Session
from app.models.driver import Driver
class Lap:
    """Represents a single completed lap by a driver within a session."""

    def __init__(
        self,
        lap_id: int,
        session: Session,
        driver: Driver,
        lap_number: int,
        lap_time_seconds: float,
        sector_times: tuple[float, float, float] | None = None,
    ):
        if not isinstance(session, Session):
            raise TypeError(f"session must be a Session, got {type(session).__name__}")
        if not isinstance(driver, Driver):
            raise TypeError(f"driver must be a Driver, got {type(driver).__name__}")

        self.lap_id = lap_id
        self.session = session
        self.driver = driver
        self.lap_number = lap_number
        self.lap_time_seconds = lap_time_seconds
        self.sector_times = sector_times

    def __repr__(self) -> str:
        return f"Lap(#{self.lap_number} {self.driver.name} {self.lap_time_seconds:.3f}s)"

    @property
    def lap_number(self) -> int:
        return self._lap_number

    @lap_number.setter
    def lap_number(self, value: int) -> None:
        if value < 1:
            raise ValueError(f"lap_number must be at least 1, got {value}")
        self._lap_number = value

    @property
    def lap_time_seconds(self) -> float:
        return self._lap_time_seconds

    @lap_time_seconds.setter
    def lap_time_seconds(self, value: float) -> None:
        if value <= 0:
            raise ValueError(f"lap_time_seconds must be positive, got {value}")
        self._lap_time_seconds = value

    @property
    def sector_times(self):
        return self._sector_times

    @sector_times.setter
    def sector_times(self, value) -> None:
        if value is not None:
            if len(value) != 3 or any(t <= 0 for t in value):
                raise ValueError("sector_times must be a tuple of exactly 3 positive numbers, or None")
        self._sector_times = value

    def __eq__(self, other) -> bool:
        if not isinstance(other, Lap):
            return NotImplemented
        return self.lap_time_seconds == other.lap_time_seconds

    def __lt__(self, other) -> bool:
        if not isinstance(other, Lap):
            return NotImplemented
        return self.lap_time_seconds < other.lap_time_seconds