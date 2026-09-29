from sqlalchemy import CheckConstraint

from app.database.base import Base
from app.database.models.track import TrackModel


def test_track_model_uses_tracks_table() -> None:
    assert TrackModel.__tablename__ == "tracks"


def test_track_model_inherits_from_base() -> None:
    assert issubclass(TrackModel, Base)


def test_track_model_has_expected_columns() -> None:
    columns = TrackModel.__table__.columns

    assert set(columns.keys()) == {
        "track_id",
        "name",
        "country",
        "length_km",
        "number_of_corners",
    }


def test_track_id_is_primary_key() -> None:
    assert TrackModel.__table__.c.track_id.primary_key is True


def test_track_columns_are_non_nullable() -> None:
    columns = TrackModel.__table__.columns

    assert columns.name.nullable is False
    assert columns.country.nullable is False
    assert columns.length_km.nullable is False
    assert columns.number_of_corners.nullable is False


def test_track_has_domain_constraints() -> None:
    constraints = TrackModel.__table__.constraints

    check_constraints = {
        constraint.name
        for constraint in constraints
        if isinstance(constraint, CheckConstraint)
    }

    assert "ck_tracks_length_km_positive" in check_constraints
    assert "ck_tracks_number_of_corners_positive" in check_constraints