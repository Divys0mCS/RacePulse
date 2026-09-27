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
        """Add a driver to this team's roster, moving them off any previous team first."""
        if driver.team is self:
            return  # already here — nothing to do

        if driver.team is not None:
            driver.team.remove_driver(driver)

        self.drivers.append(driver)
        driver.team = self

    def remove_driver(self, driver: Driver) -> None:
        """Remove a driver from this team's roster and clear their team link."""
        if driver in self.drivers:
            self.drivers.remove(driver)
        if driver.team is self:
            driver.team = None