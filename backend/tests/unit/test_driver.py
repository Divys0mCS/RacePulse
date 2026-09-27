from app.models.driver import Driver
from app.models.team import Team


def make_team(team_id=1, name="Red Bull Racing", base_country="Austria"):
    return Team(team_id=team_id, name=name, base_country=base_country)


def make_driver(driver_id, name, number, nationality="Dutch", team=None):
    return Driver(driver_id=driver_id, name=name, number=number, nationality=nationality, team=team)


def test_driver_creation():
    d = make_driver(1, "Max Verstappen", 1)
    assert d.name == "Max Verstappen"
    assert d.number == 1


def test_driver_summary_without_team():
    d = make_driver(1, "Max Verstappen", 1)
    assert "No Team" in d.summary()


def test_driver_summary_with_team():
    team = make_team()
    d = make_driver(1, "Max Verstappen", 1, team=team)
    assert "Red Bull Racing" in d.summary()


def test_driver_repr():
    team = make_team()
    d = make_driver(1, "Max Verstappen", 1, team=team)
    assert repr(d) == "Driver(#1 Max Verstappen, Red Bull Racing)"


def test_is_teammate_of_same_team():
    team = make_team()
    verstappen = make_driver(1, "Max Verstappen", 1, team=team)
    perez = make_driver(2, "Sergio Perez", 11, team=team)
    assert verstappen.is_teammate_of(perez) is True


def test_is_teammate_of_different_team():
    team_a = make_team(1, "Red Bull Racing", "Austria")
    team_b = make_team(2, "Ferrari", "Italy")
    verstappen = make_driver(1, "Max Verstappen", 1, team=team_a)
    hamilton = make_driver(44, "Lewis Hamilton", 44, nationality="British", team=team_b)
    assert verstappen.is_teammate_of(hamilton) is False


def test_is_teammate_of_self_is_false():
    team = make_team()
    verstappen = make_driver(1, "Max Verstappen", 1, team=team)
    assert verstappen.is_teammate_of(verstappen) is False


def test_is_teammate_of_no_team_is_false():
    d1 = make_driver(1, "Max Verstappen", 1)
    d2 = make_driver(2, "Sergio Perez", 11)
    assert d1.is_teammate_of(d2) is False