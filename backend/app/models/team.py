from app.models.driver import Driver


class Team:
    """Represents a motorsport team and the drivers who race for it."""

    def __init__(self, team_id: int, name: str, base_country: str):
        self.team_id = team_id
        self.name = name
        self.base_country = base_country
        self.drivers: list[Driver] = []

    def __repr__(self) -> str:
        return f"Team({self.name}, {len(self.drivers)} driver(s))"

    def add_driver(self, driver: Driver) -> None:
        """Add a driver to this team's roster and link them back to this team."""
        if driver not in self.drivers:
            self.drivers.append(driver)
        driver.team = self