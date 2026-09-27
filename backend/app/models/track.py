class Track:
    """Represents a race track/circuit."""

    def __init__(self, track_id: int, name: str, country: str, length_km: float, number_of_corners: int):
        self.track_id = track_id
        self.name = name
        self.country = country
        self.length_km = length_km            # routed through the setter below
        self.number_of_corners = number_of_corners  # routed through the setter below

    def __repr__(self) -> str:
        return f"Track({self.name}, {self.country}, {self.length_km}km)"

    @property
    def length_km(self) -> float:
        return self._length_km

    @length_km.setter
    def length_km(self, value: float) -> None:
        if value <= 0:
            raise ValueError(f"length_km must be positive, got {value}")
        self._length_km = value

    @property
    def number_of_corners(self) -> int:
        return self._number_of_corners

    @number_of_corners.setter
    def number_of_corners(self, value: int) -> None:
        if value < 1:
            raise ValueError(f"number_of_corners must be at least 1, got {value}")
        self._number_of_corners = value