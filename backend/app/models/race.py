from app.models.track import Track
class Race:
    """Represents a single race weekend (one round of a season) held at a Track."""

    def __init__(self, race_id: int, name: str, season: int, round_number: int, track: Track, race_date: date):
        if not isinstance(track, Track):
            raise TypeError(f"track must be a Track, got {type(track).__name__}")

        self.race_id = race_id
        self.name = name
        self.season = season
        self.round_number = round_number
        self.track = track
        self.race_date = race_date

    def __repr__(self) -> str:
        return f"Race({self.name}, {self.season} Round {self.round_number}, {self.track.name})"

    @property
    def season(self) -> int:
        return self._season

    @season.setter
    def season(self, value: int) -> None:
        if value < 1950:
            raise ValueError(f"season must be 1950 or later, got {value}")
        self._season = value

    @property
    def round_number(self) -> int:
        return self._round_number

    @round_number.setter
    def round_number(self, value: int) -> None:
        if value < 1:
            raise ValueError(f"round_number must be at least 1, got {value}")
        self._round_number = value