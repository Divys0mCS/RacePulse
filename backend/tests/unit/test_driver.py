from app.models.driver import Driver


def test_driver_creation():
    d = Driver(driver_id=1, name="Max Verstappen", number=1, team="Red Bull Racing", nationality="Dutch")
    assert d.name == "Max Verstappen"
    assert d.number == 1


def test_driver_summary():
    d = Driver(driver_id=1, name="Max Verstappen", number=1, team="Red Bull Racing", nationality="Dutch")
    assert "Max Verstappen" in d.summary()
    assert "#1" in d.summary()


def test_driver_repr():
    d = Driver(driver_id=1, name="Max Verstappen", number=1, team="Red Bull Racing", nationality="Dutch")
    assert repr(d) == "Driver(#1 Max Verstappen, Red Bull Racing)"