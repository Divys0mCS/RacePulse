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

def test_add_driver_moves_from_previous_team():
    team_a = Team(team_id=1, name="Red Bull Racing", base_country="Austria")
    team_b = Team(team_id=2, name="Ferrari", base_country="Italy")
    driver = Driver(driver_id=1, name="Max Verstappen", number=1, nationality="Dutch")

    team_a.add_driver(driver)
    team_b.add_driver(driver)

    assert driver not in team_a.drivers
    assert driver in team_b.drivers
    assert driver.team is team_b


def test_driver_constructor_registers_with_team():
    team = Team(team_id=1, name="Red Bull Racing", base_country="Austria")
    driver = Driver(driver_id=1, name="Max Verstappen", number=1, nationality="Dutch", team=team)

    assert driver in team.drivers
    assert driver.team is team


def test_remove_driver_clears_team_link():
    team = Team(team_id=1, name="Red Bull Racing", base_country="Austria")
    driver = Driver(driver_id=1, name="Max Verstappen", number=1, nationality="Dutch", team=team)

    team.remove_driver(driver)

    assert driver not in team.drivers
    assert driver.team is None