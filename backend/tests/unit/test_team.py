from app.models.team import Team
from app.models.driver import Driver


def test_team_creation():
    team = Team(team_id=1, name="Red Bull Racing", base_country="Austria")
    assert team.name == "Red Bull Racing"
    assert team.drivers == []


def test_add_driver_links_both_ways():
    team = Team(team_id=1, name="Red Bull Racing", base_country="Austria")
    driver = Driver(driver_id=1, name="Max Verstappen", number=1, nationality="Dutch")

    team.add_driver(driver)

    assert driver in team.drivers
    assert driver.team is team


def test_add_driver_does_not_duplicate():
    team = Team(team_id=1, name="Red Bull Racing", base_country="Austria")
    driver = Driver(driver_id=1, name="Max Verstappen", number=1, nationality="Dutch")

    team.add_driver(driver)
    team.add_driver(driver)

    assert team.drivers.count(driver) == 1


def test_team_repr():
    team = Team(team_id=1, name="Red Bull Racing", base_country="Austria")
    driver = Driver(driver_id=1, name="Max Verstappen", number=1, nationality="Dutch")
    team.add_driver(driver)

    assert repr(team) == "Team(Red Bull Racing, 1 driver(s))"