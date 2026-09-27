class Driver:
    """Represents a single motorsport driver."""

    def __init__(self, driver_id: int, name: str, number: int, nationality: str, team: "Team | None" = None):
        self.driver_id = driver_id
        self.name = name
        self.number = number
        self.nationality = nationality
        self.team = team

    def __repr__(self) -> str:
        team_name = self.team.name if self.team else "No Team"
        return f"Driver(#{self.number} {self.name}, {team_name})"

    def summary(self) -> str:
        team_name = self.team.name if self.team else "No Team"
        return f"{self.name} (#{self.number}) — {team_name}, {self.nationality}"

    def is_teammate_of(self, other: "Driver") -> bool:
        """True if `other` is on the same Team object and isn't this same driver."""
        if not isinstance(other, Driver):
            return False
        if self.team is None or other.team is None:
            return False
        return self.driver_id != other.driver_id and self.team is other.team