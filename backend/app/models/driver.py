class Driver:
    
    """Represents a single motorsport driver."""

    def __init__(self, driver_id: int, name: str, number: int, team: str, nationality: str):
        self.driver_id = driver_id
        self.name = name
        self.number = number
        self.team = team
        self.nationality = nationality

    def __repr__(self) -> str:
        return f"Driver(#{self.number} {self.name}, {self.team})"

    def summary(self) -> str:
        return f"{self.name} (#{self.number}) — {self.team}, {self.nationality}"
    
    def is_teammate_of(self, other: "Driver") -> bool:
        
        """True if `other` races for the same team and isn't this same driver."""
        
        if not isinstance(other, Driver):
            return False
        return self.driver_id != other.driver_id and self.team == other.team