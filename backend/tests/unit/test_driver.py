from app.models.driver import Driver


def make_driver(driver_id, name, number, team="Red Bull Racing", nationality="Dutch"):
    return Driver(driver_id=driver_id, name=name, number=number, team=team, nationality=nationality)


def test_driver_creation():
    d = make_driver(1, "Max Verstappen", 1)
    assert d.name == "Max Verstappen"
    assert d.number == 1


def test_driver_summary():
    d = make_driver(1, "Max Verstappen", 1)
    assert "Max Verstappen" in d.summary()
    assert "#1" in d.summary()


def test_driver_repr():
    d = make_driver(1, "Max Verstappen", 1)
    assert repr(d) == "Driver(#1 Max Verstappen, Red Bull Racing)"


def test_is_teammate_of_same_team():
    verstappen = make_driver(1, "Max Verstappen", 1)
    perez = make_driver(2, "Sergio Perez", 11)  # same default team
    assert verstappen.is_teammate_of(perez) is True


def test_is_teammate_of_different_team():
    verstappen = make_driver(1, "Max Verstappen", 1)
    hamilton = make_driver(44, "Lewis Hamilton", 44, team="Ferrari", nationality="British")
    assert verstappen.is_teammate_of(hamilton) is False


def test_is_teammate_of_self_is_false():
    verstappen = make_driver(1, "Max Verstappen", 1)
    assert verstappen.is_teammate_of(verstappen) is False