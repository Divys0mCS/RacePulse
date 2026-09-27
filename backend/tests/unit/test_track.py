# backend/tests/unit/test_track.py

import pytest
from app.models.track import Track


def make_track(track_id=1, name="Silverstone", country="United Kingdom", length_km=5.891, number_of_corners=18):
    return Track(track_id=track_id, name=name, country=country, length_km=length_km, number_of_corners=number_of_corners)


def test_track_creation():
    t = make_track()
    assert t.name == "Silverstone"
    assert t.length_km == 5.891


def test_track_repr():
    t = make_track()
    assert repr(t) == "Track(Silverstone, United Kingdom, 5.891km)"


def test_length_km_rejects_zero():
    with pytest.raises(ValueError):
        make_track(length_km=0)


def test_length_km_rejects_negative():
    with pytest.raises(ValueError):
        make_track(length_km=-2.5)


def test_number_of_corners_rejects_zero():
    with pytest.raises(ValueError):
        make_track(number_of_corners=0)


def test_updating_length_km_after_creation_validates_too():
    t = make_track()
    with pytest.raises(ValueError):
        t.length_km = -1